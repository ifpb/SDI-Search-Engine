#!/bin/sh

docker-compose up -d --build
echo "sleep 3s for solr start, after create core"
sleep 3
docker exec -it geotools_solr_app_1 solr create_core -c inde -d inde
