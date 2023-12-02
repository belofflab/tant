import os
import re
import requests
import uuid
import base64
import random
import typing as t
from aiogram import types
from decimal import Decimal
from loader import dp, bot
from data.config import SERVER_URL, BASE_DIR, CHANNEL_ID
from aiogram.dispatcher import FSMContext
from states.receipt import ReceiptState
from states.user_payment_detail import UserPaymentDetail
from states.payout import PayoutState
from keyboards.user import inline

matrix = {
    "характер": {
        "1": [
            "Ты классный слушатель - впитываешь идеи от других людей. Из множества вариантов находишь что-то свое и действуешь.",
            "В море идей и чужих мнений тебе важно слышать СЕБЯ, почаще спрашивай 'А что Я хочу?', уделяй сознательно время творчеству и хобби. Вспомни те периоды, когда 'душа радовалась', хотелось просыпаться и творить, заводить новые знакомства и делиться впечатлениями. ",
            "Важно окружать себя единомышленниками, которые будут подпитывать тебя идеями и вдохновением.Найди в соцсетях группу по своим интересам и общайся с людьми на любимые для тебя темы.Посещай нетворкинги в своем городе, там не только познакомишься с новыми людьми, но и прокачаешь навык презентации себя.",
        ],
        "11": [
            "Все ли ты реализуешь, из того, что можешь придумать? Поспорим, что только часть своих идей ты уже осуществил/осуществила. ",
            "Ты можешь придумать выход из любой ситуации и дать дельный совет коллеге, другу или близкому. ",
            "Чаще выбирайся на мероприятия, стань заметнее и делись своими идеями с миром. Открыто выражай свою точку зрения, ведь именно так другие люди услышат твои желания, поддержат и пойдут вместе с тобой. ",
            "Ты классный!!! Чтобы стать еще многограннее, можешь записаться на уроки вокала или ораторского мастерства, так через речь и голос ты ещё больше раскроешь свой потенциал.",
        ],
        "111": [
            "Вау!!!! Сколько у тебя идей!!!! Начни делиться с миром своими мыслями и наработками, напиши пост или создай группу, куда позовешь тех, кому твоя тема интересна.",
            "Идей на столько много, что каждый новый шаг рождает новую идею!!! Можешь выписывать их в тетрадь, а можешь транслировать через соцсети. Для кого-то ты станешь поддержкой, и поддержишь новыми смыслами.",
            "Например, у подруги есть блог, и ты видишь, как ей лучше продвигаться и позиционировать себя для поиска новых клиентов, поделись с ней своими мыслями по этому поводу.",
            "И да, когда обещаешь, бери столько, сколько сможешь выполнить 😜",
        ],
    },
    "энергия": {
        "2": [
            "Так-так, чувствуется, что длительные физические нагрузки тебя перенапрягают. Добавляй спорт и активность в небольшом объеме, чисто для себя, выбирай деятельность, связанную с коммуникациями, людьми, умственным трудом.",
            "Наблюдай, какие энергии несет общение с другими людьми и окружай себя теми, кто классно заряжает окружающих позитивом, вдохновляет на сотрудничество и новые проекты.",
            "Организуй удобное место для сна, для тебя это очень важно.",
            "Принимай решения в одиночестве, чтобы эмоции других людей не мешали тебе ЧУВСТВОВАТЬ СЕБЯ.",
        ],
        "22": [
            "На сколько твоей энергии хватает на тебя самого? Или можешь поделиться с другими?",
            "Если чувствуешь, что энергии маловато, можно поинтересоваться духовными практиками, которые генерируют энергию (аскеза, ранний подъем). ",
            "А можно ее увеличить с помощью посильной физической нагрузки: скандинавская хотьба, бассейн, приседания, регулярные прогулки по лесу.",
            "А что если энергии много? Тогда смело дари пользу через это качество другим людям: овладей техниками массажа, проведи мини-экскурсию по своему краю, помоги соседке с огородом или займись любой другой физической активностью, которая будет разгружать тело от напряжения.",
        ],
        "222": [
            "Уау!!! Сколько у тебя энергии!!!! Трудолюбие и настойчивость - твое кредо по жизни!!!!",
            "Через создание своих проектов ты реализуешься в мир, а еще можешь помочь создать свой проект другому!!!",
            "Энергии на столько много, что можешь перепахать непаханное поле, и прийти к своим твердым результатам.",
            "Сила здоровья, харизма, умение влиять на других людей, способность исполнять свои желания - это все про тебя!!! Да- да, это не опечатка, действуй, все у тебя получится!!!!",
        ],
    },
    "интерес": {
        "пусто": [
            "Ты свободен от навязанных стереотипов!!!! Ты даже можешь создать новую профессию или направление (так когда-то новыми были аромастилист или грумер) или объединить несколько направлений и создать свое (нейрографика - концентрат из психологии и творчества). ",
            "Нестандартное мышление и творческий подход - вот твоя сила!!! Не бойся предлагать миру идеи в том варианте, в котором видишь это ТЫ.",
            "Волнительно? Возможно, но именно ты научаешь людей не зависеть от материального.",
            "Иди своим путем, прими то, что ты не такой, как все!!! Обходи паникеров стороной, тебе важен твой собственный путь!!!",
        ],
        "3": [
            "Тебе вообще повезло!!! Ты четко ощущаешь понятия 'мои вещи', 'мои люди', 'моя территория'.",
            "Знаешь, куда вложиться, где найти нужную тебе информацию, с кем договориться и найти нужных людей.",
            "Легко внедряешь чужой опыт и накапливаешь связи, можешь обучаться и путешествовать, находить многочисленные способы решения вопроса.",
            "Замечай, легко ли тебе делиться? Выйти в соцсеть с 'говорящей головой' или написать пост, перевести на благотворительность или красочно поведать о своем путешествии, проработать обиды с психологом или собрать группу профессионалов. ",
            "Помни, мир любит баланс, будь тем, кто соблюдает этот баланс внутри себя.",
        ],
        "333": [
            "Ты как волшебная шкатулка - умеешь беречь самое лучшее!!! Ты ценишь свой опыт и опыт других людей, подмечаешь их интересы, и на основе этого создаешь что-то бОльшее!!!",
            "Возможно, ты любишь обучаться, узнавать технологии, покупать инструменты для бизнеса или хобби, собирать друзей или коллекционировать фото природы. ",
            "Расскажи близким или подписчикам о своих интересах, пишешь стихи или программы, любишь скорость или крутые горные склоны - сумей поделиться впечатлениями, так твой талант раскроется во всей красе!!! ",
            "А когда ощущаешь себя в 'болоте', значит снова пора выходить из зоны комфорта и знакомиться с новыми людьми, исследовать науки, хобби и места или просто написать список обид, ведь порой именно они так отягощает нашу душу.",
        ],
    },
    "здоровье": {
        "пусто": {
            "Ты, конечно, красавчик или красавица - умеешь жить как хочешь, из своей личной выгоды.",
            "Слушай, а ты часто раздаешь советы и рекомендации? А, может, впадаешь в жертву и думаешь, что все виноваты?",
            "Отслеживай, как реагируешь на коллектив, правила коллектива, начальника и его просьбы. Порой тебе сложно сдержать себя от высказываний и непрошенных советов, но именно это поможет тебе эффективно коммуницировать с людьми и быть полезным в команде.",
        },
        "4": [
            "Ты классно встраиваешься в коллектив, если конечно темперамент не слишком озорной.",
            "Чувствуешь личные границы других людей и бережешь свои. У тебя есть четкое понимание, что с коллективом можно сделать больше, чем в одиночку.",
            "Осознаешь ценность коллектива и готов взаимодействовать, не устраивая конфликты. Да, у всех у нас различные интересы, но для общих целей  ты способен следовать правилам, чтобы результат был просто потрясающим!!!!",
        ],
        "444": [
            "Постой, что ты там прячешь? А, так это же организаторские способности.Ты скажешь: 'Какой из меня управленец?'. Например, ты любишь йогу, создай свою группу по занятиям йогой и реализуй свой потенциал.",
            "Ты суперски умеешь объединять людей одной идеей и вести за собой. Сфера может быть любой: бизнес, духовные практики, спорт, экспертность, обучения и прочее.",
            "В плюсе у тебя дисциплина и ответственность, в минусе - критиканство и контроль.",
            "Верь в себя и в людей, делегируй обязанности и корректно объясняй их зону ответственности, держи слово и все сложится наилучшим образом для тебя!!!!",
        ],
    },
    "логика": {
        "пусто": [
            "Выбирай окружение!!! Важно выбирать тех, кто дарит тебе положительные эмоции, транслирует энергию благодарности и бодрого духа!!!",
            "Наполняй пространство вокруг себя красивыми вещами, приятной музыкой, классными фильмами. Ах, да!!!!",
            "На регулярной основе включи в свою жизнь какое-нибудь хобби:рисование, вокал, дизайн интерьера или одежды, поэзию, создание аксессуаров или любой другой вид творчества.",
            "Бывает так, что не чувствуешь волну другого человека и можешь выразить правду в жесткой, категоричной форме, старайся контролировать речь, чтобы не обидеть собеседника.",
        ],
        "5": [
            "Знаешь, многие так погружаются в работу и быт, что забывают про творчество... Надеюсь, ты не из таких",
            "Выбери, в чем тебе хочется больше проявляться, у тебя может здорово получаться все, что связано с красотой и эстетикой. А может, ты прирожденный артист, поэт или суперзвезда.",
            "Умеешь поймать 'волну' собеседника и донести информацию на душевном уровне.",
            "Тренируйся говорить комплименты, ведь от улыбки каждый становится чуточку счастливее!!!",
        ],
        "555": [
            "Ты способен создавать шедевры!!! Наверняка слышал про Гарри Поттера, так вот твой потенциал как у  его создателя!!!",
            "Ты можешь донести свои чувства до души другого человека, собрать слова в чудесные образы, а гардероб в стильные луки. Можешь вообще создать свою коллекцию!!!! Представляешь, как ты крут!!!",
            "Ты хорошо контактируешь с детьми, может даже любишь сцену, танцы или создавать красивые ролики и фото. Сейчас это особенно популярно!!!",
            "Остерегайся ревности и обид, они далеко не помощники на пути к твоим мечтам.",
        ],
    },
    "труд": {
        "пусто": [
            "Твое окружение делится на две категории: те, кто поддерживают, идут за тобой,  и те, кто пытается прогнуть, которые в тебя не верят. Вот, избавляйся от последних!!!",
            "Выбирай работу, где не нужно много копаться в цифрах и знаниях, это тебя перегружает.",
            "А при крупных покупках дай себе время, и принимай решение в одиночестве.",
            "Ты человек легкий на смену каких-то убеждений и ценностей. ",
            "Правда тебе чуть больше нужно времени, чем другим, чтобы сосредоточиться и доделать отчет или смету. Предупреждай близких, чтобы во время работы не отвлекали и отключи телефон, чтобы результат был замечательным и в срок!!!!",
        ],
        "6": [
            "Ты уверен в себе как в профессионале.",
            "При выборе профессии не зависишь от мнения других людей.",
            "Не стремишься быть хорошим, твердо транслируя именно СВОИ ценности.",
            "Расслабься, не нужно никому ничего доказывать, у тебя внутри четкое понимание 'Кто я' и 'Что я могу'.",
            "И даже если твое хобби или профессия еще или уже непопулярны, это тебя никак не смутит, а лишь подогреет интерес в более глубоком изучении любимого дела.",
        ],
        "666": [
            "Задатки руководителя или научного сотрудника!!! Вот это сюрприз: ты умеешь создать стратегию на годы вперед, глубоко изучаешь информацию и мыслишь как бы над временем, над людьми.",
            "Ты невероятно гениален!!! Изобретаешь то, что станет популярным впоследствии!!",
            "Ты классно расставляешь персонал для более эффективной работы и результатов.",
            "Не спеши обижаться, если кто-то не понимает твои инновации, всему свое время. Используй свою гениальность в профессии, или в хобби. А в общении оставайся ЧЕЛОВЕКОМ.",
        ],
    },
    "удача": {
        "пусто": [
            "Кажется, ты не доверяешь своему сердцу? Ну или не так часто, как могло быть.",
            "Разум, логика, факты - это твои инструменты по жизни.",
            "А что, если ты начнешь прислушиваться к внутреннему голосу? Наверняка, каждый такой шаг откроет чудесный путь, который так жаждет твоя душа.",
            "Смелей, доверяй интуитивным импульсам и открывай для себя новую, полную ярких красок ЖИЗНЬ!!!",
        ],
        "7": [
            "Ты знал, что тебе легче, чем другим? Ты идешь по зову собственного сердца.",
            "Пригласили тебя на мероприятие, и если внутри  рождается энергия, ты сразу действуешь в сторону внутреннего импульса.",
            "Словно у тебя есть антенны, которые подключены к внешним потокам, и ты всегда знаешь, что будешь в нужное время в нужном месте.",
            "Ты умеешь слышать знаки Вселенной и чувствуешь безопасную для себя ситуацию.",
        ],
        "777": [
            "Помогай людям в том случае, когда есть на это запрос. Бывает так, что даже не просили, а ты уже бежишь спасать.",
            "Чаще думай о своих желаниях. ",
            "У тебя есть дар считывать информацию, мысли и настроения, которые летают в воздухе. ",
            "Иногда ты можешь подсказать: 'О сделай вот это, сейчас будет полезно или 'Не ходи туда, там для тебя опасно, и такие предупреждения правдивы.",
            "Чем больше семерок в матрице, тем за большее количество людей ты душевно берешь ответственности. Береги себя!!!",
        ],
    },
    "долг": {
        "пусто": [
            "Фух, полегче!!! Ощущение, что ты любишь все контролировать. Да, это классно на руководящей должности, но не в быту и с близкими (с мужем, с сыном) ",
            "Больше доверяй другим людям, вступай на неизведанную тропу и выходи из зоны комфорта.",
            "А что если те события, которые ты не можешь просчитать наперед и спрогнозировать, приведут к еще большему счастью и твоим целям?",
            "Рискни пойти на встречу Вселенной, она всегда дает то, что человеку необходимо. Да, ты не знаешь какой будет результат, но именно так ты даешь свершиться чуду, которое так жаждет твоя душа.",
        ],
        "8": [
            "Ты четко чувствуешь связь между причиной и следствием, понимаешь законы природы, законы Вселенной.",
            "Ты доверяешь миру, осознаешь, что все происходит не просто так.",
            "Умеешь идти своей дорогой.",
            "Обрати внимание на те качества, которые у тебя выше нормы. А качество восьмерок у тебя работает как часы.",
        ],
        "888": [
            "Вспомни, может когда-то ты увлекался психологией или духовными практиками, кормил нуждающихся или волонтерил в хосписе. Это часть твоего предназначения - служить на благо людям.",
            "У тебя есть такое качество - яснознание, это когда ты не можешь логически объяснить причину событий, но точно знаешь, что это так.",
            "Иногда в погоне за материальным, этот дар  улетучивается Усмиряй гордыню, и через профессию или хобби осуществляй свою миссию. Ты посланник Бога на этой Земле!!!!",
        ],
    },
    "память": {
        "9": [
            "Любишь масштабно помечтать и пофантазировать, ведь так? 'Хочу, чтобы был мир во всем мире', 'Хочу, чтобы экология была хорошей'",
            "А что ты хочешь для себя самого прямо сейчас?",
            "Когда приходят возможности, обращай внимание не на форму (в каком виде, каким способом это пришло), а на содержание, это добавит честности с самим собой и откроет многие дороги.",
            "Перестань оправдываться и быть таким упрямцем, лучше пропиши свои цели в блокнот, разбей на микро-задачи и приступай творить свою новую ЖИЗНЬ!!!",
        ],
        "99": [
            "Сам себе мотиватор!!! Умеешь сформулировать цель, разделить ее на задачи, быстро или медленно довести до логического завершения.",
            "Классно, если будешь цели держать не только в голове, но на бумаге или в телефоне.",
            "Тебе интереснее договариваться, чем конфликтовать.",
            "Под одно дело можешь запланировать параллельно несколько звонков, встреч, перемещений, вообщем ты такой живчик!!!",
        ],
        "999": [
            "Скорость мышления и принятия решений круче, чем у других!!! Даже в быту ты быстро можешь сообразить, как что лучше организовать.",
            "Умеешь видеть выгодные знакомства, твой круг знакомств от статусных до самых обычных.",
            "Легко перестраиваешься под меняющиеся обстоятельства и решения других людей.",
            "Можешь 'пойти по головам' в достижении своей цели, но не стоит, в душе ты безконфликтный и выбираешь дружбу!!!",
            "И да, в погоне за целями, давай себе время на безцельный отдых и благодарность за проделанную работу.",
        ],
    },
}


