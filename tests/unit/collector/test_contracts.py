from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.collector.contracts import (
    CollectedFootballMatch,
    CollectedFootballMatchStats,
    CollectedFootballSeason,
    CollectedFootballTeam,
    CollectorSource,
    FootballCollection,
    MatchStatus,
)


def test_football_collection_accepts_valid_payload() -> None:
    """Collector contracts should accept a complete valid football payload."""

    season = CollectedFootballSeason(
        source=CollectorSource.FBREF,
        league_code="premier-league",
        league_name="Premier League",
        country="England",
        season_name="2025-2026",
        start_date=date(2025, 8, 1),
        end_date=date(2026, 5, 31),
        is_current=True,
    )
    home_team = CollectedFootballTeam(
        source=CollectorSource.FBREF,
        source_team_id="arsenal",
        name="Arsenal",
        short_name="ARS",
        country="England",
    )
    away_team = CollectedFootballTeam(
        source=CollectorSource.FBREF,
        source_team_id="chelsea",
        name="Chelsea",
        short_name="CHE",
        country="England",
    )
    stats = CollectedFootballMatchStats(
        home_goals=2,
        away_goals=1,
        home_corners=7,
        away_corners=4,
        home_yellow_cards=1,
        away_yellow_cards=3,
        home_red_cards=0,
        away_red_cards=0,
        home_xg=Decimal("1.82"),
        away_xg=Decimal("0.91"),
        home_possession_pct=Decimal("55.50"),
        away_possession_pct=Decimal("44.50"),
        is_final=True,
    )
    match = CollectedFootballMatch(
        source=CollectorSource.FBREF,
        source_match_id="match-001",
        league_code="premier-league",
        season_name="2025-2026",
        kickoff_at=datetime(2025, 8, 15, 19, 30, tzinfo=UTC),
        home_team=home_team,
        away_team=away_team,
        round_name="Matchweek 1",
        venue="Emirates Stadium",
        status=MatchStatus.FINISHED,
        stats=stats,
    )

    collection = FootballCollection(
        source=CollectorSource.FBREF,
        season=season,
        matches=[match],
    )

    assert collection.source == CollectorSource.FBREF
    assert collection.season.league_code == "premier-league"
    assert collection.matches[0].stats is not None
    assert collection.matches[0].stats.home_goals == 2


def test_match_stats_requires_complete_score_pair() -> None:
    """Partial score payloads should be rejected."""

    with pytest.raises(ValidationError, match="home_goals and away_goals"):
        CollectedFootballMatchStats(home_goals=1)


def test_finished_match_requires_final_stats() -> None:
    """Finished matches should not carry non-final stats."""

    team_one = CollectedFootballTeam(
        source=CollectorSource.SOFASCORE,
        source_team_id="1",
        name="Team One",
        country="Spain",
    )
    team_two = CollectedFootballTeam(
        source=CollectorSource.SOFASCORE,
        source_team_id="2",
        name="Team Two",
        country="Spain",
    )

    with pytest.raises(ValidationError, match="stats.is_final=True"):
        CollectedFootballMatch(
            source=CollectorSource.SOFASCORE,
            league_code="laliga",
            season_name="2025-2026",
            kickoff_at=datetime(2025, 9, 1, 20, 0, tzinfo=UTC),
            home_team=team_one,
            away_team=team_two,
            status=MatchStatus.FINISHED,
            stats=CollectedFootballMatchStats(home_goals=0, away_goals=0, is_final=False),
        )


def test_collection_rejects_mismatched_league() -> None:
    """Collections should reject matches from another league."""

    season = CollectedFootballSeason(
        source=CollectorSource.FBREF,
        league_code="serie-a",
        league_name="Serie A",
        country="Italy",
        season_name="2025-2026",
        start_date=date(2025, 8, 1),
    )
    home_team = CollectedFootballTeam(
        source=CollectorSource.FBREF,
        source_team_id="inter",
        name="Inter",
        country="Italy",
    )
    away_team = CollectedFootballTeam(
        source=CollectorSource.FBREF,
        source_team_id="milan",
        name="Milan",
        country="Italy",
    )
    match = CollectedFootballMatch(
        source=CollectorSource.FBREF,
        league_code="bundesliga",
        season_name="2025-2026",
        kickoff_at=datetime(2025, 8, 24, 18, 45, tzinfo=UTC),
        home_team=home_team,
        away_team=away_team,
        status=MatchStatus.SCHEDULED,
    )

    with pytest.raises(ValidationError, match="league_code"):
        FootballCollection(source=CollectorSource.FBREF, season=season, matches=[match])