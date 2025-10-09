from werkzeug.security import generate_password_hash
from backend.models import db, Player, Quest, Skill
from backend.app import app
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


with app.app_context():
    print("🌱 Checking database content...")

    existing_players = Player.query.count()

    if existing_players > 0:
        print("✅ Database already seeded, skipping.")
    else:
        print("🧹 Empty database detected — seeding now.")

        admin = Player(
            name="Game Master",
            class_name="Admin Mage",
            level=99,
            xp=9999,
            is_admin=True,
            password_hash=generate_password_hash("admin123")
        )

        user = Player(
            name="Thomas Roncin",
            class_name="Backend Wizard",
            level=1,
            xp=0,
            is_admin=False,
            password_hash=generate_password_hash("thomas123")
        )

        skill_c = Skill(name="C intermediate", level=2)
        skill_python = Skill(name="Python intermediate", level=5)
        skill_git = Skill(name="Git mastering", level=3)

        user.skills.extend([skill_c, skill_python])
        admin.skills.append(skill_git)

        quest1 = Quest(
            title="Forge the Ancient Function",
            xp=80,
            summary="Recreate the printf function in C with format handling."
        )
        quest1.skills.append(skill_c)
        user.quests.append(quest1)

        quest2 = Quest(
            title="Tame the Python Dragon",
            xp=120,
            summary="Develop an efficient Flask REST API."
        )
        quest2.skills.append(skill_python)
        admin.quests.append(quest2)

        db.session.add_all(
            [admin, user, skill_c, skill_python, skill_git, quest1, quest2])
        db.session.commit()

        print("✅ Database seeded successfully!")
        print("👑 Admin login: name='Game Master', password='admin123'")
        print("🧙‍♂️ User login: name='Thomas Roncin', password='thomas123'")
