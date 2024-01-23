import html
from aiogram.types import Message

def texttohtml(message):
    formatted_text = ""

    entities = message.entities
    current_offset = 0

    for entity in entities:
        entity_type = entity.type
        offset = entity.offset
        length = entity.length
        text = message.text[offset : offset + length]
        print(text)

        formatted_text += f"{message.text[current_offset:offset]}"

        if entity_type == "bold":
            formatted_text += f"<b>{text}</b>"
        elif entity_type == "italic":
            formatted_text += f"<em>{text}</em>"

        current_offset = offset + length

    formatted_text += f"{message.text[current_offset:]}"

    return formatted_text