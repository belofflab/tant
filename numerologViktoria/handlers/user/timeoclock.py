from aiogram import types
from keyboards.user import inline
from loader import dp
from .menu import start
from typing import Union
from .training import list_courses
from data.config import ASKEZA, VIKTORIA

WORKER_NAME = "Виктории"
WORKER_USERNAME = "viktoria_numer"

timeoclock_buttons = {
    "1": {
        "text": "Одинаковые",
        "options": [
            {
                "text": "00:00",
                "description": """
Вам нужна перегрузка. 

Обнулиться и отдохнуть. Символ свободы.
Пришло время убрать что-то или кого-то.

В том числе убрать обиду.
Убрать то, что гнетет, тормозит. 

Ноль – отправная точка.
Внутри – пустота, за его пределами – весь мир.

Не забудьте немного остановиться, перевести дух и оценить результат своего труда ранее. 

После избавления наблюдаете за новыми знаками, они подскажут, что в самое ближайшее время придет в вашу жизнь.
""",
            },
            {
                "text": "01:01",
                "description": """
Врата возможностей которые открываются. 
Совет Вселенной:

«Решайтесь»
«Делайте этот шаг»
«Идите, езжайте, действуйте».

Нужно увидеть возможность она вот-вот будет. 

Важно быть в активном движении, налаживать связи и взяться за реализацию давно запланированных проектов. 

Вам необходимо выйти из зоны комфорта, много обращаться с окружающими, чтобы завести побольше  необходимых контактов во всех сферах вашей жизни.

На пороге что-то новое. В самое ближайшее время вы начнете что-то или вам сделают выгодное предложение. Соглашайтесь.
""",
            },
            {
                "text": "02:02",
                "description": """
Какие-то изменения в личной жизни или новое сотрудничество/партнерство. Возможно вас пригласят на какое-то мероприятие. 

Будете о чем-то договариваться. 

Если какие-то конфликты во взаимоотношениях именно вы должны должны пойти на компромисс и договориться. Не прячьтесь, идите на диалог. 

Если ситуация слишком сложная и вы понимаете, что с вашей стороны идет давление нужно стать мягче. Отпустите контроль. 

Кто-то может поведать вам тайну. Но, получите вы эту информацию только в случае если будете в позиции наблюдателя и немного уйдете в тень. Если только вдруг вы начнете давить и диктовать правила вы не узнаете нужную вам информацию.
""",
            },
            {
                "text": "03:03",
                "description": """
На пороге серьезные изменения и масштаб. Возможно, что сейчас вы уже испытываете некую тревогу и нетерпение. 

В любви возможно неожиданное и необычное признание. 
Если вы уже в отношениях вы получите новые яркие впечатления. 

В самореализации вас ждет масштаб. Одна из ваших целей в скором времени осуществится и ещё круче чем вы думаете. 

Ничего не бойтесь - высшие силы на вашей стороне. То, что вы ещё раньше могли считать несбыточной мечтой вот-вот произойдет. Но, приложите усилия и главное доверьтесь. 

Хотите ещё больше помощи от высших сил? Тогда помогите советом или поддержкой тому, кто к вам обратиться. 

Это прекрасное время для воплощения задумок и проектов. Особенно делиться своими знаниями, вести блог, писать книги/посты. 

Если у вас уже есть бизнес не плохо было бы развернуть новую рекламную компанию, найти или внедрить новый способ продвижения. 

Не ведитесь на сладкие предложения, может быть обман, но самое прекрасное, что в момент опасности вам интуиция подскажет, что нужно отказаться. 

Нет цели в жизни? Скоро вы её найдете. Сейчас вы сильнее своих страхов. Вы приобретаете силу и вы это чествуете.
""",
            },
            {
                "text": "04:04",
                "description": """
Вы сейчас находитесь в рамках. Вроде вот он выход, но никак не получается выйти. Вы немного устали.

Придется приложить усилия, поработать, но потом вы поймёте, что все было не зря. 

Долго ищете работу? Скоро найдете. В ближайшее время вы достучитесь в свою дверь. Но! Награда ждет только тех кто действительно что-то делает. 

Хотите скорее притянуть то к чему идете? Прямо сейчас начните радоваться жизни, наслаждайтесь каждой секундой. И все ваши дела обязательно придут в порядок. 

Скорее всего, появится много советчиков, которые не будут верить в ваш успех, и начнут поддавать сомнению каждый ваш шаг. Гните свою линию до конца. Они также ограничивают вас. Не слушайте никого. 

Обратите внимание на состояние вашего здоровья. Пройдите необходимые обследования. Возможно, есть проблемы с физическим состояние организма.
""",
            },
            {
                "text": "05:05",
                "description": """
Грядут перемены. Все будет очень неожиданно. Новые переживания. 

Прекрасное время для приключений. 

Это ещё и денежный знак. Деньги могут поступить из неожиданного источника. 

Благоприятное время для обучения, прохождения курсов повышения квалификации и овладения новыми навыками. Все приобретения однажды сработают исключительно на вашу пользу. 

Также, хорошо передавать свои знания, обучать. 
Продавать обучение. Набирать команду. 

На пороге положительные изменения в судьбе.

Вы можете быть нетерпеливы. Вы ощущаете, что вот-вот скоро что-то произойдет, так и есть. 

Дела скапливаются снежным комом, а эмоциональное напряжение нарастает. Хватит брать на себя новые обязательства, пока не закрыты старые. 

Слишком большая расфокусировка приведет к выгоранию. 
Человеческая психика предпочитает состояние стабильности. На адаптацию к новому уходит много мыслительных процессов. Однако только за счет перемен можно продвинуться в развитии.

Это ещё символ приключений и свободы. Жизненные уроки возможно получить только через опыт. Лучше отпустить прошлое и подготовиться к небольшим переменам. Изменения позволят освободиться от старых ограничений.

Принимайте перемены. Вам не уйти от них. Энергия этого времени не позволяет стоять на одном месте, а заставляет все время стремиться к покорению новых рубежей.
""",
            },
            {
                "text": "06:06",
                "description": """
Какое-то время будет стабильность, спокойствие и даже романтика. 

Возможно, покупка чего-то дорогого, роскошного для дома или для себя. 

Для свободных - это число любви, предрекающее скорую встречу со своей судьбой либо предложение руки и сердца.

Внимание! Для тех у кого в отношениях разногласия. Это число предлагает пересмотреть свою систему ценностей: возможно, партнер отошел для вас на второй план, а многие вещи стали восприниматься как должное. Обратите внимание на отношения. 

Для тех кто в минусе. Это ещё число соблазнов. Возможно вы подверженны каким вредным привычкам и пришло время пересмотреть свое питание или злоупотребление напитками.

Для тех кто в плюсе. Вас потянет улучшить себя, заняться телом. Улучшить то, что вокруг вас. Например вы решите сделать ремонт. Идите в это. Деньги будут. 

Вас призывают остановиться в погоне за материальными благами и задуматься о духовном. Возможно, вы слишком увлеклись продажей своего времени и перестали замечать настоящую жизнь. Отдышитесь и просто порадуйтесь жизни. Такие моменты бывают не часто.
""",
            },
            {
                "text": "07:07",
                "description": """
Пришло время духовности. Вас неожиданно может потянуть в эзотерику или вы начнете выполнять практики, обучаться чему-то мистическому. Если так происходит - не сопротивляйтесь. 

Это особое число, связанное с самопознанием и духовным ростом. Его появление является признаком того, что вы находитесь на правильном пути и вам следует продолжать исследовать свой потенциал.

Вселенная будет поддерживать вас в достижении ваших духовных целей.

Сейчас ваши мысли реализуются намного быстрее, а интуиция особо обострена. Обязательно поддерживайте позитивный настрой, вы привлечете больше положительной энергии в свою жизнь.

В любовных отношениях. Может означать, что сейчас время прислушиваться к своему внутреннему голосу и интуиции, особенно когда дело касается вашего романтического партнера или возможных романтических отношений.

Это может указывать на то, что вам нужно больше доверять своему сердцу и интуиции, а не только своему разуму. Если вы чувствуете какую-то неискренность - вскоре это подтвердится каким-то фактом. 

И наоборот, если вы чувствуете особую связь с человеком - также убедитесь, что вы на верном пути. 

В контексте карьеры и финансов, это может быть знаком того, что вам нужно руководствоваться своим внутренним голосом при принятии важных решений.
""",
            },
            {
                "text": "08:08",
                "description": """
Это один из денежных знаков. Радуйтесь. Вам даны все ресурсы для достижения желаемого, осталось только делать. 

Впереди вас ждут важные возможности для роста и достижения ваших целей, особенно в финансовой сфере.

В отношениях: этот час символизирует единство между двумя людьми, а также дружбу и прочную любовь. Считается, что час - хорошее время, чтобы это время выразить свои чувства другому человеку и показать свою любовь.

Это также признак того, что на горизонте появятся новые отношения. Вы можете встретить нового человека, который принесет волнение и радость в вашу жизнь. Этот человек может быть романтическим партнером, новым другом или даже деловым партнером. В любом случае, держите свое сердце и разум открытыми для новых связей и возможностей.

Удача благоволит вам в любых начинаниях. Впереди у вас еще больше радости и счастья. Вы находитесь под опекой высших сил. Не забывайте о быстротечности жизни и не упускайте свой шанс. Двигайтесь вперед, продолжайте трудиться и самосовершенствуйтесь.
""",
            },
            {
                "text": "09:09",
                "description": """
Это период когда вы слишком импульсивны. 

Это завершение одного цикла и начало нового. Иногда это указывает на возможную потерю. Однако помним: все нужное всегда будет с нами. Воспринимаем потери и завершения как освобождение. 

В отношениях: возможно в данный момент вы слишком  опекаете близких, заботитесь о них, но это может доходить до жесткого контроля. 

Иногда вам кажется, что вы лучше знаете, как поступить вашему близкому человеку, и предпочли бы решить все самостоятельно. Этим вы незаметно для себя обижаете любимых людей, ограничивая их свободу выбора.

Для тех у кого отношения уже шли к завершению, оно вот-вот наступит. Можете узнать какую-то тайну или новость которая поставит точку. 

Если вы без отношений закончится ваше одиночество в ближайшее время вас ждет интересное знакомство. 

В работе и проектах: что-то тревожит вас, и, вероятно, это связано с людьми. Возможно, это не лучшие отношения с коллегами или конфликт с начальством. Ситуация сказывается на вашем желании работать. На вас много ответственности.

Не идите на поводу у эмоций и сохраняйте лицо.

Вы найдете вдохновение если смените обстановку, сходите в новое место.

В денежных вопросах ожидайте изменений. Какие это изменения зависит от вас, от вашего настроя и как вы мыслите с целом. Если вы сами по себе негативный человек это же и притянете, поэтому учитесь работать со своим мышлением, чтобы оно вам не вредило. 
А если вы умеете видеть во всем плюсы, тогда вы на пороге доп.источника доходов или просто случайных денег.

Контролируйте свои доходы и расходы. Воздержитесь от необдуманных поступков хотя бы на время. Иначе вас будут ожидать разочарование и финансовые потери.

Вероятно, вы заложник одних и тех же ситуаций, возвращающих вас в одно и то же место, где вы совсем не желаете находиться. Вы находитесь в ожидании подходящего момента, откладывая все действия на завтра.

Перестаньте витать в облаках и бросать слова на ветер. Выработайте план действий и приступайте к его претворению в жизнь.

Пусть это будет завершением ваших отговорок и вы начнете действовать. 

Вдохновляясь прошлым, вы двигаетесь назад. Используйте свои навыки для открытия новых горизонтов.

Как только поставите цель, возможность сразу появится. 

Перемены близко.
""",
            },
            {
                "text": "10:10",
                "description": """
Время открыть себя с точки зрения создателя своей судьбы. Пора взять ответственность за всё, что происходит в жизни, будь то хорошее или плохое.

В скором времени труды будут вознаграждены как материально, так и морально. Откроются новые пути развития и самореализации, посетит вдохновение после застоя.

Пора сделать выбор в пользу чего-то одного и не распаляться сразу на несколько дел. Не следует действовать на горячую голову, это может обернуться неудачей. В принятии решений лучше взвешивать все «за» и «против»

Вас ждет начало нового, но сначала вы пройдете некое обнуление. Может вы устали, выгорели и нужно сначала набраться сил, а потом действовать. Вам будет открыт путь.

Новое немного вас ограничит. Вместе с возможностями придет ограничение, но это нормально. Например ещё один источник дохода, но придется больше времени уделять работе и вы будете ограничены в свободном времени на себя или семью.

Если новая дружба, меньше времени сможете уделять старым друзьям.

Эти ограничения не плохо. Ведь в вашу жизнь придет что-то новое, интересное и нужное.
""",
            },
            {
                "text": "11:11",
                "description": """
Мистический знак.

Настал благоприятный момент для полного принятия своих внутренних знаний и претворения в жизнь значимых планов.

Знак отвечает за отвечающего за удачу и безмятежность.

Интуиция вам помогает найти ответы на нужные вопросы. Но, эти ответы вы находите когда находитесь наедине с собой. Через сны, знаки, символы, практики. Самое время попробовать медитации или что-то подобное, но главное, чтобы вам было интересно, а не просто потому, что надо.

Считается, что этот знак связан с духовным пробуждением и новым мощным началом.

11:11 означает, что ваши мысли быстро проявляются, поэтому выберите свои мысли осознанно  (загадывайте желание), когда вы видите 11:11.

В конце концов, желание увидеть 11:11 - это личный ритуал, который может принести в вашу жизнь чувство покоя и комфорта. Это также может быть средством регулярно возвращаться к своему желанию и наблюдать, как оно проявляется с течением времени.

Это ещё означает встречу с кем-то очень особенным.

Пришло время финансово выгодной сделки или путешествия, которое окажется полезным для семейного бюджета в будущем.
""",
            },
            {
                "text": "12:12",
                "description": """
Вы мыслите в правильном направлении и делаете правильные, последовательные шаги к своей цели.

Во что верите, то и получите. Вскоре, то, над чем вы работаете благоприятно скажется на вашей жизни. В ближайшее время ждите изменений в вашей жизни. 

Вам необходимо посетить духовное энергетическое место (например, церковь, храм или какое-то мероприятие онлайн или офлайн где выполняют какие-то практики для духовного развития), чтобы Вселенная позаботилась о ваших потребностях.

Подсказка: либо вы уже обладаете какими-то нужными знаниями и их необходимо уже использовать/ либо они вам нужны и вы их точно используете. 

Самый лучший знак если вы планируете идти обучаться или обучать других. 
Смело создавайте курсы/марафоны и т.д
Это знак масштаба и успеха.
""",
            },
            {
                "text": "13:13",
                "description": """
Сейчас вы очень подверженны негативному мышлению и притягиваете все плохое сами. 

Не спешите доверяться новым людям. Ваш новый знакомый может оказаться неблагонадежным. Будьте осмотрительны, не связывайтесь с теми, кто нарушает закон.

Скоро вам повезет. Вы заработаете больше денег. Конечно, не лежа на диване. Надо будет много работать, и тогда все будет классно. Работа немного может ограничить.

Ведите себя скромнее, не выставляйте напоказ свои успехи, не рассказывайте о планах ведь вы являетесь объектом зависти. Не провоцируйте людей на сплетни.

Если вы искали работу. Скоро вы её найдете, ту которая вам понравится. Если вы долго работаете на одном месте – вас повысят. Закончите все дела, не оставляйте ничего на потом, и ждите. Нужные люди заметят вас, и вы получите заслуженную награду.
""",
            },
            {
                "text": "14:14",
                "description": """
Знак говорит тебе, что тебе нужно что-то изменить в своей жизни. Почему бы не отправиться в путешествие? Там ты сможешь разобраться в своих мыслях и найти решения своих проблем.

Вы не можете быть спокойны за свои финансы. Не расходуйте больше, чем получаете. Следите за своим бюджетом. Откладывайте деньги на будущее. Не берите в долг. У вас должна быть финансовая подстраховка на «черный день».

На работе и в бизнесе вы - лидер, но дома не пытайтесь командовать своим любимым. Это может испортить вашу любовную историю в один миг.

Это также предупреждение о переутомлении организма. Если вы часто видите это значение, помните, что долгая работа без выходных и отпуска – прямая дорога к врачу. Желательно сменить обстановку. 

Вероятны финансовые поступления и возникновение новых отношений для тех кто одинок.
""",
            },
            {
                "text": "15:15",
                "description": """
Жизнь готовит тебе сюрпризы. Не унывай, а радуйся. Попроси помощи, если нужно. Слушай голос разума, он тебе подскажет, как решить все трудности. Не действуй по наитию. Избегай ссор и недобрых людей.

Осторожно с соблазнами. Не злоупотребляй. 

Знак говорит тебе, что твои друзья или родственники нуждаются в твоей помощи. Не забывай о своих близких. Они ждут от тебя поддержки и заботы.

Это знак того, что ты получишь денежный сюрприз. Ты можешь найти деньги на улице или получить премию. Но не будь легкомысленным. Не принимай импульсивных решений в делах и бизнесе.

Тебя могут соблазнять заманчивыми предложениями, вполне вероятно, что человек слишком сладко говорит, очень хорошо обдумай прежде чем принимать решение особенно, что качается каких-либо вложений.
""",
            },
            {
                "text": "16:16",
                "description": """
Освобождайтесь от ограничений. Не думайте о том, на что не можете повлиять. Ваши мысли влияют на количество получаемых денег. Если думаете, что деньги текут рекой, так оно и будет. Если думаете, что деньги достаются тяжело, значит так должно быть. Готовьтесь к переменам, ситуация решиться в вашу пользу. 

Этоо знак того, что нужно научиться отпускать людей. Кто-то из вашего окружения хочет разорвать отношения с вами.

Если друг или любимый человек пытаются порвать с вами, не пытайтесь удержать их. Научитесь отпускать прошлое, и смело стартовать к светлому будущему.

Это время может раскрыть в вас скрытые таланты. Не бойтесь творить. Даже если вы давно не молоды, но вас «осенило» научиться играть на гитаре – примите этот вызов. Скорее, новое хобби принесет вам кучу удовольствия, и откроет новые грани. 
Вы можете достичь невероятного успеха даже в тех областях, которые ранее были для вас «темным лесом».

Есть вероятность услышать важный совет, который кардинально изменит вашу жизнь. Произнесен он будет с уст ребенка. Вам необходимо рационально использовать свои возможности, чтобы сбалансировать свой внутренний мир и силы.

Если вы путешествуете, будьте осторожны. Лишние меры безопасности еще никому не помешали.
""",
            },
            {
                "text": "17:17",
                "description": """
Пора действовать! Удача на вашей стороне. Сейчас время самых смелых задумок и роста доходов. Все ваши планы в ближайшее время осуществляться. От вашей силы духа и готовности действовать зависит воплощение желаний в жизнь.

Символ финансовой выгоды. Новые знакомства могут принести пользу в материальном плане.

Это хороший знак для старта новых отношений. Если вы их ищете конечно.
Вам сулят удачу во всех начинаниях. 
Поэтому, не бойтесь открываться чему-то новому, стремитесь к новым знакомствам. Идите на свидания. 
Есть большие шансы встретить нового человека. 

Если женщина часто видит цифры 17:17, она способна быстро влюбить в себя мужчину. Достаточно всего лишь по-настоящему этого захотеть.

Значение 17:17 на часах может говорить о том, что вы озадачены материальным миром. Необходимо обратить свой взор к высшим силам, возблагодарить судьбу за все свои успехи. Также это может означать, что вы – исключительный человек, который постоянно транслирует это окружающим. Вы можете быть чрезмерно конфликтными, поэтому данное число послано вам как намек, для решения ссор с близкими.

это дополнительная возможность подготовиться к любым поворотам судьбы. Пользуйтесь подсказками свыше и не забывайте благодарить. 

Для вашего бизнеса и финансов это также хороший знак. Удача во всех сферах жизни человека. Любое дело, которое вы начнете, обязательно принесет успех. Вас ждёт материальная выгода, будьте активны и используйте новые знакомства во благо
""",
            },
            {
                "text": "18:18",
                "description": """
Освобождайтесь от ограничений. Не думайте о том, на что не можете повлиять. Ваши мысли влияют на количество получаемых денег. Если думаете, что деньги текут рекой, так оно и будет. Если думаете, что деньги достаются тяжело, значит так должно быть. Готовьтесь к переменам, ситуация решиться в вашу пользу. 

Этоо знак того, что нужно научиться отпускать людей. Кто-то из вашего окружения хочет разорвать отношения с вами.

Если друг или любимый человек пытаются порвать с вами, не пытайтесь удержать их. Научитесь отпускать прошлое, и смело стартовать к светлому будущему.

Это время может раскрыть в вас скрытые таланты. Не бойтесь творить. Даже если вы давно не молоды, но вас «осенило» научиться играть на гитаре – примите этот вызов. Скорее, новое хобби принесет вам кучу удовольствия, и откроет новые грани. 
Вы можете достичь невероятного успеха даже в тех областях, которые ранее были для вас «темным лесом».

Есть вероятность услышать важный совет, который кардинально изменит вашу жизнь. Произнесен он будет с уст ребенка. Вам необходимо рационально использовать свои возможности, чтобы сбалансировать свой внутренний мир и силы.

Если вы путешествуете, будьте осторожны. Лишние меры безопасности еще никому не помешали.
""",
            },
            {
                "text": "19:19",
                "description": """
Сейчас чувства преобладают над разумом. Станьте немного рациональнее.

Вас предупреждают о приятных переменах. Возможно, сначала они окажутся болезненными, но это малая жертва, необходимая для счастья:

- Закончатся старые, исчерпавшие себя отношения и появится человек, который заставит испытать любовь, жизнь заиграет новыми красками;
- Придет разочарование во второй половине, но именно это позволит посмотреть другими глазами на давнего друга. Это послужит началом романтического периода.
- Вы взглянете по-новому на любимого человека, изжившие, казалось, себя отношения, оживут и окрепнут, закалившись в испытаниях бытом и проблемами. Два любящих человека поймут, что не хотят терять друг друга. Начнут уделять внимание отношениям и проводить вместе время.

В финансовом плане исключительно благоприятное значение. Высшие силы помогают, когда человек готов сдаться, отказаться от задуманного. Если он испытывает трудности с финансами, это знак грядущих перемен, связанных с улучшением положения. Требуется ни столько напряженная работа, сколько позитивный настрой и капелька удачи. И в скором времени она обязательно появится.
""",
            },
            {
                "text": "20:20",
                "description": """
Это знак того, что ты имеешь дружескую поддержку. Ты можешь обратиться к своим друзьям. Они тебе подскажут, что делать.

Возможно, будут возникать конфликты со второй половинкой. Скорее всего, это будут мелкие ссоры, которые легко уладить.

Сейчас наступает такой период, когда вам придется быть советчиком. Если кто-то из знакомых обратился за помощью, советом, не отказывайте. 

Хорошее послание для ваших финансов. Существует необходимость сделать вклад или инвестицию. Деньги, которые вы пустите в оборот, принесут значительные дивиденды.

Ваши финансы – это маленькое растение, которое всегда нужно поливать и удобрять. Удобрение – это постоянный труд, стремление быть успешным.

Время бумеранга. Пришло время пожинать плоды своих деяний и слов. 
Если вы были добры, честны перед собой и людьми – получите благосклонное отношение небес. Соответственно, за весь негатив, сплетни, пожелания зла принесенные в жизни других людей, придется также отвечать. Поэтому, всегда помните простую истину: добро возвращается в стократном размере. Пусть это движет вашими поступками.
""",
            },
            {
                "text": "21:21",
                "description": """
Время принятия решений. Научитесь радоваться тому, что имеете. Уберите прочь все пессимистические мысли. Не гневите наставников. Оптимизм поможет в делах. В ближайшее время вы увидите результат своего упорного труда, ожидайте награду за свою работу. 

Скоро в ваших кругах появится новый интересный человек. 

Может быть бурный роман или глубокое переживание.

Настало благоприятное время для получения финансовой выгоды. Вы не упустите своего, и утрете нос конкурентам по бизнесу.

Пришла пора перемен, поэтому меняйте все, что раньше не устраивало вас в собственном деле.

Это знак пришел в вашу жизнь не просто так. Это знак, что скоро начнут происходить положительные изменения во всех сферах вашей жизни. Главное пользоваться всеми шансами, которые дают вам. А они будут, не упустите момент.
""",
            },
            {
                "text": "22:22",
                "description": """
Скоро в вашей жизни произойдёт очень мощное событие, которое сильно изменит вашу судьбу. 

Это может быть как позитивное событие, которое вы так сильно ждёте, так и негативное. 

Зависит от ваших мыслей и действий. Ваши желания услышаны и будут очень скоро исполнены. 

Нужно набраться терпения, продолжать делать и не останавливаться, главное верить, что всё исполнится. 

Не падайте духом. Вы приложили максимум усилий, для реализации задуманного, и процесс запущен. 

Слушайте свою интуицию. Вас ожидает баланс, гармония и благоприятный период в жизни. Наполнитесь энергией. 

Вас ждут новые знакомства.

Время 22:22 также предостерегает от необдуманных поступков. Нужно тщательно планировать каждый шаг, иначе прошлые успехи потеряют значимость. 

Лучше немного потерпеть, поразмыслить, а не бросаться в омут с головой.

- сохранять позитивный настрой;
- продолжать двигаться к намеченной цели.
Только уверенность, упорство приведут к желаемому результату. А они уже показались на горизонте.

Цифры 22:22 предвещают благоприятное событие или подталкивают к переменам. Это словно поддержка свыше, намекающая не отказываться от идей и планов, забыть о суете и обдуманно идти вперед. 

Придется потрудиться, но вы останетесь довольны результатом.
""",
            },
            {
                "text": "23:23",
                "description": """
Пришло время обдумать свои действия, извлечь опыт, исправить или принять ошибки. И только после двигаться дальше.

Стоит внимательно следить за тем, с кем общаетесь и кому доверяете. Время тщательного анализа. Не доверяйте тайны незнакомцам. Время указывает на предстоящее событие, связанное с вашим окружением, которое может нарушить привычный уклад вашей жизни. Будьте осторожны в общении с людьми. Ваши просьбы и молитвы скоро будут услышаны. Осталось совсем немного. 

Наберитесь терпения, возьмите волю в кулак, сделайте рывок для достижения цели.

Знак трактуется как приносящий прибыль, процветание, постоянное развитие и благоприятное партнерство. Это ещё универсальный успех в любой сфере. Для бизнесмена 23:23 на часах значение дает только одно – стоит заключать сделку, она станет выгодной.

Совершенные действия могут оказать значительный эффект на всю дальнейшую жизнь, необходимо остановиться и обдумать свои поступки – нумерология рекомендует вспомнить, не обидел ли кого-то человек, не допустил ли несправедливости. 

Лучше попросить прощения сразу, не допуская глобальных последствий.
""",
            },
        ],
    },
}

