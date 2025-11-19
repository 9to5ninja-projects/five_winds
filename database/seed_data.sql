-- ============================================
-- CLANS (4 total: 2 White, 2 Black)
-- ============================================

-- Note: Ensure Zones are inserted before Clans if enforcing FK constraints, 
-- or insert Clans with NULL starting_zone_id and update later.
-- Assuming standard sequence for this seed file.

INSERT INTO clans (name, faction, description, starting_zone_id) VALUES
-- Imperial Court Faction
('Northern Wind', 'imperial', 'Masters of ice and discipline. They believe in structure, patience, and overwhelming defense.', 1),
('Eastern Wind', 'imperial', 'Storm riders who value speed and precision. Swift strikes like lightning from the east.', 2),

-- Free Clans Faction  
('Southern Wind', 'free', 'Fierce fire warriors who fight with passion. They answer to no emperor, only their own honor.', 3),
('Western Wind', 'free', 'Metal-forged fighters from the frontier. Strength through adversity and relentless assault.', 4);

-- ============================================
-- ROLES (2-3 per clan)
-- ============================================

INSERT INTO roles (clan_id, name, archetype, primary_weapon, description) VALUES
-- Northern Wind roles
(1, 'Frost Blade', 'warrior', 'sword', 'Ice-forged swordsmen who strike with calculated precision'),
(1, 'Winter Sage', 'healer', 'staff', 'Mystics who channel healing frost and protective barriers'),
(1, 'Glacier Fist', 'caster', 'palm', 'Masters of freezing energy attacks'),
(1, 'Permafrost Guardian', 'hybrid', 'spear', 'Balanced fighters who blend offense and defense'),

-- Eastern Wind roles
(2, 'Storm Striker', 'warrior', 'staff', 'Lightning-fast combatants who overwhelm with speed'),
(2, 'Thunder Caller', 'caster', 'palm', 'Invokers of storm energy and crackling lightning'),
(2, 'Tempest Dancer', 'hybrid', 'dual_blade', 'Agile fighters who move like the wind itself'),

-- Southern Wind roles
(3, 'Ember Warrior', 'warrior', 'axe', 'Aggressive fighters who burn with righteous fury'),
(3, 'Flame Weaver', 'caster', 'palm', 'Wielders of devastating fire techniques'),
(3, 'Inferno Monk', 'hybrid', 'staff', 'Balanced combatants who harness inner fire'),

-- Western Wind roles
(4, 'Iron Vanguard', 'warrior', 'saber', 'Relentless berserkers forged in battle'),
(4, 'Steel Sage', 'caster', 'palm', 'Masters of metal energy manipulation'),
(4, 'Razor Dancer', 'hybrid', 'dagger', 'Swift assassins who strike from the shadows');

-- ============================================
-- ZONES (Starting areas + progression)
-- ============================================

INSERT INTO zones (name, zone_type, recommended_level_min, recommended_level_max, description, is_safe_zone, pvp_enabled) VALUES
-- Clan Starting Towns (safe)
('Frost Haven', 'town', 1, 36, 'A snow-covered fortress where Northern Wind disciples train in icy courtyards.', TRUE, FALSE),
('Storm Peak', 'town', 1, 36, 'Mountain monastery where Eastern Wind warriors harness the power of thunder.', TRUE, FALSE),
('Ember Camp', 'town', 1, 36, 'A vibrant settlement where Southern Wind fighters gather around eternal flames.', TRUE, FALSE),
('Iron Garrison', 'town', 1, 36, 'A fortified stronghold where Western Wind warriors forge themselves in battle.', TRUE, FALSE),

-- Neutral Hub
('Hefei City', 'town', 1, 36, 'Major trading hub where all factions meet. Markets, merchants, and opportunities.', TRUE, FALSE),

-- Wilderness progression zones
('Bamboo Forest', 'wilderness', 1, 6, 'Thick bamboo groves hide bandits and wild beasts. Sunlight filters through green stalks.', FALSE, FALSE),
('Mountain Path', 'wilderness', 7, 12, 'Treacherous mountain trail with wolves and thieves. Mist obscures dangers ahead.', FALSE, FALSE),
('River Valley', 'wilderness', 13, 18, 'Flowing waters and rocky outcrops. Stronger bandits control the trade routes.', FALSE, FALSE),
('Dark Woods', 'wilderness', 19, 24, 'Twisted trees and unnatural silence. Spirits and demons lurk here.', FALSE, FALSE),
('Bloody Plains', 'pvp', 25, 36, 'Contested battleground between factions. Only the strong survive.', FALSE, TRUE);