@dp.message_handler(commands="start")
async def start(message: t.Union[types.Message, types.CallbackQuery], **kwargs) -> None:
    response = requests.get(url=SERVER_URL + f"/workers/{message.from_user.id}")
    if response.status_code != 200:
        return
    data = response.json()
    payment_details_response = requests.get(SERVER_URL + "/admin/payment/details/")
    payment_details = payment_details_response.json()

    if isinstance(message, types.Message):
        await message.answer(
            f"""
С возвращением, {message.from_user.full_name}

Ваш баланс: <b>{data.get("amount")}₽</b>
Замороженный баланс: <b>{data.get('freezed_amount')}₽</b>

Реквизиты для оплаты:

"""
            + "\n".join(
                [
                    f"<b>{payment_detail.get('name')}</b> : <code>{payment_detail.get('text')}</code>"
                    for payment_detail in payment_details
                ]
            ),
            reply_markup=await inline.worker_menu_keyboard(),
        )
    elif isinstance(message, types.CallbackQuery):
        message: types.CallbackQuery
        await message.message.edit_text(
            f"""
С возвращением, {message.from_user.full_name}

Ваш баланс: <b>{data.get("amount")}₽</b>
Замороженный баланс: <b>{data.get('freezed_amount')}₽</b>
    """,
            reply_markup=await inline.worker_menu_keyboard(),
        )


