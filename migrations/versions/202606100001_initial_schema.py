"""initial schema

Revision ID: 202606100001
Revises:
Create Date: 2026-06-10 00:01:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "202606100001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "sports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sports")),
    )
    op.create_index(op.f("ix_sports_code"), "sports", ["code"], unique=True)
    op.create_index(op.f("ix_sports_id"), "sports", ["id"], unique=False)

    op.create_table(
        "leagues",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sport_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("country", sa.String(length=80), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["sport_id"],
            ["sports.id"],
            name=op.f("fk_leagues_sport_id_sports"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_leagues")),
        sa.UniqueConstraint("sport_id", "code", name="uq_leagues_sport_id_code"),
    )
    op.create_index(op.f("ix_leagues_code"), "leagues", ["code"], unique=False)
    op.create_index(op.f("ix_leagues_id"), "leagues", ["id"], unique=False)
    op.create_index("ix_leagues_sport_country", "leagues", ["sport_id", "country"], unique=False)
    op.create_index(op.f("ix_leagues_sport_id"), "leagues", ["sport_id"], unique=False)

    op.create_table(
        "seasons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("league_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["league_id"],
            ["leagues.id"],
            name=op.f("fk_seasons_league_id_leagues"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_seasons")),
        sa.UniqueConstraint("league_id", "name", name="uq_seasons_league_id_name"),
    )
    op.create_index(op.f("ix_seasons_id"), "seasons", ["id"], unique=False)
    op.create_index(op.f("ix_seasons_league_id"), "seasons", ["league_id"], unique=False)
    op.create_index("ix_seasons_league_current", "seasons", ["league_id", "is_current"], unique=False)

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sport_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=140), nullable=False),
        sa.Column("short_name", sa.String(length=80), nullable=True),
        sa.Column("country", sa.String(length=80), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["sport_id"],
            ["sports.id"],
            name=op.f("fk_teams_sport_id_sports"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teams")),
        sa.UniqueConstraint("sport_id", "code", name="uq_teams_sport_id_code"),
    )
    op.create_index(op.f("ix_teams_code"), "teams", ["code"], unique=False)
    op.create_index(op.f("ix_teams_id"), "teams", ["id"], unique=False)
    op.create_index("ix_teams_sport_country", "teams", ["sport_id", "country"], unique=False)
    op.create_index(op.f("ix_teams_sport_id"), "teams", ["sport_id"], unique=False)

    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("home_team_id", sa.Integer(), nullable=False),
        sa.Column("away_team_id", sa.Integer(), nullable=False),
        sa.Column("kickoff_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("round_name", sa.String(length=80), nullable=True),
        sa.Column("venue", sa.String(length=160), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=True),
        sa.Column("source_match_id", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("home_team_id <> away_team_id", name=op.f("ck_matches_different_teams")),
        sa.ForeignKeyConstraint(
            ["away_team_id"],
            ["teams.id"],
            name=op.f("fk_matches_away_team_id_teams"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["home_team_id"],
            ["teams.id"],
            name=op.f("fk_matches_home_team_id_teams"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["season_id"],
            ["seasons.id"],
            name=op.f("fk_matches_season_id_seasons"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_matches")),
        sa.UniqueConstraint(
            "season_id",
            "home_team_id",
            "away_team_id",
            "kickoff_at",
            name="uq_matches_season_home_away_kickoff",
        ),
    )
    op.create_index(op.f("ix_matches_away_team_id"), "matches", ["away_team_id"], unique=False)
    op.create_index(op.f("ix_matches_home_team_id"), "matches", ["home_team_id"], unique=False)
    op.create_index("ix_matches_home_away", "matches", ["home_team_id", "away_team_id"], unique=False)
    op.create_index(op.f("ix_matches_id"), "matches", ["id"], unique=False)
    op.create_index(op.f("ix_matches_season_id"), "matches", ["season_id"], unique=False)
    op.create_index("ix_matches_season_kickoff", "matches", ["season_id", "kickoff_at"], unique=False)
    op.create_index("ix_matches_status", "matches", ["status"], unique=False)

    op.create_table(
        "team_seasons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("display_name", sa.String(length=140), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["season_id"],
            ["seasons.id"],
            name=op.f("fk_team_seasons_season_id_seasons"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            name=op.f("fk_team_seasons_team_id_teams"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_team_seasons")),
        sa.UniqueConstraint("team_id", "season_id", name="uq_team_seasons_team_id_season_id"),
    )
    op.create_index(op.f("ix_team_seasons_id"), "team_seasons", ["id"], unique=False)
    op.create_index(op.f("ix_team_seasons_season_id"), "team_seasons", ["season_id"], unique=False)
    op.create_index(
        "ix_team_seasons_season_active",
        "team_seasons",
        ["season_id", "is_active"],
        unique=False,
    )
    op.create_index(op.f("ix_team_seasons_team_id"), "team_seasons", ["team_id"], unique=False)

    op.create_table(
        "match_stats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("match_id", sa.Integer(), nullable=False),
        sa.Column("home_goals", sa.Integer(), nullable=True),
        sa.Column("away_goals", sa.Integer(), nullable=True),
        sa.Column("home_corners", sa.Integer(), nullable=True),
        sa.Column("away_corners", sa.Integer(), nullable=True),
        sa.Column("home_yellow_cards", sa.Integer(), nullable=True),
        sa.Column("away_yellow_cards", sa.Integer(), nullable=True),
        sa.Column("home_red_cards", sa.Integer(), nullable=True),
        sa.Column("away_red_cards", sa.Integer(), nullable=True),
        sa.Column("home_xg", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("away_xg", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("home_possession_pct", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("away_possession_pct", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("is_final", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["match_id"],
            ["matches.id"],
            name=op.f("fk_match_stats_match_id_matches"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_match_stats")),
        sa.UniqueConstraint("match_id", name="uq_match_stats_match_id"),
    )
    op.create_index(op.f("ix_match_stats_id"), "match_stats", ["id"], unique=False)
    op.create_index("ix_match_stats_match_id", "match_stats", ["match_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_match_stats_match_id", table_name="match_stats")
    op.drop_index(op.f("ix_match_stats_id"), table_name="match_stats")
    op.drop_table("match_stats")

    op.drop_index(op.f("ix_team_seasons_team_id"), table_name="team_seasons")
    op.drop_index("ix_team_seasons_season_active", table_name="team_seasons")
    op.drop_index(op.f("ix_team_seasons_season_id"), table_name="team_seasons")
    op.drop_index(op.f("ix_team_seasons_id"), table_name="team_seasons")
    op.drop_table("team_seasons")

    op.drop_index("ix_matches_status", table_name="matches")
    op.drop_index("ix_matches_season_kickoff", table_name="matches")
    op.drop_index(op.f("ix_matches_season_id"), table_name="matches")
    op.drop_index(op.f("ix_matches_id"), table_name="matches")
    op.drop_index("ix_matches_home_away", table_name="matches")
    op.drop_index(op.f("ix_matches_home_team_id"), table_name="matches")
    op.drop_index(op.f("ix_matches_away_team_id"), table_name="matches")
    op.drop_table("matches")

    op.drop_index(op.f("ix_teams_sport_id"), table_name="teams")
    op.drop_index("ix_teams_sport_country", table_name="teams")
    op.drop_index(op.f("ix_teams_id"), table_name="teams")
    op.drop_index(op.f("ix_teams_code"), table_name="teams")
    op.drop_table("teams")

    op.drop_index("ix_seasons_league_current", table_name="seasons")
    op.drop_index(op.f("ix_seasons_league_id"), table_name="seasons")
    op.drop_index(op.f("ix_seasons_id"), table_name="seasons")
    op.drop_table("seasons")

    op.drop_index(op.f("ix_leagues_sport_id"), table_name="leagues")
    op.drop_index("ix_leagues_sport_country", table_name="leagues")
    op.drop_index(op.f("ix_leagues_id"), table_name="leagues")
    op.drop_index(op.f("ix_leagues_code"), table_name="leagues")
    op.drop_table("leagues")

    op.drop_index(op.f("ix_sports_id"), table_name="sports")
    op.drop_index(op.f("ix_sports_code"), table_name="sports")
    op.drop_table("sports")