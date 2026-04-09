#!/bin/bash

BOT_TOKEN="8744576713:AAFuvJ9vay9-G0rGChUeVokGs_BSaTDKQCM"
CHAT_ID="-1002002451658"

TEXT='📰 <b>ДАЙДЖЕСТ</b> | 2 апреля | последние 10 часов

<b>@popsmarketing</b>
• Яндекс Маркет снижает комиссии до 9% для FBY при подписке (против прежних 41–48%) → <a href="https://t.me/popsmarketing/15662">пост</a>
• Минцифры поручило крупнейшим платформам блокировать трафик с VPN с 15 апреля → <a href="https://t.me/popsmarketing/15660">пост</a>

<b>@collegi</b>
• Apple сохранит данные россиян из iCloud+ даже после окончания подписки → <a href="https://t.me/collegi/20468">пост</a>
• Минцифры: блокировка VPN с 15 апреля — методичка готова, список компаний огромный → <a href="https://t.me/collegi/20465">пост</a>
• В Питере включили белые списки — интернет упал → <a href="https://t.me/collegi/20461">пост</a>
• Ашан запустил раменные прямо в супермаркетах → <a href="https://t.me/collegi/20470">пост</a>

<b>@costperlead</b>
• С 15 апреля нельзя зайти в Сбер, Яндекс, VK, WB, Ozon с включённым VPN → <a href="https://t.me/costperlead/12667">пост</a>
• Запросы на переезд в Беларусь резко выросли в дни новостей о Telegram и VPN → <a href="https://t.me/costperlead/12669">пост</a>
• Электричка Смоленск–Орша/Витебск: 2 часа, до 500 руб, ежедневно → <a href="https://t.me/costperlead/12666">пост</a>
• HBO: 5 апреля выйдет спецвыпуск о съёмках «Гарри Поттера» → <a href="https://t.me/costperlead/12670">пост</a>'

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data-binary @- <<EOF
{
  "chat_id": "${CHAT_ID}",
  "parse_mode": "HTML",
  "disable_web_page_preview": true,
  "text": $(echo "$TEXT" | python3 -c "import sys, json; print(json.dumps(sys.stdin.read()))")
}
EOF
