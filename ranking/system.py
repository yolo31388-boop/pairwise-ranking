
class Ranking:
    def __init__(self):
        self.players = {}
        self.season_points = {}
        self.historical_best = {}
        self.rewards_claimed = set()

    def update_score(self, pid, score):
        self.players[pid] = score
        self.season_points[pid] = self.season_points.get(pid, 0) + score

    def get_rank(self, pid):
        # BUG: 用行号而非密集排名
        sorted_players = sorted(self.players.items(), key=lambda x: -x[1])
        for i, (p, s) in enumerate(sorted_players):
            if p == pid:
                return i + 1
        return None

    def reset_season(self):
        # BUG: 只清排行榜不清赛季积分
        self.players = {}

    def get_page(self, page, page_size=10):
        # BUG: 不做边界检查
        sorted_players = sorted(self.players.items(), key=lambda x: -x[1])
        start = page * page_size
        return sorted_players[start:start + page_size]

    def claim_reward(self, pid, reward_id):
        # BUG: 不查重
        self.rewards_claimed.add((pid, reward_id))
        return True
