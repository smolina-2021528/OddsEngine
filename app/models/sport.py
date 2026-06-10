from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Sport(TimestampMixin, Base):
    """Sport supported by the platform, such as football or basketball."""

    __tablename__ = "sports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    leagues: Mapped[list[League]] = relationship(
        back_populates="sport",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"Sport(id={self.id!r}, code={self.code!r}, name={self.name!r})"


class League(TimestampMixin, Base):
    """Sports league or competition, such as LaLiga or Premier League."""

    __tablename__ = "leagues"
    __table_args__ = (
        UniqueConstraint("sport_id", "code", name="uq_leagues_sport_id_code"),
        Index("ix_leagues_sport_country", "sport_id", "country"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sport_id: Mapped[int] = mapped_column(
        ForeignKey("sports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    country: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    sport: Mapped[Sport] = relationship(back_populates="leagues")
    seasons: Mapped[list[Season]] = relationship(
        back_populates="league",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return (
            "League("
            f"id={self.id!r}, "
            f"code={self.code!r}, "
            f"name={self.name!r}, "
            f"country={self.country!r}"
            ")"
        )


class Season(TimestampMixin, Base):
    """Season belonging to a specific league."""

    __tablename__ = "seasons"
    __table_args__ = (
        UniqueConstraint("league_id", "name", name="uq_seasons_league_id_name"),
        Index("ix_seasons_league_current", "league_id", "is_current"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    league_id: Mapped[int] = mapped_column(
        ForeignKey("leagues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    league: Mapped[League] = relationship(back_populates="seasons")

    def __repr__(self) -> str:
        return (
            "Season("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"league_id={self.league_id!r}, "
            f"is_current={self.is_current!r}"
            ")"
        )