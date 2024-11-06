--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

-- Started on 2024-11-05 02:29:26

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
--
-- TOC entry 4904 (class 1262 OID 16389)
-- Name: dtse-assignment-task-db; Type: DATABASE; Schema: -; Owner: postgres
--

ALTER DATABASE "dtse-assignment-task-db" OWNER TO postgres;


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 218 (class 1259 OID 24644)
-- Name: housing_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.housing_data (
    id integer NOT NULL,
    longitude numeric(5,2) NOT NULL,
    latitude numeric(4,2) NOT NULL,
    housing_median_age numeric(4,1) NOT NULL,
    total_rooms integer NOT NULL,
    total_bedrooms integer NOT NULL,
    population integer NOT NULL,
    households integer NOT NULL,
    median_income numeric(7,4) NOT NULL,
    "ocean_proximity_<1H OCEAN" smallint DEFAULT 0,
    "ocean_proximity_INLAND" smallint DEFAULT 0,
    "ocean_proximity_ISLAND" smallint DEFAULT 0,
    "ocean_proximity_NEAR BAY" smallint DEFAULT 0,
    "ocean_proximity_NEAR OCEAN" smallint DEFAULT 0,
    predicted_house_value numeric
);


ALTER TABLE public.housing_data OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24643)
-- Name: housing_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.housing_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.housing_data_id_seq OWNER TO postgres;

--
-- TOC entry 4905 (class 0 OID 0)
-- Dependencies: 217
-- Name: housing_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.housing_data_id_seq OWNED BY public.housing_data.id;


--
-- TOC entry 4742 (class 2604 OID 24647)
-- Name: housing_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.housing_data ALTER COLUMN id SET DEFAULT nextval('public.housing_data_id_seq'::regclass);


--
-- TOC entry 4898 (class 0 OID 24644)
-- Dependencies: 218
-- Data for Name: housing_data; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4906 (class 0 OID 0)
-- Dependencies: 217
-- Name: housing_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.housing_data_id_seq', 27, true);


--
-- TOC entry 4749 (class 2606 OID 24656)
-- Name: housing_data housing_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.housing_data
    ADD CONSTRAINT housing_data_pkey PRIMARY KEY (id);


--
-- TOC entry 4751 (class 2606 OID 24658)
-- Name: housing_data housing_data_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.housing_data
    ADD CONSTRAINT housing_data_unique UNIQUE (longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households, median_income, "ocean_proximity_<1H OCEAN", "ocean_proximity_INLAND", "ocean_proximity_ISLAND", "ocean_proximity_NEAR BAY", "ocean_proximity_NEAR OCEAN");


-- Completed on 2024-11-05 02:29:29

--
-- PostgreSQL database dump complete
--

