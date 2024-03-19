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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: tarologueuser
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO tarologueuser;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: tarologueuser
--

CREATE TABLE public.payments (
    idx bigint NOT NULL,
    input_info character varying(2048),
    "user" bigint,
    service bigint,
    date timestamp without time zone
);


ALTER TABLE public.payments OWNER TO tarologueuser;

--
-- Name: payments_idx_seq; Type: SEQUENCE; Schema: public; Owner: tarologueuser
--

CREATE SEQUENCE public.payments_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_idx_seq OWNER TO tarologueuser;

--
-- Name: payments_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tarologueuser
--

ALTER SEQUENCE public.payments_idx_seq OWNED BY public.payments.idx;


--
-- Name: sender_templates; Type: TABLE; Schema: public; Owner: tarologueuser
--

CREATE TABLE public.sender_templates (
    idx bigint NOT NULL,
    photo character varying(2048),
    text character varying(2048),
    buttons character varying(2048),
    date timestamp without time zone
);


ALTER TABLE public.sender_templates OWNER TO tarologueuser;

--
-- Name: sender_templates_idx_seq; Type: SEQUENCE; Schema: public; Owner: tarologueuser
--

CREATE SEQUENCE public.sender_templates_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sender_templates_idx_seq OWNER TO tarologueuser;

--
-- Name: sender_templates_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tarologueuser
--

ALTER SEQUENCE public.sender_templates_idx_seq OWNED BY public.sender_templates.idx;


--
-- Name: service_types; Type: TABLE; Schema: public; Owner: tarologueuser
--

CREATE TABLE public.service_types (
    idx bigint NOT NULL,
    name character varying(255)
);


ALTER TABLE public.service_types OWNER TO tarologueuser;

--
-- Name: service_types_idx_seq; Type: SEQUENCE; Schema: public; Owner: tarologueuser
--

CREATE SEQUENCE public.service_types_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.service_types_idx_seq OWNER TO tarologueuser;

--
-- Name: service_types_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tarologueuser
--

ALTER SEQUENCE public.service_types_idx_seq OWNED BY public.service_types.idx;


--
-- Name: services; Type: TABLE; Schema: public; Owner: tarologueuser
--

CREATE TABLE public.services (
    idx bigint NOT NULL,
    type bigint,
    name character varying(255),
    description character varying(1024),
    amount numeric(12,2)
);


ALTER TABLE public.services OWNER TO tarologueuser;

--
-- Name: services_idx_seq; Type: SEQUENCE; Schema: public; Owner: tarologueuser
--

CREATE SEQUENCE public.services_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.services_idx_seq OWNER TO tarologueuser;

--
-- Name: services_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tarologueuser
--

ALTER SEQUENCE public.services_idx_seq OWNED BY public.services.idx;


--
-- Name: user_templates; Type: TABLE; Schema: public; Owner: tarologueuser
--

CREATE TABLE public.user_templates (
    idx bigint NOT NULL,
    name character varying(255),
    date timestamp without time zone
);


ALTER TABLE public.user_templates OWNER TO tarologueuser;

--
-- Name: user_templates_idx_seq; Type: SEQUENCE; Schema: public; Owner: tarologueuser
--

CREATE SEQUENCE public.user_templates_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_templates_idx_seq OWNER TO tarologueuser;

--
-- Name: user_templates_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tarologueuser
--

ALTER SEQUENCE public.user_templates_idx_seq OWNED BY public.user_templates.idx;


--
-- Name: user_user_template_association; Type: TABLE; Schema: public; Owner: tarologueuser
--

CREATE TABLE public.user_user_template_association (
    idx bigint NOT NULL,
    user_template_id bigint,
    user_id bigint
);


ALTER TABLE public.user_user_template_association OWNER TO tarologueuser;

--
-- Name: user_user_template_association_idx_seq; Type: SEQUENCE; Schema: public; Owner: tarologueuser
--

CREATE SEQUENCE public.user_user_template_association_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_user_template_association_idx_seq OWNER TO tarologueuser;

--
-- Name: user_user_template_association_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tarologueuser
--

