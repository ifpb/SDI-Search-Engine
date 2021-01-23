# SDI Search Engine
Readme em andamento...

### Integração como serviço secundário.

#### Serviços 
* `db_postgres`: Container postgres com os feature types e services extraidos da [INDE](http://metadados.inde.gov.br/geonetwork/srv/por/main.home). Use o [Link](https://drive.google.com/file/d/1OyIXQI2fiCnP-1Nclp1AZJJOD1D1mmQp/view?usp=sharing) para fazer o donwload do backup do banco com parte dos dados da `INDE`. **Após o download import os dados no banco através de uma conexão localhost na porta `:5433` database:`inde_database_docker`.**

* `solr_app`: Container [Solr](https://lucene.apache.org/solr/) para busca temática da ferramente. Use o arquivo `backup/features_and_services_backup.json` para inserir o backup dos dados.

* `api_search_engine`: API Flask responsável por disponibilizar endpoints para consulta ao dados da ferramenta.  

###### Passos para importar os dados no solr

>> Após iniciar o container do solr execute os sequintes passos:

1. Acesse a interface web do solr através da url `http://localhost:8983/solr/#/`

2. Selecione o core `inde` na barra de menu esquerda. Imagem abaixo.

![](./backup/img_tutorial/core_inde.jpeg?raw=true "Core inde")

3. Selecione a opção `Documents` abaixo do select de cores.

4. Selecione a opção `JSON` e copie os dados do arquivo `backup/features_and_services_backup.json` para o campo `Document(s)`

5. Envie os dados clicando em `Submit Document`

##### Construir imagens e inicar containers

Use o script `build.sh` para criar as imagens e fazer o download de suas dependências. Ao final, o script já iniciará os containers para uso. Caso queira parar use o comando `Ctrl + c` e aguarde as mensagens `container_name done`.

##### Reiniciar containers

Use o script `start.sh` para iniciar novamente os containers. Desta vez os mesmos ficarão em background.

##### Parar sem remover os containers

Use o scrtip `stop.sh` para parar os containers em uso.

### API

``````
 - Similar Service
 - Returns a list of services similar to the one sent, according to your bounding box and theme
GET /similar/services/{service_id} HTTP/1.1
Host: api_search_engine:5000


 - Similar feature type
 - Returns a list of feature types similar to the one sent, according to your bounding box and theme
GET /similar/feature-types/{feature_type_id} HTTP/1.1
Content-Type: application/json
Host: api_search_engine:5000


 - Similar feature types bounding box
 - Returns the types of features most similar to the sent bounding box
GET /find/feature-type/bounding-box HTTP/1.1
Content-Type: application/json
Host: api_search_engine:5000
Content-Length: ...

{
	"xmin": "-47.320429043949524",
	"ymin": "-23.132468267449756",
	"xmax": "-46.74008861210897",
	"ymax": "-22.69721294356934",
	"start_date": "",
	"end_date": "",
	"theme": ""
}

 - Retrive data
 - Retrieves the information from the id
 - resource_type: 'feature-type' or 'service'
POST /retrieve/{resource_type} HTTP/1.1
Content-Type: application/json
Host: api_search_engine:5000
Content-Length: ...

[
	"23125c81-f581-46e6-93e7-64d74c07ab6d",
	"d0c8bb6b-81b9-4700-a6ca-0b310a2b2a1f"
]
