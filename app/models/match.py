from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.sport import Season
    from app.models.team import Team


class Match(TimestampMixin, Base):
    """Scheduled or finished match between two teams."""

    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint("home_team_id <> away_team_id", name="different_teams"),
        UniqueConstraint(
            "season_id",
            "home_team_id",
            "away_team_id",
            "kickoff_at",
            name="uq_matches_season_home_away_kickoff",
        ),
        Index("ix_matches_season_kickoff", "season_id", "kickoff_at"),
        Index("ix_matches_home_away", "home_team_id", "away_team_id"),
        Index("ix_matches_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    kickoff_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    round_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    venue: Mapped[str | None] = mapped_column(String(160), nullable=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="scheduled")
    source: Mapped[str | None] = mapped_column(String(80), nullable=True)
    source_match_id: Mapped[str | None] = mapped_column(String(120), nullable=True)

    season: Mapped[Season] = relationship("Season", back_populates="matches")
    home_team: Mapped[Team] = relationship(
        "Team",
        back_populates="home_matches",
        foreign_keys=[home_team_id],
    )
    away_team: Mapped[Team] = relationship(
        "Team",
        back_populates="away_matches",
        foreign_keys=[away_team_id],
    )
    stats: Mapped[MatchStats | None] = relationship(
        "MatchStats",
        back_populates="match",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False,
    )

    def __repr__(self) -> str:
        return (
            "Match("
            f"id={self.id!r}, "
            f"season_id={self.season_id!r}, "
            f"home_team_id={self.home_team_id!r}, "
            f"away_team_id={self.away_team_id!r}, "
            f"kickoff_at={self.kickoff_at!r}, "
            f"status={self.status!r}"
            ")"
        )


class MatchStats(TimestampMixin, Base):
    """Canonical match statistics used by collectors and odds models."""

    __tablename__ = "match_stats"
    __table_args__ = (
        UniqueConstraint("match_id", name="uq_match_stats_match_id"),
        Index("ix_match_stats_match_id", "match_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    home_goals: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_goals: Mapped[int | None] = mapped_column(Integer, nullable=True)

    home_corners: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_corners: Mapped[int | None] = mapped_column(Integer, nullable=True)

    home_yellow_cards: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_yellow_cards: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_red_cards: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_red_cards: Mapped[int | None] = mapped_column(Integer, nullable=True)

    home_xg: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    away_xg: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)

    home_possession_pct: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    away_possession_pct: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)

    is_final: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    match: Mapped[Match] = relationship("Match", back_populates="stats")

    def __repr__(self) -> str:
        return (
            "MatchStats("
            f"id={self.id!r}, "
            f"match_id={self.match_id!r}, "
            f"home_goals={self.home_goals!r}, "
            f"away_goals={self.away_goals!r}, "
            f"is_final={self.is_final!r}"
            ")"
        )