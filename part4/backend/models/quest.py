from backend.models import db

# Association table between quests and skills
quest_skills = db.Table(
    'quest_skills',
    db.Column('quest_id', db.Integer, db.ForeignKey(
        'quests.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey(
        'skills.id'), primary_key=True)
)


class Quest(db.Model):
    __tablename__ = 'quests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.Text, nullable=True)

    # Relationship with player
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    player = db.relationship('Player', back_populates='quests')

    # Relationship with skills
    skills = db.relationship(
        'Skill', secondary=quest_skills, back_populates='quests')

    # ------------------------
    # Serialization
    # ------------------------
    def to_dict(self, detailed=True):
        """Return a dict representation of the quest."""
        data = {
            "id": self.id,
            "title": self.title,
            "xp": self.xp,
            "summary": self.summary,
        }

        if detailed:
            data["skills"] = [skill.to_dict(False) for skill in self.skills]
            if self.player:
                data["player"] = {"id": self.player.id,
                                  "name": self.player.name}

        return data

    def __repr__(self):
        return f"<Quest {self.title} ({self.xp} XP)>"
