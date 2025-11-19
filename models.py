from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    characters = db.relationship('Character', backref='account', cascade='all, delete-orphan')

class Character(db.Model):
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete='CASCADE'))
    name = db.Column(db.String(50), unique=True, nullable=False)
    faction = db.Column(db.String(10))
    
    # Clan/Role
    clan_id = db.Column(db.Integer, db.ForeignKey('clans.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    # Leveling
    level = db.Column(db.Integer, default=1)
    sub_level = db.Column(db.Integer, default=1)
    tier = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    chi_breathing_completed = db.Column(db.Boolean, default=False)
    
    # Core Stats
    body = db.Column(db.Integer, default=10)
    spirit = db.Column(db.Integer, default=10)
    flow = db.Column(db.Integer, default=10)
    chi_points = db.Column(db.Integer, default=50)  # unspent points
    
    # Derived Stats (calculated)
    max_hp = db.Column(db.Integer)
    current_hp = db.Column(db.Integer)
    max_chi = db.Column(db.Integer)
    current_chi = db.Column(db.Integer)
    
    # Combat Stats
    damage_min = db.Column(db.Integer)
    damage_max = db.Column(db.Integer)
    chi_kung_damage = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    dodge = db.Column(db.Integer)
    attack_rating = db.Column(db.Integer)
    
    # Karma & Social
    good_karma = db.Column(db.Integer, default=0)
    bad_karma = db.Column(db.Integer, default=0)
    karma_title = db.Column(db.String(50))
    active_epithet_id = db.Column(db.Integer, db.ForeignKey('epithets.id'))
    
    # Location & State
    current_zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    gold = db.Column(db.Integer, default=100)
    blood_count = db.Column(db.Integer, default=0)
    rage_percent = db.Column(db.Integer, default=0)
    
    # Wounds
    external_wounds = db.Column(db.Integer, default=0)
    internal_wounds = db.Column(db.Integer, default=0)
    
    # Timestamps
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Elixir Tracking
    elixir_body = db.Column(db.Integer, default=0)
    elixir_spirit = db.Column(db.Integer, default=0)
    elixir_flow = db.Column(db.Integer, default=0)
    
    # Relationships
    skills = db.relationship('CharacterSkill', backref='character', cascade='all, delete-orphan')
    inventory = db.relationship('CharacterInventory', backref='character', cascade='all, delete-orphan')
    quests = db.relationship('CharacterQuest', backref='character', cascade='all, delete-orphan')
    epithets = db.relationship('CharacterEpithet', backref='character', cascade='all, delete-orphan')
    
    def calculate_derived_stats(self):
        """Recalculate HP, Chi, Defense based on core stats + gear"""
        self.max_hp = 100 + (self.body * 10)
        self.max_chi = 100 + (self.spirit * 10)
        self.defense = 5 + (self.body // 2)
        self.dodge = self.flow // 2
        
        # Initialize current values if not set
        if self.current_hp is None:
            self.current_hp = self.max_hp
        if self.current_chi is None:
            self.current_chi = self.max_chi
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'sub_level': self.sub_level,
            'tier': self.tier,
            'body': self.body,
            'spirit': self.spirit,
            'flow': self.flow,
            'hp': self.current_hp,
            'max_hp': self.max_hp,
            'chi': self.current_chi,
            'max_chi': self.max_chi,
            'defense': self.defense,
            'xp': self.experience,
            'gold': self.gold,
            'good_karma': self.good_karma,
            'bad_karma': self.bad_karma,
            'clan_id': self.clan_id,
            'role_id': self.role_id
        }

class Clan(db.Model):
    __tablename__ = 'clans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    faction = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text)
    starting_zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    
    # Relationships
    roles = db.relationship('Role', backref='clan')
    characters = db.relationship('Character', backref='clan')

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    clan_id = db.Column(db.Integer, db.ForeignKey('clans.id'))
    archetype = db.Column(db.String(20))
    primary_weapon = db.Column(db.String(20))
    description = db.Column(db.Text)
    
    # Starting stat bonuses
    body_bonus = db.Column(db.Integer, default=0)
    spirit_bonus = db.Column(db.Integer, default=0)
    flow_bonus = db.Column(db.Integer, default=0)
    
    # Relationships
    characters = db.relationship('Character', backref='role')

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    skill_type = db.Column(db.String(20))  # kung_fu, chi_kung, passive
    clan_id = db.Column(db.Integer, db.ForeignKey('clans.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    base_damage_min = db.Column(db.Integer)
    base_damage_max = db.Column(db.Integer)
    chi_cost = db.Column(db.Integer)
    cooldown_ms = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=False)
    
    description = db.Column(db.Text)
    unlock_level = db.Column(db.Integer, default=1)

class CharacterSkill(db.Model):
    __tablename__ = 'character_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'))
    skill_level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    hotbar_slot = db.Column(db.Integer)
    hotbar_page = db.Column(db.Integer, default=1)
    
    # Relationships
    skill = db.relationship('Skill')

class ItemTemplate(db.Model):
    __tablename__ = 'item_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    item_type = db.Column(db.String(20))
    sub_type = db.Column(db.String(20))
    
    # Requirements
    required_level = db.Column(db.Integer, default=1)
    required_body = db.Column(db.Integer, default=0)
    required_spirit = db.Column(db.Integer, default=0)
    required_flow = db.Column(db.Integer, default=0)
    required_karma_title = db.Column(db.String(50))
    
    # Stats
    damage_min = db.Column(db.Integer)
    damage_max = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    dodge = db.Column(db.Integer)
    body_bonus = db.Column(db.Integer)
    spirit_bonus = db.Column(db.Integer)
    flow_bonus = db.Column(db.Integer)
    
    # Item Properties
    durability_max = db.Column(db.Integer)
    stack_size = db.Column(db.Integer, default=1)
    vendor_price = db.Column(db.Integer)
    ornament_slots = db.Column(db.Integer, default=0)
    
    description = db.Column(db.Text)
    rarity = db.Column(db.String(20), default='common')

class CharacterInventory(db.Model):
    __tablename__ = 'character_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'))
    item_template_id = db.Column(db.Integer, db.ForeignKey('item_templates.id'))
    quantity = db.Column(db.Integer, default=1)
    durability_current = db.Column(db.Integer)
    
    # Unique item properties
    refinement_level = db.Column(db.Integer, default=0)
    ornament_1_id = db.Column(db.Integer, db.ForeignKey('item_templates.id'))
    ornament_2_id = db.Column(db.Integer, db.ForeignKey('item_templates.id'))
    
    bag_slot = db.Column(db.Integer)
    equipped_slot = db.Column(db.String(20))
    acquired_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    item = db.relationship('ItemTemplate', foreign_keys=[item_template_id])

