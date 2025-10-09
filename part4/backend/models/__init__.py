from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here to make them available everywhere
from .player import Player
from .quest import Quest
from .skill import Skill