-- Connect zones (adjacency)
UPDATE zones SET east_zone_id = 5 WHERE name = 'Frost Haven';
UPDATE zones SET south_zone_id = 5 WHERE name = 'Storm Peak';
UPDATE zones SET west_zone_id = 5 WHERE name = 'Ember Camp';
UPDATE zones SET north_zone_id = 5 WHERE name = 'Iron Garrison';

UPDATE zones SET 
    north_zone_id = (SELECT id FROM zones WHERE name = 'Storm Peak'),
    south_zone_id = (SELECT id FROM zones WHERE name = 'Iron Garrison'),
    east_zone_id = (SELECT id FROM zones WHERE name = 'Frost Haven'),
    west_zone_id = (SELECT id FROM zones WHERE name = 'Ember Camp'),
    south_zone_id = (SELECT id FROM zones WHERE name = 'Bamboo Forest')
WHERE name = 'Hefei City';

UPDATE zones SET 
    north_zone_id = (SELECT id FROM zones WHERE name = 'Hefei City'),
    south_zone_id = (SELECT id FROM zones WHERE name = 'Mountain Path')
WHERE name = 'Bamboo Forest';

UPDATE zones SET 
    north_zone_id = (SELECT id FROM zones WHERE name = 'Bamboo Forest'),
    south_zone_id = (SELECT id FROM zones WHERE name = 'River Valley')
WHERE name = 'Mountain Path';

-- ============================================
-- UNIVERSAL SKILLS (available to all)
-- ============================================

INSERT INTO skills (name, skill_type, base_damage_min, base_damage_max, chi_cost, cooldown_ms, is_active, description, unlock_level) VALUES
-- Basic Kung Fu
('Basic Fist', 'kung_fu', 5, 10, 2, 0, TRUE, 'Simple punch attack. Levels quickly with use.', 1),
('Kick', 'kung_fu', 8, 15, 3, 0, FALSE, 'Powerful kick that knocks back enemies.', 3),

-- Basic Chi Kung
('Meditate', 'chi_kung', 0, 0, 0, 30000, FALSE, 'Restore Chi over time. Can be interrupted.', 1),
('Chi Heal', 'chi_kung', 0, 0, 20, 10000, FALSE, 'Heal yourself for 30% max HP.', 5),

-- Utility
('Lightfoot', 'chi_kung', 0, 0, 10, 5000, FALSE, 'Move quickly through zones. Reduces random encounters.', 7),
('Iron Body', 'chi_kung', 0, 0, 15, 60000, FALSE, 'Increase defense by 50% for 30 seconds.', 10);

-- ============================================
-- CLAN-SPECIFIC SKILLS
-- ============================================

-- Northern Wind Skills (Ice + Defense)
INSERT INTO skills (name, skill_type, clan_id, role_id, base_damage_min, base_damage_max, chi_cost, cooldown_ms, is_active, description, unlock_level) VALUES
-- Frost Blade (Warrior)
('Frozen Edge', 'kung_fu', 1, 1, 12, 20, 3, 0, TRUE, 'Swift icy blade strike', 1),
('Glacial Pierce', 'kung_fu', 1, 1, 20, 35, 5, 0, FALSE, 'Armor-shattering frozen thrust', 8),
('Avalanche Cleave', 'kung_fu', 1, 1, 35, 60, 8, 0, FALSE, 'Devastating overhead slash trailing ice', 15),

-- Glacier Fist (Caster)
('Frost Bolt', 'chi_kung', 1, 3, 15, 25, 15, 3000, FALSE, 'Fire a bolt of freezing energy', 1),
('Ice Shard Storm', 'chi_kung', 1, 3, 30, 50, 25, 5000, FALSE, 'Barrage of frozen projectiles', 10),
('Absolute Zero', 'chi_kung', 1, 3, 50, 80, 40, 8000, FALSE, 'Crushing sphere of pure cold', 18);

-- Eastern Wind Skills (Storm + Speed)
INSERT INTO skills (name, skill_type, clan_id, role_id, base_damage_min, base_damage_max, chi_cost, cooldown_ms, is_active, description, unlock_level) VALUES
-- Storm Striker (Warrior)
('Lightning Staff', 'kung_fu', 2, 4, 10, 18, 3, 0, TRUE, 'Crackling staff blow infused with electricity', 1),
('Thunder Sweep', 'kung_fu', 2, 4, 18, 30, 5, 0, FALSE, 'Wide arc attack that stuns enemies', 8),
('Storm Barrier', 'chi_kung', 2, 4, 0, 0, 20, 45000, FALSE, 'Electric shield that deflects attacks', 15),

