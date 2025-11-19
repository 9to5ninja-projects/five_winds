-- ============================================
-- ACCOUNTS & CHARACTERS
-- ============================================

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(id) ON DELETE CASCADE,
    name VARCHAR(50) UNIQUE NOT NULL,
    faction VARCHAR(10) CHECK (faction IN ('imperial', 'free', 'none')),
    clan_id INT REFERENCES clans(id),
    role_id INT REFERENCES roles(id),
    
    -- Leveling
    level INT DEFAULT 1,
    sub_level INT DEFAULT 1,
    tier INT DEFAULT 1,
    experience INT DEFAULT 0,
    chi_breathing_completed BOOLEAN DEFAULT FALSE,
    
    -- Core Stats
    body INT DEFAULT 10,
    spirit INT DEFAULT 10,
    flow INT DEFAULT 10,
    chi_points INT DEFAULT 50, -- unspent points
    
    -- Derived Stats (calculated from body/spirit/flow + gear)
    max_hp INT,
    current_hp INT,
    max_chi INT,
    current_chi INT,
    
    -- Combat Stats
    damage_min INT,
    damage_max INT,
    chi_kung_damage INT,
    defense INT,
    dodge INT,
    attack_rating INT,
    
    -- Karma & Social
    good_karma INT DEFAULT 0,
    bad_karma INT DEFAULT 0,
    karma_title VARCHAR(50),
    active_epithet_id INT REFERENCES epithets(id),
    
    -- Location & State
    current_zone_id INT REFERENCES zones(id),
    gold INT DEFAULT 100,
    blood_count INT DEFAULT 0,
    rage_percent INT DEFAULT 0,
    
    -- Wounds
    external_wounds INT DEFAULT 0,
    internal_wounds INT DEFAULT 0,
    
    -- Timestamps
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Elixir Tracking (permanent bonuses)
    elixir_body INT DEFAULT 0,
    elixir_spirit INT DEFAULT 0,
    elixir_flow INT DEFAULT 0
);

-- ============================================
-- CLANS & ROLES
-- ============================================

CREATE TABLE clans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    faction VARCHAR(10) CHECK (faction IN ('imperial', 'free')),
    description TEXT,
    starting_zone_id INT REFERENCES zones(id)
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    clan_id INT REFERENCES clans(id),
    name VARCHAR(50) NOT NULL,
    archetype VARCHAR(20), -- 'warrior', 'caster', 'hybrid', 'healer'
    primary_weapon VARCHAR(20), -- 'sword', 'staff', 'dagger', etc
    description TEXT
);

-- ============================================
-- SKILLS SYSTEM
-- ============================================

CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    skill_type VARCHAR(20) CHECK (skill_type IN ('kung_fu', 'chi_kung', 'passive')),
    clan_id INT REFERENCES clans(id), -- NULL = universal skill
    role_id INT REFERENCES roles(id), -- NULL = available to all in clan
    
    base_damage_min INT,
    base_damage_max INT,
    chi_cost INT,
    cooldown_ms INT, -- for chi kung
    is_active BOOLEAN DEFAULT FALSE, -- kung fu active vs smashing
    
    description TEXT,
    unlock_level INT DEFAULT 1
);

CREATE TABLE character_skills (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    skill_id INT REFERENCES skills(id),
    skill_level INT DEFAULT 1 CHECK (skill_level >= 1 AND skill_level <= 10),
    experience INT DEFAULT 0, -- uses to level up
    hotbar_slot INT CHECK (hotbar_slot >= 0 AND hotbar_slot <= 9),
    hotbar_page INT DEFAULT 1 CHECK (hotbar_page >= 1 AND hotbar_page <= 3),
    
    UNIQUE(character_id, skill_id),
    UNIQUE(character_id, hotbar_slot, hotbar_page)
);

-- ============================================
-- ITEMS & INVENTORY
-- ============================================

CREATE TABLE item_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    item_type VARCHAR(20), -- 'weapon', 'armor', 'consumable', 'elixir', 'material'
    sub_type VARCHAR(20), -- 'sword', 'helmet', 'potion', etc
    
    -- Requirements
    required_level INT DEFAULT 1,
    required_body INT DEFAULT 0,
    required_spirit INT DEFAULT 0,
    required_flow INT DEFAULT 0,
    required_karma_title VARCHAR(50),
    
    -- Stats
    damage_min INT,
    damage_max INT,
    defense INT,
    dodge INT,
    body_bonus INT,
    spirit_bonus INT,
    flow_bonus INT,
    
    -- Item Properties
    durability_max INT,
    stack_size INT DEFAULT 1,
    vendor_price INT,
    
    -- Ornament Slots
    ornament_slots INT DEFAULT 0,
    
    description TEXT,
    rarity VARCHAR(20) DEFAULT 'common' -- common, precious, artifact
);

