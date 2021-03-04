FROM postgres:9.6
ENV POSTGRES_DB inde_database_docker
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres

ENV POSTGIS_MAJOR 2.3

RUN apt-get update \
      && apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
      && apt-get install -y --no-install-recommends\
      postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR\
      postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts\
      && rm -rf /var/lib/apt/lists/*

# RUN apt-get install postgresql-client

RUN mkdir -p /docker-entrypoint-initdb.d

COPY ./01-initdb-postgis.sh /docker-entrypoint-initdb.d/01-postgis.sh

COPY ./02_tables.sql /docker-entrypoint-initdb.d

COPY ./03_bbox_intersects_area.sql /docker-entrypoint-initdb.d

COPY ./04_similarity.sql /docker-entrypoint-initdb.d

COPY ./05_place_insert.sql /docker-entrypoint-initdb.d


