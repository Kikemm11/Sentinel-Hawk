--
-- PostgreSQL database dump
--

-- Dumped from database version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)

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
-- Name: currency; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.currency (
    currency_id integer NOT NULL,
    name character varying NOT NULL,
    code character varying(10) NOT NULL
);


ALTER TABLE public.currency OWNER TO sentinel;

--
-- Name: currency_currency_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.currency_currency_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.currency_currency_id_seq OWNER TO sentinel;

--
-- Name: currency_currency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.currency_currency_id_seq OWNED BY public.currency.currency_id;


--
-- Name: deteccion; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.deteccion (
    id integer NOT NULL,
    tipo_vehiculo character varying,
    hora time without time zone,
    fecha date
);


ALTER TABLE public.deteccion OWNER TO sentinel;

--
-- Name: deteccion_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.deteccion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.deteccion_id_seq OWNER TO sentinel;

--
-- Name: deteccion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.deteccion_id_seq OWNED BY public.deteccion.id;


--
-- Name: deteccion_status; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.deteccion_status (
    id integer NOT NULL,
    status boolean
);


ALTER TABLE public.deteccion_status OWNER TO sentinel;

--
-- Name: deteccion_status_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.deteccion_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.deteccion_status_id_seq OWNER TO sentinel;

--
-- Name: deteccion_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.deteccion_status_id_seq OWNED BY public.deteccion_status.id;


--
-- Name: payment; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.payment (
    payment_id integer NOT NULL,
    ticket_id smallint NOT NULL,
    charge real NOT NULL,
    currency_id smallint NOT NULL,
    payment_method_id smallint NOT NULL,
    exchange_rate real NOT NULL,
    local_currency real NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT valid_charge CHECK ((charge > (0.0)::double precision))
);


ALTER TABLE public.payment OWNER TO sentinel;

