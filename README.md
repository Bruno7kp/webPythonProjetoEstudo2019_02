Trabalho da 4ª fase do curso de Sistemas de Informação da UNIPLAC (2019/2).


### Instalação

Clone o repositório

```
git clone https://github.com/bruno7kp/mural-virtual.git
```

No diretório raiz do projeto, execute os seguintes comandos para criar o ambiente virtual e instalar as bibliotecas utilizadas

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Importe o banco de dados com o arquivo db_abc_bolinhas.sql
Os dados de acesso ao banco ficam no arquivo mod_base/base.py
Para inserir o administrador, execute o código do arquivo db_abc_bolinhas_insert.sql

Por fim, execute os comandos abaixo para rodar o projeto

```
set FLASK_ENV='development'
set FLASK_DEBUG=1
python -m flask run
```
