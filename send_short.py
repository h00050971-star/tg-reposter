import urllib.request
import json
import time

BOT_TOKEN = "8744576713:AAFuvJ9vay9-G0rGChUeVokGs_BSaTDKQCM"
CHAT_ID = "-1002002451658"

posts = [
    {
        "text": 'Избирательный слух - недооценённый управленческий инструмент. Работает ровно до первого звонка хедхантера. <a href="https://t.me/popsmarketing/15668">🙉</a>',
        "preview_url": "https://t.me/popsmarketing/15668"
    },
    {
        "text": 'Продуктовый ритейл наконец открыл якорный трафик. Торговые центры объясняли эту механику ещё в 90-х. <a href="https://t.me/collegi/20470">🍜</a>',
        "preview_url": "https://t.me/collegi/20470"
    },
    {
        "text": 'Лучший FOMO-маркетинг - тот, который ты не запускал. Apple ничего не делал, просто не мешал панике работать. <a href="https://t.me/collegi/20469">🍎</a>',
        "preview_url": "https://t.me/collegi/20469"
    },
    {
        "text": 'Спецвыпуск за 3 дня до первых кадров - классический прогрев. В продукт включают ещё до того, как он есть. <a href="https://t.me/costperlead/12670">🎬</a>',
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