--
-- Name: payment_method; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.payment_method (
    payment_method_id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.payment_method OWNER TO sentinel;

--
-- Name: payment_method_payment_method_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.payment_method_payment_method_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_method_payment_method_id_seq OWNER TO sentinel;

--
-- Name: payment_method_payment_method_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.payment_method_payment_method_id_seq OWNED BY public.payment_method.payment_method_id;


--
-- Name: payment_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.payment_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_payment_id_seq OWNER TO sentinel;

--
-- Name: payment_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.payment_payment_id_seq OWNED BY public.payment.payment_id;


--
-- Name: status; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.status (
    status_id integer NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE public.status OWNER TO sentinel;

--
-- Name: status_status_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.status_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.status_status_id_seq OWNER TO sentinel;

--
-- Name: status_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.status_status_id_seq OWNED BY public.status.status_id;


--
-- Name: ticket; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.ticket (
    ticket_id integer NOT NULL,
    vehicle_type_id smallint NOT NULL,
    charge real NOT NULL,
    status_id smallint NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_charge CHECK ((charge > (0.0)::double precision))
);


ALTER TABLE public.ticket OWNER TO sentinel;

--
-- Name: ticket_ticket_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.ticket_ticket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ticket_ticket_id_seq OWNER TO sentinel;

--
-- Name: ticket_ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.ticket_ticket_id_seq OWNED BY public.ticket.ticket_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    permisology character varying(50) NOT NULL
);


ALTER TABLE public.users OWNER TO sentinel;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO sentinel;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: vehicle_type; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.vehicle_type (
    vehicle_type_id integer NOT NULL,
    name character varying(25) NOT NULL,
    charge real NOT NULL,
    CONSTRAINT valid_charge CHECK ((charge > (0.0)::double precision))
);


ALTER TABLE public.vehicle_type OWNER TO sentinel;

--
-- Name: vehicle_type_vehicle_type_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.vehicle_type_vehicle_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vehicle_type_vehicle_type_id_seq OWNER TO sentinel;

--
-- Name: vehicle_type_vehicle_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.vehicle_type_vehicle_type_id_seq OWNED BY public.vehicle_type.vehicle_type_id;


--
-- Name: currency currency_id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.currency ALTER COLUMN currency_id SET DEFAULT nextval('public.currency_currency_id_seq'::regclass);


--
-- Name: deteccion id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.deteccion ALTER COLUMN id SET DEFAULT nextval('public.deteccion_id_seq'::regclass);


--
-- Name: deteccion_status id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.deteccion_status ALTER COLUMN id SET DEFAULT nextval('public.deteccion_status_id_seq'::regclass);


--
-- Name: payment payment_id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.payment ALTER COLUMN payment_id SET DEFAULT nextval('public.payment_payment_id_seq'::regclass);


--
-- Name: payment_method payment_method_id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.payment_method ALTER COLUMN payment_method_id SET DEFAULT nextval('public.payment_method_payment_method_id_seq'::regclass);


--
-- Name: status status_id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.status ALTER COLUMN status_id SET DEFAULT nextval('public.status_status_id_seq'::regclass);


--
-- Name: ticket ticket_id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.ticket ALTER COLUMN ticket_id SET DEFAULT nextval('public.ticket_ticket_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: vehicle_type vehicle_type_id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.vehicle_type ALTER COLUMN vehicle_type_id SET DEFAULT nextval('public.vehicle_type_vehicle_type_id_seq'::regclass);


--
-- Data for Name: currency; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.currency (currency_id, name, code) FROM stdin;
1	Dolares	USD
2	Bolivares	Bs
\.


--
-- Data for Name: deteccion; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.deteccion (id, tipo_vehiculo, hora, fecha) FROM stdin;
\.


--
-- Data for Name: deteccion_status; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.deteccion_status (id, status) FROM stdin;
1	f
\.


--
-- Data for Name: payment; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.payment (payment_id, ticket_id, charge, currency_id, payment_method_id, exchange_rate, local_currency, created_at) FROM stdin;
1	708	100	1	2	36.35	3635	2024-04-22 19:45:32.819918
2	757	100	1	2	36.43	3643	2024-04-26 12:35:31.977239
3	756	100	1	1	36.43	3643	2024-04-26 12:35:38.528586
4	755	100	2	1	36.43	3643	2024-04-26 12:35:43.862816
5	754	100	2	1	36.43	3643	2024-04-26 12:35:50.224363
\.


--
-- Data for Name: payment_method; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.payment_method (payment_method_id, name) FROM stdin;
1	pago movil
2	Zinli
\.


--
-- Data for Name: status; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.status (status_id, name) FROM stdin;
1	paid
2	unpaid
3	canceled
\.


--
-- Data for Name: ticket; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.ticket (ticket_id, vehicle_type_id, charge, status_id, created_at) FROM stdin;
679	1	100	2	2024-04-26 12:29:35.301725
680	1	100	2	2024-04-26 12:29:35.301725
681	1	100	2	2024-04-26 12:29:35.301725
682	1	100	2	2024-04-26 12:29:35.301725
683	1	100	2	2024-04-26 12:29:35.301725
684	1	100	2	2024-04-26 12:29:35.301725
685	1	100	2	2024-04-26 12:29:35.301725
686	2	7	2	2024-04-26 12:29:35.301725
687	1	100	2	2024-04-26 12:29:35.301725
688	1	100	2	2024-04-26 12:29:35.301725
689	1	100	2	2024-04-26 12:29:35.301725
690	1	100	2	2024-04-26 12:29:35.301725
691	1	100	2	2024-04-26 12:29:35.301725
692	1	100	2	2024-04-26 12:29:35.301725
693	1	100	2	2024-04-26 12:29:35.301725
694	2	7	2	2024-04-26 12:29:35.301725
695	1	100	2	2024-04-26 12:29:35.301725
696	2	7	2	2024-04-26 12:29:35.301725
697	1	100	2	2024-04-26 12:29:35.301725
698	1	100	2	2024-04-26 12:29:35.301725
699	1	100	2	2024-04-26 12:29:35.301725
700	1	100	2	2024-04-26 12:29:35.301725
701	1	100	2	2024-04-26 12:29:35.301725
702	2	7	2	2024-04-26 12:29:35.301725
703	1	100	2	2024-04-26 12:29:35.301725
704	1	100	2	2024-04-26 12:29:35.301725
705	1	100	2	2024-04-26 12:29:35.301725
706	1	100	2	2024-04-26 12:29:35.301725
707	1	100	2	2024-04-26 12:29:35.301725
708	1	100	1	2024-04-26 12:29:35.301725
709	1	100	2	2024-04-26 12:29:35.301725
710	1	100	2	2024-04-26 12:29:35.301725
711	1	100	2	2024-04-26 12:29:35.301725
712	1	100	2	2024-04-26 12:29:35.301725
713	1	100	2	2024-04-26 12:29:35.301725
714	1	100	2	2024-04-26 12:29:35.301725
715	1	100	2	2024-04-26 12:29:35.301725
716	2	7	2	2024-04-26 12:29:35.301725
717	1	100	2	2024-04-26 12:29:35.301725
718	1	100	2	2024-04-26 12:29:35.301725
719	1	100	2	2024-04-26 12:29:35.301725
720	1	100	2	2024-04-26 12:29:35.301725
721	1	100	2	2024-04-26 12:29:35.301725
722	1	100	2	2024-04-26 12:29:35.301725
723	1	100	2	2024-04-26 12:29:35.301725
724	2	7	2	2024-04-26 12:29:35.301725
725	1	100	2	2024-04-26 12:29:35.301725
726	2	7	2	2024-04-26 12:29:35.301725
727	1	100	2	2024-04-26 12:29:35.301725
728	1	100	2	2024-04-26 12:29:35.301725
729	1	100	2	2024-04-26 12:29:35.301725
730	1	100	2	2024-04-26 12:29:35.301725
731	1	100	2	2024-04-26 12:29:35.301725
732	2	7	2	2024-04-26 12:29:35.301725
733	1	100	2	2024-04-26 12:29:35.301725
734	1	100	2	2024-04-26 12:29:35.301725
735	1	100	2	2024-04-26 12:29:35.301725
736	1	100	2	2024-04-26 12:29:35.301725
737	1	100	2	2024-04-26 12:29:35.301725
738	1	100	2	2024-04-26 12:29:35.301725
739	1	100	2	2024-04-26 12:29:35.301725
740	1	100	2	2024-04-26 12:29:35.301725
741	1	100	2	2024-04-26 12:29:35.301725
742	1	100	2	2024-04-26 12:29:35.301725
743	1	100	2	2024-04-26 12:29:35.301725
744	4	10	2	2024-04-26 12:29:35.301725
745	4	10	2	2024-04-26 12:29:35.301725
746	1	100	2	2024-04-26 12:29:35.301725
747	4	10	2	2024-04-26 12:29:35.301725
748	2	7	2	2024-04-26 12:29:35.301725
749	2	7	2	2024-04-26 12:29:35.301725
750	1	100	2	2024-04-26 12:29:35.301725
751	1	100	2	2024-04-26 12:29:35.301725
752	1	100	2	2024-04-26 12:29:35.301725
753	1	100	2	2024-04-26 12:29:35.301725
757	1	100	1	2024-04-26 12:29:35.301725
756	1	100	1	2024-04-26 12:29:35.301725
755	1	100	1	2024-04-26 12:29:35.301725
754	1	100	1	2024-04-26 12:29:35.301725
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.users (id, username, password, permisology) FROM stdin;
1	admin	$2b$12$WreM6PI1qX9fmA6.Pn7xLOS3kfXscGVYdpgWu/K9XRnjuvMMZRxDq	admin
14	daniel	$2b$12$UIiU.KXsblJzqYTTWvsanOn/1U7msxEBrIY4tJ4LXkFaBaSkCws8u	employee
\.


--
-- Data for Name: vehicle_type; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.vehicle_type (vehicle_type_id, name, charge) FROM stdin;
2	truck	7
3	motorcycle	2.5
4	bus	10
1	car	100
\.


--
-- Name: currency_currency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.currency_currency_id_seq', 2, true);


--
-- Name: deteccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.deteccion_id_seq', 89, true);


--
-- Name: deteccion_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.deteccion_status_id_seq', 1, true);


--
-- Name: payment_method_payment_method_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.payment_method_payment_method_id_seq', 2, true);


--
-- Name: payment_payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.payment_payment_id_seq', 5, true);


--
-- Name: status_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.status_status_id_seq', 3, true);


--
-- Name: ticket_ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.ticket_ticket_id_seq', 757, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.users_id_seq', 14, true);


--
-- Name: vehicle_type_vehicle_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.vehicle_type_vehicle_type_id_seq', 12, true);


--
-- Name: currency currency_name_key; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_name_key UNIQUE (name);


--
-- Name: currency currency_pk; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_pk PRIMARY KEY (currency_id);


--
-- Name: deteccion deteccion_pkey; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.deteccion
    ADD CONSTRAINT deteccion_pkey PRIMARY KEY (id);


--
-- Name: deteccion_status deteccion_status_pkey; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.deteccion_status
    ADD CONSTRAINT deteccion_status_pkey PRIMARY KEY (id);


--
-- Name: payment_method payment_method_name_key; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.payment_method
    ADD CONSTRAINT payment_method_name_key UNIQUE (name);


--
-- Name: payment payment_pk; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_pk PRIMARY KEY (payment_id);


--
-- Name: payment_method pyment_method_pk; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.payment_method
    ADD CONSTRAINT pyment_method_pk PRIMARY KEY (payment_method_id);


--
-- Name: status status_name_key; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_name_key UNIQUE (name);


--
-- Name: status status_pk; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pk PRIMARY KEY (status_id);


--
-- Name: ticket ticket_pk; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_pk PRIMARY KEY (ticket_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: vehicle_type vehicle_type_name_key; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.vehicle_type
    ADD CONSTRAINT vehicle_type_name_key UNIQUE (name);


--
-- Name: vehicle_type vehicle_type_pk; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.vehicle_type
    ADD CONSTRAINT vehicle_type_pk PRIMARY KEY (vehicle_type_id);


--
-- Name: payment currency_fk; Type: FK CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT currency_fk FOREIGN KEY (currency_id) REFERENCES public.currency(currency_id) NOT VALID;


--
-- Name: payment payment_method_fk; Type: FK CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_method_fk FOREIGN KEY (payment_method_id) REFERENCES public.payment_method(payment_method_id) NOT VALID;


--
-- Name: ticket status_fk; Type: FK CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT status_fk FOREIGN KEY (status_id) REFERENCES public.status(status_id) NOT VALID;


--
-- Name: payment ticket_fk; Type: FK CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT ticket_fk FOREIGN KEY (ticket_id) REFERENCES public.ticket(ticket_id) NOT VALID;


--
-- Name: ticket vehicle_fk; Type: FK CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT vehicle_fk FOREIGN KEY (vehicle_type_id) REFERENCES public.vehicle_type(vehicle_type_id) NOT VALID;


--
-- PostgreSQL database dump complete
--

