import html
from aiogram.types import Message

def texttohtml(message: Message):
    entities = message.entities
    text = message.text
    entities.sort(key=lambda x: x["offset"])
    formatted_text_parts = []
    current_offset = 0
    entity_types = {
        "bold": "b",
        "italic": "i",
        "code": "code",
        "strikethrough": "s",
        "text_link": "a"
    }
    for entity in entities:
        offset = entity.offset
        length = entity.length
        raw_text = text[current_offset:offset]
        formatted_text_parts.append(html.escape(raw_text))
        entity_type = entity_types.get(entity.type)
        if entity_type:
            formatted_text_parts.append(f"<{entity_type}>")
            formatted_text_parts.append(html.escape(text[offset:offset + length]))
            formatted_text_parts.append(f"</{entity_type}>")
        current_offset = offset + length
    raw_text = text[current_offset:]
    formatted_text_parts.append(html.escape(raw_text))

    formatted_text = "".join(formatted_text_parts)

    return formatted_text