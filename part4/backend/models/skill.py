from backend.models import db


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=1)

    # Relationships
    players = db.relationship(
        'Player', secondary='player_skills', back_populates='skills')
    quests = db.relationship(
        'Quest', secondary='quest_skills', back_populates='skills')

    # ------------------------
    # Serialization
    # ------------------------
    def to_dict(self, detailed=True):
        """Return a dict representation of the skill."""
        data = {
            "id": self.id,
            "name": self.name,
            "level": self.level
        }

        if detailed:
            data["players"] = [p.name for p in self.players]
            data["quests"] = [q.title for q in self.quests]

        return data

    def __repr__(self):
        return f"<Skill {self.name} (Lvl {self.level})>"
