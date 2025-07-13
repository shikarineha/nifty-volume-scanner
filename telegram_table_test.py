
import requests

# --- Your Telegram bot token & chat ID ---
TELEGRAM_TOKEN = "7632650061:AAFWRVJuIKCOwsuzio9j3HVDp5xWq4ki4gA"
TELEGRAM_CHAT_ID = "6712530011"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except Exception as e:
        print("Telegram Error:", e)

def main():
    data = [
        {"Symbol": "SBIN-EQ", "Close": 582.25, "Volx7": 3.5, "Volx15": 2.8, "Volx30": 1.9},
        {"Symbol": "TCS-EQ", "Close": 3721.10, "Volx7": 6.2, "Volx15": 4.4, "Volx30": 2.7},
        {"Symbol": "RELIANCE-EQ", "Close": 2895.75, "Volx7": 1.2, "Volx15": 0.9, "Volx30": 1.0}
    ]

    msg_lines = [
        "📊 *Test Volume Table*",
        "```",
        f"{'Symbol':<12} {'Close':>8} {'Volx7':>7} {'Volx15':>7} {'Volx30':>7}",
        f"{'-'*12} {'-'*8} {'-'*7} {'-'*7} {'-'*7}"
    ]

    for row in data:
        msg_lines.append(
            f"{row['Symbol']:<12} {row['Close']:>8.2f} {row['Volx7']:>7} {row['Volx15']:>7} {row['Volx30']:>7}"
        )

    msg_lines.append("```")
    message = "\n".join(msg_lines)

    send_telegram_message(message)

if __name__ == "__main__":
    main()
