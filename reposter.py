"""
ТГ Репостер — парсит 3 канала, нумерует посты, отправляет в канал
Зависимости: pip install requests
"""

import re
import json
import time
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

import os
import requests

# ─── КОНФИГ ────────────────────────────────────────────────
TG_BOT_TOKEN  = os.environ.get("TG_BOT_TOKEN", "8744576713:AAFuvJ9vay9-G0rGChUeVokGs_BSaTDKQCM")
TG_CHAT_ID    = "-1002002451658"
CHANNELS      = ["popsmarketing", "collegi", "costperlead"]
HOURS_BACK    = 10
CACHE_FILE    = Path(__file__).parent / "posts_cache.json"
# ────────────────────────────────────────────────────────────


def fetch_posts(channel: str, hours_back: int) -> list[dict]:
    url = f"https://t.me/s/{channel}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    html = r.text

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    posts = []
    post_blocks = re.split(r'(?=data-post="' + channel + r'/\d+")', html)

    for block in post_blocks:
        try:
            m_id = re.search(r'data-post="[^/]+/(\d+)"', block)
            if not m_id:
                continue
            post_id = m_id.group(1)

            m_dt = re.search(r'<time datetime="([^"]+)"', block)
            if not m_dt:
                continue
            dt = datetime.fromisoformat(m_dt.group(1))
            if dt < cutoff:
                continue

            m_text = re.search(
                r'class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',
                block, re.DOTALL
            )
            if not m_text:
                continue

            text = re.sub(r'<br\s*/?>', '\n', m_text.group(1))
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'&amp;', '&', text)
            text = re.sub(r'&lt;', '<', text)
            text = re.sub(r'&gt;', '>', text)
            text = re.sub(r'&nbsp;', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()

            if len(text) < 15:
                continue

            posts.append({
                "channel": f"@{channel}",
                "post_id": post_id,
                "url": f"https://t.me/{channel}/{post_id}",
                "date": dt.isoformat(),
                "text": text
            })
        except Exception:
            continue

    return posts


def send_telegram(text: str, preview_url: str = None) -> bool:
    payload = {
        "chat_id": TG_CHAT_ID,
        "parse_mode": "HTML",
        "text": text,
    }
    if preview_url:
        payload["link_preview_options"] = {
            "url": preview_url,
            "show_above_text": False
        }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read()).get("ok", False)


MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

def format_date_ru(iso_date: str) -> str:
    dt = datetime.fromisoformat(iso_date).astimezone(timezone(timedelta(hours=3)))
    return f"{dt.day} {MONTHS_RU[dt.month]} {dt.year}"


def main():
    print(f"Парсю последние {HOURS_BACK} часов...")
    all_posts = []

    for channel in CHANNELS:
        try:
            posts = fetch_posts(channel, HOURS_BACK)
            print(f"  @{channel}: {len(posts)} постов")
            all_posts.extend(posts)
        except Exception as e:
            print(f"  @{channel}: ошибка — {e}")

    if not all_posts:
        print("Новых постов нет.")
        return

    # Сортируем по времени, нумеруем
    all_posts.sort(key=lambda x: x["date"])
    for i, post in enumerate(all_posts, 1):
        post["num"] = i

    # Сохраняем кэш
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)
    print(f"Сохранено {len(all_posts)} постов в {CACHE_FILE.name}")

    # Отправляем каждый пост отдельным сообщением
    sent = 0
    for post in all_posts:
        date_str = format_date_ru(post["date"])
        header = f"{post['num']} за {date_str}"
        text_safe = post["text"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        message = f"{header}\n\n{text_safe}\n\n<a href=\"{post['url']}\">→ {post['channel']}</a>"

        ok = send_telegram(message, post["url"])
        print(f"  [{post['num']}] {post['channel']}: {'OK' if ok else 'FAIL'}")
        if ok:
            sent += 1
        time.sleep(0.5)

    print(f"Отправлено: {sent}/{len(all_posts)}")


if __name__ == "__main__":
    main()