@dp.callback_query_handler(lambda c: c.data == "proceed_receipt")
async def proceed_receipt(callback: types.CallbackQuery, state: FSMContext):
    await ReceiptState.receipt.set()

    message = await callback.message.edit_text(
        "Отправьте чек и укажите сумму",
        reply_markup=await inline.worker_receipt_keyboard(),
    )
    await state.set_data({"last_message_id": message.message_id})


@dp.callback_query_handler(lambda c: c.data == "proceed_payout")
async def proceed_payout(callback: types.CallbackQuery, state: FSMContext, **kwargs):
    await PayoutState.amount.set()

    response = requests.get(url=SERVER_URL + f"/workers/{callback.from_user.id}")
    if response.status_code != 200:
        return
    data = response.json()

    message = await callback.message.edit_text(
        f"Доступный баланс: <b>{data.get('amount')}</b>\nЗамороженный баланс: <b>{data.get('freezed_amount')}</b>\nДля вывода доступно: <b>{data.get('amount') - data.get('freezed_amount')}</b>\n\nВведите сумму выплаты: ",
        reply_markup=await inline.worker_payout_keyboard(),
    )
    await state.set_data({"last_message_id": message.message_id})


@dp.message_handler(state=PayoutState.amount)
async def payout_amount(
    message: t.Union[types.Message, types.CallbackQuery], state: FSMContext, **kwargs
):
    cdata = await state.get_data()
    if isinstance(message, types.Message):
        response = requests.get(url=SERVER_URL + f"/workers/{message.from_user.id}")
        if response.status_code != 200:
            return
        data = response.json()
        amount = int(data.get("amount"))
        await message.delete()
        try:
            input_amount = Decimal(message.text)
        except Exception as e:
            return await bot.edit_message_text(
                chat_id=message.from_user.id,
                text=f"Доступный баланс: <b>{data.get('amount')}</b>\nЗамороженный баланс: <b>{data.get('freezed_amount')}</b>\nДля вывода доступно: <b>{data.get('amount') - data.get('freezed_amount')}</b>\n\nНеверный формат ввода. Попробуйте ещё раз или нажмите 'назад'",
                message_id=cdata.get("last_message_id"),
                reply_markup=await inline.worker_payout_keyboard(),
            )

        if int(input_amount) > amount:
            return await bot.edit_message_text(
                chat_id=message.from_user.id,
                text=f"Доступный баланс: <b>{data.get('amount')}</b>\nЗамороженный баланс: <b>{data.get('freezed_amount')}</b>\nДля вывода доступно: <b>{data.get('amount') - data.get('freezed_amount')}</b>\n\nСумма вывода больше баланса. Попробуйте ещё раз или нажмите 'назад'",
                message_id=cdata.get("last_message_id"),
                reply_markup=await inline.worker_payout_keyboard(),
            )
        async with state.proxy() as data:
            data["amount"] = input_amount
            new_message = await bot.edit_message_text(
                chat_id=message.from_user.id,
                text="Выберите способ оплаты: ",
                reply_markup=await inline.chooose_payment_detail_keyboard(
                    user_id=message.from_user.id, amount=input_amount
                ),
                message_id=data["last_message_id"],
            )

            data["last_message_id"] = new_message.message_id
    elif isinstance(message, types.CallbackQuery):
        async with state.proxy() as data:
            new_message = await bot.edit_message_text(
                chat_id=message.from_user.id,
                text="Выберите способ оплаты: ",
                reply_markup=await inline.chooose_payment_detail_keyboard(
                    user_id=message.from_user.id, amount=data["amount"]
                ),
                message_id=data["last_message_id"],
            )

            data["last_message_id"] = new_message.message_id


