import urllib.request
import json
import time

BOT_TOKEN = "8744576713:AAFuvJ9vay9-G0rGChUeVokGs_BSaTDKQCM"
CHAT_ID = "-1002002451658"

posts = [
    {
        "text": 'классика жанра... слух отличный, пока не заходит разговор о деньгах. внезапная глухота - это теперь корпоративный навык что ли <a href="https://t.me/popsmarketing/15668">🙉</a>',
        "preview_url": "https://t.me/popsmarketing/15668"
    },
    {
        "text": 'ашан открыл лапшичную внутри себя и вы думаете это забота о покупателях... нет, ты зашёл за лапшой а вышел с тележкой. старый трюк торгцентров просто теперь с соусом <a href="https://t.me/collegi/20470">🍜</a>',
        "preview_url": "https://t.me/collegi/20470"
    },
    {
        "text": 'ну и кто виноват... никто не заставлял закидывать apple id на 50к из-за слухов в тг. зато теперь знаем что страх конвертит лучше любой акции <a href="https://t.me/collegi/20469">🍎</a>',
        "preview_url": "https://t.me/collegi/20469"
    },
    {
        "text": 'hbo не дураки... спецвыпуск о съёмках за 3 дня до первых кадров. типичный прогрев - в воронку затягивают ещё до того как есть что смотреть <a href="https://t.me/costperlead/12670">🎬</a>',
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
