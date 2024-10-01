import sqlite3
from fake_useragent import UserAgent
import time

# Set up SQLite connection
db_path = ""
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table for storing mobile and tablet user agents
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mobile_user_agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_agent TEXT NOT NULL
    )
''')

# Initialize UserAgent instance
ua = UserAgent()

# Function to check if a user agent is mobile or tablet
def is_mobile_or_tablet(user_agent):
    return any(keyword in user_agent for keyword in ["Mobile", "iPhone", "Android", "iPad", "Tablet"])

# Infinite loop to generate and save mobile and tablet user agents
while True:
    try:
        user_agent = ua.random
        if is_mobile_or_tablet(user_agent):
            # Check if this user agent is already in the database
            cursor.execute("SELECT 1 FROM mobile_user_agents WHERE user_agent = ?", (user_agent,))
            result = cursor.fetchone()

            if result is None:  # Only insert if it's not already in the database
                cursor.execute('INSERT INTO mobile_user_agents (user_agent) VALUES (?)', (user_agent,))
                conn.commit()  # Commit after each insertion
                print(f"Saved: {user_agent}")
        else:
            print("Skipped: not a mobile/tablet user agent")
            
        # Optional: add a small sleep to avoid spamming requests too fast
        time.sleep(0.1)
        
    except Exception as e:
        print(f"Error: {e}")
        break  # Break the loop on an error

# Close the connection after finishing
conn.close()

print("Finished saving mobile and tablet user agents.")
