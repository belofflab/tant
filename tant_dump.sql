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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: tantuser
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO tantuser;

--
-- Name: proxies; Type: TABLE; Schema: public; Owner: tantuser
--

CREATE TABLE public.proxies (
    id bigint NOT NULL,
    host character varying(255) NOT NULL,
    port integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    scheme character varying(255) NOT NULL
);


ALTER TABLE public.proxies OWNER TO tantuser;

--
-- Name: proxies_id_seq; Type: SEQUENCE; Schema: public; Owner: tantuser
--

CREATE SEQUENCE public.proxies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.proxies_id_seq OWNER TO tantuser;

--
-- Name: proxies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tantuser
--

ALTER SEQUENCE public.proxies_id_seq OWNED BY public.proxies.id;


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: tantuser
--

CREATE TABLE public.transactions (
    id bigint NOT NULL,
    worker bigint,
    amount numeric(12,2),
    date timestamp without time zone,
    receipt character varying(1024) NOT NULL
);


ALTER TABLE public.transactions OWNER TO tantuser;

--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: tantuser
--

CREATE SEQUENCE public.transactions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transactions_id_seq OWNER TO tantuser;

--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tantuser
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: transitions; Type: TABLE; Schema: public; Owner: tantuser
--

CREATE TABLE public.transitions (
    id bigint NOT NULL,
    worker_name character varying(255) NOT NULL,
    date timestamp without time zone
);


ALTER TABLE public.transitions OWNER TO tantuser;

--
-- Name: transitions_id_seq; Type: SEQUENCE; Schema: public; Owner: tantuser
--

CREATE SEQUENCE public.transitions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transitions_id_seq OWNER TO tantuser;

--
-- Name: transitions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tantuser
--

ALTER SEQUENCE public.transitions_id_seq OWNED BY public.transitions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: tantuser
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    username character varying(255),
    worker bigint,
    last_activity timestamp without time zone,
    first_touch timestamp without time zone,
    first_name character varying(255),
    last_name character varying(255),
    is_processing boolean,
    is_free_consulting boolean
);


ALTER TABLE public.users OWNER TO tantuser;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: tantuser
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO tantuser;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tantuser
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: workers; Type: TABLE; Schema: public; Owner: tantuser
--

CREATE TABLE public.workers (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    api_id bigint NOT NULL,
    api_hash character varying(1024) NOT NULL,
    proxy bigint,
    is_active boolean,
    created_at timestamp without time zone,
    api_port bigint,
    amount numeric(12,2),
    username character varying(255)
);


ALTER TABLE public.workers OWNER TO tantuser;

--
-- Name: workers_id_seq; Type: SEQUENCE; Schema: public; Owner: tantuser
--

CREATE SEQUENCE public.workers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.workers_id_seq OWNER TO tantuser;

--
-- Name: workers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tantuser
--

ALTER SEQUENCE public.workers_id_seq OWNED BY public.workers.id;