TIMEOCLOCK_DESCRIPTION = "Время на часах"


async def list_buttons(
    callback: Union[types.CallbackQuery, types.Message], worker: str, **kwargs
):
    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.InputFile(VIKTORIA), caption=TIMEOCLOCK_DESCRIPTION
            ),
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                *[
                    types.InlineKeyboardButton(
                        text=value["text"],
                        callback_data=inline.make_timeockock_cd(
                            level=2, worker=worker, cid=key
                        ),
                    )
                    for key, value in timeoclock_buttons.items()
                ],
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=inline.make_timeockock_cd(level=0, worker=worker),
                ),
            ),
        )
    elif isinstance(callback, types.Message):
           await callback.answer_photo(
            photo=types.InputFile(VIKTORIA),
            caption=TIMEOCLOCK_DESCRIPTION,
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                *[
                    types.InlineKeyboardButton(
                        text=value["text"],
                        callback_data=inline.make_timeockock_cd(
                            level=2, worker=worker, cid=key
                        ),
                    )
                    for key, value in timeoclock_buttons.items()
                ],
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=inline.make_timeockock_cd(level=0, worker=worker),
                ),
            ),
        )

async def list_options(
    callback: Union[types.CallbackQuery, types.Message], worker: str, cid: str, **kwargs
):
    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.InputFile(VIKTORIA), caption=TIMEOCLOCK_DESCRIPTION
            ),
            reply_markup=types.InlineKeyboardMarkup(row_width=3).add(
                *[
                    types.InlineKeyboardButton(
                        text=option["text"],
                        callback_data=inline.make_timeockock_cd(
                            level=3, worker=worker, cid=cid, oid=option["text"].replace(":", "|")
                        ),
                    )
                    for option in timeoclock_buttons[cid]["options"]
                ],
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=inline.make_timeockock_cd(level=1, worker=worker, cid=cid),
                ),
            ),
        )

