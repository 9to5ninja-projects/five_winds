from flask import Flask, render_template, jsonify, request, session
from models import db, Character, Enemy, Clan, Role, Skill, Zone, ItemTemplate, CharacterSkill
from combat import Combat
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dragons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# In-memory combat sessions (replace with Redis/DB later)
active_combats = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/combat')
def combat_page():
    return render_template('combat.html')

@app.route('/api/clans', methods=['GET'])
def get_clans():
    """Get all available clans with their roles."""
    clans = Clan.query.all()
    result = []
    for clan in clans:
        roles = Role.query.filter_by(clan_id=clan.id).all()
        result.append({
            'id': clan.id,
            'name': clan.name,
            'faction': clan.faction,
            'description': clan.description,
            'roles': [{
                'id': r.id,
                'name': r.name,
                'archetype': r.archetype,
                'primary_weapon': r.primary_weapon,
                'description': r.description
            } for r in roles]
        })
    return jsonify(result)

@app.route('/api/character/create', methods=['POST'])
def create_character():
    """Create a new character."""
    data = request.json
    
    # Validate required fields
    if not data.get('name') or not data.get('clan_id') or not data.get('role_id'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if name is taken
    if Character.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Character name already exists'}), 400
    
    # Get clan and role
    clan = Clan.query.get(data['clan_id'])
    role = Role.query.get(data['role_id'])
    
    if not clan or not role or role.clan_id != clan.id:
        return jsonify({'error': 'Invalid clan or role'}), 400
    
    # Create character
    char = Character(
        name=data['name'],
        clan_id=clan.id,
        role_id=role.id,
        faction=clan.faction,
        body=10 + (role.body_bonus or 0),
        spirit=10 + (role.spirit_bonus or 0),
        flow=10 + (role.flow_bonus or 0),
        current_zone_id=clan.starting_zone_id
    )
    
    char.calculate_derived_stats()
    
    db.session.add(char)
    db.session.flush()  # Get character ID
    
    # Learn starting skills for this role
    starting_skills = Skill.query.filter(
        Skill.clan_id == clan.id,
        Skill.role_id == role.id,
        Skill.unlock_level == 1
    ).all()
    
    for skill in starting_skills:
        char_skill = CharacterSkill(
            character_id=char.id,
            skill_id=skill.id,
            skill_level=1,
            experience=0,
            hotbar_slot=1,  # Equip to first hotbar slot
            hotbar_page=1
        )
        db.session.add(char_skill)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Character created successfully',
        'character': char.to_dict()
    })

@app.route('/api/characters', methods=['GET'])
def get_characters():
    """Get all characters for current user (simplified - no auth yet)."""
    characters = Character.query.all()
    result = [{
        'id': c.id,
        'name': c.name,
        'level': c.level,
        'sub_level': c.sub_level,
        'hp': c.current_hp,
        'max_hp': c.max_hp,
        'chi': c.current_chi,
        'max_chi': c.max_chi,
        'body': c.body,
        'spirit': c.spirit,
        'flow': c.flow
    } for c in characters]
    return jsonify(result)

@app.route('/api/character/<int:char_id>', methods=['GET'])
def get_character(char_id):
    """Get a single character's full details."""
    char = Character.query.get_or_404(char_id)
    
    return jsonify({
        'id': char.id,
        'name': char.name,
        'clan_id': char.clan_id,
        'role_id': char.role_id,
        'level': char.level,
        'sub_level': char.sub_level,
        'tier': char.tier,
        'xp': char.experience,
        'hp': char.current_hp,
        'max_hp': char.max_hp,
        'chi': char.current_chi,
        'max_chi': char.max_chi,
        'body': char.body,
        'spirit': char.spirit,
        'flow': char.flow,
        'defense': char.defense,
        'gold': char.gold,
        'current_zone_id': char.current_zone_id
    })

@app.route('/api/zone/<int:zone_id>', methods=['GET'])
def get_zone(zone_id):
    """Get zone information."""
    zone = Zone.query.get_or_404(zone_id)
    
    return jsonify({
        'id': zone.id,
        'name': zone.name,
        'description': zone.description,
        'zone_type': zone.zone_type,
        'recommended_level_min': zone.recommended_level_min,
        'recommended_level_max': zone.recommended_level_max,
        'is_safe_zone': zone.is_safe_zone
    })

@app.route('/api/meditate', methods=['POST'])
def meditate():
    """Restore HP and Chi through meditation."""
    data = request.json
    char_id = data.get('character_id')
    
    char = Character.query.get_or_404(char_id)
    
    # Restore based on spirit stat
    hp_restore = min(char.spirit * 10, char.max_hp - char.current_hp)
    chi_restore = min(char.spirit * 15, char.max_chi - char.current_chi)
    
    char.current_hp = min(char.max_hp, char.current_hp + hp_restore)
    char.current_chi = min(char.max_chi, char.current_chi + chi_restore)
    
    db.session.commit()
    
    return jsonify({
        'hp_restored': hp_restore,
        'chi_restored': chi_restore,
        'character': {
            'id': char.id,
            'hp': char.current_hp,
            'max_hp': char.max_hp,
            'chi': char.current_chi,
            'max_chi': char.max_chi
        }
    })

@app.route('/api/start_combat', methods=['POST'])
def start_combat():
    """Initialize a new combat"""
    data = request.json
    char_id = data.get('character_id')
    
    if char_id:
        character = Character.query.get_or_404(char_id)
    else:
        # Fallback to first character
        character = Character.query.first()
    
    # Get a random enemy from the current zone
    enemy = Enemy.query.first()
    
    if not character or not enemy:
        return jsonify({'error': 'No character or enemy found'}), 404
    
    # Load character's equipped skills
    char_skills = CharacterSkill.query.filter_by(character_id=character.id).all()
    
    combat = Combat(character, enemy, char_skills)
    combat_id = f"combat_{id(combat)}"
    active_combats[combat_id] = combat
    
    session['combat_id'] = combat_id
    
    return jsonify({
        'combat_id': combat_id,
        'state': combat.get_state()
    })

@app.route('/api/combat_action', methods=['POST'])
def combat_action():
    """Execute a combat turn"""
    combat_id = session.get('combat_id')
    
    if not combat_id or combat_id not in active_combats:
        return jsonify({'error': 'No active combat'}), 404
    
    combat = active_combats[combat_id]
    action = request.json.get('action', 'attack')
    
    state = combat.execute_turn(action)
    
    # Clean up finished combats
    if state['victory'] or state['defeat']:
        del active_combats[combat_id]
        session.pop('combat_id', None)
    
    return jsonify(state)

@app.route('/api/create_test_data', methods=['POST'])
def create_test_data():
    """Create test character and enemy"""
    # Check if test data already exists
    if Character.query.filter_by(name="TestWarrior").first():
        return jsonify({'message': 'Test data already exists'})

    # Test character
    char = Character(
        name="TestWarrior",
        body=15,
        spirit=10,
        flow=12
    )
    char.calculate_derived_stats()
    
    # Test enemy
    enemy = Enemy(
        name="Shadow Bandit",
        level=1,
        max_hp=80,
        attack_power=15,
        defense=5,
        agility=8,
        xp_reward=50,
        gold_reward=20
    )
    
    db.session.add(char)
    db.session.add(enemy)
    db.session.commit()
    
    return jsonify({'message': 'Test data created'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
