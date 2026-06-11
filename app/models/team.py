from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.match import Match
    from app.models.sport import Season, Sport


class Team(TimestampMixin, Base):
    """Team participating in one or more seasons."""

    __tablename__ = "teams"
    __table_args__ = (
        UniqueConstraint("sport_id", "code", name="uq_teams_sport_id_code"),
        Index("ix_teams_sport_country", "sport_id", "country"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sport_id: Mapped[int] = mapped_column(
        ForeignKey("sports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(140), nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    country: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    sport: Mapped[Sport] = relationship("Sport", back_populates="teams")
    seasons: Mapped[list[TeamSeason]] = relationship(
        "TeamSeason",
        back_populates="team",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    home_matches: Mapped[list[Match]] = relationship(
        "Match",
        back_populates="home_team",
        foreign_keys="Match.home_team_id",
    )
    away_matches: Mapped[list[Match]] = relationship(
        "Match",
        back_populates="away_team",
        foreign_keys="Match.away_team_id",
    )

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, code={self.code!r}, name={self.name!r})"


class TeamSeason(TimestampMixin, Base):
    """Team registration inside a specific season."""

    __tablename__ = "team_seasons"
    __table_args__ = (
        UniqueConstraint("team_id", "season_id", name="uq_team_seasons_team_id_season_id"),
        Index("ix_team_seasons_season_active", "season_id", "is_active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_name: Mapped[str | None] = mapped_column(String(140), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    team: Mapped[Team] = relationship("Team", back_populates="seasons")
    season: Mapped[Season] = relationship("Season", back_populates="team_seasons")

    def __repr__(self) -> str:
        return (
            "TeamSeason("
            f"id={self.id!r}, "
            f"team_id={self.team_id!r}, "
            f"season_id={self.season_id!r}"
            ")"
        )