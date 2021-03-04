CREATE OR REPLACE FUNCTION public.v3similarity(double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision)
 RETURNS double precision AS '
DECLARE
	geomA_xmin ALIAS for $1;
	geomA_ymin ALIAS for $2;
	geomA_xmax ALIAS for $3;
	geomA_ymax ALIAS for $4;
	--
	geomB_xmin ALIAS for $5;
	geomB_ymin ALIAS for $6;
	geomB_xmax ALIAS for $7;
	geomB_ymax ALIAS for $8;

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
' language plpgsql