class Zone(db.Model):
    __tablename__ = 'zones'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    zone_type = db.Column(db.String(20))
    recommended_level_min = db.Column(db.Integer)
    recommended_level_max = db.Column(db.Integer)
    description = db.Column(db.Text)
    
    # Adjacent zones
    north_zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    south_zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    east_zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    west_zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    
    is_safe_zone = db.Column(db.Boolean, default=False)
    pvp_enabled = db.Column(db.Boolean, default=False)
    
    # Relationships
    characters = db.relationship('Character', backref='current_zone')

class EnemyTemplate(db.Model):
    __tablename__ = 'enemy_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enemy_type = db.Column(db.String(20))
    level = db.Column(db.Integer)
    
    # Stats
    hp = db.Column(db.Integer)
    chi = db.Column(db.Integer)
    damage_min = db.Column(db.Integer)
    damage_max = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    dodge = db.Column(db.Integer)
    
    # Rewards
    xp_reward = db.Column(db.Integer)
    gold_min = db.Column(db.Integer)
    gold_max = db.Column(db.Integer)
    good_karma_chance = db.Column(db.Float)
    
    can_wound = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)

class ZoneEnemy(db.Model):
    __tablename__ = 'zone_enemies'
    
    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    enemy_template_id = db.Column(db.Integer, db.ForeignKey('enemy_templates.id'))
    spawn_weight = db.Column(db.Integer, default=100)
    is_boss = db.Column(db.Boolean, default=False)
    
    # Relationships
    enemy = db.relationship('EnemyTemplate')

class LootTable(db.Model):
    __tablename__ = 'loot_tables'
    
    id = db.Column(db.Integer, primary_key=True)
    enemy_template_id = db.Column(db.Integer, db.ForeignKey('enemy_templates.id'))
    item_template_id = db.Column(db.Integer, db.ForeignKey('item_templates.id'))
    drop_chance = db.Column(db.Float)
    quantity_min = db.Column(db.Integer, default=1)
    quantity_max = db.Column(db.Integer, default=1)

class Epithet(db.Model):
    __tablename__ = 'epithets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Stat Bonuses
    body_bonus = db.Column(db.Integer, default=0)
    spirit_bonus = db.Column(db.Integer, default=0)
    flow_bonus = db.Column(db.Integer, default=0)
    damage_bonus = db.Column(db.Integer, default=0)
    defense_bonus = db.Column(db.Integer, default=0)
    
    obtained_from = db.Column(db.String(100))
    cooldown_hours = db.Column(db.Integer, default=2)

class CharacterEpithet(db.Model):
    __tablename__ = 'character_epithets'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'))
    epithet_id = db.Column(db.Integer, db.ForeignKey('epithets.id'))
    acquired_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    epithet = db.relationship('Epithet')

class Quest(db.Model):
    __tablename__ = 'quests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quest_type = db.Column(db.String(20))
    
    # Requirements
    required_level = db.Column(db.Integer, default=1)
    required_clan_id = db.Column(db.Integer, db.ForeignKey('clans.id'))
    prerequisite_quest_id = db.Column(db.Integer, db.ForeignKey('quests.id'))
    
    # Rewards
    xp_reward = db.Column(db.Integer)
    gold_reward = db.Column(db.Integer)
    good_karma_reward = db.Column(db.Integer)
    item_reward_id = db.Column(db.Integer, db.ForeignKey('item_templates.id'))
    epithet_reward_id = db.Column(db.Integer, db.ForeignKey('epithets.id'))

class CharacterQuest(db.Model):
    __tablename__ = 'character_quests'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'))
    quest_id = db.Column(db.Integer, db.ForeignKey('quests.id'))
    status = db.Column(db.String(20), default='active')
    progress = db.Column(db.Text)  # JSON stored as text
    accepted_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    quest = db.relationship('Quest')

# Legacy compatibility - keep for existing combat system
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

# Legacy compatibility
class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    item_type = db.Column(db.String(20))
    subtype = db.Column(db.String(20))
    
    required_level = db.Column(db.Integer, default=1)
    
    damage_min = db.Column(db.Integer)
    damage_max = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    
    rarity = db.Column(db.String(20), default='common')
    value = db.Column(db.Integer, default=10)
