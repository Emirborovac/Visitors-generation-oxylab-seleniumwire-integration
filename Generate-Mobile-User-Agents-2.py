import requests as req
from bs4 import BeautifulSoup
import sqlite3
import time

# Set up SQLite connection
db_path = ""
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table for storing mobile and tablet user agents (if not already exists)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mobile_user_agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_agent TEXT NOT NULL
    )
''')

# List of browsers to get user agents from
lst = ['Firefox', 'Internet+Explorer', 'Opera', 'Safari', 'Chrome', 'Edge', 'Android+Webkit+Browser']

# Function to check if a user agent is mobile or tablet
def is_mobile_or_tablet(user_agent):
    return any(keyword in user_agent for keyword in ["Mobile", "iPhone", "Android", "iPad", "Tablet"])

# Function to save user agent to the database
def save_user_agent(user_agent):
    # Check if this user agent is already in the database
    cursor.execute("SELECT 1 FROM mobile_user_agents WHERE user_agent = ?", (user_agent,))
    result = cursor.fetchone()

    if result is None:  # Only insert if it's not already in the database
        cursor.execute('INSERT INTO mobile_user_agents (user_agent) VALUES (?)', (user_agent,))
        conn.commit()  # Commit after each insertion
        print(f"Saved: {user_agent}")
    else:
        print("Skipped: user agent already in database")

# Function to get user agents from the website
def get_user_agents(br):
    url = f'http://www.useragentstring.com/pages/useragentstring.php?name={br}'
    try:
        r = req.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            div = soup.find('div', {'id': 'liste'})
            if div:
                links = div.findAll('a')
                for link in links:
                    user_agent = link.text.strip()
                    if is_mobile_or_tablet(user_agent):
                        save_user_agent(user_agent)
                    else:
                        print(f"Skipped: not a mobile/tablet user agent ({user_agent})")
            else:
                print(f"No user agents found for {br}")
        else:
            print(f"Failed to retrieve user agents for {br}")
    except Exception as e:
        print(f"Error fetching user agents for {br}: {e}")

# Loop through the list of browsers
for browser in lst:
    get_user_agents(browser)
    time.sleep(10)  # Add a delay to avoid overwhelming the server

# Close the database connection
conn.close()

print("Finished saving mobile and tablet user agents.")
