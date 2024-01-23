from aiogram.types import Message



data = {
    "message_id": 755,
    "from": {
        "id": 875044476,
        "is_bot": False,
        "first_name": "Beloff",
        "username": "belofflab",
        "language_code": "ru",
        "is_premium": True,
    },
    "chat": {
        "id": 875044476,
        "first_name": "Beloff",
        "username": "belofflab",
        "type": "private",
    },
    "date": 1706008481,
    "text": "‼️Акция за донейшн ‼️\nдо 31 января\n\nБлагодаря такому   прогнозу сможете:\n\n— скорректировать свои планы, поездки. Так же заранее предпринять действия, для того что бы сохранить свои ресурсы.\n— получите подсказки ;\n— как обойти острые углы в отношениях (если таковы будут);\n— вероятные события;\n— какие люди будут учавствовать в вашей жизни и многое другое…\n\nПрогноз является ключом для открытия самой выгодной для Вас двери, и верного выбора пути. \n\nПредупреждён значит вооружён😉\n\n‼️Кодовое  слово «Акция донат»‼️\nПиши свою дату рождения и сколько тебе полных лет.\n\nЗаписаться на прогноз ⤵️\n🙎‍♀️ @valentina_numerologEnerg", 
    "entities":[{"type": "bold", "offset": 0, "length": 18
       }, {"type": "bold", "offset": 19, "length": 16
       }, {"type": "bold", "offset": 355, "length": 7
       }, {"type": "bold", "offset": 447, "length": 28
       }, {"type": "bold", "offset": 496, "length": 5
       }, {"type": "bold", "offset": 502, "length": 5
       }, {"type": "mention", "offset": 594, "length": 25,
}]}
def convert_to_html(message: Message):
    print(message.parse_entities())
    entities = message.get("entities", [])
    text = message.get("text", "").strip()

    formatted_text = text

    for entity in entities:
        entity_type = entity["type"]
        offset = entity["offset"]
        length = entity["length"]
        text_to_format = text[offset:offset + length]

        if entity_type == "bold":
            text_to_format = f"<b>{text_to_format}</b>"

        formatted_text = f"{formatted_text[:offset]}{text_to_format}{formatted_text[offset + length:]}"

    return formatted_text

html_string = convert_to_html(data)
print(html_string)