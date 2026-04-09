import urllib.request
import json
import time

BOT_TOKEN = "8744576713:AAFuvJ9vay9-G0rGChUeVokGs_BSaTDKQCM"
CHAT_ID = "-1002002451658"

posts = [
    {
        "from_chat_id": "@popsmarketing",
        "message_id": 15668,
        "caption": """Есть такой управленческий навык - избирательный слух.

Когда сотрудник говорит "мы не успеваем в срок" - начальник слышит всё.
Когда тот же сотрудник спрашивает "оплатите переработку" - помехи.

Я много нанимал людей в маркетинговые команды. И такие руководители всегда искренне удивляются высокой текучке. Они правда не понимают почему.

Потому что одностороннее слышание работает недолго. Рынок всё равно расскажет сотруднику его цену.

<a href="https://t.me/popsmarketing/15668">→ оригинал</a>"""
    },
    {
        "from_chat_id": "@collegi",
        "message_id": 20470,
        "caption": """Ашан поставил лапшичную внутри супермаркета.

С точки зрения маркетинга это не общепит - это инструмент. Человек зашёл поесть, а вышел с корзиной. Трафик, который уже пришёл сам, конвертируется в дополнительный чек.

Ритейл давно понял: продавать надо не товар, а причину остаться подольше.

Горнолыжные курорты это знают. Ресторан на склоне - не ресторан, это якорь, который держит гостя на территории ещё на два часа и увеличивает средний чек втрое.

<a href="https://t.me/collegi/20470">→ оригинал</a>"""
    },
    {
        "from_chat_id": "@collegi",
        "message_id": 20469,
        "caption": """Маркетинговый кейс без единого рубля бюджета.

Россияне массово пополнили Apple ID на десятки тысяч - потому что в один день все поверили, что сервис отключат завтра.

Apple ничего не делал. Просто слух плюс страх - и конверсия случилась сама.

FOMO продаёт лучше любого оффера. Это не манипуляция - это базовая механика. Умные бренды её не создают, они просто не мешают ей работать.

Если у вас есть реальный дедлайн в продукте - не прячьте его. Он ваш лучший продажник.

<a href="https://t.me/collegi/20469">→ оригинал</a>"""
    },
    {
        "from_chat_id": "@costperlead",
        "message_id": 12670,
        "caption": """HBO выпускает спецвыпуск о съёмках за три дня до первых кадров сериала.

Это не новость - это прогрев.

Не "вот продукт - смотрите", а "вот как мы его делаем - присоединяйтесь к процессу". Зрителя включают в историю ещё до релиза.

Классическая воронка: интерес к закулисью - вовлечённость - ожидание - просмотр.

Если вы запускаете что-то и молчите до дня икс - вы теряете самый тёплый момент для контакта с аудиторией.

<a href="https://t.me/costperlead/12670">→ оригинал</a>"""
    },
]

def copy_message(from_chat_id, message_id, caption):
    payload = {
        "chat_id": CHAT_ID,
        "from_chat_id": from_chat_id,
        "message_id": message_id,
        "caption": caption,
        "parse_mode": "HTML"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result

for p in posts:
    result = copy_message(p["from_chat_id"], p["message_id"], p["caption"])
    ok = result.get("ok")
    print(f"{'OK' if ok else 'FAIL'} — {p['from_chat_id']}/{p['message_id']}")
    if not ok:
        print(f"  Error: {result.get('description')}")
    time.sleep(0.5)