@dp.callback_query_handler(
    lambda c: c.data.startswith("payment_detail"), state=PayoutState.amount
)
async def payment_detail(callback: types.CallbackQuery, state: FSMContext, **kwargs):
    if kwargs.get("message"):
        cdata = await state.get_data()
        await UserPaymentDetail.name.set()
        new_message = await callback.message.edit_text(
            "Укажите наименование добавляемых реквизитов:\n\n<b>Пример: </b>Тинькофф",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=f"payment_detail#back#{cdata.get('amount')}#-#-",
                )
            ),
        )
        return await state.set_data(
            {
                "name": cdata.get("name"),
                "amount": cdata.get("amount"),
                "last_message_id": new_message.message_id,
            }
        )
    splitted_data = callback.data.split("#")
    do = splitted_data[1]
    amount = splitted_data[2]
    where = splitted_data[3]
    pid = splitted_data[4]
    if do == "add":
        await UserPaymentDetail.name.set()
        new_message = await callback.message.edit_text(
            "Укажите наименование добавляемых реквизитов:\n\n<b>Пример: </b>Тинькофф",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    text="Назад", callback_data=f"payment_detail#back#{amount}#-#-"
                )
            ),
        )
        await state.set_data(
            {"amount": amount, "last_message_id": new_message.message_id}
        )

    elif do == "back":
        wheres = {
            "-": proceed_payout,
            "name": payment_detail,
            "text": payment_detail_text,
        }
        await wheres[where](message=callback, callback=callback, state=state)

    elif do == "choose":
        await payment_detail_choose(
            callback=callback, state=state, amount=amount, pid=pid
        )