ALTER SEQUENCE public.user_user_template_association_idx_seq OWNED BY public.user_user_template_association.idx;


--
-- Name: users; Type: TABLE; Schema: public; Owner: tarologueuser
--

CREATE TABLE public.users (
    idx bigint NOT NULL,
    username character varying(255),
    first_name character varying(255),
    last_name character varying(255),
    is_active boolean
);


ALTER TABLE public.users OWNER TO tarologueuser;

--
-- Name: users_idx_seq; Type: SEQUENCE; Schema: public; Owner: tarologueuser
--

CREATE SEQUENCE public.users_idx_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_idx_seq OWNER TO tarologueuser;

--
-- Name: users_idx_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tarologueuser
--

ALTER SEQUENCE public.users_idx_seq OWNED BY public.users.idx;


--
-- Name: payments idx; Type: DEFAULT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.payments ALTER COLUMN idx SET DEFAULT nextval('public.payments_idx_seq'::regclass);


--
-- Name: sender_templates idx; Type: DEFAULT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.sender_templates ALTER COLUMN idx SET DEFAULT nextval('public.sender_templates_idx_seq'::regclass);


--
-- Name: service_types idx; Type: DEFAULT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.service_types ALTER COLUMN idx SET DEFAULT nextval('public.service_types_idx_seq'::regclass);


--
-- Name: services idx; Type: DEFAULT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.services ALTER COLUMN idx SET DEFAULT nextval('public.services_idx_seq'::regclass);


--
-- Name: user_templates idx; Type: DEFAULT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.user_templates ALTER COLUMN idx SET DEFAULT nextval('public.user_templates_idx_seq'::regclass);


--
-- Name: user_user_template_association idx; Type: DEFAULT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.user_user_template_association ALTER COLUMN idx SET DEFAULT nextval('public.user_user_template_association_idx_seq'::regclass);


