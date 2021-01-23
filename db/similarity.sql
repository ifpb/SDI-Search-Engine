CREATE OR REPLACE FUNCTION public.v3similarity(double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision)
 RETURNS double precision
 LANGUAGE plpgsql
AS $
DECLARE
	geomA_xmin ALIAS for ;
	geomA_ymin ALIAS for ;
	geomA_xmax ALIAS for ;
	geomA_ymax ALIAS for ;
	--
	geomB_xmin ALIAS for ;
	geomB_ymin ALIAS for ;
	geomB_xmax ALIAS for ;
	geomB_ymax ALIAS for ;

	areaA float := 0;
	areaB float := 0;
	intersect_area float;
	similarityResult float;
BEGIN
	select into areaA ST_Area(ST_Makeenvelope(geomA_xmin, geomA_ymin, geomA_xmax, geomA_ymax));
	select into areaB ST_Area(ST_Makeenvelope(geomB_xmin, geomB_ymin, geomB_xmax, geomB_ymax));
	select into intersect_area bbox_intersects_area(geomA_xmin, geomA_ymin, geomA_xmax, geomA_ymax, geomB_xmin, geomB_ymin, geomB_xmax, geomB_ymax);
	select into similarityResult (
            ( intersect_area )
            /
            ( intersect_area
             + 0.5 * ( areaA - intersect_area )
            + 0.5 * ( areaB - intersect_area ) )
        );
	return similarityResult;
END
$
;