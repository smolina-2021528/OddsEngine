"""Data collection package.

This package contains contracts, scrapers, and normalization utilities used to
collect raw sports data before it is persisted into canonical database models.
"""

from app.collector.contracts import (
    CollectedFootballMatch,
    CollectedFootballMatchStats,
    CollectedFootballSeason,
    CollectedFootballTeam,
    CollectorSource,
    FootballCollection,
    MatchStatus,
)

__all__ = [
    "CollectedFootballMatch",
    "CollectedFootballMatchStats",
    "CollectedFootballSeason",
    "CollectedFootballTeam",
    "CollectorSource",
    "FootballCollection",
    "MatchStatus",
]