@dp.callback_query_handler(
    lambda c: c.data.startswith("payment_detail"), state=UserPaymentDetail.all_states
)
async def user_payment_detail(
    callback: types.CallbackQuery, state: FSMContext, **kwargs
):
    splitted_data = callback.data.split("#")
    do = splitted_data[1]
    amount = splitted_data[2]
    where = splitted_data[3]
    pid = splitted_data[4]
    wheres = {
        "-": proceed_payout,
        "name": payment_detail,
        "text": payment_detail_name,
        "confirm": payment_detail_confirm,
    }
    if do == "back":
        await wheres[where](
            message=callback, callback=callback, state=state, amount=amount
        )
    elif do == "confirm":
        await payment_detail_confirm(callback=callback, state=state)
    elif do == "choose":
        await payment_detail_choose(
            callback=callback, state=state, amount=amount, pid=pid
        )


async def payment_detail_confirm(callback: types.CallbackQuery, state: FSMContext):
    cdata = await state.get_data()
    name = cdata["name"]
    text = cdata["recv"]
    requests.post(
        SERVER_URL + "/users/payment/details/",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={"name": name, "text": text, "user": callback.from_user.id},
    )

    await payout_amount(message=callback, state=state)


async def payment_detail_choose(
    callback: types.CallbackQuery, state: FSMContext, amount: str, pid: str
):
    cdata = await state.get_data()
    new_lead_response = requests.post(
        SERVER_URL
        + f"/worker/requests/?worker={callback.from_user.id}&amount={cdata.get('amount')}&type=withdrawal"
    )
    if new_lead_response.status_code != 200:
        return await bot.edit_message_text(
            chat_id=callback.from_user.id,
            text=f"<b>Возникла ошибка сервера при создании заявки, попробуйте ещё раз...</b>\n\nДля выхода жмите 'назад'",
            reply_markup=await inline.worker_payout_keyboard(all_sum=False),
            message_id=cdata.get("last_message_id"),
        )
    new_lead_data = new_lead_response.json()
    await state.finish()
    if new_lead_response.status_code != 200:
        return await bot.edit_message_text(
            chat_id=callback.from_user.id,
            text=f"<b>Возникла ошибка сервера при создании заявки, попробуйте ещё раз...</b>\n\nДля выхода жмите 'назад'",
            reply_markup=await inline.worker_payout_keyboard(all_sum=False),
            message_id=cdata.get("last_message_id"),
        )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        text=f"<b>Заявка на вывод успешно отправлена!</b>\n\nДля выхода жмите 'назад'",
        reply_markup=await inline.worker_payout_keyboard(all_sum=False),
        message_id=cdata.get("last_message_id"),
    )

    payment_detail = requests.get(
        SERVER_URL + f"/users/payment/details/?id={pid}"
    ).json()
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"<b>Новая заявка на вывод</b>\n\nРаботник: @{new_lead_data.get('worker').get('username')}\nРеквизиты:\n<b>{payment_detail.get('name')}</b> : {payment_detail.get('text')}\nСумма: {new_lead_data.get('amount')}₽",
        reply_markup=await inline.confirm_withdrawal_request_keyboard(
            new_lead_data.get("id")
        ),
    )