-- Thunder Caller (Caster)
('Chain Lightning', 'chi_kung', 2, 5, 18, 28, 18, 3500, FALSE, 'Arcing electricity that jumps between foes', 1),
('Thunderclap', 'chi_kung', 2, 5, 35, 55, 30, 6000, FALSE, 'Explosive burst of thunder energy', 12);

-- Southern Wind Skills (Fire + Aggression)
INSERT INTO skills (name, skill_type, clan_id, role_id, base_damage_min, base_damage_max, chi_cost, cooldown_ms, is_active, description, unlock_level) VALUES
-- Ember Warrior (Warrior)
('Blazing Axe', 'kung_fu', 3, 6, 14, 22, 3, 0, TRUE, 'Burning axe chop', 1),
('Inferno Spiral', 'kung_fu', 3, 6, 25, 40, 6, 0, FALSE, 'Spinning attack wreathed in flames', 10),

-- Flame Weaver (Caster)
('Fire Dart', 'chi_kung', 3, 7, 12, 20, 12, 3000, FALSE, 'Searing projectile', 1),
('Scorching Wave', 'chi_kung', 3, 7, 25, 40, 25, 7000, FALSE, 'Wall of flame that burns all before it', 14);

-- Western Wind Skills (Metal + Power)
INSERT INTO skills (name, skill_type, clan_id, role_id, base_damage_min, base_damage_max, chi_cost, cooldown_ms, is_active, description, unlock_level) VALUES
-- Iron Vanguard (Berserker)
('Steel Cleave', 'kung_fu', 4, 8, 16, 24, 4, 0, TRUE, 'Brutal saber cut', 1),
('Rending Fury', 'kung_fu', 4, 8, 30, 50, 7, 0, FALSE, 'Savage strike that costs health but deals massive damage', 9),
('Iron Body', 'chi_kung', 4, 8, 0, 0, 25, 60000, FALSE, 'Transform skin to metal, increasing all damage', 16),

-- Steel Sage (Elemental caster)
('Metal Shard', 'chi_kung', 4, 9, 20, 32, 20, 4000, FALSE, 'Razor-sharp projectile of solidified energy', 1),
('Iron Rain', 'chi_kung', 4, 9, 40, 65, 35, 7000, FALSE, 'Shower of metal spikes from above', 11),

-- Razor Dancer (Hybrid)
('Quick Cut', 'kung_fu', 4, 10, 10, 16, 2, 0, TRUE, 'Lightning-fast dagger strike', 1),
('Phantom Step', 'chi_kung', 4, 10, 0, 0, 15, 20000, FALSE, 'Vanish and reappear, next attack always critical', 13);

-- ============================================
-- ENEMY TEMPLATES
-- ============================================

INSERT INTO enemy_templates (name, enemy_type, level, hp, chi, damage_min, damage_max, defense, dodge, xp_reward, gold_min, gold_max, good_karma_chance, description) VALUES
-- Tier 1 enemies (Bamboo Forest)
('Young Bandit', 'humanoid', 2, 50, 20, 5, 10, 5, 10, 15, 3, 8, 0.15, 'Inexperienced thief looking for easy marks'),
('Wild Boar', 'beast', 3, 70, 0, 8, 12, 3, 5, 20, 1, 5, 0.10, 'Aggressive boar with sharp tusks'),
('Bandit Lookout', 'humanoid', 4, 80, 30, 10, 15, 8, 15, 25, 5, 12, 0.15, 'More experienced bandit, watches for trouble'),
('Forest Spirit', 'spirit', 6, 150, 80, 15, 25, 10, 20, 60, 15, 30, 0.25, 'Ethereal guardian of the bamboo groves'),

-- Tier 2 enemies (Mountain Path)
('Mountain Wolf', 'beast', 8, 120, 0, 15, 22, 8, 18, 45, 8, 15, 0.12, 'Pack hunter with keen senses'),
('Rogue Warrior', 'humanoid', 9, 140, 50, 18, 28, 15, 20, 55, 12, 20, 0.18, 'Skilled fighter turned outlaw'),
('Ice Wraith', 'spirit', 11, 180, 100, 22, 35, 12, 25, 75, 18, 35, 0.22, 'Frozen spirit that haunts the peaks'),

-- Tier 3 enemies (River Valley)
('River Raider', 'humanoid', 14, 200, 70, 28, 40, 20, 22, 90, 20, 40, 0.20, 'Well-armed bandit controlling trade routes'),
('Giant Crab', 'beast', 15, 250, 0, 30, 45, 30, 10, 100, 15, 30, 0.15, 'Massive crustacean with iron shell'),
('Water Demon', 'spirit', 17, 300, 150, 35, 55, 18, 28, 130, 30, 60, 0.28, 'Malevolent spirit bound to the river'),

