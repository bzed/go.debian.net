--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: godebian_urls; Type: TABLE; Schema: public; Owner: godebian; Tablespace: 
--

CREATE TABLE godebian_urls (
    pk integer NOT NULL,
    id bigint NOT NULL,
    url character varying,
    is_static boolean NOT NULL,
    create_date timestamp without time zone,
    log text
);


ALTER TABLE godebian_urls OWNER TO godebian;

--
-- Name: godebian_urls_pk_seq; Type: SEQUENCE; Schema: public; Owner: godebian
--

CREATE SEQUENCE godebian_urls_pk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE godebian_urls_pk_seq OWNER TO godebian;

--
-- Name: godebian_urls_pk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: godebian
--

ALTER SEQUENCE godebian_urls_pk_seq OWNED BY godebian_urls.pk;


--
-- Name: url_id_seq; Type: SEQUENCE; Schema: public; Owner: godebian
--

CREATE SEQUENCE url_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE url_id_seq OWNER TO godebian;

--
-- Name: pk; Type: DEFAULT; Schema: public; Owner: godebian
--

ALTER TABLE ONLY godebian_urls ALTER COLUMN pk SET DEFAULT nextval('godebian_urls_pk_seq'::regclass);


--
-- Name: godebian_urls_pkey; Type: CONSTRAINT; Schema: public; Owner: godebian; Tablespace: 
--

ALTER TABLE ONLY godebian_urls
    ADD CONSTRAINT godebian_urls_pkey PRIMARY KEY (pk);


--
-- Name: ix_godebian_urls_id; Type: INDEX; Schema: public; Owner: godebian; Tablespace: 
--

CREATE UNIQUE INDEX ix_godebian_urls_id ON godebian_urls USING btree (id);


--
-- Name: ix_godebian_urls_url; Type: INDEX; Schema: public; Owner: godebian; Tablespace: 
--

CREATE INDEX ix_godebian_urls_url ON godebian_urls USING btree (url);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

