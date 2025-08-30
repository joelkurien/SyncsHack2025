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


