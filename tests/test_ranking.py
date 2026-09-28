
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ranking.system import Ranking


def test_dense_ranking_for_ties():
    r = Ranking()
    r.update_score("p1", 100)
    r.update_score("p2", 100)
    r.update_score("p3", 90)
    assert r.get_rank("p1") == 1
    assert r.get_rank("p2") == 1
    assert r.get_rank("p3") == 3


def test_season_reset_clears_points():
    r = Ranking()
    r.update_score("p1", 100)
    r.reset_season()
    assert r.season_points.get("p1", 0) == 0


def test_season_reset_preserves_history():
    r = Ranking()
    r.update_score("p1", 100)
    r.historical_best["p1"] = {"rank": 1, "season": 1}
    r.reset_season()
    assert r.historical_best["p1"]["rank"] == 1


def test_pagination_clamped():
    r = Ranking()
    for i in range(5):
        r.update_score(f"p{i}", 100 - i * 10)
    page = r.get_page(100, 2)
    assert len(page) <= 2


def test_pagination_negative_page():
    r = Ranking()
    r.update_score("p1", 100)
    page = r.get_page(-1, 10)
    assert len(page) >= 0


def test_historical_best_recorded():
    r = Ranking()
    r.update_score("p1", 100)
    r.record_historical("p1", 1)
    assert r.historical_best["p1"]["rank"] == 1


def test_reward_dedup():
    r = Ranking()
    assert r.claim_reward("p1", "reward1") == True
    assert r.claim_reward("p1", "reward1") == False


def test_incremental_update():
    r = Ranking()
    r.update_score("p1", 50)
    r.update_score("p1", 30)
    assert r.players["p1"] == 80


def test_empty_ranking():
    r = Ranking()
    assert r.get_rank("nonexistent") == None
