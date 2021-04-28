# ClientLocator

Projeto desenvolvido para aperfeiçoar alguns conhecimentos de arquitetura de software. O fluxo é simples onde ao ser iniciada a aplicação
é feita uma chamada aos endpoints de dados, no caso, dados vindos de JSON e CSV, e logo após o tratamento desses dados, são inseridos no
Redis como armazenamento em memória. A api possue apenas um endpoint para consulta por coordenada, onde é retornada uma lista paginada de 
usuários clientes disponíveis na coordenada informada. A aplicação foi desenvolvida em camadas OO, seguindo critérios do DDD, SOLID e DRY.

## Requisitos

* Docker
* Python 3.7 >

## Tecnologias

* Django
* Django RestFramework 
* Black
* Docker
* Redis
* Pandas


## Iniciando

Passos para configurar o projeto com docker:

1. `cd` na pasta do projeto
2. `docker-compose up --build`

Caso não deseje o uso de docker:
1. `Inicie um virtual env`
3. `pip install -r requirements.txt`
2. `python manage.py runserver`

O projeto por padrão estará em localhost:8000 

## Como usar ? 

### Search Endpoint

Endpoint responsável por buscar lista de usuários pela coordenada. Deve-se passar como parâmetros o número da página, 
a quantidade de elementos por página e as coordenadas definidas pela latitude e longitude. O cURL abaixo é um exemplo 
da requisição esperada: 

```
curl --request POST \
  --url http://localhost:8000/search \
  --header 'Content-Type: application/json' \
  --data '{
	"pageNumber": 1,
	"pageSize": 10,
	"coordinates": {
		"lat": -38.9614,
		"lon": -10.766959
	}
}
```




