import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1385893417262907392/uXJZkvxyN0fgYV2nMDi0ciDMuMvfIhMB52fNNaMHTBIed8nF03EBMkdNQ17a0tdm0NUy"

CHARACTERS = {
    "Hex Good": "https://guildstats.eu/transferability-calc?nick=Hex+good&dat=&worldType=0",
    "Kamikadzei": "https://guildstats.eu/transferability-calc?nick=Kamikadzei&dat=&worldType=0"
}

def get_world(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # GuildStats specific selector for the world name
        world_tag = soup.find('a', href=lambda x: x and 'world=' in x)
        return world_tag.text.strip() if world_tag else "Unknown"
    except:
        return "Error"

report = "## 🛡️ Tibia Transfer Daily Report\n"
for name, url in CHARACTERS.items():
    world = get_world(url)
    status = "✅ No change" if world == "Damora" else f"🚨 **MOVED TO {world.upper()}**"
    report += f"* **{name}**: {world} ({status})\n"

requests.post(WEBHOOK_URL, json={"content": report})