--
-- Name: users idx; Type: DEFAULT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.users ALTER COLUMN idx SET DEFAULT nextval('public.users_idx_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: tarologueuser
--

COPY public.alembic_version (version_num) FROM stdin;
25f53ca1c08d
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: tarologueuser
--

COPY public.payments (idx, input_info, "user", service, date) FROM stdin;
\.


--
-- Data for Name: sender_templates; Type: TABLE DATA; Schema: public; Owner: tarologueuser
--

COPY public.sender_templates (idx, photo, text, buttons, date) FROM stdin;
8	\N	Поо	\N	2023-10-14 07:40:51.881838
11	\N	/admin	\N	2023-10-14 07:57:19.670629
12	\N	А	\N	2023-10-16 16:32:21.715815
13	\N	О	\N	2023-10-16 16:32:30.014592
14	\N	A	\N	2023-10-18 19:43:59.301037
\.


--
-- Data for Name: service_types; Type: TABLE DATA; Schema: public; Owner: tarologueuser
--

COPY public.service_types (idx, name) FROM stdin;
1	Консультации
2	Ритуалы
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: tarologueuser
--

COPY public.services (idx, type, name, description, amount) FROM stdin;
40	1	Всё обо мне	\n<b>В этом разборе мы детально разберем данные темы👇🏻</b>\n         \n1. Какие аспекты моей личности я должен лучше понять?\n2. Какие таланты и способности я не использую в полной мере?\n3. Какие прошлые опыты оказывают влияние на мое текущее состояние?\n4. Какие страхи или сомнения могут сдерживать мой личностный рост?\n5. Какие аспекты моей жизни требуют большего внимания и развития?\n6. Какие жизненные ценности для меня наиболее важны?\n7. Как я могу лучше управлять своими эмоциями и стрессом?\n8. Какие отношения и взаимодействия в моей жизни могут быть улучшены?\n9. Какие новые возможности или направления развития могут открыться для меня?\n10. Какие шаги или действия я могу предпринять, чтобы достичь более гармоничной и удовлетворительной жизни?\n         \nНапишите «Разбор Все обо мне» 👇🏻\n🙎‍♀️@{worker}\n         \n	2000.00
41	1	Один вопрос 🙋🏻‍♀️	\n- Напишите «Хочу ответ на один вопрос» сформулируйте свой вопрос, напишите дату рождения и пришлите свое фото. Все это направьте 👇🏻\n \n🙎‍♀️@{worker}\n	500.00
42	1	Два вопроса 🙋🏻‍♀️	\n- Напишите «Хочу ответ на два вопроса» сформулируйте свой вопрос, напишите дату рождения и пришлите свое фото. Все это направьте 👇🏻\n\n🙎‍♀️@{worker}\n	750.00
43	1	Три вопроса 🙋🏻‍♀️	\n- Напишите «Хочу ответ на три вопроса» сформулируйте свои вопросы, напишите дату рождения и пришлите свое фото. Все это направьте 👇🏻\n\n🙎‍♀️@{worker}\n	1050.00
44	1	Детский разбор от 0 до 3	\n<b>Детский разбор от 0 до 3</b>\n\nЧто входит в разбор 👇🏻\n\n1. Каково общее состояние моего малыша на данный момент?\n2. Какие аспекты развития моего малыша требуют особого внимания?\n3. Как я могу поддержать здоровье и благополучие моего малыша?\n4. Какие игры или занятия могут помочь развить навыки и интересы моего малыша?\n5. Как я могу создать безопасное и любящее окружение для моего малыша?\n6. Какие аспекты воспитания могут быть особенно важными для моего ребенка на данный момент?\n7. Какие уроки жизни могут быть полезными для моего малыша на этой стадии его развития?\n8. Как я могу поддерживать эмоциональное благополучие моего малыша и помогать ему выражать свои чувства?\n\nНапишите мне @{worker} «Детский разбор от 0 до 3»\n	2000.00
45	1	Детский разбор от 3 лет	\n<b>«Детский разбор от 3»</b>\n\n1. Как я могу лучше понять своего ребенка?\n2. Какие аспекты воспитания нуждаются в моем внимании?\n3. Каковы сильные стороны моего ребенка, которые стоит развивать?\n4. Как я могу помочь своему ребенку развить самоуверенность?\n5. Каковы лучшие способы обучения и образования для моего ребенка?\n6. Какие преграды могут возникнуть в будущем, и как их можно преодолеть?\n7. Как я могу создать более гармоничные отношения с моим ребенком?\n8. Какие уроки жизни важно усвоить моему ребенку на данный момент?\n\nНапишите мне @{worker} «Детский разбор от 3»\n	2000.00
46	1	Глубокий анализ отношений 🔍	\n<b>В этом разборе мы детально разберем данные темы👇🏻</b>\n\n1. Какие энергии влияют на мои отношения в данный момент?\n2. Какие аспекты моей личности могут влиять на развитие отношений?\n3. Какие вызовы или преграды стоят на пути к гармоничным отношениям?\n4. Какова динамика отношений между мной и моим партнером/партнеркой?\n5. Какие аспекты нашей связи нуждаются в укреплении или изменении?\n6. Какие уроки или опыт я могу извлечь из моих текущих отношений?\n7. Какие действия мне следует предпринять, чтобы улучшить мои отношения?\n8. Какие пути к разрешению конфликтов или недопониманий можно применить?\n9. Какие изменения могут произойти в моих отношениях в ближайшем будущем?\n10. Какие возможности или перспективы открываются передо мной в контексте моих отношений?\n11. Перспективы развития отношений 6 месяцев.\n\nНапишите 👇🏻\n@{worker} «Разбор Глубокий анализ отношений»\n\n	2000.00
47	1	Сложная жизненная ситуация 🙈	\n<b>«Сложная жизненная ситуация»</b>\n\n1. Какова природа этой сложной ситуации?\n2. Какие факторы или обстоятельства привели к возникновению этой проблемы?\n3. Какие аспекты ситуации я должен учесть, чтобы справиться с ней наилучшим образом?\n4. Какие уроки или опыт я могу извлечь из этой ситуации?\n5. Какие ресурсы или поддержку мне следует использовать для решения проблемы?\n6. Какие действия я могу предпринять, чтобы изменить ход событий в свою пользу?\n7. Какие возможные исходы могут ожидать меня в будущем, если я останусь в этой ситуации?\n8. Какие аспекты собственной личности или поведения могут влиять на разрешение этой проблемы?\n9. Какие шаги или решения могут привести к более гармоничному развитию событий?\n10. Как я могу использовать этот опыт для своего долгосрочного роста и самосовершенствования?\n\nНапишите 👇🏻\n@{worker} «Разбор Сложная жизненная ситуация»\n\n	2000.00
48	1	Созвон 📱	\n<b>•30 минут—2000₽</b>\n<b>•60 минут— 3000₽</b>\n<b>•90 минут—4500₽</b>\n\nНапишите слово «Созвон» и количество минут.👇🏻\n\n🙎‍♀️@{worker}\n\n	0.00
49	2	Эмоциональная отвязка	\n<b>Эмоциональная отвязка</b>\n\nЭмоциональная отвязка с помощью свечи является частью магической практики, направленной на разрыв эмоциональной связи с определенным человеком или событием.\n\nЭтот процесс может быть выполнен один раз или несколько раз, в зависимости от вашей потребности. Важно помнить, что эмоциональная отвязка может потребовать времени и практики.\n\nНапиши мне в директ слово «Отвязка»\n👇👇👇\n \n🕯️@{worker}\n	2000.00
50	2	Открытие финансового потока	\n<b>Открытие финансового потока</b>\n\nМощная свечная магия, направленная на привлечение богатства и открытия финансового потока. \n\nНапишите мне в личные сообщения слово \n«Финансовый поток»\n👇👇👇\n\n🕯️@{worker}\n	1500.00
51	2	Снятие негатива	\n<b>Снятие негатива</b>\n\nДанный мощный метод практики сжигает весь негатив в вашем поле, освобождает новые пути, снимает стресс, тревогу и депрессию. Освобождает от негативных привязанностей. \n\nНапиши мне в личные сообщения слово \n«Чистка»\n👇👇👇\n\n🕯️@{worker}\n	2000.00
52	2	❤️Привлечение любви	\n<b>❤️Привлечение любви</b>\n\nМощный метод ритуала по привлечению любви в вашу жизнь и раскрытию сексуального потока \n\nНапишите мне в личные сообщения слово\n «Любовь»\n👇👇👇\n \n🕯️@{worker}\n	1500.00
\.


--
-- Data for Name: user_templates; Type: TABLE DATA; Schema: public; Owner: tarologueuser
--

COPY public.user_templates (idx, name, date) FROM stdin;
2	Шаболда	2023-10-14 07:55:23.264708
3	Личка саша1	2023-10-14 08:01:18.094772
\.


--
-- Data for Name: user_user_template_association; Type: TABLE DATA; Schema: public; Owner: tarologueuser
--

COPY public.user_user_template_association (idx, user_template_id, user_id) FROM stdin;
15	2	269993873
16	2	391072383
17	2	875044476
18	2	888196461
19	2	950192332
20	2	1017035235
21	2	1062114023
22	2	1123783955
23	2	1345227557
24	2	1407537356
25	2	1684739130
26	2	1805208500
27	2	6208832294
28	2	6639144962
29	3	269993873
30	3	391072383
31	3	875044476
32	3	888196461
33	3	950192332
34	3	1017035235
35	3	1062114023
36	3	1123783955
37	3	1345227557
38	3	1407537356
39	3	1684739130
40	3	1805208500
41	3	6208832294
42	3	6639144962
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: tarologueuser
--

COPY public.users (idx, username, first_name, last_name, is_active) FROM stdin;
875044476	belofflab	\N	\N	t
269993873	viktoria_numer	\N	\N	t
1684739130	taskmanagment	\N	\N	t
6208832294	Tutre666	\N	\N	t
1345227557	vivitko7	\N	\N	t
1062114023	noizolk	\N	\N	t
1407537356	Anna_osteoNV	\N	\N	t
6095443048	no username	\N	\N	t
2069950167	no username	\N	\N	t
1123783955	omarkova_om	\N	\N	t
950192332	Olga_karelina_u	\N	\N	t
391072383	dmitrybevz	\N	\N	t
5556813612	no username	\N	\N	t
895872844	sanfit	\N	\N	f
1063092820	ssyy222ggsj	\N	\N	f
6119365399	no username	\N	\N	f
1805208500	Swetlana190876	\N	\N	t
1017035235	noaklida	\N	\N	t
888196461	Maria2596	\N	\N	t
6639144962	meguava	\N	\N	f
515041464	ulyana_mazur	\N	\N	t
1333838895	no username	\N	\N	t
6382051968	kukijoy93	\N	\N	t
6270915055	g3nt1m3n	\N	\N	t
5220239319	Ymagechka78	\N	\N	t
5152114717	no username	\N	\N	t
6451915886	no username	\N	\N	t
774617141	no username	\N	\N	t
2064198395	no username	\N	\N	t
850737337	no username	\N	\N	t
1279375001	no username	\N	\N	t
624054681	VolchenkoE	\N	\N	t
1990574001	no username	\N	\N	t
1169294375	yluaz4	\N	\N	t
1991098419	alina_altaftinovna	\N	\N	t
6278394548	no username	\N	\N	t
1378992448	no username	\N	\N	t
1308984203	no username	\N	\N	t
2033457967	no username	\N	\N	t
5329826570	no username	\N	\N	t
1432544720	no username	\N	\N	t
\.


--
-- Name: payments_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: tarologueuser
--

SELECT pg_catalog.setval('public.payments_idx_seq', 1, false);


--
-- Name: sender_templates_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: tarologueuser
--

SELECT pg_catalog.setval('public.sender_templates_idx_seq', 14, true);


--
-- Name: service_types_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: tarologueuser
--

SELECT pg_catalog.setval('public.service_types_idx_seq', 1, false);


--
-- Name: services_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: tarologueuser
--

SELECT pg_catalog.setval('public.services_idx_seq', 52, true);


--
-- Name: user_templates_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: tarologueuser
--

SELECT pg_catalog.setval('public.user_templates_idx_seq', 3, true);


--
-- Name: user_user_template_association_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: tarologueuser
--

SELECT pg_catalog.setval('public.user_user_template_association_idx_seq', 42, true);


--
-- Name: users_idx_seq; Type: SEQUENCE SET; Schema: public; Owner: tarologueuser
--

SELECT pg_catalog.setval('public.users_idx_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (idx);


--
-- Name: sender_templates sender_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.sender_templates
    ADD CONSTRAINT sender_templates_pkey PRIMARY KEY (idx);


--
-- Name: service_types service_types_pkey; Type: CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.service_types
    ADD CONSTRAINT service_types_pkey PRIMARY KEY (idx);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (idx);


--
-- Name: user_templates user_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.user_templates
    ADD CONSTRAINT user_templates_pkey PRIMARY KEY (idx);


--
-- Name: user_user_template_association user_user_template_association_pkey; Type: CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.user_user_template_association
    ADD CONSTRAINT user_user_template_association_pkey PRIMARY KEY (idx);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (idx);


--
-- Name: payments payments_service_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_service_fkey FOREIGN KEY (service) REFERENCES public.services(idx);


--
-- Name: payments payments_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_fkey FOREIGN KEY ("user") REFERENCES public.users(idx);


--
-- Name: services services_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_type_fkey FOREIGN KEY (type) REFERENCES public.service_types(idx);


--
-- Name: user_user_template_association user_user_template_association_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.user_user_template_association
    ADD CONSTRAINT user_user_template_association_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(idx);


--
-- Name: user_user_template_association user_user_template_association_user_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tarologueuser
--

ALTER TABLE ONLY public.user_user_template_association
    ADD CONSTRAINT user_user_template_association_user_template_id_fkey FOREIGN KEY (user_template_id) REFERENCES public.user_templates(idx);


--
-- PostgreSQL database dump complete
--

