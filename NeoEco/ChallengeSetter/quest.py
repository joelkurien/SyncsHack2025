from typing import List, Dict

class Skill:
    def __init__(self, name: str, unlock_level: int):
        self.name = name
        self.unlock_level = unlock_level

class Quest:
    def __init__(self, quest_id: str, title: str, xp_reward: int, chain_ids: List[str] = []):
        self.quest_id = quest_id
        self.title = title
        self.xp_reward = xp_reward
        self.chain_ids = chain_ids  
        self.completed = False

class User:
    LEVELS = [0, 100, 250, 500, 1000, 2000]  
    RANKS = ["Bronze", "Silver", "Gold", "Platinum"]

    def __init__(self, username: str):
        self.username = username
        self.xp = 0
        self.level = 1
        self.unlocked_skills = []
        self.completed_quests = set()
        self.active_quests = []
    
    def add_xp(self, amount: int):
        self.xp += amount
        self.update_level()
    
    def update_level(self):
        for idx, xp_threshold in enumerate(self.LEVELS):
            if self.xp >= xp_threshold:
                self.level = idx + 1

        for skill in SKILL_TREE:
            if skill.unlock_level == self.level and skill.name not in self.unlocked_skills:
                self.unlocked_skills.append(skill.name)
    
    @property
    def rank(self):
        if self.level <= len(self.RANKS):
            return self.RANKS[self.level - 1]
        return self.RANKS[-1]
    
    def complete_quest(self, quest: Quest):
        if not quest.completed:
            quest.completed = True
            self.completed_quests.add(quest.quest_id)
            self.add_xp(quest.xp_reward)

            for chain_id in quest.chain_ids:
                self.active_quests.append(chain_id)

SKILL_TREE = [
    Skill("Daily Challenge Streak Bonus", unlock_level=5),
    Skill("Double Points Weekend", unlock_level=10),
    # Add more as needed
]

# --- Example usage ---
user = User("eco_player")
quest1 = Quest("q001", "Become a Transport Ninja 🚆", xp_reward=50)
user.complete_quest(quest1)
print(user.xp, user.level, user.rank, user.unlocked_skills)

# Grant XP for streaks, mini-bosses, etc.
def grant_daily_streak_bonus(user: User):
    if "Daily Challenge Streak Bonus" in user.unlocked_skills:
        user.add_xp(20)

# Progress bar — backend can calculate % to next level
def xp_progress(user: User):
    current_level_xp = User.LEVELS[user.level - 1]
    next_level_xp = User.LEVELS[user.level] if user.level < len(User.LEVELS) else User.LEVELS[-1]
    progress = (user.xp - current_level_xp) / (next_level_xp - current_level_xp)
    return max(0, min(1, progress))

print("Progress to next level:", xp_progress(user))
