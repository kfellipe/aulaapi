# Aplicativo FastAPI
Para iniciar a aplicação FastAPI, primeiro precisamos instalar as bibliotecas que estão guardadas no arquivo requirements.txt:
<code>pip install -r requirements.txt</code>
<hr>
Após a instalação, precisamos iniciar o serviço web uvicorn com o comando:
<code>uvicorn main:app --reload</code>
<hr>
Após a inicialização do aplicativo, acessamos via web na URL localhost:8000/docs onde podemos acessar o swagger, documentação da nossa API.
