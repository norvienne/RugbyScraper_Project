from stats import _get_result_for_team, get_team_form, build_form_data


def test_home_win():
    match = {
        "home": "France",
        "away": "Ireland",
        "home_score": "30",
        "away_score": "10",
    }
    assert _get_result_for_team("France", match) == "W"


def test_home_loss():
    match = {
        "home": "France",
        "away": "Ireland",
        "home_score": "10",
        "away_score": "30",
    }
    assert _get_result_for_team("France", match) == "L"


def test_home_draw():
    match = {
        "home": "France",
        "away": "Ireland",
        "home_score": "20",
        "away_score": "20",
    }
    assert _get_result_for_team("France", match) == "D"


def test_away_win():
    match = {
        "home": "France",
        "away": "Ireland",
        "home_score": "10",
        "away_score": "30",
    }
    assert _get_result_for_team("Ireland", match) == "W"


def test_away_loss():
    match = {
        "home": "France",
        "away": "Ireland",
        "home_score": "30",
        "away_score": "10",
    }
    assert _get_result_for_team("Ireland", match) == "L"


def test_away_draw():
    match = {
        "home": "France",
        "away": "Ireland",
        "home_score": "20",
        "away_score": "20",
    }
    assert _get_result_for_team("Ireland", match) == "D"


def test_team_not_in_match():
    match = {
        "home": "France",
        "away": "Ireland",
        "home_score": "30",
        "away_score": "10",
    }
    assert _get_result_for_team("Wales", match) is None


def test_invalid_score():
    match = {
        "home": "France",
        "away": "Ireland",
        "home_score": "TBC",
        "away_score": "TBC",
    }
    assert _get_result_for_team("France", match) is None


def test_form_returns_last_five():
    results = [
        {"home": "France", "away": "Ireland", "home_score": "30", "away_score": "10"},
        {"home": "France", "away": "Wales", "home_score": "20", "away_score": "20"},
        {"home": "France", "away": "Italy", "home_score": "10", "away_score": "30"},
        {"home": "France", "away": "England", "home_score": "25", "away_score": "15"},
        {"home": "France", "away": "Scotland", "home_score": "30", "away_score": "10"},
        {"home": "France", "away": "Wales", "home_score": "10", "away_score": "20"},
    ]
    form = get_team_form("France", results)
    assert len(form) == 5
    assert form == ["D", "L", "W", "W", "L"]


def test_form_empty_results():
    assert get_team_form("France", []) == []


def test_form_team_not_in_results():
    results = [
        {"home": "Ireland", "away": "Wales", "home_score": "30", "away_score": "10"},
    ]
    assert get_team_form("France", results) == []


def test_build_form_data():
    standings = [
        {"team_name": "France"},
        {"team_name": "Ireland"},
    ]
    results = [
        {"home": "France", "away": "Ireland", "home_score": "30", "away_score": "10"},
    ]
    form_data = build_form_data(standings, results)
    assert "France" in form_data
    assert "Ireland" in form_data
    assert form_data["France"] == ["W"]
    assert form_data["Ireland"] == ["L"]
