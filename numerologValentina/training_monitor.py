import asyncio
import datetime
from loader import bot
from data.config import TRAINING_CHANNEL
from database.models import TaroTraining


async def main():
    while True:
        trainings = await TaroTraining.query.where(
            TaroTraining.is_banned == False
        ).gino.all()
        now = datetime.datetime.now()
        for training in trainings:
            if now > training.end_date:
                await training.update(is_banned=True).apply()
                await bot.ban_chat_member(TRAINING_CHANNEL,user_id=training.user)

        await asyncio.sleep(60 * 30)


if __name__ == "__main__":
    import database.connection

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
