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
\.


--
-- Data for Name: payment; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.payment (payment_id, ticket_id, charge, currency_id, payment_method_id, exchange_rate, local_currency, created_at) FROM stdin;
\.


--
-- Data for Name: payment_method; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.payment_method (payment_method_id, name) FROM stdin;
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

COPY public.ticket (ticket_id, vehicle_type_id, charge, status_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.users (id, username, password, permisology) FROM stdin;
13	admin	$2b$12$WreM6PI1qX9fmA6.Pn7xLOS3kfXscGVYdpgWu/K9XRnjuvMMZRxDq	admin
\.


--
-- Data for Name: vehicle_type; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.vehicle_type (vehicle_type_id, name, charge) FROM stdin;
1	car	5
2	truck	7
3	motorcycle	2.5
4	bus	10
\.


--
-- Name: currency_currency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.currency_currency_id_seq', 1, false);


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

SELECT pg_catalog.setval('public.payment_method_payment_method_id_seq', 1, false);


--
-- Name: payment_payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.payment_payment_id_seq', 1, false);


--
-- Name: status_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.status_status_id_seq', 3, true);


--
-- Name: ticket_ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.ticket_ticket_id_seq', 670, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.users_id_seq', 13, true);


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