CREATE TABLE character_inventory (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    item_template_id INT REFERENCES item_templates(id),
    quantity INT DEFAULT 1,
    durability_current INT,
    
    -- For unique items (refined weapons, bound ornaments)
    refinement_level INT DEFAULT 0,
    ornament_1_id INT REFERENCES item_templates(id),
    ornament_2_id INT REFERENCES item_templates(id),
    
    bag_slot INT, -- NULL = equipped
    equipped_slot VARCHAR(20), -- 'weapon', 'head', 'chest', etc
    
    acquired_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- ZONES & EXPLORATION
-- ============================================

CREATE TABLE zones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    zone_type VARCHAR(20), -- 'town', 'wilderness', 'dungeon', 'pvp'
    recommended_level_min INT,
    recommended_level_max INT,
    description TEXT,
    
    -- Adjacent zones for travel
    north_zone_id INT REFERENCES zones(id),
    south_zone_id INT REFERENCES zones(id),
    east_zone_id INT REFERENCES zones(id),
    west_zone_id INT REFERENCES zones(id),
    
    is_safe_zone BOOLEAN DEFAULT FALSE,
    pvp_enabled BOOLEAN DEFAULT FALSE
);

CREATE TABLE zone_enemies (
    id SERIAL PRIMARY KEY,
    zone_id INT REFERENCES zones(id),
    enemy_template_id INT REFERENCES enemy_templates(id),
    spawn_weight INT DEFAULT 100, -- higher = more common
    is_boss BOOLEAN DEFAULT FALSE
);

CREATE TABLE enemy_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    enemy_type VARCHAR(20), -- 'beast', 'humanoid', 'spirit'
    level INT,
    
    -- Stats
    hp INT,
    chi INT,
    damage_min INT,
    damage_max INT,
    defense INT,
    dodge INT,
    
    -- Rewards
    xp_reward INT,
    gold_min INT,
    gold_max INT,
    good_karma_chance DECIMAL(3,2), -- 0.00 to 1.00
    
    -- Loot table reference
    can_wound BOOLEAN DEFAULT TRUE,
    description TEXT
);

CREATE TABLE loot_tables (
    id SERIAL PRIMARY KEY,
    enemy_template_id INT REFERENCES enemy_templates(id),
    item_template_id INT REFERENCES item_templates(id),
    drop_chance DECIMAL(5,4), -- 0.0001 to 1.0000
    quantity_min INT DEFAULT 1,
    quantity_max INT DEFAULT 1
);

-- ============================================
-- EPITHETS
-- ============================================

CREATE TABLE epithets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Stat Bonuses
    body_bonus INT DEFAULT 0,
    spirit_bonus INT DEFAULT 0,
    flow_bonus INT DEFAULT 0,
    damage_bonus INT DEFAULT 0,
    defense_bonus INT DEFAULT 0,
    
    -- How to obtain
    obtained_from VARCHAR(100), -- 'quest', 'boss:ShenMo', 'karma:tier_5', etc
    
    cooldown_hours INT DEFAULT 2 -- time before can switch
);

CREATE TABLE character_epithets (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    epithet_id INT REFERENCES epithets(id),
    acquired_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(character_id, epithet_id)
);

-- ============================================
-- QUESTS
-- ============================================

CREATE TABLE quests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    quest_type VARCHAR(20), -- 'main', 'clan', 'repeatable', 'karma'
    
    -- Requirements
    required_level INT DEFAULT 1,
    required_clan_id INT REFERENCES clans(id),
    prerequisite_quest_id INT REFERENCES quests(id),
    
    -- Rewards
    xp_reward INT,
    gold_reward INT,
    good_karma_reward INT,
    item_reward_id INT REFERENCES item_templates(id),
    epithet_reward_id INT REFERENCES epithets(id)
);

CREATE TABLE character_quests (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    quest_id INT REFERENCES quests(id),
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'completed', 'failed'
    progress JSON, -- flexible for different quest types
    accepted_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    
    UNIQUE(character_id, quest_id)
);

-- ============================================
-- COMBAT & ACTIVITY LOGS
-- ============================================

CREATE TABLE combat_log (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    enemy_template_id INT REFERENCES enemy_templates(id),
    zone_id INT REFERENCES zones(id),
    
    result VARCHAR(20), -- 'victory', 'defeat', 'fled'
    xp_gained INT,
    gold_gained INT,
    loot_gained JSON,
    
    combat_start TIMESTAMP DEFAULT NOW(),
    combat_end TIMESTAMP
);

CREATE TABLE travel_log (
    id SERIAL PRIMARY KEY,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    from_zone_id INT REFERENCES zones(id),
    to_zone_id INT REFERENCES zones(id),
    travel_method VARCHAR(20), -- 'walk', 'lightfoot', 'fast_travel'
    travel_start TIMESTAMP DEFAULT NOW(),
    travel_end TIMESTAMP
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX idx_characters_account ON characters(account_id);
CREATE INDEX idx_characters_zone ON characters(current_zone_id);
CREATE INDEX idx_character_skills_char ON character_skills(character_id);
CREATE INDEX idx_character_inventory_char ON character_inventory(character_id);
CREATE INDEX idx_combat_log_char ON combat_log(character_id);
CREATE INDEX idx_zone_enemies_zone ON zone_enemies(zone_id);
CREATE INDEX idx_loot_tables_enemy ON loot_tables(enemy_template_id);
