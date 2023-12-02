--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Debian 16.0-1.pgdg120+1)
-- Dumped by pg_dump version 16.0 (Debian 16.0-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: numerologuser
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO numerologuser;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: numerologuser
--

CREATE TABLE public.payments (
    idx bigint NOT NULL,
    input_info character varying(2048),
    "user" bigint,
    service bigint,
    date timestamp without time zone
);


ALTER TABLE public.payments OWNER TO numerologuser;

--
-- Name: payments_idx_seq; Type: SEQUENCE; Schema: public; Owner: numerologuser
--

CREATE SEQUENCE public.payments_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_idx_seq OWNER TO numerologuser;

--
-- Name: payments_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: numerologuser
--

ALTER SEQUENCE public.payments_idx_seq OWNED BY public.payments.idx;


--
-- Name: sender_templates; Type: TABLE; Schema: public; Owner: numerologuser
--

CREATE TABLE public.sender_templates (
    idx bigint NOT NULL,
    photo character varying(2048),
    text character varying(2048),
    buttons character varying(2048),
    date timestamp without time zone
);


ALTER TABLE public.sender_templates OWNER TO numerologuser;

--
-- Name: sender_templates_idx_seq; Type: SEQUENCE; Schema: public; Owner: numerologuser
--

CREATE SEQUENCE public.sender_templates_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sender_templates_idx_seq OWNER TO numerologuser;

--
-- Name: sender_templates_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: numerologuser
--

ALTER SEQUENCE public.sender_templates_idx_seq OWNED BY public.sender_templates.idx;


--
-- Name: service_types; Type: TABLE; Schema: public; Owner: numerologuser
--

CREATE TABLE public.service_types (
    idx bigint NOT NULL,
    name character varying(255)
);


ALTER TABLE public.service_types OWNER TO numerologuser;

--
-- Name: service_types_idx_seq; Type: SEQUENCE; Schema: public; Owner: numerologuser
--

CREATE SEQUENCE public.service_types_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.service_types_idx_seq OWNER TO numerologuser;

--
-- Name: service_types_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: numerologuser
--

ALTER SEQUENCE public.service_types_idx_seq OWNED BY public.service_types.idx;


--
-- Name: services; Type: TABLE; Schema: public; Owner: numerologuser
--

CREATE TABLE public.services (
    idx bigint NOT NULL,
    type bigint,
    name character varying(255),
    description character varying(1024),
    amount numeric(12,2)
);


ALTER TABLE public.services OWNER TO numerologuser;

--
-- Name: services_idx_seq; Type: SEQUENCE; Schema: public; Owner: numerologuser
--

CREATE SEQUENCE public.services_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.services_idx_seq OWNER TO numerologuser;

--
-- Name: services_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: numerologuser
--

ALTER SEQUENCE public.services_idx_seq OWNED BY public.services.idx;


--
-- Name: user_templates; Type: TABLE; Schema: public; Owner: numerologuser
--

CREATE TABLE public.user_templates (
    idx bigint NOT NULL,
    name character varying(255),
    date timestamp without time zone
);


ALTER TABLE public.user_templates OWNER TO numerologuser;

--
-- Name: user_templates_idx_seq; Type: SEQUENCE; Schema: public; Owner: numerologuser
--

CREATE SEQUENCE public.user_templates_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_templates_idx_seq OWNER TO numerologuser;

--
-- Name: user_templates_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: numerologuser
--

ALTER SEQUENCE public.user_templates_idx_seq OWNED BY public.user_templates.idx;


--
-- Name: user_user_template_association; Type: TABLE; Schema: public; Owner: numerologuser
--

CREATE TABLE public.user_user_template_association (
    idx bigint NOT NULL,
    user_template_id bigint,
    user_id bigint
);


ALTER TABLE public.user_user_template_association OWNER TO numerologuser;

--
-- Name: user_user_template_association_idx_seq; Type: SEQUENCE; Schema: public; Owner: numerologuser
--

CREATE SEQUENCE public.user_user_template_association_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_user_template_association_idx_seq OWNER TO numerologuser;

--
-- Name: user_user_template_association_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: numerologuser
--

ALTER SEQUENCE public.user_user_template_association_idx_seq OWNED BY public.user_user_template_association.idx;


--
-- Name: users; Type: TABLE; Schema: public; Owner: numerologuser
--

CREATE TABLE public.users (
    idx bigint NOT NULL,
    username character varying(255),
    first_name character varying(255),
    last_name character varying(255),
    is_active boolean
);


ALTER TABLE public.users OWNER TO numerologuser;

--
-- Name: users_idx_seq; Type: SEQUENCE; Schema: public; Owner: numerologuser
--

CREATE SEQUENCE public.users_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_idx_seq OWNER TO numerologuser;

--
-- Name: users_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: numerologuser
--

ALTER SEQUENCE public.users_idx_seq OWNED BY public.users.idx;


--
-- Name: payments idx; Type: DEFAULT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.payments ALTER COLUMN idx SET DEFAULT nextval('public.payments_idx_seq'::regclass);


--
-- Name: sender_templates idx; Type: DEFAULT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.sender_templates ALTER COLUMN idx SET DEFAULT nextval('public.sender_templates_idx_seq'::regclass);


--
-- Name: service_types idx; Type: DEFAULT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.service_types ALTER COLUMN idx SET DEFAULT nextval('public.service_types_idx_seq'::regclass);


--
-- Name: services idx; Type: DEFAULT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.services ALTER COLUMN idx SET DEFAULT nextval('public.services_idx_seq'::regclass);


--
-- Name: user_templates idx; Type: DEFAULT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.user_templates ALTER COLUMN idx SET DEFAULT nextval('public.user_templates_idx_seq'::regclass);


--
-- Name: user_user_template_association idx; Type: DEFAULT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.user_user_template_association ALTER COLUMN idx SET DEFAULT nextval('public.user_user_template_association_idx_seq'::regclass);


--
-- Name: users idx; Type: DEFAULT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.users ALTER COLUMN idx SET DEFAULT nextval('public.users_idx_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: numerologuser
--

COPY public.alembic_version (version_num) FROM stdin;
25f53ca1c08d
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: numerologuser
--

COPY public.payments (idx, input_info, "user", service, date) FROM stdin;
\.


--
-- Data for Name: sender_templates; Type: TABLE DATA; Schema: public; Owner: numerologuser
--

COPY public.sender_templates (idx, photo, text, buttons, date) FROM stdin;
\.


--
-- Data for Name: service_types; Type: TABLE DATA; Schema: public; Owner: numerologuser
--

COPY public.service_types (idx, name) FROM stdin;
1	TEST
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: numerologuser
--

COPY public.services (idx, type, name, description, amount) FROM stdin;
9	1	1️⃣ Детский разбор	\n👶Каждый ребёнок приходит в эту жизнь со своим набором качеств, талантов, уроков из прошлой жизни, заложенных в нем при рождении.\n‌Задача родителей — научиться понимать своего ребёнка, и помочь ему раскрыться самым благоприятным способом для ребёнка.\n‌\n✅<b>На консультации вы узнаете:</b>\n— таланты и природные склонности вашего ребенка;\n— подбор/рекомендации профессий для ребёнка\n— какие качества нужно развивать и усиливать, и какие качества, наоборот, мешают;\n— как общаться, чтобы понимать своего ребенка;\n— какие установки/триггеры могут развиться у Вашего ребёнка- и как этого избежать\n— как лучше взаимодействовать именно с вашим ребенком, ваша совместимость;\n— какие особенности ребенка следует учитывать;\n— кружки, секции, направления, благоприятные сферы для реализации;\n\n<b>Формат:</b> аудио сообщение в WhatsApp 30-50 минут.\n🙎‍♀️@{worker}\n         \n	2100.00
10	1	2️⃣ Полный разбор	\n✅<b>Вы узнаете какие энергии на Вас влияют</b>\n— какую задачу Вы принесли с собой из прошлого воплощения\n— разберем миссию и уровни предназначения\n— узнаете в чем Ваша сила и какие есть слабости\n— определим слабые стороны здоровья и возможные заболевания\n— получите информацию и поймете на каком уровне вы сейчас находитесь и как поднять свои вибрации, чтобы улучшить все сферы жизни, подружиться с Вашими планетами и раскачать свой денежный потенциал на максимум.\n— после консультации и выполнения рекомендаций Ваши энергии станут вашими союзниками судьба будет вам благоволить и вы начнете притягивать удачу. \n\nФормат: аудио сообщение в Whats App 30-50 минут.\n🙎‍♀️@{worker}\n	4000.00
11	1	3️⃣ Прогноз на 1-2 месяца	\n✅<b>Благодаря прогнозу Вы можете:</b>\n— скорректировать планы, поездки, действия;\n— проанализировать финансы и ваши расходы;\n— получите подсказку стоит ли совершать ту или иную сделку;\n— ознакомится с подводными камнями в отношениях и обойти острые углы;\n— заранее предпринять действия, которые сохранят ваши ресурсы, время, деньги, жизненные силы;\n\n\nВ прогнозе будет не только расчёт перспектив, но и совет для вас, и предостережение, которые являются ключами для открытия самой выгодной для Вас двери и самого верного выбора. \n\nЗнакомясь с прогнозом, Вы заранее знаете о тенденциях месяца, и получаете подсказки и пути решения.\n\nФормат: аудио сообщение в Whats App 15-40 минут. \n💰<b>Стоимость прогноза на месяц 500₽/на 2 месяца - 850₽</b>\n🙎‍♀️@{worker}\n	0.00
12	1	4️⃣ Прогноз на год	\n🍀То, что вы называете удачей - это по сути правильные действия в правильное время. Данный прогноз является инструкцией и вашим персональным объёмом работы на этот год. \nДля всего есть своё благоприятное время🕐 покупка машины, запуск бизнеса, инвестиции, недвижимость. Если вы выбрали неблагоприятное время, все будет против вас. \n \n\n📝В прогнозе будет не только расчёт перспектив, но и совет для вас, и предостережение, которые являются ключами для открытия самой выгодной для Вас двери и самого верного выбора. \n\nЗнакомясь с прогнозом, Вы заранее знаете о тенденциях года получаете подсказки и получаете максимум от влияния управителя вашего личного года.\n\n🙎‍♀️@{worker}\n	0.00
13	1	5️⃣ Став денежный амулет	\n<b>Став «Денежный Амулет»</b> - это нумерологические вибрации и сакральные символы в рамках сакральной геометрии.\n\n<b>Помогает: </b>\n✅ Очистить ваши денежные каналы\n✅ Активирует вашу денежную воронку\n✅Вы заметите изменения после первой активации \n✅ Став влияет на ваши денежные каналы экологичным способом \n\n🧚‍♀️ «Денежный Амулет» - это новый Став🔥 \nОн состоит из ваших персональных цифровых вибраций и которые активируют вашу денежную энергию.\n\nВ течение 3-х суток отправляю вам ваши цифровые вибрации насчитанные по вашей дате и инструкцию для Активации.\nСтав рассчитывается один раз и навсегда. \nПереодически его нужно усиливать, я об этом напоминаю на канале. \n\n🙎‍♀️@{worker}\n	1070.00
14	1	6️⃣ Финансовый код	\n<b>Данный 5-значный код рассчитан моей собственной методикой.</b>\n\n-  код рассчитан для привлечения финансов на 2023 год.\n\nВажно слушать и слышать свой внутренний голос и <b>БЫТЬ ОТКРЫТЫМ К НОВЫМ ИДЕЯМ И ПРЕДЛОЖЕНИЯМ.</b>\nВозможно ли рассчитать самостоятельно финансовый код изобилия❓\n<b>НЕТ!</b>\n\n<b>Финансовый код</b> - это денежная энергия, которая работает по принципу: мы получаем тогда, когда что то отдаём взамен.Произведя оплату финансового кода изобилия он начинает работать на Вас.\n<b>Не покупайте данный код на последние деньги. Отдавайте с благодарностью.</b>\nТакже вы получаете даты в которые можно активировать код. Все даты рассчитываю индивидуально. \n\n👩‍💻Для расчета вашего личного финансового кода на 2023 год нужна ваша полная дата рождения (день, месяц, год и ФИО)\nВ течение 3-х дней я отправляю ваш личный рассчитанный код и инструкцию. \n🙎‍♀️@{worker}\n	500.00
15	1	7️⃣ Став «Помощь»	\nЧем помогает Став для привлечения высших сил в важных жизненных ситуациях? \n\nВ моменты когда вы не чувствуете поддержки, когда у вас важная ситуация, важные жизненные обстоятельства Став дает экстренную помощь. \n\nЧто такое Став? Это графическое изображение. В него заворачиваться определенным потоком набор энергий через цифровые коды, сакральные символы, геометрические фигуры которые вы должны нарисовать следуя инструкции.\nДля каждого Став рассчитывается индивидуально. \n❌ Вы не можете активировать Став за других людей. \n❌ Запрещено 🚫 Активировать Став, чтобы к вам вернулся человек, или с целью наладить отношения с теми, кто от вас ушел. \n\nУ многих из вас уже есть став на привлечение высших сил в сложной жизненной ситуации, этот став модернизирован и теперь вы можете использовать не только в сложной ситуации, но и в любой важной для вас ситуации. \n\nДля тех у кого став уже есть стоимость новой формулы - 300₽\nДля тех кто ранее не приобретал\n- 1800₽\n🙎‍♀️@{worker}\n\n	0.00
16	1	8️⃣ Личный финансовый код	\n<b>Данный 5-значный код рассчитан моей собственной методикой.</b>\n\n-  код рассчитан для привлечения финансов на 2023 год.\n\nВажно слушать и слышать свой внутренний голос и <b>БЫТЬ ОТКРЫТЫМ К НОВЫМ ИДЕЯМ И ПРЕДЛОЖЕНИЯМ.</b>\nВозможно ли рассчитать самостоятельно финансовый код изобилия❓\n<b>НЕТ!</b>\n\n<b>Финансовый код</b> - это денежная энергия, которая работает по принципу: мы получаем тогда, когда что то отдаём взамен.Произведя оплату финансового кода изобилия он начинает работать на Вас.\n<b>Не покупайте данный код на последние деньги. Отдавайте с благодарностью.</b>\nТакже вы получаете даты в которые можно активировать код. Все даты рассчитываю индивидуально. \n\n👩‍💻Для расчета вашего личного финансового кода на 2023 год нужна ваша полная дата рождения (день, месяц, год и ФИО)\nВ течение 3-х дней я отправляю ваш личный рассчитанный код и инструкцию. \n🙎‍♀️@{worker}\n	0.00
\.


--
-- Data for Name: user_templates; Type: TABLE DATA; Schema: public; Owner: numerologuser
--

COPY public.user_templates (idx, name, date) FROM stdin;
\.


--
-- Data for Name: user_user_template_association; Type: TABLE DATA; Schema: public; Owner: numerologuser
--

COPY public.user_user_template_association (idx, user_template_id, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: numerologuser
--

COPY public.users (idx, username, first_name, last_name, is_active) FROM stdin;
875044476	belofflab	\N	\N	t
6639144962	meguava	\N	\N	t
\.


--
-- Name: payments_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: numerologuser
--

SELECT pg_catalog.setval('public.payments_idx_seq', 1, false);


--
-- Name: sender_templates_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: numerologuser
--

SELECT pg_catalog.setval('public.sender_templates_idx_seq', 1, false);


--
-- Name: service_types_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: numerologuser
--

SELECT pg_catalog.setval('public.service_types_idx_seq', 1, false);


--
-- Name: services_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: numerologuser
--

SELECT pg_catalog.setval('public.services_idx_seq', 16, true);


--
-- Name: user_templates_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: numerologuser
--

SELECT pg_catalog.setval('public.user_templates_idx_seq', 1, false);


--
-- Name: user_user_template_association_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: numerologuser
--

SELECT pg_catalog.setval('public.user_user_template_association_idx_seq', 1, false);


--
-- Name: users_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: numerologuser
--

SELECT pg_catalog.setval('public.users_idx_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (idx);


--
-- Name: sender_templates sender_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.sender_templates
    ADD CONSTRAINT sender_templates_pkey PRIMARY KEY (idx);


--
-- Name: service_types service_types_pkey; Type: CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.service_types
    ADD CONSTRAINT service_types_pkey PRIMARY KEY (idx);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (idx);


--
-- Name: user_templates user_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.user_templates
    ADD CONSTRAINT user_templates_pkey PRIMARY KEY (idx);


--
-- Name: user_user_template_association user_user_template_association_pkey; Type: CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.user_user_template_association
    ADD CONSTRAINT user_user_template_association_pkey PRIMARY KEY (idx);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (idx);


--
-- Name: payments payments_service_fkey; Type: FK CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_service_fkey FOREIGN KEY (service) REFERENCES public.services(idx);


--
-- Name: payments payments_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_fkey FOREIGN KEY ("user") REFERENCES public.users(idx);


--
-- Name: services services_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_type_fkey FOREIGN KEY (type) REFERENCES public.service_types(idx);


--
-- Name: user_user_template_association user_user_template_association_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.user_user_template_association
    ADD CONSTRAINT user_user_template_association_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(idx);


--
-- Name: user_user_template_association user_user_template_association_user_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: numerologuser
--

ALTER TABLE ONLY public.user_user_template_association
    ADD CONSTRAINT user_user_template_association_user_template_id_fkey FOREIGN KEY (user_template_id) REFERENCES public.user_templates(idx);


--
-- PostgreSQL database dump complete
--