@dp.message_handler(state=UserPaymentDetail.name)
async def payment_detail_name(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        last_message_id = data["last_message_id"]
        if not kwargs.get("callback"):
            data["name"] = message.text
            await message.delete()

            new_message = await bot.edit_message_text(
                chat_id=message.from_user.id,
                text=f"<b>Наименование:</b> {message.text}\n\nУкажите сами реквизиты:\n\n<b>Пример: </b>+79999999999 или 0000000000000000",
                message_id=last_message_id,
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"payment_detail#back#{data['amount']}#name#-",
                    )
                ),
            )
            data["last_message_id"] = new_message.message_id
        else:
            new_message = await bot.edit_message_text(
                chat_id=message.from_user.id,
                text=f"<b>Наименование:</b> {data['name']}\n\nУкажите сами реквизиты:\n\n<b>Пример: </b>+79999999999 или 0000000000000000",
                message_id=last_message_id,
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"payment_detail#back#{data['amount']}#name#-",
                    )
                ),
            )
            data["last_message_id"] = new_message.message_id
        await UserPaymentDetail.text.set()


@dp.message_handler(state=UserPaymentDetail.text)
async def payment_detail_text(message: types.Message, state: FSMContext, **kwargs):
    async with state.proxy() as data:
        data["recv"] = message.text
        await message.delete()
        name = data["name"]
        last_message_id = data["last_message_id"]

        new_message = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"<b>Наименование:</b> {name}\n<b>Реквизиты: {message.text}</b>\n\nВы уверены что хотите добавить реквизиты?",
            message_id=last_message_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    text="Да",
                    callback_data=f"payment_detail#confirm#{data['amount']}#text#-",
                ),
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=f"payment_detail#back#{data['amount']}#text#-",
                ),
            ),
        )
        data["last_message_id"] = new_message.message_id
        await UserPaymentDetail.text.set()


