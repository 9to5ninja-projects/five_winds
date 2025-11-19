# Changelog

All notable changes to Five Winds will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Full database model expansion with all game systems
- Account model for user management
- Skill and CharacterSkill models for ability system
- ItemTemplate and CharacterInventory for equipment
- Zone, EnemyTemplate, ZoneEnemy for world content
- Epithet system for character titles
- Quest tracking system
- Proper model relationships and foreign keys
- Database initialization script (init_db.py) with PostgreSQL to SQLite conversion
- Character creation API endpoint (`/api/character/create`)
  - Name uniqueness validation
  - Role stat bonus application
  - Starting zone assignment
  - Derived stat calculation
- Clans listing API endpoint (`/api/clans`)
  - Returns all clans with nested role information
  - Includes faction and description data

### Fixed
- Added missing stat bonus columns to roles table (body_bonus, spirit_bonus, flow_bonus)
- Resolved database file location issue (Flask instance/ folder)

## [0.1.0] - 2025-11-18

### Added
- Initial project setup with Flask and SQLAlchemy
- Basic turn-based combat engine
  - Initiative system based on Flow stat
  - Physical attacks with critical hit system
  - Rage mode activation at 50% wounds
  - Wound tracking and damage calculation
- Simple combat HTML interface
  - Health and Chi bars
  - Combat log display
  - Attack and Defend buttons
- Database schema design (PostgreSQL)
  - Characters, Clans, Roles
  - Skills (kung_fu and chi_kung types)
  - Items and Inventory
  - Zones and Enemies
  - Quests and Epithets
- Seed data for game content
  - 4 elemental clans: Northern Wind, Eastern Wind, Southern Wind, Western Wind
  - 13 unique roles across clans
  - 30+ clan-specific skills
  - 13 enemy templates
  - 10 zones including starting towns
  - Basic items and consumables
- REST API endpoints
  - `/api/start_combat` - Initialize combat session
  - `/api/combat_action` - Execute combat turns
  - `/api/create_test_data` - Generate test character and enemy
- Project documentation
  - README with game overview and setup instructions
  - .gitignore for Python projects

### Technical Details
- Python 3.13 with Flask 3.0
- SQLAlchemy ORM
- SQLite for development database
- Faction system: Imperial Court vs Free Clans
- Elemental combat themes (ice, storm, fire, metal)
