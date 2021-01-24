
-- Drop table

-- DROP TABLE public.catalogue;

CREATE TABLE public.catalogue (
	id text NULL,
	url text NULL
);
CREATE INDEX ix_catalogue_id ON public.catalogue USING btree (id);

-- Drop table

-- DROP TABLE public.feature_type;

CREATE TABLE public.feature_type (
	id text NULL,
	title text NULL,
	"name" text NULL,
	description text NULL,
	keywords text NULL,
	service_id text NULL,
	start_date date NULL,
	end_date date NULL,
	geometry geometry NULL,
	area float8 NULL,
	features_of_service int4 NULL,
	x_min float8 NULL,
	y_min float8 NULL,
	x_max float8 NULL,
	y_max float8 NULL
);
CREATE INDEX ft_geometry_index ON public.feature_type USING gist (geometry);
CREATE INDEX ix_feature_type_id ON public.feature_type USING btree (id);

-- Drop table

-- DROP TABLE public.place;

CREATE TABLE public.place (
	gid serial NOT NULL,
	nome varchar(254) NULL,
	tipo varchar(80) NULL,
	geom geometry(MULTIPOLYGON) NULL,
	area float8 NULL,
	x_min float8 NULL,
	y_min float8 NULL,
	y_max float8 NULL,
	x_max float8 NULL,
	CONSTRAINT place_pkey PRIMARY KEY (gid)
);
CREATE INDEX geomindex ON public.place USING gist (geom);

-- Drop table

-- DROP TABLE public.register;

CREATE TABLE public.register (
	id text NULL,
	title text NULL,
	publisher text NULL,
	bounding_box text NULL,
	description text NULL,
	keywords text NULL,
	catalogue_id text NULL,
	"date" date NULL
);
CREATE INDEX ix_register_id ON public.register USING btree (id);

-- Drop table

-- DROP TABLE public.service;

CREATE TABLE public.service (
	id text NULL,
	wfs_url text NULL,
	wms_url text NULL,
	service_processed text NULL,
	title text NULL,
	description text NULL,
	publisher text NULL,
	register_id text NULL,
	geometry geometry NULL,
	start_date date NULL,
	end_date date NULL,
	area float8 NULL,
	x_min float8 NULL,
	y_min float8 NULL,
	x_max float8 NULL,
	y_max float8 NULL
);
-- CREATE INDEX ix_service_id ON public.service USING btree (id);
-- CREATE INDEX service_geometry_geohash ON public.service USING btree (st_geohash(st_transform(st_setsrid(geometry, 4326), 4326)));
CREATE INDEX service_geometry_geohash ON public.service USING btree (st_geohash(st_transform(st_setsrid(geometry, 4326), 4326)));
CLUSTER service USING service_geometry_geohash;
