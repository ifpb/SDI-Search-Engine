--CREATE TABLE public.place_2 (
--	gid serial NOT NULL,
--	nome varchar(254) NULL,
--	tipo varchar(80) NULL,
--	geom geometry(MULTIPOLYGON) NULL,
--	area float8 NULL,
--	x_min float8 NULL,
--	y_min float8 NULL,
--	y_max float8 NULL,
--	x_max float8 NULL,
--	CONSTRAINT place_pkey_2 PRIMARY KEY (gid)
--);
--CREATE INDEX geomindex_place_2 ON public.place_2 USING gist (geom);

delete from catalogue;
delete from service;
delete from feature_type;
delete from register;


select count(*) from place

-- FEATURE TYPE


--belo horizonte
select id, v3similarity(-44.05918970680698, -20.02324822544587, -43.8524043297312, -19.776240238384315, x_min, y_min, x_max, y_max) from feature_type
where id = '288df881-9db5-4c91-8c75-a7fa133e1771' and ST_Intersects(ST_GeomFromText(''), geometry)

-- id, v3similarity from place
select id, v3similarity(pdata.x_min, pdata.y_min, pdata.x_max, pdata.y_max, ft.x_min, ft.y_min, ft.x_max, ft.y_max) as sim from feature_type ft,
(
	select p.geom, p.x_min, p.y_min, p.x_max, p.y_max from place p where p.nome ilike 'belo horizonte' 
) as pdata
where ST_Intersects(pdata.geom, ft.geometry) and v3similarity(pdata.x_min, pdata.y_min, pdata.x_max, pdata.y_max, ft.x_min, ft.y_min, ft.x_max, ft.y_max) > 0


select p.geom, feature.geometry from place p, (
	select geometry from feature_type limit 10
) as feature where p.nome ilike 'sudeste'

                        
select ft.geometry, bh.geometry from feature_type ft, (
	select p.geom as geometry from place p where p.nome ilike 'belo horizonte' 
) as bh where ft.id ilike '288df881-9db5-4c91-8c75-a7fa133e1771'

select * from feature_type where id = 'dae2a907-f5d4-4d1a-98b2-f735019e08d7'
select * from feature_type where title ilike 'equipamento de saude'
select * from place where nome ilike 'belo horizonte'

-44.05918970680698, -20.02324822544587, -43.8524043297312, -19.776240238384315