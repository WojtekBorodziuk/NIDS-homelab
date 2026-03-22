import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1484912066409271480/3VGIJ4UPpnQuKX3aB34t--6dZpJOmurHogUuMMOEzviNafmkCJhQYdJSGa8ezVLsXKWi"

def send_discord_alert(source_ip, attack_type, details):
    # Tworzymy ładunek w formacie JSON
    message = {
        "embeds": [{
            "title": "🚨 ALERT NIDS!",
            "color": 15548997,
            "fields": [
                {"name": "Typ ataku", "value": attack_type, "inline": True},
                {"name": "Źródło", "value": source_ip, "inline": True},
                {"name": "Szczegóły", "value": details, "inline": False}
            ]
        }]
    }
    
    try:
        # Wysyłamy żądanie do serwerów Discorda
        requests.post(DISCORD_WEBHOOK_URL, json=message, timeout=3)
    except Exception as e:
        print(f"[!] Błąd Discorda: {e}")