--
-- Name: proxies id; Type: DEFAULT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.proxies ALTER COLUMN id SET DEFAULT nextval('public.proxies_id_seq'::regclass);


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Name: transitions id; Type: DEFAULT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.transitions ALTER COLUMN id SET DEFAULT nextval('public.transitions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: workers id; Type: DEFAULT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.workers ALTER COLUMN id SET DEFAULT nextval('public.workers_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: tantuser
--

COPY public.alembic_version (version_num) FROM stdin;
b7f0f816ab58
\.


--
-- Data for Name: proxies; Type: TABLE DATA; Schema: public; Owner: tantuser
--

COPY public.proxies (id, host, port, username, password, scheme) FROM stdin;
1	217.29.62.212	13035	sG25hk	GoqVfS	socks5
2	217.29.63.40	13515	PBpazk	TEagmL	socks5
3	217.29.62.214	12092	fy2w0z	NgxTcY	socks5
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: tantuser
--

COPY public.transactions (id, worker, amount, date, receipt) FROM stdin;
\.


--
-- Data for Name: transitions; Type: TABLE DATA; Schema: public; Owner: tantuser
--

COPY public.transitions (id, worker_name, date) FROM stdin;
1	sasha_tarolog	2023-10-12 16:02:30
2	sasha_tarolog	2023-09-09 05:37:29
3	sasha_tarolog	2023-09-07 13:44:30
4	sasha_tarolog	2023-09-13 07:36:16
5	sasha_tarolog	2023-09-23 10:48:47
6	sasha_tarolog	2023-09-09 18:13:43
7	sasha_tarolog	2023-09-11 12:43:48
8	sasha_tarolog	2023-10-09 08:05:52
9	sasha_tarolog	2023-10-13 06:49:14
10	sasha_tarolog	2023-09-10 11:56:47
11	sasha_tarolog	2023-10-12 09:37:30
12	sasha_tarolog	2023-09-10 07:41:27
13	sasha_tarolog	2023-09-10 08:50:39
14	sasha_tarolog	2023-10-13 06:52:01
15	sasha_tarolog	2023-09-13 09:21:10
16	sasha_tarolog	2023-09-26 11:21:21
17	sasha_tarolog	2023-09-25 06:58:24
18	sasha_tarolog	2023-09-09 11:40:32
19	sasha_tarolog	2023-09-19 07:45:58
20	sasha_tarolog	2023-09-13 15:48:12
21	sasha_tarolog	2023-09-26 07:30:22
22	sasha_tarolog	2023-09-09 15:39:53
23	sasha_tarolog	2023-10-04 11:18:52
24	sasha_tarolog	2023-09-28 17:45:30
25	sasha_tarolog	2023-09-10 07:13:03
26	sasha_tarolog	2023-09-13 15:41:15
27	sasha_tarolog	2023-09-11 12:17:15
28	sasha_tarolog	2023-09-20 05:55:57
29	sasha_tarolog	2023-09-18 09:50:52
30	sasha_tarolog	2023-09-29 10:52:01
31	sasha_tarolog	2023-09-07 08:21:38
32	sasha_tarolog	2023-09-14 12:13:37
33	sasha_tarolog	2023-09-08 09:38:19
34	sasha_tarolog	2023-10-13 07:57:44
35	sasha_tarolog	2023-09-09 11:22:38
36	sasha_tarolog	2023-10-04 11:39:26
37	sasha_tarolog	2023-09-07 15:39:04
38	sasha_tarolog	2023-09-25 07:31:32
39	sasha_tarolog	2023-09-27 17:20:43
40	sasha_tarolog	2023-09-10 15:39:16
41	sasha_tarolog	2023-10-12 09:37:36
42	sasha_tarolog	2023-10-13 17:51:00
43	sasha_tarolog	2023-09-13 15:51:25
44	sasha_tarolog	2023-09-20 06:08:18
45	sasha_tarolog	2023-10-11 08:10:54
46	sasha_tarolog	2023-09-14 18:15:29
47	sasha_tarolog	2023-09-27 08:19:54
48	sasha_tarolog	2023-10-02 13:18:57
49	sasha_tarolog	2023-09-21 09:14:03
50	sasha_tarolog	2023-10-13 22:10:56
51	sasha_tarolog	2023-09-22 13:03:53
52	sasha_tarolog	2023-09-17 08:52:38
53	sasha_tarolog	2023-09-20 05:15:22
54	sasha_tarolog	2023-09-10 13:15:03
55	sasha_tarolog	2023-10-06 08:11:55
56	sasha_tarolog	2023-09-09 08:35:14
57	sasha_tarolog	2023-09-09 16:07:25
58	sasha_tarolog	2023-09-10 08:12:39
59	sasha_tarolog	2023-09-10 11:38:01
60	sasha_tarolog	2023-09-10 11:29:34
61	sasha_tarolog	2023-09-10 11:20:01
62	sasha_tarolog	2023-10-05 06:31:13
63	sasha_tarolog	2023-09-14 08:08:02
64	sasha_tarolog	2023-10-05 14:13:31
65	sasha_tarolog	2023-09-19 07:54:48
66	sasha_tarolog	2023-10-09 09:00:00
67	sasha_tarolog	2023-09-13 16:18:05
68	sasha_tarolog	2023-09-09 14:12:02
69	sasha_tarolog	2023-09-10 20:44:14
70	sasha_tarolog	2023-10-11 08:03:51
71	sasha_tarolog	2023-09-09 08:03:01
72	sasha_tarolog	2023-09-09 21:37:32
73	sasha_tarolog	2023-09-09 15:03:07
74	sasha_tarolog	2023-09-22 11:02:49
75	sasha_tarolog	2023-09-09 14:08:37
76	sasha_tarolog	2023-09-26 07:32:53
77	sasha_tarolog	2023-09-27 16:36:45
78	sasha_tarolog	2023-10-05 06:48:00
79	sasha_tarolog	2023-09-13 02:43:31
80	sasha_tarolog	2023-09-11 12:00:04
81	sasha_tarolog	2023-09-13 12:30:07
82	sasha_tarolog	2023-09-07 13:53:04
83	sasha_tarolog	2023-10-06 15:04:01
84	sasha_tarolog	2023-09-09 13:00:24
85	sasha_tarolog	2023-09-09 16:04:34
86	sasha_tarolog	2023-10-05 16:49:15
87	sasha_tarolog	2023-09-09 15:13:54
88	sasha_tarolog	2023-09-09 14:12:48
89	sasha_tarolog	2023-09-15 16:10:58
90	sasha_tarolog	2023-09-09 13:01:35
91	sasha_tarolog	2023-09-15 06:26:49
92	sasha_tarolog	2023-10-04 15:25:43
93	sasha_tarolog	2023-09-29 10:35:10
94	sasha_tarolog	2023-09-10 12:41:33
95	sasha_tarolog	2023-09-12 07:55:39
96	sasha_tarolog	2023-09-12 16:33:50
97	sasha_tarolog	2023-09-14 10:15:39
98	sasha_tarolog	2023-09-23 11:21:07
99	sasha_tarolog	2023-09-09 13:21:33
100	sasha_tarolog	2023-09-09 16:36:38
101	sasha_tarolog	2023-09-22 08:57:59
102	sasha_tarolog	2023-09-14 07:43:49
103	sasha_tarolog	2023-10-14 08:53:23
104	sasha_tarolog	2023-10-03 10:59:08
105	sasha_tarolog	2023-10-04 10:09:17
106	sasha_tarolog	2023-09-19 07:47:09
107	sasha_tarolog	2023-09-13 14:00:28
108	sasha_tarolog	2023-09-07 12:39:58
109	sasha_tarolog	2023-09-13 09:37:46
110	sasha_tarolog	2023-09-10 07:46:48
111	sasha_tarolog	2023-09-22 11:51:44
112	sasha_tarolog	2023-10-07 13:35:34
113	sasha_tarolog	2023-09-13 09:03:20
114	sasha_tarolog	2023-09-14 10:27:37
115	sasha_tarolog	2023-09-26 16:55:22
116	sasha_tarolog	2023-09-12 12:45:36
117	sasha_tarolog	2023-09-29 08:28:09
118	sasha_tarolog	2023-10-04 10:55:35
119	sasha_tarolog	2023-09-23 08:28:46
120	sasha_tarolog	2023-09-07 08:59:06
121	sasha_tarolog	2023-09-10 12:48:38
122	sasha_tarolog	2023-09-15 13:21:12
123	sasha_tarolog	2023-10-14 04:04:32
124	sasha_tarolog	2023-09-18 06:58:33
125	sasha_tarolog	2023-10-13 09:27:06
126	sasha_tarolog	2023-09-27 08:19:46
127	sasha_tarolog	2023-09-19 07:20:07
128	sasha_tarolog	2023-09-14 17:01:39
129	sasha_tarolog	2023-09-19 17:41:42
130	sasha_tarolog	2023-09-07 08:30:27
131	sasha_tarolog	2023-09-13 10:15:32
132	sasha_tarolog	2023-10-13 18:36:42
133	sasha_tarolog	2023-10-06 07:43:44
134	sasha_tarolog	2023-09-19 18:45:57
135	sasha_tarolog	2023-09-26 08:04:33
136	sasha_tarolog	2023-09-09 14:06:49
137	sasha_tarolog	2023-10-06 08:33:16
138	sasha_tarolog	2023-09-16 06:10:34
139	sasha_tarolog	2023-10-14 13:37:07
140	sasha_tarolog	2023-10-04 10:43:54
141	sasha_tarolog	2023-09-10 11:38:05
142	sasha_tarolog	2023-09-25 06:51:31
143	sasha_tarolog	2023-09-09 07:34:07
144	sasha_tarolog	2023-09-07 12:56:13
145	sasha_tarolog	2023-09-09 11:35:12
146	sasha_tarolog	2023-09-09 12:55:30
147	sasha_tarolog	2023-09-07 09:00:54
148	sasha_tarolog	2023-09-22 09:51:31
149	sasha_tarolog	2023-09-09 14:59:46
150	sasha_tarolog	2023-09-10 12:27:16
151	sasha_tarolog	2023-09-15 17:01:08
152	sasha_tarolog	2023-10-12 16:03:25.60808
153	sasha_tarolog	2023-09-09 13:48:54
154	sasha_tarolog	2023-09-10 13:36:12
155	sasha_tarolog	2023-09-23 11:51:28
156	sasha_tarolog	2023-09-07 15:10:47
157	sasha_tarolog	2023-10-13 12:13:23
158	sasha_tarolog	2023-09-13 09:14:40
159	sasha_tarolog	2023-09-22 10:38:05
160	sasha_tarolog	2023-09-11 10:04:15
161	sasha_tarolog	2023-09-09 14:26:57
162	sasha_tarolog	2023-09-09 13:00:39
163	sasha_tarolog	2023-09-13 15:28:34
164	sasha_tarolog	2023-09-28 17:59:14
165	sasha_tarolog	2023-10-03 16:47:38
166	sasha_tarolog	2023-09-20 11:41:36
167	sasha_tarolog	2023-09-09 14:38:02
168	sasha_tarolog	2023-09-10 19:10:41
169	sasha_tarolog	2023-09-21 04:16:05
170	sasha_tarolog	2023-09-30 11:08:14
171	sasha_tarolog	2023-09-09 15:05:52
172	sasha_tarolog	2023-09-10 08:21:34
173	sasha_tarolog	2023-09-23 08:06:26
174	sasha_tarolog	2023-09-20 05:08:52
175	sasha_tarolog	2023-09-15 06:32:22
176	sasha_tarolog	2023-10-06 07:55:59
177	sasha_tarolog	2023-10-05 14:14:24
178	sasha_tarolog	2023-09-10 12:57:17
179	sasha_tarolog	2023-09-07 11:04:53
180	sasha_tarolog	2023-09-14 12:14:02
181	sasha_tarolog	2023-09-20 05:02:37
182	sasha_tarolog	2023-09-11 07:59:26
183	sasha_tarolog	2023-09-19 10:15:07
184	sasha_tarolog	2023-09-11 08:04:53
185	sasha_tarolog	2023-10-14 13:04:36
186	sasha_tarolog	2023-09-14 12:13:43
187	sasha_tarolog	2023-09-19 10:11:35
188	sasha_tarolog	2023-09-10 16:45:55
189	sasha_tarolog	2023-09-22 08:53:46
190	sasha_tarolog	2023-10-10 08:56:52
191	sasha_tarolog	2023-10-04 10:05:00
192	sasha_tarolog	2023-10-05 11:11:25
193	sasha_tarolog	2023-09-07 06:50:12
194	sasha_tarolog	2023-09-10 15:30:27
195	sasha_tarolog	2023-10-04 15:15:50
196	sasha_tarolog	2023-10-06 15:12:33
197	sasha_tarolog	2023-10-10 11:22:45
198	sasha_tarolog	2023-09-11 07:22:37
199	sasha_tarolog	2023-10-03 17:09:53
200	sasha_tarolog	2023-09-22 10:38:10
201	sasha_tarolog	2023-10-13 12:20:03
202	sasha_tarolog	2023-09-13 12:29:10
203	sasha_tarolog	2023-09-07 09:29:16
204	sasha_tarolog	2023-09-11 18:11:45
205	sasha_tarolog	2023-09-27 14:39:11
206	sasha_tarolog	2023-09-26 16:54:56
207	sasha_tarolog	2023-09-09 05:49:41
208	sasha_tarolog	2023-09-14 12:14:21
209	sasha_tarolog	2023-10-10 07:23:06
210	sasha_tarolog	2023-09-11 08:04:56
211	sasha_tarolog	2023-09-22 09:15:36
212	sasha_tarolog	2023-09-27 17:20:48
213	sasha_tarolog	2023-09-15 16:25:43
214	sasha_tarolog	2023-10-05 06:39:59
215	sasha_tarolog	2023-09-22 16:44:14
216	sasha_tarolog	2023-09-14 07:05:27
217	sasha_tarolog	2023-09-11 07:23:41
218	sasha_tarolog	2023-09-07 07:15:47
219	sasha_tarolog	2023-09-09 14:23:28
220	sasha_tarolog	2023-09-29 18:01:23
221	sasha_tarolog	2023-09-10 11:51:23
222	sasha_tarolog	2023-09-07 06:19:37
223	sasha_tarolog	2023-09-22 09:01:08
224	sasha_tarolog	2023-09-14 07:21:15
225	sasha_tarolog	2023-09-07 12:21:58
226	sasha_tarolog	2023-10-02 13:32:23
227	sasha_tarolog	2023-10-05 06:44:43
228	sasha_tarolog	2023-09-21 07:52:31
229	sasha_tarolog	2023-10-11 09:53:31
230	sasha_tarolog	2023-09-30 10:08:24
231	sasha_tarolog	2023-09-25 07:33:41
232	sasha_tarolog	2023-09-10 11:26:37
233	sasha_tarolog	2023-09-09 18:40:53
234	sasha_tarolog	2023-09-20 05:56:03
235	sasha_tarolog	2023-09-09 15:17:01
236	sasha_tarolog	2023-09-10 12:41:58
237	sasha_tarolog	2023-09-11 16:45:51
238	sasha_tarolog	2023-09-13 16:51:00
239	sasha_tarolog	2023-09-09 15:04:22
240	sasha_tarolog	2023-09-11 16:33:27
241	sasha_tarolog	2023-09-26 11:37:19
242	sasha_tarolog	2023-09-10 15:22:00
243	sasha_tarolog	2023-09-16 09:17:24
244	sasha_tarolog	2023-09-27 08:22:53
245	sasha_tarolog	2023-09-13 07:23:48
246	sasha_tarolog	2023-09-07 07:13:46
247	sasha_tarolog	2023-10-06 08:07:02
248	sasha_tarolog	2023-09-09 13:16:11
249	sasha_tarolog	2023-09-09 14:55:57
250	sasha_tarolog	2023-10-13 17:58:58
251	sasha_tarolog	2023-09-09 13:59:54
252	sasha_tarolog	2023-09-13 11:42:09
253	sasha_tarolog	2023-09-07 10:03:44
254	sasha_tarolog	2023-09-09 11:19:47
255	sasha_tarolog	2023-09-30 13:22:55
256	sasha_tarolog	2023-10-04 15:24:59
257	sasha_tarolog	2023-09-15 06:29:17
258	sasha_tarolog	2023-10-13 06:49:25
259	sasha_tarolog	2023-10-01 07:38:53
260	sasha_tarolog	2023-09-09 16:07:58
261	sasha_tarolog	2023-09-10 11:38:16
262	sasha_tarolog	2023-09-07 13:06:04
263	sasha_tarolog	2023-09-14 08:00:56
264	sasha_tarolog	2023-09-10 11:00:17
265	sasha_tarolog	2023-10-10 09:04:22
266	sasha_tarolog	2023-09-22 09:00:13
267	sasha_tarolog	2023-09-12 08:04:56
268	sasha_tarolog	2023-09-26 07:30:26
269	sasha_tarolog	2023-09-27 16:36:34
270	sasha_tarolog	2023-09-10 12:09:19
271	sasha_tarolog	2023-09-28 06:16:23
272	sasha_tarolog	2023-09-15 16:00:37
273	sasha_tarolog	2023-10-03 19:17:53
274	sasha_tarolog	2023-09-09 16:32:08
275	sasha_tarolog	2023-09-13 08:10:00
276	sasha_tarolog	2023-09-23 07:02:32
277	sasha_tarolog	2023-09-30 13:23:06
278	sasha_tarolog	2023-09-21 08:14:46
279	sasha_tarolog	2023-10-03 19:10:54
280	sasha_tarolog	2023-09-09 14:44:09
281	sasha_tarolog	2023-09-10 10:39:22
282	sasha_tarolog	2023-09-09 11:40:48
283	sasha_tarolog	2023-09-29 18:07:01
284	sasha_tarolog	2023-09-11 14:28:15
285	sasha_tarolog	2023-09-07 15:38:47
286	sasha_tarolog	2023-09-29 10:30:12
287	sasha_tarolog	2023-09-22 09:46:34
288	sasha_tarolog	2023-09-12 08:19:45
289	sasha_tarolog	2023-09-22 09:51:48
290	sasha_tarolog	2023-09-09 14:40:23
291	sasha_tarolog	2023-09-30 10:49:56
292	sasha_tarolog	2023-09-30 10:48:32
293	sasha_tarolog	2023-09-09 05:37:01
294	sasha_tarolog	2023-10-04 15:32:21
295	sasha_tarolog	2023-09-10 10:44:17
296	sasha_tarolog	2023-09-30 05:31:43
297	sasha_tarolog	2023-09-22 11:50:51
298	sasha_tarolog	2023-09-18 10:22:16
299	sasha_tarolog	2023-09-18 15:25:56
300	sasha_tarolog	2023-09-10 10:57:38
301	sasha_tarolog	2023-10-12 10:31:37
302	sasha_tarolog	2023-09-10 11:10:18
303	sasha_tarolog	2023-09-10 17:11:58
304	sasha_tarolog	2023-09-09 14:02:53
305	sasha_tarolog	2023-09-19 11:52:56
306	sasha_tarolog	2023-09-18 06:27:40
307	sasha_tarolog	2023-10-05 11:11:37
308	sasha_tarolog	2023-09-09 14:30:40
309	sasha_tarolog	2023-09-07 17:20:36
310	sasha_tarolog	2023-09-09 14:31:21
311	sasha_tarolog	2023-09-07 16:31:58
312	sasha_tarolog	2023-09-12 12:00:04
313	sasha_tarolog	2023-09-14 10:41:43
314	sasha_tarolog	2023-09-14 14:16:02
315	sasha_tarolog	2023-10-02 14:29:55
316	sasha_tarolog	2023-09-11 07:35:13
317	sasha_tarolog	2023-09-09 14:32:54
318	sasha_tarolog	2023-09-27 08:11:48
319	sasha_tarolog	2023-09-22 08:15:12
320	sasha_tarolog	2023-09-23 08:09:28
321	sasha_tarolog	2023-10-05 06:37:40
322	sasha_tarolog	2023-09-09 14:26:44
323	sasha_tarolog	2023-09-29 18:54:28
324	sasha_tarolog	2023-10-02 13:18:35
325	sasha_tarolog	2023-09-22 13:26:48
326	sasha_tarolog	2023-09-26 12:53:54
327	sasha_tarolog	2023-09-10 10:48:02
328	sasha_tarolog	2023-09-13 16:22:51
329	sasha_tarolog	2023-10-04 09:56:59
330	sasha_tarolog	2023-09-12 11:45:21
331	sasha_tarolog	2023-09-26 10:26:46
332	sasha_tarolog	2023-09-09 15:35:56
333	sasha_tarolog	2023-09-19 12:08:10
334	sasha_tarolog	2023-10-13 14:24:29
335	sasha_tarolog	2023-09-14 04:37:43
336	sasha_tarolog	2023-09-14 09:16:08
337	sasha_tarolog	2023-09-26 06:50:39
338	sasha_tarolog	2023-09-10 12:24:43
339	sasha_tarolog	2023-09-07 07:27:19
340	sasha_tarolog	2023-09-09 13:10:17
341	sasha_tarolog	2023-09-10 19:15:21
342	sasha_tarolog	2023-09-11 09:32:27
343	sasha_tarolog	2023-10-05 12:26:42
344	sasha_tarolog	2023-09-12 09:43:51
345	sasha_tarolog	2023-09-29 03:25:45
346	sasha_tarolog	2023-09-18 07:56:25
347	sasha_tarolog	2023-09-12 15:56:30
348	sasha_tarolog	2023-09-12 08:48:13
349	sasha_tarolog	2023-09-13 16:12:39
350	sasha_tarolog	2023-10-04 15:15:50
351	sasha_tarolog	2023-10-03 12:38:59
352	sasha_tarolog	2023-10-13 06:50:21
353	sasha_tarolog	2023-09-13 09:35:54
354	sasha_tarolog	2023-10-10 12:40:18
355	sasha_tarolog	2023-09-11 06:42:06
356	sasha_tarolog	2023-09-19 10:03:29
357	sasha_tarolog	2023-09-11 08:04:46
358	sasha_tarolog	2023-09-25 09:53:10
359	sasha_tarolog	2023-09-09 14:55:30
360	sasha_tarolog	2023-09-22 12:18:52
361	sasha_tarolog	2023-10-09 09:08:30
362	sasha_tarolog	2023-10-13 12:59:50
363	sasha_tarolog	2023-09-09 14:13:47
364	sasha_tarolog	2023-10-02 13:27:05
365	sasha_tarolog	2023-09-10 12:04:22
366	sasha_tarolog	2023-09-19 08:59:30
367	sasha_tarolog	2023-09-09 11:53:35
368	sasha_tarolog	2023-10-09 12:00:05
369	sasha_tarolog	2023-09-29 10:29:49
370	sasha_tarolog	2023-09-09 12:04:08
371	sasha_tarolog	2023-09-09 12:53:11
372	sasha_tarolog	2023-09-14 08:34:21
373	sasha_tarolog	2023-09-15 16:39:48
374	sasha_tarolog	2023-09-11 07:11:50
375	sasha_tarolog	2023-09-09 11:37:36
376	sasha_tarolog	2023-10-04 15:16:59
377	sasha_tarolog	2023-09-09 10:04:59
378	sasha_tarolog	2023-09-09 08:03:22
379	sasha_tarolog	2023-09-11 15:28:00
380	sasha_tarolog	2023-10-13 14:19:22
381	sasha_tarolog	2023-09-30 10:34:24
382	sasha_tarolog	2023-09-22 11:57:25
383	sasha_tarolog	2023-09-09 13:16:18
384	sasha_tarolog	2023-09-09 08:03:03
385	sasha_tarolog	2023-09-10 10:55:29
386	sasha_tarolog	2023-09-09 12:21:53
387	sasha_tarolog	2023-10-13 09:17:07
388	sasha_tarolog	2023-09-13 09:28:00
389	sasha_tarolog	2023-09-22 09:15:52
390	sasha_tarolog	2023-10-13 12:09:56
391	sasha_tarolog	2023-09-09 09:43:34
392	sasha_tarolog	2023-09-26 11:53:04
393	sasha_tarolog	2023-10-13 13:14:30
394	sasha_tarolog	2023-09-09 13:51:01
395	sasha_tarolog	2023-09-20 06:33:05
396	sasha_tarolog	2023-09-11 12:09:07
397	sasha_tarolog	2023-09-11 15:06:43
398	sasha_tarolog	2023-09-30 11:07:53
399	sasha_tarolog	2023-09-09 14:07:27
400	sasha_tarolog	2023-09-30 11:08:50
401	sasha_tarolog	2023-09-23 07:59:36
402	sasha_tarolog	2023-09-12 08:20:36
403	sasha_tarolog	2023-09-11 06:51:34
404	sasha_tarolog	2023-10-13 07:23:35
405	sasha_tarolog	2023-09-18 07:00:23
406	sasha_tarolog	2023-09-23 11:54:38
407	sasha_tarolog	2023-10-09 09:24:55
408	sasha_tarolog	2023-10-13 10:27:23
409	sasha_tarolog	2023-10-04 11:40:23
410	sasha_tarolog	2023-09-10 08:25:06
411	sasha_tarolog	2023-09-09 14:36:21
412	sasha_tarolog	2023-09-16 09:18:48
413	sasha_tarolog	2023-09-10 12:04:44
414	sasha_tarolog	2023-10-04 15:19:30
415	sasha_tarolog	2023-09-13 15:42:41
416	sasha_tarolog	2023-09-09 15:50:51
417	sasha_tarolog	2023-09-09 13:55:41
418	sasha_tarolog	2023-09-09 08:02:54
419	sasha_tarolog	2023-09-07 07:26:16
420	sasha_tarolog	2023-09-27 17:14:11
421	sasha_tarolog	2023-09-26 06:50:35
422	sasha_tarolog	2023-09-11 09:29:30
423	sasha_tarolog	2023-09-14 16:42:52
424	sasha_tarolog	2023-09-10 12:48:51
425	sasha_tarolog	2023-09-10 11:45:21
426	sasha_tarolog	2023-09-11 07:23:50
427	sasha_tarolog	2023-09-27 14:57:30
428	sasha_tarolog	2023-09-26 09:25:35
429	sasha_tarolog	2023-09-14 08:46:03
430	sasha_tarolog	2023-09-19 10:57:37
431	sasha_tarolog	2023-09-18 07:00:47
432	sasha_tarolog	2023-09-14 12:35:45
433	sasha_tarolog	2023-09-09 15:07:39
434	sasha_tarolog	2023-10-14 13:59:19
435	sasha_tarolog	2023-09-20 07:50:39
436	sasha_tarolog	2023-09-26 11:37:31
437	sasha_tarolog	2023-09-14 09:41:04
438	sasha_tarolog	2023-09-11 07:12:43
439	sasha_tarolog	2023-09-09 15:13:38
440	sasha_tarolog	2023-10-12 06:02:31
441	sasha_tarolog	2023-10-11 14:38:46
442	sasha_tarolog	2023-09-20 08:50:01
443	sasha_tarolog	2023-09-26 07:04:49
444	sasha_tarolog	2023-09-20 08:03:32
445	sasha_tarolog	2023-09-14 08:18:27
446	sasha_tarolog	2023-10-14 15:04:48
447	sasha_tarolog	2023-09-09 16:39:18
448	sasha_tarolog	2023-09-13 10:46:04
449	sasha_tarolog	2023-10-03 12:46:43
450	sasha_tarolog	2023-09-22 09:46:46
451	sasha_tarolog	2023-09-09 15:11:45
452	sasha_tarolog	2023-10-11 09:11:13
453	sasha_tarolog	2023-10-14 07:01:30
454	sasha_tarolog	2023-09-15 15:39:18
455	sasha_tarolog	2023-10-11 12:38:14.933879
456	sasha_tarolog	2023-10-14 13:15:39.974515
457	sasha_tarolog	2023-10-11 14:28:12.501937
458	sasha_tarolog	2023-10-12 18:45:53.04699
459	sasha_tarolog	2023-10-11 12:28:01.765557
460	sasha_tarolog	2023-10-14 17:41:34.135261
461	sasha_tarolog	2023-10-11 04:43:12.302189
462	taro2_sashA	2023-10-13 15:52:10
463	taro2_sashA	2023-10-13 15:16:04
464	taro2_sashA	2023-10-13 08:27:20
465	taro2_sashA	2023-10-13 06:47:22
466	taro2_sashA	2023-10-11 09:11:13
467	taro2_sashA	2023-10-10 09:14:47.696541
468	taro2_sashA	2023-10-14 13:40:55
469	taro2_sashA	2023-10-14 13:15:39.974515
470	taro2_sashA	2023-10-11 14:28:12.501937
471	taro2_sashA	2023-10-12 18:45:53.04699
472	taro2_sashA	2023-10-11 12:28:01.765557
473	taro2_sashA	2023-10-14 17:41:34.135261
474	taro2_sashA	2023-10-11 04:43:12.302189
476	taro2_sashA	2023-10-16 15:04:48
477	sasha_tarolog	2023-10-16 15:04:48
483	taro2_sashA	2023-10-17 08:13:56.643476
484	taro2_sashA	2023-10-17 13:52:30.852624
485	taro2_sashA	2023-10-17 13:53:59.738384
486	taro2_sashA	2023-10-17 14:09:17.045814
487	taro2_sashA	2023-10-17 14:33:01.942522
488	sasha_tarolog	2023-10-17 15:12:41.295745
489	taro2_sashA	2023-10-17 15:57:10.276376
490	taro2_sashA	2023-10-17 16:08:32.678754
491	sasha_tarolog	2023-10-18 07:38:09.80128
492	viktoria_numer	2023-10-19 02:03:03.946527
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: tantuser
--

COPY public.users (id, username, worker, last_activity, first_touch, first_name, last_name, is_processing, is_free_consulting) FROM stdin;
1055416540	\N	6233422995	2023-09-27 14:38:00	2023-09-27 14:39:11	Лёлик	\N	t	t
1202095307	\N	6233422995	2023-09-26 15:19:29	2023-09-27 08:22:53	K	\N	t	t
485129959	AnyutaPrincess	6233422995	2023-09-26 19:37:49	2023-09-27 08:19:54	✨❤️Анюта❤️✨	\N	t	t
851816559	\N	6233422995	2023-10-13 05:06:57	2023-10-14 13:37:07	Юлия	\N	t	t
1002010273	\N	6233422995	2023-09-22 14:40:08	2023-10-14 13:04:36	Тыковка	\N	t	t
6326119110	\N	6233422995	2023-10-14 07:01:30	2023-10-14 07:01:30	Нинеголог	\N	t	t
810860175	\N	6233422995	2023-10-13 07:51:03	2023-10-14 04:04:32	Ольга Данчева	\N	t	t
817755215	Chio_rio_sun	6233422995	2023-09-26 18:53:39	2023-09-27 08:19:46	Алла	\N	t	t
5088679932	\N	6233422995	2023-09-26 14:29:03	2023-10-13 14:19:22	Лунара	Каплан	t	t
5171297902	Irina_Ivanova_0391	6233422995	2023-09-13 14:40:54	2023-10-13 13:14:30	@Irina	\N	t	t
2073952347	\N	6233422995	2023-09-13 14:43:21	2023-10-13 12:59:50	Наталья	\N	t	t
1044328069	Yulia_Gibadullina	6233422995	2023-10-03 17:18:34	2023-10-13 12:20:03	Юлия	\N	t	t
889871409	aigulaigula	6233422995	2023-09-11 11:41:37	2023-10-13 12:13:23	Айгуль	\N	t	t
5163989992	oxana0378	6233422995	2023-09-09 10:30:50	2023-10-13 12:09:56	Оксана	\N	t	t
5285353311	Furious_Penguin	6233422995	2023-10-03 13:23:15	2023-10-13 10:27:23	Анастасия	Кузюрина	t	t
815506483	Vseprekracna	6233422995	2023-09-09 11:02:16	2023-10-13 09:27:06	VALENTI	\N	t	t
444794907	ksenka191993	6233422995	2023-10-02 08:51:55	2023-10-13 07:57:44	Ksenia	Samigullina	t	t
5270950985	\N	6233422995	2023-10-12 07:33:05	2023-10-13 07:23:35	Darya	\N	t	t
940750512	olka202008	6233422995	2023-10-03 15:59:01	2023-10-03 16:47:38	Олька	\N	t	t
6295057425	\N	6233422995	2023-09-28 07:36:56	2023-10-03 12:46:43	Альбина	\N	t	t
1948103616	\N	6233422995	2023-09-30 14:21:29	2023-10-03 12:38:59	Lusien	Lusi	t	t
747211337	alinusikk_a	6233422995	2023-09-26 11:33:30	2023-10-03 10:59:08	Алина	\N	t	t
1555972888	zalina_kkk	6233422995	2023-09-26 11:47:19	2023-10-02 14:29:55	залиник🤍	\N	t	t
1136901814	zilibobkak	6233422995	2023-10-02 09:21:41	2023-10-02 13:32:23	ника	\N	t	t
2084048465	Julia_sl	6233422995	2023-09-30 12:43:23	2023-10-02 13:27:05	Юлия	Якобчук	t	t
485912190	dearddary	6233422995	2023-09-29 17:17:07	2023-10-02 13:18:57	丽雅 𝚍𝚊𝚛𝚢𝚊.	\N	t	t
1694408603	Iro4ka_02	6233422995	2023-09-30 10:56:36	2023-10-02 13:18:35	❤️Īříňå❤️	\N	t	t
1233419487	DashaKadeshnikova	6233422995	2023-09-29 17:13:02	2023-10-01 07:38:53	Дарья	Савичева	t	t
1293917826	o_shirokaya	6233422995	2023-09-29 15:26:00	2023-09-30 13:23:06	Ольга	\N	t	t
1226588315	alenasvalova72	6233422995	2023-09-30 10:14:42	2023-09-30 13:22:55	Алена//массаж//медицинское образование.	\N	t	t
5232181794	\N	6233422995	2023-09-30 09:50:02	2023-09-30 11:08:50	Ольга	Астафьева	t	t
954594126	sadnesselza	6233422995	2023-09-29 17:16:18	2023-09-30 11:08:14	Е.И.	\N	t	t
5207439957	galinanizheritskaja	6233422995	2023-09-30 05:28:59	2023-09-30 11:07:53	Галина Нежеритская Бизнес с Атоми	\N	t	t
1365489126	twinsAlyona	6233422995	2023-09-29 05:04:30	2023-09-30 10:49:56	Алёна	Антонова	t	t
1371975872	nasttya_dammit	6233422995	2023-09-27 11:43:52	2023-09-30 10:48:32	𝐀𝐍𝐀𝐒𝐓𝐀𝐒𝐈𝐀	\N	t	t
5111070230	ksushaa1207	6233422995	2023-09-29 13:52:05	2023-09-30 10:34:24	Оксана	Евдокимова	t	t
1154610025	\N	6233422995	2023-09-13 09:59:12	2023-09-30 10:08:24	Ксения	Данилова	t	t
1388153126	alen_a1_1	6233422995	2023-09-30 01:46:55	2023-09-30 05:31:43	🤍	\N	t	t
1323400388	\N	6233422995	2023-09-28 18:03:30	2023-09-29 18:07:01	Lesya 🕊	\N	t	t
1105764400	\N	6233422995	2023-09-27 18:17:52	2023-09-29 18:01:23	Дарья	Тур	t	t
414333059	inna_titkova	6233422995	2023-09-28 19:44:12	2023-09-29 10:52:01	Инна	Титкова	t	t
709444083	basjxs	6233422995	2023-09-29 07:44:48	2023-09-29 10:35:10	Анастасия	\N	t	t
1348758693	numerolog_larisachalapan	6233422995	2023-09-27 11:12:30	2023-09-29 10:30:12	Larisa Chalapan	\N	t	t
2129992474	\N	6233422995	2023-09-28 07:16:24	2023-09-29 10:29:49	Mariа_аа	\N	t	t
783530007	\N	6233422995	2023-09-28 20:33:24	2023-09-29 08:28:09	Ниночек🦭	\N	t	t
1902591417	\N	6233422995	2023-09-28 03:45:20	2023-09-29 03:25:45	Эва	\N	t	t
923204870	\N	6233422995	2023-09-25 16:31:40	2023-09-28 17:59:14	Hhhh	Gggh	t	t
386027802	krapivaann	6233422995	2023-09-27 15:33:54	2023-09-28 17:45:30	An	Na	t	t
1261677517	\N	6233422995	2023-09-23 08:07:03	2023-09-28 06:16:23	Сырттанова	Нургуль	t	t
1088918693	Tmm05	6233422995	2023-09-26 18:49:47	2023-09-27 17:20:48	💗🧸	\N	t	t
462426333	kyzyakuzmina	6233422995	2023-09-27 09:46:56	2023-09-27 17:20:43	Екатерина	Кузьмина	t	t
5612148254	\N	6233422995	2023-09-27 12:22:47	2023-09-27 17:14:11	🐻	\N	t	t
635208930	\N	6233422995	2023-09-26 17:22:27	2023-09-27 16:36:45	Sokolova	Nadin	t	t
1252957962	LEISAN_Z	6233422995	2023-09-27 10:11:18	2023-09-27 16:36:34	Лейсан	Залилова	t	t
5739819347	\N	6233422995	2023-09-23 05:04:57	2023-09-27 14:57:30	Nino	Nu	t	t
1639796989	\N	6233422995	2023-09-26 16:35:15	2023-09-27 08:11:48	Нина	Хартаганова	t	t
778124858	nelchek87	6233422995	2023-09-21 05:02:39	2023-09-26 16:55:22	Найля	\N	t	t
1055833324	lesia54470	6233422995	2023-09-15 14:14:19	2023-09-26 16:54:56	Леся	Высоцкая	t	t
1718096020	sssaminik	6233422995	2023-09-25 07:44:02	2023-09-26 12:53:54	саминка	\N	t	t
5167840735	\N	6233422995	2023-09-24 06:54:38	2023-09-26 11:53:04	Анастасия	\N	t	t
5878106542	\N	6233422995	2023-09-20 09:11:31	2023-09-26 11:37:31	Алёна	\N	t	t
1194752559	\N	6233422995	2023-09-24 19:38:33	2023-09-26 11:37:19	аидик	\N	t	t
314004706	katyfreelancer	6233422995	2023-09-25 09:31:54	2023-09-26 11:21:21	KATYA	\N	t	t
1772439569	\N	6233422995	2023-09-25 08:06:14	2023-09-26 10:26:46	Юлия	Алтунина	t	t
5746222523	linxsaaass	6233422995	2023-09-26 09:15:54	2023-09-26 09:25:35	лизчикс	\N	t	t
843671681	bad_kar_ma	6233422995	2023-09-26 04:24:16	2023-09-26 08:04:33	Александра 🌿	\N	t	t
633701857	dikoshk	6233422995	2023-09-25 07:52:11	2023-09-26 07:32:53	Динара	Алимсеитова	t	t
1252574966	Uyllia	6233422995	2023-09-25 07:40:30	2023-09-26 07:30:26	Юля	\N	t	t
6284621646	\N	6233422995	2023-09-13 07:43:13	2023-09-13 10:46:04	Evgenia	\N	t	t
829372208	aammmman1	6233422995	2023-09-13 05:07:51	2023-09-13 10:15:32	Aigul	\N	t	t
6208832294	Tutre666	999	2023-10-17 08:52:28.567264	2023-10-11 04:43:12.302189	FROM	BOT	f	f
1345227557	vivitko7	999	2023-10-17 08:52:29.372623	2023-10-11 12:28:01.765557	FROM	BOT	f	f
1062114023	noizolk	999	2023-10-17 08:52:30.213047	2023-10-11 14:28:12.501937	FROM	BOT	f	f
2069950167	\N	6317875729	2023-10-17 08:52:32.65493	2023-10-13 06:47:22	FROM	BOT	t	t
1123783955	omarkova_om	999	2023-10-17 08:52:33.614064	2023-10-12 18:45:53.04699	FROM	BOT	f	f
6270915055	g3nt1m3n	6317875729	2023-10-17 08:52:45.820106	2023-10-10 09:14:47.696541	FROM	BOT	t	t
5220239319	Ymagechka78	999	2023-10-17 08:52:46.680737	2023-10-14 17:41:34.135261	FROM	BOT	f	f
269993873	viktoria_numer	6233422995	2023-10-18 10:59:27.293422	2023-10-09 08:05:52	FROM	BOT	t	t
312960075	Lunnaya_ptichka_nevelichka	6233422995	2023-09-09 11:00:35	2023-10-13 06:52:01	Lunnaya ptichka nevelichka	\N	t	t
1230871213	its_katerina_m	6233422995	2023-09-13 14:43:48	2023-10-13 06:49:25	Катерина	М	t	t
280134617	RoseRahimova	6233422995	2023-10-09 07:18:35	2023-10-13 06:49:14	Розалия	Камалова	t	t
1441028313	\N	6233422995	2023-10-11 10:59:34	2023-10-12 10:31:37	Ксения	Ёлкина	t	t
466748762	\N	6233422995	2023-10-11 09:38:38	2023-10-12 09:37:36	Анна	\N	t	t
304931705	Svetlana140887	6233422995	2023-10-11 11:59:19	2023-10-12 09:37:30	Света	СвеТочка	t	t
6001134278	Hacbr	6233422995	2023-10-10 14:50:42	2023-10-12 06:02:31	Нина	Черных	t	t
6039518977	\N	6233422995	2023-09-11 10:21:54	2023-10-11 14:38:46	Alex	\N	t	t
1151853930	SSvet1980	6233422995	2023-10-10 13:00:57	2023-10-11 09:53:31	Светлана	\N	t	t
6317875729	taro2_sashA	6233422995	2023-10-11 09:11:13	2023-10-11 09:11:13	Александра	Таролог	t	t
483815586	mila_mihailovna	6233422995	2023-10-11 05:15:47	2023-10-11 08:10:54	Мила Михайловна ❤️	\N	t	t
593135617	kkgromkkk	6233422995	2023-10-10 12:56:53	2023-10-11 08:03:51	Katerina	Gromyko	t	t
1991385190	swe_tiik	6233422995	2023-10-10 02:56:36	2023-10-10 12:40:18	Swe.tiik	\N	t	t
1033093523	khryushka18	6233422995	2023-09-13 09:00:24	2023-10-10 11:22:45	Енотик	\N	t	t
1244266891	\N	6233422995	2023-10-10 07:21:19	2023-10-10 09:04:22	Elena	Minaeva	t	t
1023647040	zq_kris	6233422995	2023-10-06 16:03:16	2023-10-10 08:56:52	kriz.	\N	t	t
1070616949	Xxswwv	6233422995	2023-10-09 16:46:13	2023-10-10 07:23:06	лиза	\N	t	t
2118872190	\N	6233422995	2023-10-04 13:19:55	2023-10-09 12:00:05	Юлия	Олеговна	t	t
5279129131	Twermyy	6233422995	2023-10-06 15:02:37	2023-10-09 09:24:55	Twermyy	\N	t	t
2072666482	sshittingg	6233422995	2023-10-06 19:34:49	2023-10-09 09:08:30	mmg	\N	t	t
577410788	elena_tishkina	6233422995	2023-10-05 17:59:08	2023-10-09 09:00:00	Елена	Тишкина	t	t
767051372	\N	6233422995	2023-10-05 08:11:05	2023-10-07 13:35:34	@olga	\N	t	t
1032666801	\N	6233422995	2023-10-06 14:00:13	2023-10-06 15:12:33	Юлия	\N	t	t
666773662	ngadelia	6233422995	2023-10-04 13:47:55	2023-10-06 15:04:01	ninuca	\N	t	t
850098324	Ylia_Nikolaeva	6233422995	2023-10-06 07:52:03	2023-10-06 08:33:16	Юлия	Николаева	t	t
522626107	brkv24	6233422995	2023-10-05 12:51:48	2023-10-06 08:11:55	Екатерина	\N	t	t
1211317183	KvintRita	6233422995	2023-10-06 07:06:21	2023-10-06 08:07:02	Kvint	Rita	t	t
975073150	\N	6233422995	2023-10-04 21:27:46	2023-10-06 07:55:59	Polina_pupovina	\N	t	t
840597478	ViktoriyaNovikova95	6233422995	2023-09-09 10:41:18	2023-10-06 07:43:44	бла бла бла	\N	t	t
684250637	Kosm0s_666	6233422995	2023-10-05 16:02:41	2023-10-05 16:49:15	🔥 Koroleva	Tatiana 🔥	t	t
975591460	pri_nastya	6233422995	2023-09-09 11:27:23	2023-10-05 14:14:24	Nastya	P	t	t
562657604	\N	6233422995	2023-10-05 07:17:13	2023-10-05 14:13:31	Roman	\N	t	t
1890593803	nadejdaromanovna	6233422995	2023-09-11 10:06:10	2023-10-05 12:26:42	Надежда	\N	t	t
1489413394	kiiisssmmm	6233422995	2023-09-26 11:41:55	2023-10-05 11:11:37	эля	\N	t	t
1025755904	danon_nnn	6233422995	2023-10-05 06:53:26	2023-10-05 11:11:25	дарья	\N	t	t
1145970616	\N	6233422995	2023-09-09 13:28:25	2023-10-05 06:44:43	Любовь	\N	t	t
1091753627	nuusmanova	6233422995	2023-09-22 15:17:58	2023-10-05 06:39:59	Настя	\N	t	t
1677134684	\N	6233422995	2023-09-09 11:07:48	2023-10-05 06:37:40	Алёна	Михайловская	t	t
551610220	aleksarad	6233422995	2023-10-04 19:08:43	2023-10-05 06:31:13	Александра	Радыгина	t	t
1384972868	ksyna82	6233422995	2023-09-27 02:56:57	2023-10-04 15:32:21	Ксения	\N	t	t
1227486679	\N	6233422995	2023-09-09 15:55:02	2023-10-04 15:24:59	Ольга	Попова	t	t
355845044	syumatova72	6233422995	2023-09-25 11:33:28	2023-09-26 07:30:22	Светлана	Юматова	t	t
5790961375	tatiana_oo	6233422995	2023-09-13 14:46:40	2023-09-14 08:46:03	Tania Kolyada	\N	t	t
5002812788	\N	6233422995	2023-09-13 22:39:40	2023-09-14 08:34:21	Natali	\N	t	t
6191100454	\N	6233422995	2023-09-14 05:42:59	2023-09-14 08:18:27	LION	\N	t	t
556179622	yulia301276	6233422995	2023-09-12 17:16:51	2023-09-14 08:08:02	Каравайкина	Юлия	t	t
1239038655	\N	6233422995	2023-09-13 16:46:02	2023-09-14 08:00:56	Виталик	\N	t	t
740602926	\N	6233422995	2023-09-13 15:10:38	2023-09-14 07:43:49	Алена	\N	t	t
1128996509	Ksunya1993	6233422995	2023-09-13 16:04:01	2023-09-14 07:21:15	Ксюшенька	\N	t	t
1098534151	\N	6233422995	2023-09-13 15:23:37	2023-09-14 07:05:27	Екатерина	Пушкова	t	t
1827357757	\N	6233422995	2023-09-13 07:27:11	2023-09-14 04:37:43	Светлана	\N	t	t
1185876768	Miss_Mirolya	6233422995	2023-09-13 07:44:07	2023-09-13 16:51:00	Olga	\N	t	t
1747826728	marmeladnyi_ponchik	6233422995	2023-09-13 14:46:49	2023-09-13 16:22:51	Гузель	Тулибаева	t	t
577817049	\N	6233422995	2023-09-13 15:41:32	2023-09-13 16:18:05	Татьяна	Федорова	t	t
1932097246	Limpapushka	6233422995	2023-09-13 14:39:02	2023-09-13 16:12:39	Валентина	\N	t	t
475622458	Anna_Troc777	6233422995	2023-09-13 14:35:02	2023-09-13 15:51:25	Анна️	️	t	t
347172051	dashayudi	6233422995	2023-09-13 14:35:40	2023-09-13 15:48:12	Dasha	\N	t	t
5548334349	neighboringcoast	6233422995	2023-09-13 13:57:59	2023-09-13 15:42:41	Даша	\N	t	t
392079261	Tatiana1790	6233422995	2023-09-13 14:35:00	2023-09-13 15:41:15	Татьяна	Просветова	t	t
916844003	\N	6233422995	2023-09-13 14:34:55	2023-09-13 15:28:34	Светлана	\N	t	t
759978238	grinch0012	6233422995	2023-09-09 07:04:14	2023-09-13 14:00:28	Grigorii	Grigorii	t	t
655156877	ribkaava	6233422995	2023-09-12 20:03:52	2023-09-13 12:30:07	Анастасия❣️	\N	t	t
1045385988	\N	6233422995	2023-09-13 05:02:13	2023-09-13 12:29:10	олеся	дьяконова	t	t
1220285615	YULIA_OSYA	6233422995	2023-09-13 08:12:06	2023-09-13 11:42:09	Юлия	Осипова	t	t
762783486	\N	6233422995	2023-09-13 08:24:00	2023-09-13 09:37:46	Аня	\N	t	t
1956298682	\N	6233422995	2023-09-13 08:16:24	2023-09-13 09:35:54	❤️(◠‿◕)❤️©	\N	t	t
5143987761	\N	6233422995	2023-09-13 07:21:40	2023-09-13 09:28:00	Юлия	\N	t	t
313272791	Ksenia_Onyushkina	6233422995	2023-09-12 17:16:34	2023-09-13 09:21:10	Ксения	\N	t	t
893431064	Lesya_Sheiko	6233422995	2023-09-13 07:15:20	2023-09-13 09:14:40	Lesya	Sheiko	t	t
770122167	anna_dzyyy	6233422995	2023-09-12 19:55:25	2023-09-13 09:03:20	Анна	\N	t	t
1275968466	\N	6233422995	2023-09-13 07:23:11	2023-09-13 08:10:00	Yulia	Farad	t	t
1203426453	V_V_666	6233422995	2023-09-12 17:12:28	2023-09-13 07:23:48	V D	\N	t	t
641160052	\N	6233422995	2023-09-12 04:26:47	2023-09-13 02:43:31	Татьяна	\N	t	t
716218997	\N	6233422995	2023-09-12 15:45:09	2023-09-12 16:33:50	E	R	t	t
1920338799	alla94_23	6233422995	2023-09-09 10:31:43	2023-09-12 15:56:30	Алла	\N	t	t
754091686	\N	6233422995	2023-09-19 06:41:23	2023-09-19 07:47:09	Елена	\N	t	t
5868280854	OHelsing	6233422995	2023-09-07 08:39:23	2023-10-14 13:59:19	Helsing	\N	t	t
132920538	ULYANUDE	6233422995	2023-10-17 13:54:35.509651	2023-09-13 07:36:16	Юлия	Колесник	t	t
1954638530	happyelvirochka	6233422995	2023-10-18 07:13:26.369881	2023-10-13 06:50:21	Эльвира	\N	t	t
706610112	mi_kh_r	6233422995	2023-10-18 07:28:17.183141	2023-10-04 15:25:43	Милена	\N	t	t
640415520	Hirynova	6233422995	2023-10-18 14:31:20.605846	2023-10-05 06:48:00	Оксана	Хирьянова	t	t
5512789699	\N	6233422995	2023-10-04 12:51:36	2023-10-04 15:19:30	Ольга	Нюхарева	t	t
1941656560	\N	6233422995	2023-10-04 15:03:56	2023-10-04 15:15:50	Венера	\N	t	t
5305154538	Hellish_hanter	6233422995	2023-10-04 10:10:33	2023-10-04 11:40:23	Lilia	\N	t	t
451204149	DRFkat	6233422995	2023-10-04 09:41:39	2023-10-04 11:39:26	Екатерина	Фролова	t	t
379353998	Rimma_l	6233422995	2023-09-16 17:29:40	2023-10-04 11:18:52	Римма	\N	t	t
783672638	ktt_7	6233422995	2023-09-21 15:49:49	2023-10-04 10:55:35	Татьяна	\N	t	t
856940459	\N	6233422995	2023-10-04 10:37:29	2023-10-04 10:43:54	Василина	Воржева	t	t
747399840	Evgeniya_565	6233422995	2023-10-03 17:19:54	2023-10-04 10:09:17	Евгения	\N	t	t
6100757342	\N	6233422995	2023-09-25 12:08:25	2023-09-26 07:04:49	Наталья	Двинянинова	t	t
1834270963	msuljan	6233422995	2023-09-23 17:14:06	2023-09-26 06:50:39	Улжан	Нажимиддинова	t	t
5637914075	\N	6233422995	2023-09-22 12:47:59	2023-09-26 06:50:35	Nastya	\N	t	t
2035510639	Elebarin	6233422995	2023-09-23 11:04:39	2023-09-25 09:53:10	Елена	Баринова	t	t
1171760336	\N	6233422995	2023-09-21 17:28:08	2023-09-25 07:33:41	Елена	\N	t	t
461054493	Enot0512	6233422995	2023-09-23 09:50:15	2023-09-25 07:31:32	Анастасия	\N	t	t
337660452	AnastasiiaYo	6233422995	2023-09-23 07:49:17	2023-09-25 06:58:24	Anastasia	\N	t	t
858655111	nadiya_dsgn	6233422995	2023-09-23 05:54:58	2023-09-25 06:51:31	Nadi	Brand Designer	t	t
5276057707	\N	6233422995	2023-09-22 13:05:24	2023-09-23 11:54:38	Инна	\N	t	t
887466912	\N	6233422995	2023-09-22 12:20:53	2023-09-23 11:51:28	Natali	\N	t	t
720715721	\N	6233422995	2023-09-22 15:14:15	2023-09-23 11:21:07	Нара	\N	t	t
146529211	kroshka_sasha	6233422995	2023-09-22 16:45:38	2023-09-23 10:48:47	Kroshka	\N	t	t
783838816	i_am_nastyak	6233422995	2023-09-23 02:52:18	2023-09-23 08:28:46	nnastya	\N	t	t
1658702994	\N	6233422995	2023-09-22 17:07:47	2023-09-23 08:09:28	Анастасия	\N	t	t
966039711	Lalala_0997	6233422995	2023-09-22 12:50:38	2023-09-23 08:06:26	Даша	\N	t	t
5253180868	lenasavinatumoha	6233422995	2023-09-22 12:50:45	2023-09-23 07:59:36	Елена	Савина	t	t
1281851771	gekolga	6233422995	2023-09-22 17:01:58	2023-09-23 07:02:32	Гек	Ольга	t	t
1098213742	Natalysj	6233422995	2023-09-22 09:10:27	2023-09-22 16:44:14	Natalya	Lapina Kazakhstan	t	t
1710622167	\N	6233422995	2023-09-22 09:13:18	2023-09-22 13:26:48	Наталья	Исмайлова	t	t
505694541	vikanasonova670	6233422995	2023-09-22 09:23:32	2023-09-22 13:03:53	Виктория Насонова	\N	t	t
2047533900	\N	6233422995	2023-09-21 21:39:52	2023-09-22 12:18:52	Arina	Costin	t	t
5115155613	\N	6233422995	2023-09-22 10:57:58	2023-09-22 11:57:25	Анастасия	\N	t	t
763094167	Sholpan_19	6233422995	2023-09-22 10:49:37	2023-09-22 11:51:44	Шолпан	\N	t	t
1392598491	ozhogina_k	6233422995	2023-09-22 11:01:25	2023-09-22 11:50:51	Kristina	Ozhogina🕊️	t	t
622506338	alyacezanne	6233422995	2023-09-21 11:29:55	2023-09-22 11:02:49	alya	\N	t	t
1043705393	\N	6233422995	2023-09-21 16:04:38	2023-09-22 10:38:10	Ekaterina	\N	t	t
896444189	Valentina1201	6233422995	2023-09-22 09:16:14	2023-09-22 10:38:05	Валентина	Агаркова	t	t
1354176868	\N	6233422995	2023-09-22 07:44:30	2023-09-22 09:51:48	Мария	\N	t	t
870575492	Vsio_tolko_nachinaetsia	6233422995	2023-09-09 10:30:59	2023-09-22 09:51:31	Анастасия	\N	t	t
6308212196	\N	6233422995	2023-09-20 20:06:36	2023-09-22 09:46:46	😎	\N	t	t
1352686691	\N	6233422995	2023-09-21 17:32:30	2023-09-22 09:46:34	Константин🍀🔥	\N	t	t
5144895240	\N	6233422995	2023-09-21 17:33:09	2023-09-22 09:15:52	Саша	Мурыгина	t	t
1073815142	scteppe	6233422995	2023-09-21 03:52:52	2023-09-22 09:15:36	Aleksandra	\N	t	t
1122266052	malkaaani	6233422995	2023-09-21 06:12:14	2023-09-22 09:01:08	A	\N	t	t
1244855960	yana_raspot	6233422995	2023-09-19 16:22:46	2023-09-22 09:00:13	Яна	Распотехина	t	t
738980060	annnnnnqo	6233422995	2023-09-21 10:41:40	2023-09-22 08:57:59	Анна	\N	t	t
1018373516	GulnaraBB	6233422995	2023-09-21 17:32:29	2023-09-22 08:53:46	Gulnara BB	\N	t	t
1649369635	OlgaKuter	6233422995	2023-09-21 11:03:53	2023-09-22 08:15:12	Ольга	Ольга	t	t
490154988	alina_dazzle	6233422995	2023-09-20 11:33:19	2023-09-21 09:14:03	ALINA	\N	t	t
1295428462	yuliyapolyaninaphoto	6233422995	2023-09-20 18:10:49	2023-09-21 08:14:46	Yuliya	Polyanina	t	t
1147199591	smirno_nata	6233422995	2023-09-09 10:31:35	2023-09-21 07:52:31	Наталья	Дюмина/Смирнова	t	t
948070697	nast_a1	6233422995	2023-09-20 14:25:00	2023-09-21 04:16:05	Настя	\N	t	t
940917057	\N	6233422995	2023-09-20 10:25:07	2023-09-20 11:41:36	Олеся	\N	t	t
6047863585	\N	6233422995	2023-09-20 06:14:11	2023-09-20 08:50:01	Ирина	\N	t	t
6134179155	\N	6233422995	2023-09-20 06:41:23	2023-09-20 08:03:32	Алёна	\N	t	t
5874059047	sherimoonn	6233422995	2023-09-20 07:25:05	2023-09-20 07:50:39	sheri	\N	t	t
5187036652	PororoKrYtoi	6233422995	2023-09-17 14:22:38	2023-09-20 06:33:05	пороро❤	\N	t	t
483699242	Lashs_by_Olga	6233422995	2023-09-09 15:01:01	2023-09-20 06:08:18	Пан	Ольга	t	t
1178500634	NNASA_1	6233422995	2023-09-19 15:00:00	2023-09-20 05:56:03	NASA🫧	\N	t	t
398383897	kozzzzzlovaa	6233422995	2023-09-19 20:53:01	2023-09-20 05:55:57	🗿	\N	t	t
512176220	\N	6233422995	2023-09-19 16:33:18	2023-09-20 05:15:22	.	\N	t	t
966303042	margosha_aa	6233422995	2023-09-20 02:18:02	2023-09-20 05:08:52	Марго	\N	t	t
990289780	lzza18	6233422995	2023-09-19 13:05:29	2023-09-20 05:02:37	Elizaveta🧸	\N	t	t
842601143	ektpdefka	6233422995	2023-09-19 18:23:54	2023-09-19 18:45:57	Екатерина	\N	t	t
826099562	\N	6233422995	2023-09-19 17:41:42	2023-09-19 17:41:42	Голубоглазая	Людмилка	t	t
1804716630	\N	6233422995	2023-09-19 11:23:33	2023-09-19 12:08:10	Татьяна	Аникина	t	t
1472099366	yulia9822	6233422995	2023-09-18 18:46:20	2023-09-19 11:52:56	Юлия	\N	t	t
5796250961	\N	6233422995	2023-09-19 09:10:04	2023-09-19 10:57:37	Лиана	Ершова	t	t
997118877	\N	6233422995	2023-09-18 21:53:44	2023-09-19 10:15:07	Tania_lost	Tania_lost	t	t
1010489114	\N	6233422995	2023-09-18 16:20:03	2023-09-19 10:11:35	Решетина	Любовь	t	t
1999371361	hhhhhhiiiooopp	6233422995	2023-09-19 08:03:49	2023-09-19 10:03:29	гитлер	\N	t	t
2111850306	Alenraw	6233422995	2023-09-18 09:08:27	2023-09-19 08:59:30	Alena	\N	t	t
574940918	Suvorova_Marina_1973	6233422995	2023-09-19 05:37:05	2023-09-19 07:54:48	Marina	Suvorova	t	t
346366226	katerinakozvonina	6233422995	2023-09-18 07:40:55	2023-09-19 07:45:58	Katerina	\N	t	t
823092832	Daria12235	6233422995	2023-09-18 08:06:21	2023-09-19 07:20:07	Дария	\N	t	t
779678916	\N	6233422995	2023-09-12 12:45:19	2023-09-12 12:45:36	Екатерина	Калугина	t	t
1889280533	As1438	6233422995	2023-09-11 08:15:08	2023-09-11 09:32:27	Дарья	\N	t	t
5658871965	\N	6233422995	2023-09-10 10:08:04	2023-09-11 09:29:30	Нина	Вануйто	t	t
1071551691	kuryakova_v	6233422995	2023-09-09 11:19:51	2023-09-11 08:04:56	Вероника 🦉	\N	t	t
1000862635	iamrayanao	6233422995	2023-09-10 21:45:02	2023-09-11 08:04:53	Раиса	\N	t	t
1034278912	IV_Svetashova	6233422995	2023-09-10 19:28:29	2023-09-11 07:22:37	Ирина	\N	t	t
1902185017	\N	6233422995	2023-09-12 08:39:45	2023-09-12 09:43:51	Марина	Маруся	t	t
5066623197	Zavgar728	6233422995	2023-10-18 07:01:13.54711	2023-10-04 15:16:59	🥴	\N	t	t
1931643954	Anastasia480	6233422995	2023-09-11 20:11:02	2023-09-12 08:48:13	Анастасия	\N	t	t
5258747900	\N	6233422995	2023-09-11 15:40:50	2023-09-12 08:20:36	Екатерина	\N	t	t
742741810	tnsandra264	6233422995	2023-10-10 08:58:54	2023-10-14 08:53:23	Оля Шандер	\N	t	t
6233422995	sasha_tarolog	6317875729	2023-10-11 09:11:13	2023-10-11 09:11:13	Саша	\N	t	t
1352829330	Aksana7294	6233422995	2023-09-11 17:04:23	2023-09-12 08:19:45	Оксана	А	t	t
1218828581	Irichka_87	6233422995	2023-09-09 10:43:04	2023-10-13 17:58:58	ирина	\N	t	t
470888041	natallia_romashko	6233422995	2023-10-13 16:25:41	2023-10-13 17:51:00	Наталья	Ромашко	t	t
1817963022	anastasia_mirotvorceva	6233422995	2023-10-03 13:15:16	2023-10-13 14:24:29	Анастасия	Миротворцева/ Проработка рода и внутренней опоры	t	t
1023959625	ginkinav	6233422995	2023-10-03 17:23:19	2023-10-04 10:05:00	Veronika	\N	t	t
1749421820	\N	6233422995	2023-10-03 10:56:45	2023-10-04 09:56:59	ирина	\N	t	t
1267039944	ASa_alex	6233422995	2023-09-09 10:39:02	2023-10-03 19:17:53	Александра	\N	t	t
1298345860	mrsvromanovna	6233422995	2023-10-03 19:10:54	2023-10-03 19:10:54	Виктория	Романовна	t	t
1041242352	Marina0372477	6233422995	2023-09-10 20:25:31	2023-10-03 17:09:53	Марина	\N	t	t
1419196848	dinasarmanova	6233422995	2023-09-15 15:17:03	2023-09-18 15:25:56	Дина	\N	t	t
1413456378	NatalyaBelogorodseva	6233422995	2023-09-16 17:10:42	2023-09-18 10:22:16	Наталья	Белогородцева	t	t
407383544	shelldiii	6233422995	2023-09-17 11:05:47	2023-09-18 09:50:52	Diana	\N	t	t
1919125447	Nata_li_sem	6233422995	2023-09-18 07:26:22	2023-09-18 07:56:25	Наталья	\N	t	t
5809477542	\N	6233422995	2023-09-17 15:56:18	2023-09-18 07:00:47	Viola	\N	t	t
5273540453	UCIMsGK	6233422995	2023-09-14 08:52:40	2023-09-18 07:00:23	❤	\N	t	t
812775232	lerazabotina	6233422995	2023-09-16 08:20:27	2023-09-18 06:58:33	Валерия🧚🏻	\N	t	t
1484905960	yuulia1996	6233422995	2023-09-17 10:19:16	2023-09-18 06:27:40	Yulia	\N	t	t
508398076	Nalya_Elysium	6233422995	2023-09-15 04:05:48	2023-09-17 08:52:38	Nalya	Elysium	t	t
5391215590	OlesiaXg	6233422995	2023-09-15 16:49:33	2023-09-16 09:18:48	Олеся 🚩	\N	t	t
1201822015	RomanovnaV04	6233422995	2023-09-15 18:34:35	2023-09-16 09:17:24	Chr.Victory.R	\N	t	t
850327680	Angelina1811000	6233422995	2023-09-15 09:31:20	2023-09-16 06:10:34	Ангелина	\N	t	t
874176589	i_alenka	6233422995	2023-09-15 14:52:14	2023-09-15 17:01:08	Alenka	Tzukanova	t	t
5030351678	Kris_wf	6233422995	2023-09-15 14:03:33	2023-09-15 16:39:48	Кристюша🤍	\N	t	t
1089432352	franky9215	6233422995	2023-09-14 08:51:10	2023-09-15 16:25:43	Антон	\N	t	t
691748021	mkylva23	6233422995	2023-09-14 15:49:56	2023-09-15 16:10:58	Mkylv.a	\N	t	t
1264332805	\N	6233422995	2023-09-15 12:42:05	2023-09-15 16:00:37	Miss	Vaityuk	t	t
6342117504	\N	6233422995	2023-09-14 17:33:01	2023-09-15 15:39:18	Нина	\N	t	t
801585521	SNastya01	6233422995	2023-09-14 14:29:15	2023-09-15 13:21:12	Серебрякова Анастасия	\N	t	t
1250732375	marishakamneva	6233422995	2023-09-09 12:35:44	2023-09-12 08:04:56	Марина	Камнева	t	t
973588696	mishanya_nap	6233422995	2023-09-14 12:40:24	2023-09-15 06:32:22	Мишаня	\N	t	t
1230195508	m_Ars_A	6233422995	2023-09-14 08:35:59	2023-09-15 06:29:17	Анна	\N	t	t
701669588	\N	6233422995	2023-09-13 07:08:09	2023-09-15 06:26:49	Ольга	\N	t	t
483868503	Ya_dobray90	6233422995	2023-09-13 17:31:08	2023-09-14 18:15:29	Юляша	Добрянская	t	t
823212607	\N	6233422995	2023-09-13 14:55:21	2023-09-14 17:01:39	Анютка	\N	t	t
5673411952	\N	6233422995	2023-09-14 04:41:47	2023-09-14 16:42:52	Ирина	\N	t	t
1531145767	Laralove03	6233422995	2023-09-13 07:04:43	2023-09-14 14:16:02	Лариса	\N	t	t
5820537084	\N	6233422995	2023-09-14 11:53:15	2023-09-14 12:35:45	DimaK	\N	t	t
1069854242	Aleksis_ss	6233422995	2023-09-13 21:41:15	2023-09-14 12:14:21	Aleksis	\N	t	t
981861102	verka100	6233422995	2023-09-13 18:17:38	2023-09-14 12:14:02	Вероника	\N	t	t
1004402413	Dasha_05e	6233422995	2023-09-13 23:55:54	2023-09-14 12:13:43	elz_dashka✨	\N	t	t
431370544	garmih0gmail	6233422995	2023-09-14 08:31:33	2023-09-14 12:13:37	© м и х а и л ® г а р б а ™	\N	t	t
1526190119	neva_5no	6233422995	2023-09-13 18:35:51	2023-09-14 10:41:43	🥷🏽	\N	t	t
772678991	Alekssandri	6233422995	2023-09-09 15:09:12	2023-09-14 10:27:37	Александра	\N	t	t
717990117	marmeladka_86	6233422995	2023-09-14 08:03:31	2023-09-14 10:15:39	Marina	\N	t	t
5889890455	sk_nizzzh	6233422995	2023-09-13 14:37:20	2023-09-14 09:41:04	Sk_nizzzh	\N	t	t
1828814064	\N	6233422995	2023-09-13 14:36:06	2023-09-14 09:16:08	Marina	1990	t	t
1521267479	\N	6233422995	2023-09-12 10:34:43	2023-09-12 12:00:04	Ирина	\N	t	t
1751974705	\N	6233422995	2023-09-09 20:49:01	2023-09-12 11:45:21	Ксения	Обидина	t	t
714812624	\N	6233422995	2023-09-10 17:54:45	2023-09-12 07:55:39	Света	\N	t	t
1047821978	arishkinsv	6233422995	2023-09-09 11:54:46	2023-09-11 18:11:45	Arina	\N	t	t
1181757577	fgvhrkf	6233422995	2023-09-11 14:42:21	2023-09-11 16:45:51	полинка	\N	t	t
5084966532	\N	6233422995	2023-09-09 12:46:34	2023-09-11 15:28:00	Аndrei Leshkovich	\N	t	t
5206500015	\N	6233422995	2023-09-10 17:42:59	2023-09-11 15:06:43	Полина	Макарова	t	t
1329841988	\N	6233422995	2023-09-11 11:24:38	2023-09-11 14:28:15	Мария	Ганжа	t	t
256644235	KaterinaSabutina	6233422995	2023-09-09 10:28:49	2023-09-11 12:43:48	Екатерина	\N	t	t
392335063	lefederik	6233422995	2023-09-07 13:07:51	2023-09-11 12:17:15	L	S	t	t
5201079841	afro_zoya	6233422995	2023-09-10 18:45:57	2023-09-11 12:09:07	Зоя	Никифорова	t	t
1193657414	KseniaChaschina	6233422995	2023-09-09 12:36:46	2023-09-11 16:33:27	Ксения	Чащина	t	t
651754530	Yana_Derko	6233422995	2023-09-10 16:42:41	2023-09-11 12:00:04	Яна	Дерко	t	t
897040622	Aigulchik_makhmurova	6233422995	2023-09-11 10:02:45	2023-09-11 10:04:15	Айгуль ➡️ УДАЛËНКА С НУЛЯ	\N	t	t
2019852200	svetlanamelnikova1976	6233422995	2023-09-11 03:54:57	2023-09-11 08:04:46	Светлана	Мельникова	t	t
994187813	Zemkas1	6233422995	2023-09-10 18:54:38	2023-09-11 07:59:26	Zemka	_	t	t
1569304208	\N	6233422995	2023-09-10 17:04:00	2023-09-11 07:35:13	🍀Марина	Найдёнова🍀	t	t
5737650273	\N	6233422995	2023-09-10 13:48:43	2023-09-11 07:23:50	Светлана	Марцинкевич	t	t
1099809702	Viksii_ponomareva	6233422995	2023-09-10 15:50:04	2023-09-11 07:23:41	Виктория Наставник бьюти экспертов	\N	t	t
5927039816	\N	6233422995	2023-09-07 14:51:25	2023-09-11 07:12:43	Da Da	Prekrasnaye	t	t
5038988658	\N	6233422995	2023-09-10 17:00:00	2023-09-11 07:11:50	Евгения	\N	t	t
5268238623	\N	6233422995	2023-09-10 13:43:54	2023-09-11 06:51:34	Aikys	Oorjak	t	t
1992352566	Elena_Levalent	6233422995	2023-09-10 16:14:59	2023-09-11 06:42:06	Елена	Levalent	t	t
592434842	toma_dobro	6233422995	2023-09-09 11:31:53	2023-09-10 20:44:14	Тома	Добровольская	t	t
888196461	Maria2596	6317875729	2023-10-18 06:34:26.39686	2023-10-13 15:52:10	Машуня🌷	\N	t	t
6382051968	kukijoy93	6317875729	2023-10-18 07:16:15.281681	2023-10-14 13:40:55	Foxy	\N	t	t
1017035235	noaklida	6317875729	2023-10-17 08:52:40.261319	2023-10-13 15:16:04	FROM	BOT	t	t
833481629	Aallessya	6233422995	2023-10-18 12:08:37.939494	2023-10-13 18:36:42	Алеся	\N	t	t
1888683231	\N	6233422995	2023-09-09 10:50:03	2023-09-10 19:15:21	Кристина	\N	t	t
943492879	anjutasedova	6233422995	2023-09-10 13:29:41	2023-09-10 19:10:41	Анюта	Куz	t	t
1458883343	nasstya1808	6233422995	2023-09-10 08:35:30	2023-09-10 17:11:58	.	\N	t	t
1011332800	mara_ro	6233422995	2023-09-09 13:24:19	2023-09-10 16:45:55	Марианна	Рошка	t	t
462555694	\N	6233422995	2023-09-10 13:48:47	2023-09-10 15:39:16	Галия	Проничева	t	t
1027427795	gmyrakk	6233422995	2023-09-09 19:07:48	2023-09-10 15:30:27	Ulyana	\N	t	t
1194866754	tifani_li	6233422995	2023-09-10 15:19:18	2023-09-10 15:22:00	Ramilya	Saberzyanova	t	t
883120635	nadezhda_93	6233422995	2023-09-09 19:47:22	2023-09-10 13:36:12	Надежда	Боева	t	t
521674254	Dariana_1	6233422995	2023-09-10 09:04:08	2023-09-10 13:15:03	Дариана	\N	t	t
977227483	saint_alina	6233422995	2023-09-09 10:49:16	2023-09-10 12:57:17	Алина	\N	t	t
5676600403	\N	6233422995	2023-09-10 04:41:33	2023-09-10 12:48:51	Илона	\N	t	t
794536412	vitalinaadelina	6233422995	2023-09-10 10:57:39	2023-09-10 12:48:38	Аделина	Васильева	t	t
1180015355	\N	6233422995	2023-09-10 01:00:21	2023-09-10 12:41:58	Nastya	\N	t	t
710434735	Marusya27091985	6233422995	2023-09-10 00:29:50	2023-09-10 12:41:33	Мария Войтенко	\N	t	t
873268020	ges31	6233422995	2023-09-09 18:29:43	2023-09-10 12:27:16	Лена Глушкова	\N	t	t
1836145115	MayaPfayf	6233422995	2023-09-09 18:27:53	2023-09-10 12:24:43	Майя	\N	t	t
1259285060	\N	6233422995	2023-09-08 14:23:27	2023-09-10 12:09:19	Владислав	Мичковский	t	t
5493906446	\N	6233422995	2023-09-09 20:36:46	2023-09-10 12:04:44	Анна	Ананьева	t	t
2107780665	anyanna20	6233422995	2023-09-09 11:13:33	2023-09-10 12:04:22	anna	\N	t	t
283211844	\N	6233422995	2023-09-09 19:41:28	2023-09-10 11:56:47	Ангелина	\N	t	t
1115545583	asya_pshen	6233422995	2023-09-10 09:15:52	2023-09-10 11:51:23	Ася Пшеничникова	\N	t	t
5703923391	\N	6233422995	2023-09-09 16:50:43	2023-09-10 11:45:21	M	\N	t	t
1233726123	Ewussja	6233422995	2023-09-09 12:30:32	2023-09-10 11:38:16	Евгения	\N	t	t
857504529	\N	6233422995	2023-09-09 10:50:32	2023-09-10 11:38:05	Александра	Попова	t	t
533869287	AnnySwe	6233422995	2023-09-09 12:42:51	2023-09-10 11:38:01	Anny	\N	t	t
538697806	SveLuna	6233422995	2023-09-09 11:05:02	2023-09-10 11:29:34	Светлана	Лана	t	t
1173924792	\N	6233422995	2023-09-09 17:26:51	2023-09-10 11:26:37	Ольга Хмао	\N	t	t
540880774	KN_7u	6233422995	2023-09-09 18:49:22	2023-09-10 11:20:01	Natalia Vladimirovna	\N	t	t
1453590297	Alex_2388	6233422995	2023-09-10 05:43:59	2023-09-10 11:10:18	а	\N	t	t
1240574817	v7v3veron	6233422995	2023-09-09 17:36:58	2023-09-10 11:00:17	Елена Темерева	\N	t	t
1427389510	\N	6233422995	2023-09-09 18:19:17	2023-09-10 10:57:38	YULIYA	SHAVRINA	t	t
5134304606	\N	6233422995	2023-09-10 04:49:41	2023-09-10 10:55:29	Елена	Пикулева	t	t
1741537444	karinwqxs	6233422995	2023-09-09 15:06:05	2023-09-10 10:48:02	тётя Карин	\N	t	t
1387140916	\N	6233422995	2023-09-09 20:48:48	2023-09-10 10:44:17	Ксения	\N	t	t
1304511954	alinazuevva	6233422995	2023-09-09 19:33:38	2023-09-10 10:39:22	Алина	\N	t	t
312708481	elizabeth_khabarova	6233422995	2023-09-10 07:29:15	2023-09-10 08:50:39	Елизавета	Хабарова	t	t
5323206927	\N	6233422995	2023-09-09 11:02:39	2023-09-10 08:25:06	Natali	Ivanova	t	t
965946395	\N	6233422995	2023-09-09 18:59:04	2023-09-10 08:21:34	Лилия	\N	t	t
531046935	\N	6233422995	2023-09-09 10:43:36	2023-09-10 08:12:39	Кунджешвари д.д (Зоя)	\N	t	t
763055260	nikonova_katerina	6233422995	2023-09-09 10:37:43	2023-09-10 07:46:48	Никонова Екатерина Ивановна	\N	t	t
307785925	\N	6233422995	2023-09-09 18:38:23	2023-09-10 07:41:27	Елена	\N	t	t
386789300	NastyaBoichenko	6233422995	2023-09-09 11:42:01	2023-09-10 07:13:03	Anastasia	\N	t	t
607421118	dushu_greyaa	6233422995	2023-09-09 10:48:37	2023-09-09 21:37:32	✨	\N	t	t
1177364911	OLGA779803	6233422995	2023-09-09 18:28:53	2023-09-09 18:40:53	Ольга	\N	t	t
254598562	luckylyalya	6233422995	2023-09-08 14:18:28	2023-09-09 18:13:43	Lyalya	\N	t	t
6274273034	Albira27	6233422995	2023-09-09 13:53:33	2023-09-09 16:39:18	Альбира	Юсупова	t	t
727638208	yulil_ive	6233422995	2023-09-09 11:26:02	2023-09-09 16:36:38	yuli.l_ive	\N	t	t
1270549466	BLACK_MOMMY1998	6233422995	2023-09-09 11:26:51	2023-09-09 16:32:08	Малиновый Чаёк	\N	t	t
1233507567	marina_nihaeva	6233422995	2023-09-09 10:32:54	2023-09-09 16:07:58	Марина	Нихаева	t	t
530254284	Sokolova88	6233422995	2023-09-09 11:11:18	2023-09-09 16:07:25	Ирина	Соколова	t	t
675588621	\N	6233422995	2023-09-09 10:41:53	2023-09-09 16:04:34	ek_lerka	\N	t	t
5573231239	ALaraLiv	6233422995	2023-09-09 14:41:03	2023-09-09 15:50:51	Туня❤️	\N	t	t
367754574	jeniaiv	6233422995	2023-09-09 14:02:00	2023-09-09 15:39:53	Женя	\N	t	t
1778820847	\N	6233422995	2023-09-09 12:18:46	2023-09-09 15:35:56	Анна	\N	t	t
1179010142	Wellnasa8	6233422995	2023-09-09 10:39:49	2023-09-09 15:17:01	Настасья	\N	t	t
688592730	avvvvw	6233422995	2023-09-09 10:36:56	2023-09-09 15:13:54	Анастасия	\N	t	t
5928325218	\N	6233422995	2023-09-09 10:39:03	2023-09-09 15:13:38	Элина	\N	t	t
6316810005	\N	6233422995	2023-09-09 12:40:51	2023-09-09 15:11:45	Елена	\N	t	t
5822917042	Marat_Gataulin	6233422995	2023-09-09 11:34:32	2023-09-09 15:07:39	Марат	Гатауллин	t	t
961607730	\N	6233422995	2023-09-09 10:54:38	2023-09-09 15:05:52	м	\N	t	t
1187523473	KaterinaRub3	6233422995	2023-09-09 11:58:42	2023-09-09 15:04:22	Катя	Рубцова	t	t
614387076	yu_l_i_023	6233422995	2023-09-09 10:32:10	2023-09-09 15:03:07	Юлия	\N	t	t
872873872	Yyyuliyaaaaa	6233422995	2023-09-09 11:44:15	2023-09-09 14:59:46	Юлия	\N	t	t
1213796585	l_l_tata_l_l	6233422995	2023-09-09 10:32:02	2023-09-09 14:55:57	Тата	\N	t	t
2042307300	\N	6233422995	2023-09-09 10:38:15	2023-09-09 14:55:30	Мария	М	t	t
1300910716	\N	6233422995	2023-09-09 12:11:44	2023-09-09 14:44:09	Lyaisan	S.	t	t
1358674224	kilkaismorya	6233422995	2023-09-09 10:31:32	2023-09-09 14:40:23	ʕ •ᴥ• ʔ	\N	t	t
943178802	wfgyl	6233422995	2023-09-09 11:09:33	2023-09-09 14:38:02	Рената❤️	\N	t	t
5386487286	ksalygima2003	6233422995	2023-09-09 13:00:14	2023-09-09 14:36:21	Kristina	Salygina	t	t
1601370427	Byakugan_No_Hime21	6233422995	2023-09-09 11:12:13	2023-09-09 14:32:54	Lily	Evans	t	t
1496801050	\N	6233422995	2023-09-09 11:05:26	2023-09-09 14:31:21	Любовь	\N	t	t
1494393971	ZabelnikovaOlga	6233422995	2023-09-09 10:45:10	2023-09-09 14:30:40	Забельникова	Ольга	t	t
900440975	goodmo24	6233422995	2023-09-09 10:54:02	2023-09-09 14:26:57	💋	\N	t	t
1681393382	\N	6233422995	2023-09-09 11:00:05	2023-09-09 14:26:44	Мёльман	\N	t	t
1105155618	\N	6233422995	2023-09-09 10:31:59	2023-09-09 14:23:28	Anastasia	\N	t	t
2075825009	\N	6233422995	2023-09-09 10:52:53	2023-09-09 14:13:47	Оленька	\N	t	t
691486857	Adelina_Gumerovaa	6233422995	2023-09-09 11:18:51	2023-09-09 14:12:48	Аделина	\N	t	t
578159049	novoselova_a	6233422995	2023-09-09 10:53:21	2023-09-09 14:12:02	Анастасия	\N	t	t
627986182	Yabneshka94	6233422995	2023-09-09 12:27:08	2023-09-09 14:08:37	Ябне	Вэнго	t	t
5209315076	\N	6233422995	2023-09-09 12:13:14	2023-09-09 14:07:27	Татьяна	\N	t	t
849554641	Anna_Panina_13_08	6233422995	2023-09-09 10:47:06	2023-09-09 14:06:49	Анна	\N	t	t
1470688624	katriinaks	6233422995	2023-09-09 10:31:17	2023-09-09 14:02:53	❤️	\N	t	t
1220232545	\N	6233422995	2023-09-09 10:30:41	2023-09-09 13:59:54	🌸	\N	t	t
5575116568	markssunn	6233422995	2023-09-09 10:31:10	2023-09-09 13:55:41	Екатерина	\N	t	t
5174892840	\N	6233422995	2023-09-09 10:38:43	2023-09-09 13:51:01	Настя	\N	t	t
880886265	noskovalisa	6233422995	2023-09-09 11:21:07	2023-09-09 13:48:54	Лиза	\N	t	t
721147394	mamashasha1	6233422995	2023-09-09 10:30:38	2023-09-09 13:21:33	Candy_blonde	\N	t	t
5120195127	\N	6233422995	2023-09-09 11:38:37	2023-09-09 13:16:18	Анастасия	\N	t	t
1212439833	MarySamoil	6233422995	2023-09-09 11:38:31	2023-09-09 13:16:11	Мария	Самойлова	t	t
1858400798	TItelegramma	6233422995	2023-09-09 11:01:10	2023-09-09 13:10:17	Татьяна	\N	t	t
693522102	\N	6233422995	2023-09-09 10:31:51	2023-09-09 13:01:35	Виктория	\N	t	t
901005553	karriqw	6233422995	2023-09-09 10:37:19	2023-09-09 13:00:39	karriqw	\N	t	t
671921604	aaimoonn	6233422995	2023-09-09 10:30:42	2023-09-09 13:00:24	Айгуль Авхадиева	\N	t	t
868040385	ms_wedecor	6233422995	2023-09-09 03:13:14	2023-09-09 12:55:30	Марина	Самофалова	t	t
2139074529	Kristina_Ladan	6233422995	2023-09-09 10:31:43	2023-09-09 12:53:11	Кристина	\N	t	t
5135669765	olalex	6233422995	2023-09-09 10:36:36	2023-09-09 12:21:53	Ol'ga	\N	t	t
2131605760	Evgenievna_20_02	6233422995	2023-09-09 10:33:53	2023-09-09 12:04:08	IRINA	\N	t	t
2118023019	\N	6233422995	2023-09-09 10:29:50	2023-09-09 11:53:35	Екатерина	\N	t	t
1310839419	\N	6233422995	2023-09-09 10:33:35	2023-09-09 11:40:48	Олеся	\N	t	t
338973067	tonicanm	6233422995	2023-09-09 10:33:14	2023-09-09 11:40:32	Наташа	\N	t	t
5050250941	\N	6233422995	2023-09-09 10:31:39	2023-09-09 11:37:36	Ксения	\N	t	t
866775197	mabreoo	6233422995	2023-09-09 10:30:06	2023-09-09 11:35:12	мария 🎀	\N	t	t
447085905	missfangy	6233422995	2023-09-09 10:32:51	2023-09-09 11:22:38	Евгения🦋	\N	t	t
1225593646	\N	6233422995	2023-09-09 10:32:51	2023-09-09 11:19:47	Ксеня	\N	t	t
5068352268	\N	6233422995	2023-09-08 13:59:39	2023-09-09 10:04:59	Елена	\N	t	t
5164583272	nastasiaaaa_vs	6233422995	2023-09-08 08:38:05	2023-09-09 09:43:34	Anastasia	\N	t	t
526289322	\N	6233422995	2023-09-09 07:35:45	2023-09-09 08:35:14	Лия	\N	t	t
5071462366	\N	6233422995	2023-09-07 13:45:08	2023-09-09 08:03:22	Гульназка	Ривгатовна	t	t
5122983360	albonashved	6233422995	2023-09-08 13:56:52	2023-09-09 08:03:03	Альбина	Швед	t	t
600518048	white_phosphorus88	6233422995	2023-09-08 05:48:10	2023-09-09 08:03:01	Aljana	Mackedonskaya	t	t
5589283363	Anna_R1974	6233422995	2023-09-08 14:03:26	2023-09-09 08:02:54	10556	\N	t	t
859893655	mvm_232	6233422995	2023-09-07 16:03:40	2023-09-09 07:34:07	Privereda	🌙	t	t
1066547141	\N	6233422995	2023-09-07 07:18:47	2023-09-09 05:49:41	Алина	Хисамова	t	t
8880057	Karina_samadova	6233422995	2023-09-08 14:01:00	2023-09-09 05:37:29	Karina	\N	t	t
1372855906	\N	6233422995	2023-09-08 14:26:30	2023-09-09 05:37:01	дарья	\N	t	t
435854873	wooolfann	6233422995	2023-09-07 16:11:23	2023-09-08 09:38:19	Ann	Volkova	t	t
1495556360	\N	6233422995	2023-09-07 16:27:14	2023-09-07 17:20:36	Лилия	\N	t	t
1511888416	\N	6233422995	2023-09-07 16:18:48	2023-09-07 16:31:58	Алия	Брагина	t	t
453730270	\N	6233422995	2023-09-07 14:51:16	2023-09-07 15:39:04	Лилия	Садыкова	t	t
1346221968	nastasya_korakina	6233422995	2023-09-07 12:42:23	2023-09-07 15:38:47	Анастасия	\N	t	t
888469624	li_gali	6233422995	2023-09-07 14:22:52	2023-09-07 15:10:47	Лиля	\N	t	t
658787136	krmvdi	6233422995	2023-09-07 13:34:51	2023-09-07 13:53:04	krmvd	\N	t	t
44171888	alina116	6233422995	2023-09-07 12:43:24	2023-09-07 13:44:30	Алина	Фахрутдинова	t	t
1236164962	\N	6233422995	2023-09-07 12:38:25	2023-09-07 13:06:04	лилия	лилия	t	t
863276168	YarinkaCh	6233422995	2023-09-07 05:11:45	2023-09-07 12:56:13	Ирина	Чугреева	t	t
760785873	\N	6233422995	2023-09-07 12:34:50	2023-09-07 12:39:58	Виктория	\N	t	t
1131491473	\N	6233422995	2023-09-07 12:14:07	2023-09-07 12:21:58	Islamova	Liliya	t	t
979721747	Irinafales	6233422995	2023-09-07 10:34:42	2023-09-07 11:04:53	ирина	\N	t	t
1221858411	\N	6233422995	2023-09-07 08:48:58	2023-09-07 10:03:44	Лидия	\N	t	t
1046961205	Agarwaen_666	6233422995	2023-09-07 09:26:43	2023-09-07 09:29:16	Кира	Аккерман	t	t
868867555	\N	6233422995	2023-09-07 08:23:47	2023-09-07 09:00:54	Кристина	Веденина	t	t
784648046	\N	6233422995	2023-09-07 08:48:54	2023-09-07 08:59:06	Мелитина🌸	\N	t	t
828830295	\N	6233422995	2023-09-07 05:25:25	2023-09-07 08:30:27	Наталья	Кудашова	t	t
420875838	Queengmf	6233422995	2023-09-07 07:37:49	2023-09-07 08:21:38	Гульназ	\N	t	t
1842975300	di_s02	6233422995	2023-09-07 07:06:57	2023-09-07 07:27:19	Динарочка	Мияссарова	t	t
5590533213	\N	6233422995	2023-09-07 05:45:06	2023-09-07 07:26:16	Екатерина	Терентьева	t	t
1105055710	Arina_Guseva	6233422995	2023-09-07 07:14:25	2023-09-07 07:15:47	Арина	Гусева	t	t
1207647645	baf2412	6233422995	2023-09-07 07:09:40	2023-09-07 07:13:46	Adelina	\N	t	t
1026219752	\N	6233422995	2023-09-07 05:21:45	2023-09-07 06:50:12	Ирина	\N	t	t
1121482710	VictoriyaKorol	6233422995	2023-09-07 06:01:52	2023-09-07 06:19:37	Король Виктория	\N	t	t
6209683393	Kywar	6233422995	2023-10-16 09:04:44.876765	2023-10-14 15:04:48	Татьяна	Чумаева	t	t
1279375001	\N	999	2023-10-17 08:52:51.867092	2023-10-16 14:12:51.542817	FROM	BOT	t	t
624054681	VolchenkoE	999	2023-10-17 08:52:52.733244	2023-10-17 04:28:40.402671	FROM	BOT	t	t
850737337	\N	6317875729	2023-10-17 08:52:50.90047	2023-10-16 07:37:16.670127	FROM	BOT	t	t
503893598	Brelgina_Elena	6233422995	2023-10-16 08:40:48.201417	2023-10-13 22:10:56	Елена	\N	t	t
6451915886	\N	999	2023-10-17 08:52:48.444584	2023-10-16 07:21:33.283018	FROM	BOT	f	f
2064198395	\N	999	2023-10-17 08:52:50.068707	2023-10-16 07:32:58.638781	FROM	BOT	t	f
1990574001	\N	999	2023-10-17 08:52:53.583773	2023-10-17 08:13:56.658332	FROM	BOT	f	t
1407537356	Anna_osteoNV	6317875729	2023-10-17 08:52:31.012533	2023-10-13 08:27:20	FROM	BOT	t	t
1112720543	avokadiha	6233422995	2023-10-17 07:18:42.222969	2023-10-16 12:56:53.827379	Лаврова	Евгения	t	t
5140288052	matyushenko89	6233422995	2023-10-17 07:15:51.661998	2023-10-13 09:17:07	Алина	Матюшенко	t	t
895872844	sanfit	999	2023-10-18 14:26:38.900875	2023-10-17 08:52:37.037435	FROM	BOT	f	f
875044476	belofflab	6317875729	2023-10-19 01:02:42.555869	2023-10-17 05:41:16.28367	FROM	BOT	t	t
6095443048	\N	999	2023-10-17 08:52:31.80737	2023-10-17 08:52:31.807376	FROM	BOT	f	f
950192332	Olga_karelina_u	999	2023-10-17 08:52:34.550881	2023-10-17 08:52:34.55089	FROM	BOT	f	f
391072383	dmitrybevz	999	2023-10-17 08:52:35.320533	2023-10-17 08:52:35.320539	FROM	BOT	f	f
5556813612	\N	999	2023-10-17 08:52:36.175493	2023-10-17 08:52:36.175504	FROM	BOT	f	f
1063092820	ssyy222ggsj	999	2023-10-17 08:52:37.85514	2023-10-17 08:52:37.855149	FROM	BOT	f	f
6119365399	\N	999	2023-10-17 08:52:38.744955	2023-10-17 08:52:38.744962	FROM	BOT	f	f
1805208500	Swetlana190876	999	2023-10-17 08:52:39.491427	2023-10-17 08:52:39.491432	FROM	BOT	f	f
515041464	ulyana_mazur	999	2023-10-17 08:52:42.984252	2023-10-14 13:15:39.974515	FROM	BOT	t	f
774617141	\N	999	2023-10-17 08:52:49.25012	2023-10-16 07:24:50.083551	FROM	BOT	t	t
1684739130	taskmanagment	6233422995	2023-10-18 19:43:52.394337	2023-09-29 18:54:28	FROM	BOT	t	t
1333838895	\N	999	2023-10-17 08:52:44.056259	2023-10-17 08:52:44.056285	FROM	BOT	f	f
5152114717	\N	999	2023-10-17 08:52:47.553404	2023-10-16 07:19:47.274332	FROM	BOT	t	t
1991098419	alina_altaftinovna	999	2023-10-17 13:54:11.683059	2023-10-17 13:53:59.746351	FROM	BOT	f	t
6278394548	\N	999	2023-10-17 14:09:51.755912	2023-10-17 14:09:17.051975	FROM	BOT	f	t
1378992448	\N	999	2023-10-17 14:33:04.626538	2023-10-17 14:33:01.948717	FROM	BOT	f	t
5329826570	\N	999	2023-10-17 16:09:54.234391	2023-10-17 16:08:32.687974	FROM	BOT	f	f
1169294375	yluaz4	6317875729	2023-10-18 07:08:42.540993	2023-10-17 13:52:30.870208	ylua	\N	t	t
1308984203	\N	6233422995	2023-10-18 07:15:24.683883	2023-10-17 15:12:41.306862	Ma	riya	t	t
1432544720	\N	999	2023-10-18 07:38:17.192169	2023-10-18 07:38:09.809501	FROM	BOT	f	t
2033457967	\N	6317875729	2023-10-18 09:41:02.388949	2023-10-17 15:57:10.289995	Натали	\N	t	t
5595236777	Marseeline	6233422995	2023-10-18 10:58:19.24511	2023-10-18 10:58:19.245118	Merseline	\N	f	f
1032193646	Ksiusha_2313	6233422995	2023-10-18 13:31:57.538766	2023-10-04 15:15:50	Ксюша	\N	t	t
6639144962	meguava	9999	2023-10-19 02:03:09.309841	2023-10-19 02:03:03.958261	FROM	BOT	f	f
\.


--
-- Data for Name: workers; Type: TABLE DATA; Schema: public; Owner: tantuser
--

COPY public.workers (id, name, api_id, api_hash, proxy, is_active, created_at, api_port, amount, username) FROM stdin;
999	Бот Александры	0	_	1	f	2023-10-10 09:06:19.018559	9130	\N	\N
6317875729	Александра 2 (taro2_sashA)	29858728	d9b19aaaccf3aa961d402f86ffe361c6	2	t	2023-10-12 15:59:04.533758	9130	0.00	taro2_sashA
6233422995	Александра 1 (sasha_tarolog)	27307563	1a18b835e5359efc82c56875cf9ba4f3	1	t	2023-10-12 16:00:11.653131	9130	0.00	sasha_tarolog
9999	Бот Виктории	0	0	3	f	2023-10-18 08:57:56.257119	\N	0.00	\N
\.


--
-- Name: proxies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tantuser
--

SELECT pg_catalog.setval('public.proxies_id_seq', 3, true);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tantuser
--

SELECT pg_catalog.setval('public.transactions_id_seq', 1, false);


--
-- Name: transitions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tantuser
--

SELECT pg_catalog.setval('public.transitions_id_seq', 492, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tantuser
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: workers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tantuser
--

SELECT pg_catalog.setval('public.workers_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: proxies proxies_pkey; Type: CONSTRAINT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.proxies
    ADD CONSTRAINT proxies_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: transitions transitions_pkey; Type: CONSTRAINT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.transitions
    ADD CONSTRAINT transitions_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: workers workers_pkey; Type: CONSTRAINT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.workers
    ADD CONSTRAINT workers_pkey PRIMARY KEY (id);


--
-- Name: transactions fk_transactions_workers_id_worker; Type: FK CONSTRAINT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT fk_transactions_workers_id_worker FOREIGN KEY (worker) REFERENCES public.workers(id);


--
-- Name: users fk_users_workers_id_worker; Type: FK CONSTRAINT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_workers_id_worker FOREIGN KEY (worker) REFERENCES public.workers(id);


--
-- Name: workers fk_workers_proxies_id_proxy; Type: FK CONSTRAINT; Schema: public; Owner: tantuser
--

ALTER TABLE ONLY public.workers
    ADD CONSTRAINT fk_workers_proxies_id_proxy FOREIGN KEY (proxy) REFERENCES public.proxies(id);


--
-- PostgreSQL database dump complete
--

