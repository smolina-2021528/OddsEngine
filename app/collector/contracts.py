from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class CollectorSource(StrEnum):
    """Supported raw data sources for the collector layer."""

    FBREF = "fbref"
    SOFASCORE = "sofascore"


class MatchStatus(StrEnum):
    """Canonical match statuses produced by scraper parsers."""

    SCHEDULED = "scheduled"
    FINISHED = "finished"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


class CollectorBaseModel(BaseModel):
    """Base model for raw collector contracts."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class CollectedFootballTeam(CollectorBaseModel):
    """Team as returned by a football scraper before canonical normalization."""

    source: CollectorSource
    source_team_id: str | None = Field(default=None, max_length=120)
    name: str = Field(min_length=1, max_length=140)
    short_name: str | None = Field(default=None, max_length=80)
    country: str = Field(min_length=1, max_length=80)


class CollectedFootballSeason(CollectorBaseModel):
    """Season metadata collected from a football source."""

    source: CollectorSource
    league_code: str = Field(min_length=1, max_length=80)
    league_name: str = Field(min_length=1, max_length=120)
    country: str = Field(min_length=1, max_length=80)
    season_name: str = Field(min_length=1, max_length=50)
    start_date: date
    end_date: date | None = None
    is_current: bool = False

    @model_validator(mode="after")
    def validate_date_range(self) -> CollectedFootballSeason:
        """Ensure the season end date does not precede the start date."""

        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date")
        return self


class CollectedFootballMatchStats(CollectorBaseModel):
    """Raw match statistics collected from a football source."""

    home_goals: int | None = Field(default=None, ge=0)
    away_goals: int | None = Field(default=None, ge=0)

    home_corners: int | None = Field(default=None, ge=0)
    away_corners: int | None = Field(default=None, ge=0)

    home_yellow_cards: int | None = Field(default=None, ge=0)
    away_yellow_cards: int | None = Field(default=None, ge=0)
    home_red_cards: int | None = Field(default=None, ge=0)
    away_red_cards: int | None = Field(default=None, ge=0)

    home_xg: Decimal | None = Field(default=None, ge=Decimal("0"), max_digits=5, decimal_places=2)
    away_xg: Decimal | None = Field(default=None, ge=Decimal("0"), max_digits=5, decimal_places=2)

    home_possession_pct: Decimal | None = Field(
        default=None,
        ge=Decimal("0"),
        le=Decimal("100"),
        max_digits=5,
        decimal_places=2,
    )
    away_possession_pct: Decimal | None = Field(
        default=None,
        ge=Decimal("0"),
        le=Decimal("100"),
        max_digits=5,
        decimal_places=2,
    )

    is_final: bool = False

    @model_validator(mode="after")
    def validate_score_pairs(self) -> CollectedFootballMatchStats:
        """Ensure score fields are collected as a complete pair when present."""

        home_score_exists = self.home_goals is not None
        away_score_exists = self.away_goals is not None
        if home_score_exists != away_score_exists:
            raise ValueError("home_goals and away_goals must be provided together")
        return self

    @model_validator(mode="after")
    def validate_possession_pair(self) -> CollectedFootballMatchStats:
        """Ensure possession percentages are collected as a complete pair."""

        home_possession_exists = self.home_possession_pct is not None
        away_possession_exists = self.away_possession_pct is not None
        if home_possession_exists != away_possession_exists:
            raise ValueError(
                "home_possession_pct and away_possession_pct must be provided together"
            )
        return self


class CollectedFootballMatch(CollectorBaseModel):
    """Raw football match collected from a source before canonical normalization."""

    source: CollectorSource
    source_match_id: str | None = Field(default=None, max_length=120)
    league_code: str = Field(min_length=1, max_length=80)
    season_name: str = Field(min_length=1, max_length=50)
    kickoff_at: datetime
    home_team: CollectedFootballTeam
    away_team: CollectedFootballTeam
    round_name: str | None = Field(default=None, max_length=80)
    venue: str | None = Field(default=None, max_length=160)
    status: MatchStatus = MatchStatus.UNKNOWN
    stats: CollectedFootballMatchStats | None = None

    @model_validator(mode="after")
    def validate_distinct_teams(self) -> CollectedFootballMatch:
        """Ensure a match is not created with the same team on both sides."""

        same_source_id = (
            self.home_team.source_team_id is not None
            and self.home_team.source_team_id == self.away_team.source_team_id
        )
        same_name = self.home_team.name.casefold() == self.away_team.name.casefold()
        if same_source_id or same_name:
            raise ValueError("home_team and away_team must be different")
        return self

    @model_validator(mode="after")
    def validate_finished_match_has_final_stats(self) -> CollectedFootballMatch:
        """Ensure finished matches are marked final when stats are already present."""

        has_non_final_stats = self.stats is not None and not self.stats.is_final
        if self.status == MatchStatus.FINISHED and has_non_final_stats:
            raise ValueError("finished matches with stats must have stats.is_final=True")
        return self


class FootballCollection(CollectorBaseModel):
    """Container returned by a football scraper execution."""

    source: CollectorSource
    season: CollectedFootballSeason
    matches: list[CollectedFootballMatch] = Field(default_factory=list)

    @field_validator("matches")
    @classmethod
    def validate_match_sources(
        cls,
        matches: list[CollectedFootballMatch],
    ) -> list[CollectedFootballMatch]:
        """Ensure all matches in a collection come from a single source."""

        if not matches:
            return matches

        expected_source = matches[0].source
        for match in matches:
            if match.source != expected_source:
                raise ValueError("all matches must come from the same source")
        return matches

    @model_validator(mode="after")
    def validate_collection_consistency(self) -> FootballCollection:
        """Ensure the collection source matches season and match payloads."""

        if self.season.source != self.source:
            raise ValueError("season source must match collection source")

        for match in self.matches:
            if match.source != self.source:
                raise ValueError("match source must match collection source")
            if match.league_code != self.season.league_code:
                raise ValueError("match league_code must match season league_code")
            if match.season_name != self.season.season_name:
                raise ValueError("match season_name must match season season_name")

        return self