@dp.callback_query_handler(lambda c: c.data == "payout_all", state=PayoutState.amount)
async def payout_amount_all(callback: types.CallbackQuery, state: FSMContext):
    response = requests.get(url=SERVER_URL + f"/workers/{callback.from_user.id}")
    if response.status_code != 200:
        return
    data = response.json()
    amount = int(data.get("amount"))
    freezed_amount = int(data.get("freezed_amount"))
    if not amount > 0:
        await callback.message.edit_text(
            f"Доступный баланс: <b>{data.get('amount')}</b>\nЗамороженный баланс: <b>{data.get('freezed_amount')}</b>\nДля вывода доступно: <b>{data.get('amount') - data.get('freezed_amount')}</b>\n\nНедостаточно средств для вывода",
            reply_markup=await inline.worker_payout_keyboard(),
        )
    elif not amount - freezed_amount > 0:
        await callback.message.edit_text(
            f"Доступный баланс: <b>{data.get('amount')}</b>\nЗамороженный баланс: <b>{data.get('freezed_amount')}</b>\nДля вывода доступно: <b>{data.get('amount') - data.get('freezed_amount')}</b>\n\nНедостаточно средств для вывода",
            reply_markup=await inline.worker_payout_keyboard(),
        )
    else:
        async with state.proxy() as data:
            data["amount"] = amount - freezed_amount
            new_message = await bot.edit_message_text(
                chat_id=callback.from_user.id,
                text="Выберите способ оплаты: ",
                reply_markup=await inline.chooose_payment_detail_keyboard(
                    user_id=callback.from_user.id, amount=amount - freezed_amount
                ),
                message_id=data["last_message_id"],
            )

            data["last_message_id"] = new_message.message_id