-- Tier 4 enemies (Dark Woods)
('Corrupted Monk', 'humanoid', 20, 350, 100, 40, 60, 25, 25, 160, 40, 80, 0.25, 'Once-holy warrior now twisted by darkness'),
('Shadow Beast', 'beast', 22, 400, 0, 45, 70, 20, 30, 180, 35, 70, 0.20, 'Creature born from pure shadow'),
('Ancient Evil', 'spirit', 24, 500, 200, 50, 80, 30, 35, 220, 50, 100, 0.35, 'Powerful demon sealed in the woods');

-- Assign enemies to zones
INSERT INTO zone_enemies (zone_id, enemy_template_id, spawn_weight, is_boss) VALUES
-- Bamboo Forest
(6, 1, 100, FALSE),
(6, 2, 80, FALSE),
(6, 3, 50, FALSE),
(6, 4, 10, TRUE),

-- Mountain Path
(7, 5, 100, FALSE),
(7, 6, 70, FALSE),
(7, 7, 15, TRUE),

-- River Valley
(8, 8, 90, FALSE),
(8, 9, 60, FALSE),
(8, 10, 12, TRUE),

-- Dark Woods
(9, 11, 80, FALSE),
(9, 12, 60, FALSE),
(9, 13, 8, TRUE);

-- ============================================
-- BASIC LOOT TABLES
-- ============================================

-- Bandit drops
INSERT INTO loot_tables (enemy_template_id, item_template_id, drop_chance, quantity_min, quantity_max) VALUES
-- We'll need to create items first, but structure is here
(1, 1, 0.15, 1, 1), -- cloth scraps
(1, 2, 0.08, 1, 1), -- basic sword
(2, 3, 0.20, 1, 3), -- boar meat
(2, 4, 0.05, 1, 1); -- boar hide

-- ============================================
-- BASIC ITEMS (minimal set)
-- ============================================

INSERT INTO item_templates (name, item_type, sub_type, required_level, damage_min, damage_max, defense, vendor_price, stack_size, rarity, description) VALUES
-- Materials
('Cloth Scraps', 'material', 'cloth', 1, NULL, NULL, NULL, 5, 50, 'common', 'Torn fabric from bandits'),
('Boar Meat', 'consumable', 'food', 1, NULL, NULL, NULL, 3, 20, 'common', 'Restores 50 HP when eaten'),
('Boar Hide', 'material', 'leather', 1, NULL, NULL, NULL, 15, 20, 'common', 'Tough animal hide'),

-- Starting weapons
('Wooden Sword', 'weapon', 'sword', 1, 8, 12, NULL, 20, 1, 'common', 'Basic training sword'),
('Worn Staff', 'weapon', 'staff', 1, 6, 10, NULL, 20, 1, 'common', 'Simple wooden staff'),
('Rusty Club', 'weapon', 'club', 1, 10, 14, NULL, 20, 1, 'common', 'Heavy but crude weapon'),
('Dull Saber', 'weapon', 'saber', 1, 9, 13, NULL, 20, 1, 'common', 'Needs sharpening badly'),

-- Basic armor
('Cloth Shirt', 'armor', 'chest', 1, NULL, NULL, 5, 15, 1, 'common', 'Simple cloth protection'),
('Cloth Pants', 'armor', 'legs', 1, NULL, NULL, 3, 12, 1, 'common', 'Basic leg covering'),

-- Consumables
('Small Health Potion', 'consumable', 'potion', 1, NULL, NULL, NULL, 25, 10, 'common', 'Restores 100 HP'),
('Small Chi Potion', 'consumable', 'potion', 1, NULL, NULL, NULL, 20, 10, 'common', 'Restores 50 Chi');

-- ============================================
-- STARTER EPITHETS
-- ============================================

INSERT INTO epithets (name, description, body_bonus, spirit_bonus, flow_bonus, obtained_from, cooldown_hours) VALUES
('Novice Warrior', 'A fighter just beginning their journey', 2, 0, 1, 'reach level 5', 2),
('Student of Chi', 'One who has begun to understand energy', 0, 3, 1, 'reach level 5', 2),
('Swift Foot', 'Known for exceptional speed', 0, 1, 3, 'quest reward', 2);

-- ============================================
-- STARTER QUEST
-- ============================================

INSERT INTO quests (name, description, quest_type, required_level, required_clan_id, xp_reward, gold_reward, good_karma_reward) VALUES
('First Steps', 'Defeat 5 enemies in the Bamboo Forest', 'main', 1, NULL, 50, 20, 5),
('Prove Your Worth', 'Reach level 6 and complete Chi Breathing', 'clan', 6, NULL, 100, 50, 10);
