from flask import Flask, render_template, jsonify, request, session
from models import db, Character, Enemy
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
