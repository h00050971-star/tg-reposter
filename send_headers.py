import urllib.request
import json
import time

BOT_TOKEN = "8744576713:AAFuvJ9vay9-G0rGChUeVokGs_BSaTDKQCM"
CHAT_ID = "-1002002451658"

posts = [
    {
        # механика: разрыв ожидания / парадокс
        "text": 'слух отличный. память отличная. но ровно на вопросе об оплате переработок у гендира пропадает и то и другое <a href="https://t.me/popsmarketing/15668">🙉</a>',
        "preview_url": "https://t.me/popsmarketing/15668"
    },
    {
        # механика: прямая провокация
        "text": 'ашан поставил лапшичную не чтобы накормить. чтобы ты зашёл за лапшой и вышел с тележкой. вот и весь ритейл-маркетинг <a href="https://t.me/collegi/20470">🍜</a>',
        "preview_url": "https://t.me/collegi/20470"
    },
    {
        # механика: шок-цифра
        "text": 'люди закинули на apple id по 50 тысяч из-за одного слуха в тг. apple ничего не делал. конверсия случилась сама <a href="https://t.me/collegi/20469">🍎</a>',
        "preview_url": "https://t.me/collegi/20469"
    },
    {
        # механика: незакрытый вопрос
        "text": 'почему hbo показывает закулисье за 3 дня до первых кадров... когда сам сериал выйдет только в декабре <a href="https://t.me/costperlead/12670">🎬</a>',
        "preview_url": "https://t.me/costperlead/12670"
    },
]

def send_message(text, preview_url):
    payload = {
        "chat_id": CHAT_ID,
        "parse_mode": "HTML",
        "text": text,
        "link_preview_options": {
            "url": preview_url,
            "show_above_text": False
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result.get("ok")

for p in posts:
    ok = send_message(p["text"], p["preview_url"])
    print(f"{'OK' if ok else 'FAIL'} — {p['preview_url']}")
    time.sleep(0.5)
