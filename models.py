from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Character(db.Model):
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Core Stats
    level = db.Column(db.Integer, default=1)
    sublevel = db.Column(db.Integer, default=1)  # 1-6 within tier
    
    body = db.Column(db.Integer, default=10)
    spirit = db.Column(db.Integer, default=10)
    flow = db.Column(db.Integer, default=10)
    
    # Combat Stats (derived)
    max_hp = db.Column(db.Integer, default=100)
    current_hp = db.Column(db.Integer, default=100)
    max_chi = db.Column(db.Integer, default=100)
    current_chi = db.Column(db.Integer, default=100)
    
    defense = db.Column(db.Integer, default=5)
    
    # Progression
    xp = db.Column(db.Integer, default=0)
    gold = db.Column(db.Integer, default=100)
    karma = db.Column(db.Integer, default=0)  # Positive or negative
    
    # Clan/Role
    clan_id = db.Column(db.Integer, db.ForeignKey('clans.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    # Equipment
    weapon_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def calculate_derived_stats(self):
        """Recalculate HP, Chi, Defense based on core stats"""
        self.max_hp = 100 + (self.body * 10)
        self.max_chi = 100 + (self.spirit * 10)
        self.defense = 5 + (self.body // 2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'sublevel': self.sublevel,
            'body': self.body,
            'spirit': self.spirit,
            'flow': self.flow,
            'hp': self.current_hp,
            'max_hp': self.max_hp,
            'chi': self.current_chi,
            'max_chi': self.max_chi,
            'defense': self.defense,
            'xp': self.xp,
            'gold': self.gold,
            'karma': self.karma
        }

class Clan(db.Model):
    __tablename__ = 'clans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    faction = db.Column(db.String(10), nullable=False)  # 'white' or 'black'
    description = db.Column(db.Text)

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    clan_id = db.Column(db.Integer, db.ForeignKey('clans.id'))
    
    # Starting stat bonuses
    body_bonus = db.Column(db.Integer, default=0)
    spirit_bonus = db.Column(db.Integer, default=0)
    flow_bonus = db.Column(db.Integer, default=0)

class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    item_type = db.Column(db.String(20))  # weapon, armor, consumable
    subtype = db.Column(db.String(20))    # sword, staff, potion, etc
    
    required_level = db.Column(db.Integer, default=1)
    
    # Weapon stats
    damage_min = db.Column(db.Integer)
    damage_max = db.Column(db.Integer)
    
    # Armor stats
    defense = db.Column(db.Integer)
    
    rarity = db.Column(db.String(20), default='common')
    value = db.Column(db.Integer, default=10)

class Enemy(db.Model):
    __tablename__ = 'enemies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=1)
    
    max_hp = db.Column(db.Integer, default=50)
    attack_power = db.Column(db.Integer, default=10)
    defense = db.Column(db.Integer, default=5)
    agility = db.Column(db.Integer, default=5)
    
    xp_reward = db.Column(db.Integer, default=10)
    gold_reward = db.Column(db.Integer, default=5)
    
    zone = db.Column(db.String(50))
