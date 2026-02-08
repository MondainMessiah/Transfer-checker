import requests
from bs4 import BeautifulSoup

# Your Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1385893417262907392/uXJZkvxyN0fgYV2nMDi0ciDMuMvfIhMB52fNNaMHTBIed8nF03EBMkdNQ17a0tdm0NUy"

# Character URLs
CHARACTERS = {
    "Hex Good": "https://guildstats.eu/character?nick=Hex+good",
    "Kamikadzei": "https://guildstats.eu/character?nick=Kamikadzei"
}

# The world they are SUPPOSED to be on
HOME_WORLD = "Monza"

def get_world(url):
    try:
        # User-Agent is required to avoid being blocked by GuildStats
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # GuildStats displays world name in a specific table cell
        for td in soup.find_all('td'):
            if 'World:' in td.text:
                world_name = td.find_next_sibling('td').text.strip()
                return world_name
        return "Not Found"
    except Exception as e:
        return f"Error ({str(e)})"

# Build the Discord message
report = "## 🛡️ Daily Tibia Transfer Report\n"
for name, url in CHARACTERS.items():
    current_world = get_world(url)
    
    if current_world == HOME_WORLD:
        status = f"✅ Still on {HOME_WORLD}"
    elif "Error" in current_world or "Not Found" in current_world:
        status = "⚠️ Could not reach GuildStats"
    else:
        status = f"🚨 **TRANSFER DETECTED! Moved to {current_world.upper()}**"
    
    report += f"* **{name}**: {current_world} — {status}\n"

# Push to Discord
requests.post(WEBHOOK_URL, json={"content": report})
print("Report sent to Discord.")