@dp.callback_query_handler(lambda c: c.data == "payout_back")
async def receipt_back(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await start(callback)


@dp.callback_query_handler(
    lambda c: c.data == "payout_back", state=PayoutState.all_states
)
async def receipt_back(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await start(callback)


@dp.callback_query_handler(lambda c: c.data == "receipt_back")
async def receipt_back(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await start(callback)


@dp.callback_query_handler(
    lambda c: c.data == "receipt_back", state=ReceiptState.all_states
)
async def receipt_back(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await start(callback)


# @dp.message_handler(regexp=r"\d{2}.\d{2}.\d{4}")
# async def dob_message(message: types.Message):
#     date = re.match(r"\d{2}.\d{2}.\d{4}", message.text)
#     date = date.group()
#     headers = {
#         "accept": "application/json",
#     }

#     response = requests.get(
#         f"https://matrix.belofflab.com/matrix/{date}", headers=headers
#     )
#     data = response.json()

#     image_data = base64.b64decode(data.get("image"))

#     image_path = BASE_DIR / f"media/{uuid.uuid4()}.png"
#     with open(image_path, "wb") as f:
#         f.write(image_data)

#     caption = ""
#     matrix_data = data.get("matrix")
#     print(matrix_data)
#     for key, value in matrix_data.items():
#         try:
#             if value != "пусто":
#                 if len(value) > 2:
#                     value = value[:1] * 3
#             caption += (
#                 f"<b>{key.capitalize()}</b> : {random.choice(matrix[key][value])}\n\n"
#             )
#         except KeyError:
#             continue

#     await message.answer_photo(
#         photo=types.InputFile(image_path), caption=caption[:1024]
#     )


@dp.message_handler(
    content_types=[types.ContentType.DOCUMENT, types.ContentType.PHOTO],
    state=ReceiptState.receipt,
)
async def control_amount(message: types.Message, state: FSMContext) -> None:
    try:
        amount = Decimal(message.caption)
    except Exception as e:
        return
    document = message.document
    photo = message.photo
    last_message_id = await state.get_data("last_message_id")
    photo_to_delete = None
    if isinstance(document, types.Document):
        file_extension = os.path.splitext(document.file_name)[1]
        unique_filename = str(uuid.uuid4()) + file_extension
        file_info = await bot.get_file(document.file_id)
        file_path = file_info.file_path
        output_file = BASE_DIR / f"media/{unique_filename}"
        await bot.download_file(file_path, output_file)
        photo_to_delete = output_file
    elif isinstance(photo, list):
        file_info = await bot.get_file(photo[-1].file_id)
        file_extension = file_info.file_path.split(".")[-1]
        unique_filename = str(uuid.uuid4()) + "." + file_extension
        output_file = BASE_DIR / f"media/{unique_filename}"
        await photo[-1].download(destination_file=output_file)
        photo_to_delete = output_file
    params = {"worker": message.from_user.id, "amount": str(amount), "type": "deposit"}
    new_lead_status = False
    new_lead_data = {}
    with open(output_file, "rb") as file:
        new_lead_response = requests.post(
            SERVER_URL + f"/worker/requests/", params=params, files={"receipt": file}
        )
        if new_lead_response.status_code == 200:
            new_lead_status = True
            new_lead_data = new_lead_response.json()
        else:
            return await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"<b>Возникла ошибка сервера при создании заявки, попробуйте ещё раз...</b>\n\nДля выхода жмите 'назад'",
            reply_markup=await inline.worker_receipt_keyboard(),
            message_id=last_message_id.get("last_message_id"),
        )

    await bot.send_message(875044476, str(new_lead_data))
    
    await message.delete()
    SUCCESS_MESSAGE = (
        "Вы успешно отправили чек! \n\nДля того чтобы выйти жмите <b>'Назад'</b>"
    )
    await state.finish()
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        text=SUCCESS_MESSAGE,
        reply_markup=await inline.worker_receipt_keyboard(),
        message_id=last_message_id.get("last_message_id"),
    )

    print(new_lead_data['worker']['username'])
    await bot.send_photo(
        chat_id=CHANNEL_ID,
        caption=f"<b>Новая заявка на пополнение</b>\n\nРаботник: @123\nСумма: {new_lead_data.get('amount')}₽",
        photo=types.InputFile(output_file),
        reply_markup=await inline.confirm_deposit_request_keyboard(
            new_lead_data.get("id")
        ),
    )

    os.remove(photo_to_delete)


async def list_workers_requests(callback: types.CallbackQuery, page: str, **kwargs):
    await callback.message.edit_text(
        "Чеки (От самых новых):\n\n📈- Пополнение\n📉- Вывод",
        reply_markup=await inline.workers_requests_keyboard(
            current_page=page, worker=callback.from_user.id
        ),
    )


async def show_workers_request(
    callback: types.CallbackQuery, request: str, page: str, **kwargs
):
    response = requests.get(SERVER_URL + f"/worker/requests/{request}")
    data = response.json()
    await callback.message.edit_text(
        text=f"""
Работник: @{data['worker']['username']}

Чек на сумму: {data.get("amount")}₽

Статус: <b>{'✅ Одобрена' if data.get("is_success") else '❌ Отклонена или в процессе'}</b>

Тип: <b>{"Депозит" if data.get("type") == "deposit" else "Вывод"}</b>

""",
        reply_markup=await inline.show_worker_request_keyboard(
            page=page, request=request
        ),
    )


@dp.callback_query_handler(inline.uworkers_requests_cd.filter())
async def workers_requests_navigate(
    callback: types.CallbackQuery, callback_data: dict
) -> None:
    level = callback_data.get("level")
    request = callback_data.get("request")
    page = callback_data.get("page")

    levels = {
        "0": start,
        "1": list_workers_requests,
        "2": show_workers_request,
    }

    current_level_function = levels[level]

    await current_level_function(callback, request=request, page=page)
