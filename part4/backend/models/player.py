from backend.models import db
from werkzeug.security import generate_password_hash, check_password_hash

# Association table between players and skills
player_skills = db.Table(
    'player_skills',
    db.Column('player_id', db.Integer, db.ForeignKey(
        'players.id', ondelete="CASCADE"), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey(
        'skills.id', ondelete="CASCADE"), primary_key=True)
)


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    class_name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Relationships
    skills = db.relationship(
        'Skill', secondary=player_skills, back_populates='players')
    quests = db.relationship(
        'Quest', back_populates='player', cascade="all, delete")

    # ------------------------
    # Password management
    # ------------------------
    def set_password(self, password):
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the stored hash."""
        return check_password_hash(self.password_hash, password)

    # ------------------------
    # Serialization
    # ------------------------
    def to_dict(self, detailed=True):
        """Return a dict representation of the player."""
        data = {
            "id": self.id,
            "name": self.name,
            "class_name": self.class_name,
            "level": self.level,
            "xp": self.xp,
            "is_admin": self.is_admin
        }

        if detailed:
            data["skills"] = [skill.to_dict(False) for skill in self.skills]
            data["quests"] = [quest.to_dict(False) for quest in self.quests]

        return data

    def __repr__(self):
        return f"<Player {self.name} (Lvl {self.level})>"
