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
    chi_used: int = 0

class Combat:
    def __init__(self, character, enemy, character_skills=None):
        self.character = character
        self.enemy = enemy
        self.character_skills = character_skills or []
        
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
    
    def basic_attack(self, attacker, defender, attacker_stats, skill=None):
        """Physical attack using skill or basic attack"""
        chi_cost = 0
        
        # Use skill if provided and character has enough chi
        if skill and hasattr(attacker, 'current_chi'):
            if attacker.current_chi >= skill.chi_cost:
                weapon_damage = random.randint(skill.base_damage_min, skill.base_damage_max)
                chi_cost = skill.chi_cost
                attacker.current_chi -= chi_cost
            else:
                # Not enough chi, use basic attack
                skill = None
                weapon_damage = random.randint(8, 12)
        else:
            weapon_damage = random.randint(8, 12)
        
        # Calculate damage
        stat_multiplier = attacker_stats.get('spirit', 10) if (skill and skill.skill_type == 'chi_kung') else attacker_stats.get('body', 10)
        base_damage = stat_multiplier * (weapon_damage / 10)
        
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
        skill_name = skill.name if skill else "Basic Attack"

        return CombatResult(
            damage=final_damage,
            is_crit=is_crit,
            attacker_name=attacker_name,
            defender_name=defender_name,
            action_type='skill' if skill else 'attack',
            message=f"{skill_name}: {'Critical hit! ' if is_crit else ''}{final_damage} damage",
            chi_used=chi_cost
        )
    
    def character_turn(self, action='attack'):
        """Player's turn"""
        if action == 'attack':
            attacker_stats = {
                'body': self.character.body,
                'spirit': self.character.spirit,
                'flow': self.character.flow
            }
            
            # Try to use the first equipped skill
            skill = None
            if self.character_skills:
                for char_skill in self.character_skills:
                    if char_skill.hotbar_slot and char_skill.skill.is_active:
                        skill = char_skill.skill
                        break
            
            result = self.basic_attack(
                self.character,
                self.enemy,
                attacker_stats,
                skill=skill
            )
            
            self.enemy_hp -= result.damage
            self.character_chi = self.character.current_chi
            
            chi_msg = f" (-{result.chi_used} Chi)" if result.chi_used > 0 else ""
            self.log.append(f"You use {result.message}{chi_msg}")
            
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
