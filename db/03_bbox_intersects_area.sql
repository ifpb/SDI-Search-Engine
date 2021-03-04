CREATE OR REPLACE FUNCTION bbox_intersects_area(float, float,  float, float, float, float, float, float)
RETURNS float AS '
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
	--
	xmin_intersect float := 0;
	ymin_intersect float := 0;
	xmax_intersect float := 0;
	ymax_intersect float := 0;
BEGIN
	if geomA_xmin >= geomB_xmin and geomA_xmin <= geomB_xmax
	then
		if geomA_xmin = geomB_xmin
		then
			xmin_intersect := geomA_xmin;
			if geomA_xmax < geomB_xmax
			then
				xmax_intersect := geomA_xmax;
				if geomA_ymax = geomB_ymin
				then
					ymin_intersect := geomA_ymin;
					ymax_intersect := geomA_ymin;	
				elsif geomA_ymax = geomB_ymax
				then
					ymax_intersect := geomA_ymax;
					if geomA_ymin > geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin < geomB_ymin
					then
						ymin_intersect := geomB_ymin;
					end if;
				elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
				then
					ymax_intersect := geomA_ymax;
					if geomA_ymin > geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin < geomB_ymin
					then
						ymin_intersect := geomB_ymin;
					end if;
				elsif geomA_ymax > geomB_ymax
				then
					ymax_intersect := geomB_ymax;
					if geomB_ymax = geomA_ymin
					then
						ymin_intersect := geomB_ymax;
					elsif geomB_ymax > geomA_ymin
					then
						ymin_intersect := geomA_ymin;
					end if;
				end if;
			elsif geomA_xmax = geomB_xmax
			then
				xmax_intersect := geomA_xmax;
				if geomA_ymax = geomB_ymin
				then
					ymin_intersect := geomA_ymin;
					ymax_intersect := geomA_ymin;	
				elsif geomA_ymax = geomB_ymax
				then
					ymax_intersect := geomA_ymax;
					if geomA_ymin > geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin < geomB_ymin
					then
						ymin_intersect := geomB_ymin;
					end if;
				elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
				then
					ymax_intersect := geomA_ymax;
					if geomA_ymin > geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin < geomB_ymin
					then
						ymin_intersect := geomB_ymin;
					end if;
				elsif geomA_ymax > geomB_ymax
				then
					ymax_intersect := geomB_ymax;
					if geomB_ymax = geomA_ymin
					then
						ymin_intersect := geomB_ymax;
					elsif geomB_ymax > geomA_ymin
					then
						ymin_intersect := geomA_ymin;
					end if;
				end if;
			elsif geomA_xmax > geomB_xmax
			then
				xmax_intersect := geomB_xmax;
				if geomA_ymax = geomB_ymin
				then
					ymin_intersect := geomA_ymin;
					ymax_intersect := geomA_ymin;	
				elsif geomA_ymax = geomB_ymax
				then
					ymax_intersect := geomA_ymax;
					if geomA_ymin > geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin < geomB_ymin
					then
						ymin_intersect := geomB_ymin;
					end if;
				elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
				then
					ymax_intersect := geomA_ymax;
					if geomA_ymin > geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
					elsif geomA_ymin < geomB_ymin
					then
						ymin_intersect := geomB_ymin;
					end if;
				elsif geomA_ymax > geomB_ymax
				then
					ymax_intersect := geomB_ymax;
					if geomB_ymax = geomA_ymin
					then
						ymin_intersect := geomB_ymax;
					elsif geomB_ymax > geomA_ymin
					then
						ymin_intersect := geomA_ymin;
					end if;
				end if;
			end if;
		elsif geomA_xmin > geomB_xmin and geomA_xmin < geomB_xmax
			then
				xmin_intersect := geomA_xmin;
				if geomA_xmax < geomB_xmax
				then
					xmax_intersect := geomA_xmax;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmax = geomB_xmax
				then
					xmax_intersect := geomA_xmax;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmax > geomB_xmax
				then
					xmax_intersect := geomB_xmax;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				end if;
		elsif geomA_xmin = geomB_xmax
			then
				xmin_intersect := geomA_xmin;
				if geomA_xmax < geomB_xmax
				then
					xmax_intersect := geomA_xmax;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmax = geomB_xmax
				then
					xmax_intersect := geomA_xmax;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmax > geomB_xmax
				then
					xmax_intersect := geomB_xmax;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				end if;
		end if;
	elsif geomA_xmax >= geomB_xmin and geomA_xmax <= geomB_xmax
		then
			if geomA_xmax = geomB_xmin
			then
				xmax_intersect := geomA_xmax;
				if geomA_xmin < geomB_xmin
				then
					xmin_intersect := geomB_xmin;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmin = geomB_xmin
				then
					xmin_intersect := geomB_xmin;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmin > geomB_xmin
				then
					xmin_intersect := geomA_xmin;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				end if;
			elsif geomA_xmax > geomB_xmin and geomA_xmax < geomB_xmax
			then
				xmax_intersect := geomA_xmax;
				if geomA_xmin < geomB_xmin
				then
					xmin_intersect := geomB_xmin;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmin = geomB_xmin
				then
					xmin_intersect := geomB_xmin;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmin > geomB_xmin
				then
					xmin_intersect := geomA_xmin;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				end if;
			elsif geomA_xmax = geomB_xmax
			then
				xmax_intersect := geomA_xmax;
				if geomA_xmin < geomB_xmin
				then
					xmin_intersect := geomB_xmin;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmin = geomB_xmin
				then
					xmin_intersect := geomB_xmin;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				elsif geomA_xmin > geomB_xmin
				then
					xmin_intersect := geomA_xmin;
					if geomA_ymax = geomB_ymin
					then
						ymin_intersect := geomA_ymin;
						ymax_intersect := geomA_ymin;	
					elsif geomA_ymax = geomB_ymax
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax < geomB_ymax and geomA_ymax > geomB_ymin
					then
						ymax_intersect := geomA_ymax;
						if geomA_ymin > geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin = geomB_ymin
						then
							ymin_intersect := geomA_ymin;
						elsif geomA_ymin < geomB_ymin
						then
							ymin_intersect := geomB_ymin;
						end if;
					elsif geomA_ymax > geomB_ymax
					then
						ymax_intersect := geomB_ymax;
						if geomB_ymax = geomA_ymin
						then
							ymin_intersect := geomB_ymax;
						elsif geomB_ymax > geomA_ymin
						then
							ymin_intersect := geomA_ymin;
						end if;
					end if;
				end if;
			end if;
	end if;
	return st_area(st_makeenvelope(xmin_intersect, ymin_intersect, xmax_intersect, ymax_intersect));
END
' language plpgsql
