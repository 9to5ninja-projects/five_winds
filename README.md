# Five Winds

A browser-based martial arts RPG where elemental clans battle for supremacy. Choose your clan, master elemental techniques, and fight for either the Imperial Court or the Free Clans in this turn-based combat game.

## Game Concept

**Five Winds** is a tactical RPG where players choose from four elemental clans, each with unique fighting styles and philosophies. The game features:

- **Dual Faction Warfare**: Imperial Court (order) vs Free Clans (rebellion)
- **Elemental Combat**: Ice, Storm, Fire, and Metal-themed abilities
- **Turn-Based Strategy**: Initiative-based combat with physical and energy attacks
- **Character Progression**: Level up, allocate stats, learn new skills
- **Equipment System**: Weapons, armor, refinement, and ornaments

## Clans

### Imperial Court Faction
- **Northern Wind** - Masters of ice and discipline (Defensive/Control)
- **Eastern Wind** - Storm riders who strike like lightning (Speed/Burst)

### Free Clans Faction  
- **Southern Wind** - Fierce fire warriors fighting for freedom (Aggressive/DPS)
- **Western Wind** - Metal-forged frontier fighters (Power/Berserker)

Each clan has 3-4 specialized roles: Warriors, Casters, Hybrids, and Healers.

## Current Status

**Phase 1: Ground Floor - COMPLETE ✅**
- Basic Flask server with SQLAlchemy
- Turn-based combat engine with initiative, damage calculation, and rage system
- Simple HTML interface with health bars and combat log
- SQLite database with test data

**Phase 2: Expansion - IN PROGRESS 🚧**
- Full database schema with all game systems
- Clan/role character creation
- Zone navigation and exploration
- Skill system with hotbar
- Inventory and loot drops

## Tech Stack

- **Backend**: Python 3.13, Flask 3.0, SQLAlchemy
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: TBD

## Project Structure

```
five_winds/
├── database/
│   ├── schema.sql          # PostgreSQL database schema
│   └── seed_data.sql       # Game data (clans, skills, enemies, items)
├── templates/
│   └── combat.html         # Combat interface
├── static/
│   └── (future CSS/JS)
├── models.py               # SQLAlchemy ORM models
├── combat.py               # Combat engine
├── server.py               # Flask application
├── requirements.txt        # Python dependencies
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.13+
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/9to5ninja-projects/five_winds.git
cd five_winds
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the server**
```bash
python server.py
```

5. **Create test data** (first time only)
```bash
# In another terminal or browser:
curl -X POST http://127.0.0.1:5000/api/create_test_data
# Or use Invoke-RestMethod on PowerShell
```

6. **Play the game**
Open your browser to `http://127.0.0.1:5000`

## Game Mechanics

### Combat System
- **Initiative**: Speed (Flow stat + random roll) determines turn order
- **Physical Attacks**: Based on Body stat and weapon damage
- **Energy Attacks**: Based on Spirit stat and skill power
- **Critical Hits**: Flow stat increases crit chance
- **Rage Mode**: Activates at 50% accumulated wounds, boosts damage by 30%

### Character Stats
- **Body**: Physical damage and HP
- **Spirit**: Energy damage and Chi pool
- **Flow**: Speed, dodge, and critical hit chance

### Progression
- Gain XP from combat victories
- Level up to increase stats
- Learn new skills from your clan
- Equip better weapons and armor
- Earn titles (epithets) with stat bonuses

## Development Roadmap

### Phase 2: Core Systems
- [ ] Expand database models for all tables
- [ ] Character creation flow (clan/role selection)
- [ ] Zone navigation system
- [ ] Skill learning and hotbar management
- [ ] Inventory and equipment system
- [ ] Loot drops from enemies

### Phase 3: Progression
- [ ] Experience and leveling
- [ ] Stat point allocation
- [ ] Skill progression (level 1-10)
- [ ] Quest system
- [ ] Epithet/title unlocking

### Phase 4: Content
- [ ] Multiple zones and enemies
- [ ] Boss encounters
- [ ] Rare loot and crafting
- [ ] PvP zones

### Phase 5: Polish
- [ ] Enhanced UI/UX
- [ ] Sound effects and music
- [ ] Tutorial system
- [ ] Balance adjustments

## Contributing

This is a solo development project for learning purposes, but feedback and suggestions are welcome!

## License

TBD

---

**Project Start Date**: November 18, 2025  
**Current Version**: 0.1.0 (Ground Floor)
