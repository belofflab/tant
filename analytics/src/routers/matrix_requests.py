import typing as t
import base64
import uuid
import requests
import random
from fastapi import APIRouter, HTTPException, status
from src.data.config import BASE_DIR
from src import schemas
from src.database.models import (
    WorkerRequest,
    Worker,
    User,
    MatrixUserRequest,
)

router = APIRouter(prefix="/api/v1/matrix/requests", tags=["Заявки на матрицу"])


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
        "пусто": [
            "Ты, конечно, красавчик или красавица - умеешь жить как хочешь, из своей личной выгоды.",
            "Слушай, а ты часто раздаешь советы и рекомендации? А, может, впадаешь в жертву и думаешь, что все виноваты?",
            "Отслеживай, как реагируешь на коллектив, правила коллектива, начальника и его просьбы. Порой тебе сложно сдержать себя от высказываний и непрошенных советов, но именно это поможет тебе эффективно коммуницировать с людьми и быть полезным в команде.",
        ],
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


@router.post("/")
async def create(matrix_request: schemas.MatrixRequestCreate) -> schemas.MatrixRequest:
    user = await User.objects.get_or_none(id=matrix_request.user)
    response = requests.get(
        f"https://matrix.belofflab.com/matrix/{matrix_request.dob}",
        headers={
            "accept": "application/json",
        },
    )

    data = response.json()

    image_data = base64.b64decode(data.get("image"))
    image_path = f"media/matrix/{uuid.uuid4()}.png"

    with open(BASE_DIR / image_path, "wb") as f:
        f.write(image_data)

    result = ""
    matrix_data = data.get("matrix")

    for key, value in matrix_data.items():
        try:
            if value != "пусто":
                if len(value) > 2:
                    value = value[:1] * 3
            result += (
                f"{key.capitalize()} : {random.choice(matrix[key][value])}\n\n"
            )
        except KeyError:
            continue
        except TypeError as ex:
            print(ex, key, value, matrix[key])

    new_matrix_request = await MatrixUserRequest.objects.create(
        user=user,
        dob=matrix_request.dob,
        image=image_path,
        result=result,
    )

    return new_matrix_request


@router.get("/{request}")
async def get_request(request: int):
    s_matrix_request = await MatrixUserRequest.objects.prefetch_related(
        "worker_request"
    ).get_or_none(id=request)
    if not s_matrix_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена"
        )

    return s_matrix_request


@router.get("/")
async def get_all() -> t.List[schemas.WorkerRequest]:
    return (
        await MatrixUserRequest.objects.prefetch_related("worker_request")
        .order_by("-worker_request__date")
        .all()
    )


@router.get("/worker/{worker}/")
async def get_by_worker(worker: int) -> t.List[schemas.WorkerRequest]:
    s_worker = await Worker.objects.get_or_none(id=worker)
    if s_worker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден"
        )

    return (
        await MatrixUserRequest.objects.prefetch_related("worker_request")
        .filter(worker_request__worker=s_worker)
        .order_by("-worker_request__date")
        .all()
    )


@router.get("/user/{user}/")
async def get_by_user(user: int) -> t.List[schemas.WorkerRequest]:
    s_user = await User.objects.get_or_none(id=user)
    if s_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден"
        )

    return (
        await MatrixUserRequest.objects.prefetch_related("worker_request")
        .filter(user=s_user, worker_request__isnull=False)
        .order_by("-worker_request__date")
        .all()
    )


@router.patch("/{request}/")
async def matrix_request_update(request: int, worker_request: int):
    matrix_request = await MatrixUserRequest.objects.get_or_none(id=request)
    s_worker_request = await WorkerRequest.objects.get_or_none(id=worker_request)

    return await matrix_request.update(worker_request=s_worker_request)
