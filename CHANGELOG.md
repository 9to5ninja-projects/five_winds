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
  - **Auto-learns starting skills based on clan/role**
- Clans listing API endpoint (`/api/clans`)
  - Returns all clans with nested role information
  - Includes faction and description data
- **Main Game Interface (`/` - index.html)**
  - Beautiful character selection screen
  - Responsive grid layout for character cards
  - Visual display of character stats (HP, Chi, Level, etc.)
  - "Create New Character" button with form toggle
  - Character creation wizard with clan and role selection
  - Interactive clan cards with faction badges (Imperial/Free)
  - Role selection with archetype and description display
  - Gradient UI theme with cyberpunk aesthetic
- **Game View (`/game` - game.html)**
  - Character stats sidebar with HP/Chi bars
  - Live stat display (Body, Spirit, Flow, Defense, Gold)
  - Zone information panel
  - Action menu with four core actions:
    - Hunt - initiate combat
    - Explore - search for items (coming soon)
    - Meditate - restore HP and Chi
    - Travel - zone navigation (coming soon)
  - Game log with scrollable history
  - Responsive two-column layout
- **New API Endpoints**
  - `/api/characters` - List all characters
  - `/api/character/<id>` - Get character details
  - `/api/zone/<id>` - Get zone information
  - `/api/meditate` - Restore HP/Chi based on Spirit stat
- **Real Skills Combat System**
  - Characters auto-learn starting skills on creation
  - Skills equipped to hotbar slots (slot 1 used in combat)
  - Combat uses character's equipped skills instead of generic attacks
  - Chi consumption based on skill costs
  - Damage scaling: kung_fu uses Body stat, chi_kung uses Spirit stat
  - Skill names displayed in combat log
  - Chi usage tracked and displayed
- **Zone-Based Enemy Spawning**
  - Enemies spawn from zone's enemy pool with weighted random selection
  - Boss enemies excluded from random spawns
  - Fallback to level-appropriate enemies if zone has no assigned enemies
  - Enemies created from EnemyTemplate with proper stats
- **Combat Progression System**
  - Victory awards XP and gold from defeated enemies
  - Simplified leveling: 100 XP per level
  - Automatic level up when XP threshold reached
  - Stats recalculated on level up
  - Victory screen shows rewards (XP, Gold, Level Up notification)
  - Defeat screen with return option
  - Combat auto-starts when clicking Hunt
  - Return to game link after combat ends

### Fixed
- Added missing stat bonus columns to roles table (body_bonus, spirit_bonus, flow_bonus)
- Resolved database file location issue (Flask instance/ folder)
- Updated index route to render new character selection interface
- Fixed Zone model attribute names (recommended_level_min/max)
- Fixed CharacterSkill to use hotbar_slot instead of is_equipped

### Technical Improvements
- Modular route structure with separate handlers for /, /game, /combat
- RESTful API design for character and zone management
- Client-side JavaScript for dynamic UI updates
- CSS Grid and Flexbox for responsive layouts
- Gradient backgrounds and smooth transitions
- Weighted random selection algorithm for enemy spawning
- Template-based enemy instantiation system

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