def split_text_into_pages(text, chars_per_page):
    return [text[i:i + chars_per_page] for i in range(0, len(text), chars_per_page)]

async def show_button(
    callback: types.CallbackQuery, worker: str, cid: str, oid: str, opage: str
):
    from math import ceil
    CURRENT_LEVEL = 3
    current_page = int(opage)
    p_oid = oid.replace("|", ":")
    s_oid = [el for el in timeoclock_buttons[cid]["options"] if el["text"] == p_oid][0]
    text_to_display = s_oid["description"]
    pages = split_text_into_pages(text_to_display, 900)
    MAX_PAGES = len(pages)
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(
        types.InlineKeyboardButton(
            text="Назад",
            callback_data=inline.make_timeockock_cd(level=2, worker=worker, cid=cid, oid=oid),
        )
    )
    if len(text_to_display) > 900:
        markup.row(
            types.InlineKeyboardButton(
                text="<<",
                callback_data=inline.make_timeockock_cd(
                    level=CURRENT_LEVEL,
                    opage=(current_page - 1) if current_page != 1 else current_page,
                    worker=worker,
                    cid=cid,
                    oid=oid
                ),
            ),
            types.InlineKeyboardButton(text=f"{current_page}/{MAX_PAGES}", callback_data="..."),
            types.InlineKeyboardButton(
                text=">>",
                callback_data=inline.make_timeockock_cd(
                    level=CURRENT_LEVEL,
                    opage=(
                        (current_page + 1)
                        if not current_page >= MAX_PAGES
                        else current_page
                    ),
                    worker=worker,
                    cid=cid,
                    oid=oid
                ),
            ),
        )

    # Calculate the start and end index for the current page
    chars_per_page = 900  # Replace with the actual number of characters per page
    start_index = (current_page - 1) * chars_per_page
    end_index = min(current_page * chars_per_page, len(text_to_display))

    # Display the current portion of the description
    await callback.message.edit_caption(
        text_to_display[start_index:end_index],
        reply_markup=markup,
    )

@dp.callback_query_handler(inline.timeockock_cd.filter())
async def timeoclock_navigate(
    callback: types.CallbackQuery, callback_data: dict
) -> None:
    level = callback_data.get("level")
    worker = callback_data.get("worker")
    cid = callback_data.get("cid")
    oid = callback_data.get("oid")
    opage = callback_data.get("opage")

    levels = {"0": start, "1": list_buttons, "2": list_options, "3": show_button}

    current_level_function = levels[level]

    await current_level_function(
        callback, worker=worker, cid=cid, oid=oid, opage=opage
    )
