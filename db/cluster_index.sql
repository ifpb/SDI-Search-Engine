CREATE INDEX service_geometry_geohash ON public.service USING btree (st_geohash(st_transform(st_setsrid(geometry, 4326), 4326)));
CLUSTER service USING service_geometry_geohash;

CREATE INDEX ft_geometry_index ON public.feature_type USING gist (geometry);