import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class CombatResult:
    """Single turn result"""
    damage: int
    is_crit: bool
    attacker_name: str
    defender_name: str
    action_type: str  # 'attack', 'skill', 'defend'
    message: str

class Combat:
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        
        # Current combat state
        self.character_hp = character.current_hp
        self.character_chi = character.current_chi
        self.enemy_hp = enemy.max_hp
        
        self.wounds = 0
        self.rage_active = False
        self.rage_threshold = character.max_hp * 0.5
        
        self.turn_number = 1
        self.log = []
    
    def calculate_initiative(self):
        """Who goes first this turn"""
        char_speed = self.character.flow + random.randint(1, 10)
        enemy_speed = self.enemy.agility + random.randint(1, 10)
        return char_speed >= enemy_speed
    
    def basic_attack(self, attacker, defender, attacker_stats):
        """Physical attack"""
        # Get weapon damage
        weapon_damage = random.randint(8, 12)  # Placeholder for now
        
        # Calculate damage
        base_damage = attacker_stats['body'] * (weapon_damage / 10)
        
        # Critical hit chance
        crit_chance = (attacker_stats.get('flow', 10) / 100) + 0.05
        is_crit = random.random() < crit_chance
        
        if is_crit:
            base_damage *= 2
        
        # Apply defense
        defense_val = getattr(defender, 'defense', 5)
        final_damage = max(1, int(base_damage - defense_val))
        
        attacker_name = attacker.name if hasattr(attacker, 'name') else "Enemy"
        defender_name = defender.name if hasattr(defender, 'name') else "Enemy"

        return CombatResult(
            damage=final_damage,
            is_crit=is_crit,
            attacker_name=attacker_name,
            defender_name=defender_name,
            action_type='attack',
            message=f"{'Critical hit! ' if is_crit else ''}{final_damage} damage"
        )
    
    def character_turn(self, action='attack'):
        """Player's turn"""
        if action == 'attack':
            attacker_stats = {
                'body': self.character.body,
                'flow': self.character.flow
            }
            
            result = self.basic_attack(
                self.character,
                self.enemy,
                attacker_stats
            )
            
            self.enemy_hp -= result.damage
            self.log.append(f"You attack for {result.damage} damage{' CRITICAL!' if result.is_crit else ''}")
            
            return result
        
        elif action == 'defend':
            # TODO: Implement defense boost
            self.log.append("You take a defensive stance")
            return None
    
    def enemy_turn(self):
        """Enemy's turn"""
        enemy_stats = {
            'body': self.enemy.attack_power // 2,
            'flow': self.enemy.agility
        }
        
        result = self.basic_attack(
            self.enemy,
            self.character,
            enemy_stats
        )
        
        self.character_hp -= result.damage
        self.wounds += result.damage
        
        # Check rage activation
        if self.wounds >= self.rage_threshold and not self.rage_active:
            self.rage_active = True
            self.log.append("🔥 RAGE ACTIVATED!")
        
        self.log.append(f"{self.enemy.name} attacks for {result.damage} damage")
        
        return result
    
    def execute_turn(self, player_action='attack'):
        """Full turn cycle"""
        player_first = self.calculate_initiative()
        
        self.log.append(f"\n--- Turn {self.turn_number} ---")
        
        if player_first:
            self.character_turn(player_action)
            if self.enemy_hp > 0:
                self.enemy_turn()
        else:
            self.enemy_turn()
            if self.character_hp > 0:
                self.character_turn(player_action)
        
        self.turn_number += 1
        
        return self.get_state()
    
    def get_state(self):
        """Current combat state"""
        return {
            'character_hp': self.character_hp,
            'character_max_hp': self.character.max_hp,
            'character_chi': self.character_chi,
            'character_max_chi': self.character.max_chi,
            'enemy_hp': self.enemy_hp,
            'enemy_max_hp': self.enemy.max_hp,
            'enemy_name': self.enemy.name,
            'wounds': self.wounds,
            'rage_active': self.rage_active,
            'turn': self.turn_number,
            'log': self.log.copy(),
            'victory': self.enemy_hp <= 0,
            'defeat': self.character_hp <= 0
        }
