from scraper import parse_standings, parse_results, parse_fixtures


# ── parse_standings ───────────────────────────────────────────────────────────


def test_parse_standings_empty_html():
    assert parse_standings("") == []


def test_parse_standings_none():
    assert parse_standings(None) == []


def test_parse_standings_invalid_html():
    assert parse_standings("<html><body>nothing here</body></html>") == []


# ── parse_results ─────────────────────────────────────────────────────────────


def test_parse_results_empty_html():
    assert parse_results("") == []


def test_parse_results_none():
    assert parse_results(None) == []


def test_parse_results_invalid_html():
    assert parse_results("<html><body>nothing here</body></html>") == []


def test_parse_results_skips_fixtures():
    # scores that are not digits should be skipped
    html = """
    <section class="Scoreboard">
        <ul>
            <li class="ScoreboardScoreCell__Item ScoreboardScoreCell__Item--home">
                <div class="ScoreCell__TeamName">France</div>
                <div class="ScoreCell__Score">TBC</div>
            </li>
            <li class="ScoreboardScoreCell__Item ScoreboardScoreCell__Item--away">
                <div class="ScoreCell__TeamName">Ireland</div>
                <div class="ScoreCell__Score">TBC</div>
            </li>
        </ul>
    </section>
    """
    assert parse_results(html) == []


# ── parse_fixtures ────────────────────────────────────────────────────────────


def test_parse_fixtures_empty_html():
    assert parse_fixtures("") == []


def test_parse_fixtures_none():
    assert parse_fixtures(None) == []


def test_parse_fixtures_invalid_html():
    assert parse_fixtures("<html><body>nothing here</body></html>") == []


def test_parse_fixtures_skips_completed_matches():
    # matches with digit scores should be skipped
    html = """
    <section class="Scoreboard">
        <ul>
            <li class="ScoreboardScoreCell__Item ScoreboardScoreCell__Item--home">
                <div class="ScoreCell__TeamName">France</div>
                <div class="ScoreCell__Score">30</div>
            </li>
            <li class="ScoreboardScoreCell__Item ScoreboardScoreCell__Item--away">
                <div class="ScoreCell__TeamName">Ireland</div>
                <div class="ScoreCell__Score">10</div>
            </li>
        </ul>
    </section>
    """
    assert parse_fixtures(html) == []
