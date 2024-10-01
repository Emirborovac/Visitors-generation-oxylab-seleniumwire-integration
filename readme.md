# Automated Web Visit Simulation with Selenium Wire

## Overview

This project is designed to simulate automated visits to a specified webpage using **Selenium Wire**. It features proxy integration, random user agents, and realistic browsing behavior like scrolling and clicking. The script uses **Oxylabs** proxies to rotate IPs, and a **SQLite database** to select random mobile user agents for each session.

### Key Features

- **Randomized User Agents**: User agents are fetched from a SQLite database of mobile user agents, ensuring that each session mimics a different browser or device.
- **Proxy Rotation**: Each visit is routed through a randomly chosen Oxylabs proxy, simulating users from different IP addresses or regions.
- **Simulated Browsing Behavior**: The script simulates real user activity by scrolling the page randomly and clicking on various clickable elements.
- **Concurrency and Random Timing**: Supports multiple concurrent visits with random intervals between visits. Each visit spends a random amount of time on the page.
- **Session Logging**: Logs each session, including the proxy used, user agent, time spent on the page, and domain visited.

## How It Works

1. **Database of User Agents**:
   - The script uses a SQLite database (`user_agents.db`) that contains a list of mobile user agents. The table `mobile_user_agents` stores the user agents.
   - For each visit, a random user agent is selected from this database.

2. **Proxy Integration**:
   - Proxies are provided via **Oxylabs**.
   - The script integrates these proxies using **Selenium Wire** for authenticated requests. A random proxy is selected for each web visit.

3. **Simulating Visits**:
   - The script starts one or more threads to simulate concurrent visits. The number of concurrent visitors is randomly chosen within a defined range (`concurrency_range`).
   - Each visitor is assigned a random user agent and proxy.
   - The visitor spends a random amount of time on the page (`min_time_range`, `max_time_range`), scrolls randomly, and optionally clicks on page elements like links or buttons.
   - After the visit, the session details are logged.

## Structure of the Code

### Main Components:

1. **Proxy Configuration (`chrome_proxy`)**:
   - This function configures the proxy using Oxylabs credentials. The proxy is applied to the browser session using **Selenium Wire**.

2. **Random User Agent Selection (`get_random_user_agent`)**:
   - The script fetches a random user agent from the `mobile_user_agents` table in the SQLite database.

3. **Browser Configuration (`configure_browser`)**:
   - Sets up a new browser session using the selected proxy and user agent. The session is then ready for browsing.

4. **Browsing Simulation (`browse_website`)**:
   - This function simulates browsing behavior. It scrolls randomly within the page and can optionally click on page elements. The browser session lasts for a random time between the defined `min_time_range` and `max_time_range`.

5. **Visitor Threading (`visitor_thread`)**:
   - Each visitor thread is responsible for simulating a visit to the website. It configures the browser, visits the domain, and logs the session.

6. **Start Simulation (`start_simulation`)**:
   - Orchestrates the entire process. This function manages concurrency and ensures the target number of visits is achieved. It randomly determines the number of concurrent visitors and the time intervals between them.

### Database Structure

The SQLite database contains a single table for storing user agents:

```sql
CREATE TABLE mobile_user_agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_agent TEXT NOT NULL
);
```

### Logs

The script logs session data to a log file, including:

- Proxy used
- User agent used
- Time spent on the page
- Domain visited
- Country (if available)

Example log entry:

```
Proxy: emirborova_brluB@tr-pr.oxylabs.io:30000, User Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1, Max Time: 4.57s, Domain: https://example.com, Country: Unknown
```

## How to Run the Script

### Prerequisites

- **Python 3.x**
- **Selenium Wire** and **Selenium** libraries
- **webdriver-manager** for managing Chrome WebDriver
- Oxylabs proxy account

### Install Required Packages

1. Clone this repository.
2. Install required libraries using the following command:

```bash
pip install -r requirements.txt
```

### Database Setup

1. Ensure that the `user_agents.db` database exists in the specified path.
2. Populate the `mobile_user_agents` table with mobile user agents.

### Running the Simulation

1. Configure the number of visits and concurrency in the `start_simulation` function:

```python
concurrency_range = (1, 3)  # Range of concurrent visitors
domain = "https://yourdomain.com"  # The target domain
min_time_range = (1, 2)  # Min time on page (seconds)
max_time_range = (3, 5)  # Max time on page (seconds)
cooldown_range = (1, 3)  # Cooldown between visitors (seconds)
target_visits = 5  # Total number of visits
```

2. Run the script:

```bash
python visit_simulation.py
```

## Areas of Improvement

Here are some potential areas of improvement for further enhancement:

1. **Error Handling**: Implement robust error handling and retry logic, especially for proxy connection failures, timeouts, or browser crashes.
2. **More Dynamic Interactions**: Enhance the browsing simulation by adding more interactive behavior such as filling out forms, hovering over elements, etc.
3. **Geolocation Simulation**: Use proxies from specific regions and simulate geolocation by adding headers or using location-based proxies.
4. **Captcha Handling**: If the target site implements Captchas, consider integrating a Captcha-solving service or building logic to handle Captcha challenges.
5. **Headless Mode**: Currently, the browser is visible during the simulation. You can enable headless mode for a more efficient, less resource-intensive run by adding `options.headless = True` in the `configure_browser` function.

