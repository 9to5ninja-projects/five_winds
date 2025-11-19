import sqlite3

conn = sqlite3.connect('dragons.db')
cursor = conn.cursor()

# Check clans table
cursor.execute('PRAGMA table_info(clans)')
print('Clans columns:')
for row in cursor.fetchall():
    print(f'  {row[1]} {row[2]}')

# Check sample data
cursor.execute('SELECT id, name, faction, starting_zone_id FROM clans')
print('\nClans data:')
for row in cursor.fetchall():
    print(f'  {row}')

conn.close()
