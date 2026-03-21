import database
import pytest
from unittest.mock import patch

from database import (
    get_known_match_ids,
    get_match_score,
    get_team_id,
    initialise_database,
    insert_competition,
    insert_match,
    insert_team,
)


@pytest.fixture(autouse=True)
def temp_db(tmp_path):
    # redirects all db operations to a temporary file so real db is never touched
    temp_db_path = str(tmp_path / "test.db")
    with patch.object(database, "DB_PATH", temp_db_path):
        initialise_database()
        yield


# ── insert_team ───────────────────────────────────────────────────────────────


def test_insert_team():
    insert_team("France", None, None, None)
    assert get_team_id("France") is not None


def test_insert_team_duplicate_ignored():
    insert_team("France", None, None, None)
    insert_team("France", None, None, None)
    assert get_team_id("France") is not None


def test_insert_team_empty_name_ignored():
    insert_team("", None, None, None)
    assert get_team_id("") is None


# ── insert_competition ────────────────────────────────────────────────────────


def test_insert_competition():
    insert_competition("Six Nations", "international", 2026)
    conn = database.create_connection()
    row = conn.execute(
        "SELECT * FROM competitions WHERE competition_name = 'Six Nations'"
    ).fetchone()
    conn.close()
    assert row is not None


def test_insert_competition_empty_name_ignored():
    insert_competition("", "international", 2026)
    conn = database.create_connection()
    row = conn.execute("SELECT * FROM competitions").fetchone()
    conn.close()
    assert row is None


# ── get_team_id ───────────────────────────────────────────────────────────────


def test_get_team_id_returns_none_for_unknown():
    assert get_team_id("Unknown Team") is None


def test_get_team_id_returns_id_for_known():
    insert_team("Ireland", None, None, None)
    team_id = get_team_id("Ireland")
    assert isinstance(team_id, int)
    assert team_id > 0


# ── get_known_match_ids ───────────────────────────────────────────────────────


def test_get_known_match_ids_empty():
    assert get_known_match_ids(1) == set()


def test_get_known_match_ids_returns_matches():
    insert_competition("Six Nations", "international", 2026)
    insert_match(1, "France", "Ireland", 30, 10, "2026-03-21")
    ids = get_known_match_ids(1)
    assert ("France", "Ireland", "2026-03-21") in ids


# ── get_match_score ───────────────────────────────────────────────────────────


def test_get_match_score_returns_scores():
    insert_competition("Six Nations", "international", 2026)
    insert_match(1, "France", "Ireland", 30, 10, "2026-03-21")
    assert get_match_score(1, "France", "Ireland", "2026-03-21") == (30, 10)


def test_get_match_score_returns_zero_zero_if_not_found():
    assert get_match_score(1, "France", "Ireland", "2026-03-21") == (0, 0)
