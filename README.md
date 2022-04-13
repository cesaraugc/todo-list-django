# Todo List
## Sobre o projeto

Esta é uma API onde as pessoas podem cadastrar listas e items de atividades dentro destas listas. Ela possui controle de acesso com autenticação.

## Escopo do projeto

Os itens abaixo marcados no checkbox foram implementados.

### Must have
- [x] Endpoint de autenticação
  - [X] Autenticação com JWT
- [x] Endpoints de Usuários (GET/POST/PUT)
  - [X] /api/v1/users/{ID} (GET/PUT)
  - [X] /api/v1/users (POST)
- [x] Endpoints de Lista (GET/POST/DELETE)
  - [X] /api/v1/lists/{ID} (GET/DELETE)
  - [X] /api/v1/lists (POST)
- [x] Endpoints de Itens da lista (GET/POST/PUT/DELETE)
  - [x] /api/v1/lists/{ID}/items (GET/POST)
  - [x] /api/v1/lists/{ID}/items/{ID} (PUT/DELETE)
- [x] Níveis de permissão

### May Have
- [X] Códigos de testes em todos os endpoints
- [x] Utilização de Docker e docker-compose
- [ ] Itens possuindo subitens.

### Tasks e tempo previsto

- [X] Montar escopo do Banco de Dados (tabelas e relacionamentos) - 1h
- [X] Inicialiar o framework com Docker e Models do BD - 2h
- [x] Escrever os serializadores dos Models - 1h
- [x] TDD dos Endpoints de Users - 3h
- [x] TDD dos Endpoints de Lists - 3h
- [x] TDD dos Endpoints de Items - 2h
- [x] TDD do Endpoint de Autenticação - 3h
- [x] Adicionar testes de permissões de autenticação nos Endpoints anteriores - 1h
- [x] Adicionar código de de autenticação nos Endpoints anteriores - 2h
- [x] Documentação do README - 2h 


## Prazo de entrega
Previsão de 20 horas de trabalho. Entrega em cinco (5) dias úteis.

## Método

A API foi desenvolvida na linguagem Python utilizando o framework Django e conteinerizada com Docker.

Todo o desenvolvimento foi realizado utilizando a técnica de TDD, então o projeto possui testes consistentes e relevantes.

## Como executar

Para executar pela primeira vez, basta ter o Docker instalado e executar os comandos:

`docker-compose build`

`docker-compose run web python manage.py migrate`

`docker-compose up`

Nas próximas execuções, após a inicialização da imagem e do banco de dados, basta executar o comando:

`docker-compose up`

## Testando a API


Para testar o projeto, deve ser executado o comando:

`docker-compose run web python manage.py test`

## Autenticação

Para chamar os endpoints que não são públicos, é necessário realizar uma chamada a "/api/v1/authenticate" para obter o token. Em seguida, as demais chamadas devem ser realizadas com o Header: "Authorization: Bearer {token}".

O banco de dados fornecido juntamente com o código já possui um superuser criado com as credenciais:

- login=admin
- password=12345

## Endpoints implementados

Foram implementadas os seguintes endpoints:

- Autenticação
    - URI: /api/v1/authenticate
        - Public: SIM
        - Tipo: POST
        - Request: { "login": STRING; "password": STRING }
        - Return Success: { "token": JWT, "user": OBJECT }
        - Return Fail: { "detail" : STRING }

- Usuário
    - URI: /api/v1/users/{ID}
        - Public: NÃO
        - Tipo: GET
        - Return Success: { "user" : OBJECT }
        - Return Fail: { "detail" : STRING }

    - URI: /api/v1/users
        - Public: Não
        - Tipo: POST
        - Request: { "name": STRING, "email": STRING, "login": STRING; "password": STRING  }
        - Return Success: { "user" : OBJECT }
        - Return Fail: { "error" : STRING }

    - URI: /api/v1/users/{ID}
        - Public: Não
        - Tipo: PUT
        - Request: { "name": STRING, "email": STRING, "login": STRING; "password": STRING  }
        - Return Success: { "user" : OBJECT }
        - Return Fail: { "error" : STRING }


- LISTA:

    - URI: /api/v1/lists/{ID}
        - Public: Sim
        - Tipo: GET
        - Return Success: { "list" : OBJECT,  “user_id”: INTEGER }
        - Return Fail: { "message" : STRING }

    - URI: /api/v1/lists
        - Public: Sim
        - Tipo: POST
        - Request: { "title": STRING }
        - Return Success: { "list" : { "title" : STRING } }
        - Return Fail: { "message" : STRING }

    - URI: /api/v1/lists/{ID}
        - Public: Não
        - Tipo: DELETE
        - Request: { "id": INTEGER }
        - Return Fail: { "message" : STRING }


- ITENS DA LISTA

    - URI: /api/v1/lists/{ID}/items
        - Public: Não
        - Tipo: GET
        - Return Success: { "items" : [ OBJECT1, OBJECT2 ] }
        - Return Fail: { "message" : STRING }

    - URI: /api/v1/lists/{ID}/items
        - Public: Não
        - Tipo: POST
        - Request: { "title": STRING, "description": STRING }
        - Return Success: { "item" : OBJECT }
        - Return Fail: { "message" : STRING }

    - URI: /api/v1/lists/{ID}/items/{ID}
        - Public: Não
        - Tipo: PUT
        - Request: { "title": STRING, "description": STRING }
        - Return Success: { "item" : OBJECT }
        - Return Fail: { "message" : STRING }

    - URI: /api/v1/lists/{ID}/items/{ID}
      - Public: Não
      - Tipo: DELETE
      - Request: { "id": INTEGER }
      - Return Fail: { "message" : STRING }
