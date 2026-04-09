"""
Обработчик команд: ты пишешь число в канал → бот переписывает пост и постит обратно
Зависимости: pip install requests
"""

import os
import re
import json
import time
import urllib.request
from pathlib import Path

import requests

# ─── КОНФИГ ────────────────────────────────────────────────
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8744576713:AAFuvJ9vay9-G0rGChUeVokGs_BSaTDKQCM")
TG_CHAT_ID   = "-1002002451658"
GH_PAT       = os.environ.get("GH_PAT", "")
CACHE_FILE   = Path(__file__).parent / "posts_cache.json"
OFFSET_FILE  = Path(__file__).parent / "last_update_id.txt"
# ────────────────────────────────────────────────────────────

STYLE_PROMPT = """Ты - голос маркетолога. Бывший директор по маркетингу горнолыжного курорта.
Пиши короткий ироничный комментарий к новости. 100-200 символов максимум.

Правила:
- строчные буквы, разговорный стиль, жаргон миллениалов/зумеров
- многоточия, живые интонации, можно ошибаться в пунктуации
- применяй одну механику: парадокс, шок-цифра, провокация или незакрытый вопрос
- в конце тематическое эмодзи как кликабельная ссылка: <a href="POST_URL">EMOJI</a>
- замени POST_URL на реальную ссылку из данных
- перед эмодзи точку не ставь
- запрещено: слово "про", длинные тире, конструкция "это не X а Y"

Выдай только готовый HTML-текст, без пояснений."""


def tg_api(method: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/{method}",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def get_updates(offset: int) -> list:
    result = tg_api("getUpdates", {
        "offset": offset,
        "timeout": 5,
        "allowed_updates": ["channel_post"]
    })
    return result.get("result", [])


def delete_message(message_id: int):
    try:
        tg_api("deleteMessage", {"chat_id": TG_CHAT_ID, "message_id": message_id})
    except Exception:
        pass


def rewrite_with_github_models(post: dict) -> str:
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": STYLE_PROMPT},
            {"role": "user", "content": f"Новость из {post['channel']}:\n{post['text']}\n\nСсылка: {post['url']}"}
        ],
        "max_tokens": 300,
        "temperature": 0.8
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://models.inference.ai.azure.com/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {GH_PAT}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
        return result["choices"][0]["message"]["content"].strip()


def send_rewrite(text: str, preview_url: str):
    tg_api("sendMessage", {
        "chat_id": TG_CHAT_ID,
        "parse_mode": "HTML",
        "text": text,
        "link_preview_options": {
            "url": preview_url,
            "show_above_text": False
        }
    })


def load_cache() -> list:
    if CACHE_FILE.exists():
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def load_offset() -> int:
    if OFFSET_FILE.exists():
        try:
            return int(OFFSET_FILE.read_text().strip())
        except Exception:
            pass
    return 0


def save_offset(offset: int):
    OFFSET_FILE.write_text(str(offset))


def main():
    offset = load_offset()
    cache = load_cache()
    print(f"Проверяю обновления (offset={offset}), постов в кэше: {len(cache)}")

    updates = get_updates(offset)
    if not updates:
        print("Новых сообщений нет.")
        return

    processed = 0
    new_offset = offset

    for update in updates:
        new_offset = max(new_offset, update["update_id"] + 1)
        post_update = update.get("channel_post", {})

        # Проверяем что это наш канал и сообщение — просто число
        chat_id = str(post_update.get("chat", {}).get("id", ""))
        text = post_update.get("text", "").strip()
        message_id = post_update.get("message_id")

        if chat_id != TG_CHAT_ID:
            continue

        if not re.fullmatch(r'\d+', text):
            continue

        num = int(text)
        post = next((p for p in cache if p.get("num") == num), None)

        if not post:
            print(f"  Пост #{num} не найден в кэше.")
            delete_message(message_id)
            continue

        print(f"  Переписываю пост #{num} из {post['channel']}...")
        try:
            rewritten = rewrite_with_github_models(post)
            delete_message(message_id)
            send_rewrite(rewritten, post["url"])
            print(f"  #{num} отправлен.")
            processed += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  Ошибка при обработке #{num}: {e}")

    save_offset(new_offset)
    print(f"Готово. Обработано команд: {processed}")


if __name__ == "__main__":
    main()
