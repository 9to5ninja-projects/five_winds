from flask import Flask, render_template, jsonify, request, session
from models import db, Character, Enemy, Clan, Role, Skill, Zone, ItemTemplate
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
    db.session.commit()
    
    return jsonify({
        'message': 'Character created successfully',
        'character': char.to_dict()
    })

@app.route('/api/start_combat', methods=['POST'])
def start_combat():
    """Initialize a new combat"""
    # For now, use a test character and enemy
    character = Character.query.first()
    enemy = Enemy.query.first()
    
    if not character or not enemy:
        return jsonify({'error': 'No character or enemy found'}), 404
    
    combat = Combat(character, enemy)
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
