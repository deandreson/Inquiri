O Inquiri é um sistema de cadastro e de perguntas para auxiliar os estudos. Sendo desenvolvido com um série de Tecnologias desde a FrameWork Flask, Banco de Dados SQLite, JavaScript e Lattex.
Dessa forma, para efetuar a instalação basta segiur os passos, comandos para executar no Linux/Fedora.

> Acesse o sistema em Funciomento: [Inquiri On-line](https://deandreson.pythonanywhere.com/)

Comandos:
- Para criar o ambiente virtual:  `python3 -m venv venv`
	- Acessando o ambiente virtual `source venv/bin/activate`
	- Para instalar as bibliotecas: `pip install -r requirements.txt`
Assim, o próximo passo é configurar as variáveis do Flask
	- Na pasta do projeto, então
    - `export FLASK_ENV=development`
    - `export FLASK_APP=Inquiri`

E por fim, para executar a aplicação:
    - `flask run`