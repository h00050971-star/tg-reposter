import urllib.request
import json
import time

BOT_TOKEN = "8744576713:AAFuvJ9vay9-G0rGChUeVokGs_BSaTDKQCM"
CHAT_ID = "-1002002451658"

posts = [
    {
        "channel": "@popsmarketing",
        "summary": "Гендир не слышит вопросов о переработках — видимо, избирательная глухота входит в топ-менеджерский пакет.",
        "url": "https://t.me/popsmarketing/15668"
    },
    {
        "channel": "@collegi",
        "summary": "Ашан открыл раменные прямо в своих супермаркетах: лапша, токпокки, суп суджеби — всё самостоятельно. Первая точка в московском Авиапарке, сеть будет расширяться.",
        "url": "https://t.me/collegi/20470"
    },
    {
        "channel": "@collegi",
        "summary": "Реакция россиян, которые в панике пополняли Apple ID на десятки тысяч рублей — теперь Telegram жив, а деньги потрачены.",
        "url": "https://t.me/collegi/20469"
    },
    {
        "channel": "@costperlead",
        "summary": "5 апреля HBO выпустит спецвыпуск о съёмках сериала «Гарри Поттер»: первые кадры, актёры на роли Дамблдора, Хагрида и Снейпа. Сам сериал — в ночь на 26 декабря.",
        "url": "https://t.me/costperlead/12670"
    },
]

def send_message(channel, summary, url):
    text = f"📌 <b>{channel}</b>\n\n{summary}\n\n<a href=\"{url}\">→ оригинал</a>"
    payload = {
        "chat_id": CHAT_ID,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "text": text
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
    ok = send_message(p["channel"], p["summary"], p["url"])
    print(f"{'OK' if ok else 'FAIL'} — {p['channel']}: {p['summary'][:50]}...")
    time.sleep(0.5)
