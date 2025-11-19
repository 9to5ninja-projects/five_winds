"""
Database initialization script for Five Winds.
Loads seed data from SQL files into the SQLite database.
"""

import sqlite3
from pathlib import Path

def init_database():
    """Initialize database with schema and seed data."""
    
    db_path = Path('dragons.db')
    schema_path = Path('database/schema.sql')
    seed_path = Path('database/seed_data.sql')
    
    # Delete existing database to start fresh
    if db_path.exists():
        print(f"Removing existing database: {db_path}")
        db_path.unlink()
    
    print("Creating new database...")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Read and execute schema
    # Note: PostgreSQL syntax needs some adjustments for SQLite
    print("Loading schema...")
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        
        # Convert PostgreSQL to SQLite syntax
        schema_sql = schema_sql.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
        schema_sql = schema_sql.replace('TEXT[]', 'TEXT')
        schema_sql = schema_sql.replace('JSON', 'TEXT')
        schema_sql = schema_sql.replace('TIMESTAMP', 'DATETIME')
        schema_sql = schema_sql.replace('NOW()', "datetime('now')")
        schema_sql = schema_sql.replace('DECIMAL(3,2)', 'REAL')
        schema_sql = schema_sql.replace('DECIMAL(5,4)', 'REAL')
        
        # Split into individual statements and execute
        statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
        for statement in statements:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                print(f"Warning: {e}")
                print(f"Statement: {statement[:100]}...")
    
    conn.commit()
    print("Schema loaded successfully.")
    
    # Read and execute seed data
    print("Loading seed data...")
    with open(seed_path, 'r', encoding='utf-8') as f:
        seed_sql = f.read()
        
        # Convert PostgreSQL to SQLite syntax
        seed_sql = seed_sql.replace("NOW()", "datetime('now')")
        
        # Split into individual statements
        statements = [s.strip() for s in seed_sql.split(';') if s.strip()]
        for statement in statements:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                print(f"Warning: {e}")
                print(f"Statement: {statement[:100]}...")
    
    conn.commit()
    print("Seed data loaded successfully.")
    
    # Verify data
    cursor.execute("SELECT COUNT(*) FROM clans")
    clan_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM roles")
    role_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM skills")
    skill_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM zones")
    zone_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM enemy_templates")
    enemy_count = cursor.fetchone()[0]
    
    print(f"\n✓ Database initialized successfully!")
    print(f"  - {clan_count} clans")
    print(f"  - {role_count} roles")
    print(f"  - {skill_count} skills")
    print(f"  - {zone_count} zones")
    print(f"  - {enemy_count} enemies")
    
    conn.close()

if __name__ == '__main__':
    init_database()
