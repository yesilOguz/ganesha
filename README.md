# Ganesha
Ganesha is an application made for the `Gemini API Developer Competition`  and also has a mobile application.

Ganesha is a software that aims to guide people by using the power of Gemini. The project aims to guide you in your life and make your life easier by providing you with life coaching. It listens to your conversations to get to know you and it also has endpoints so you can chat with it.

## Setup
### For your development environment, set these variables 
> **GEMINI_API_KEY** =  [Gemini api key.](https://aistudio.google.com/app/apikey)

> **SECRET** = something ( you can generate with openssl or take it from online )	

> **APP_MODE** = **DEV** 
 
 > **MONGO_HOST** = **localhost**<br/>
 > **MONGO_PORT** = **27017**<br/>
 > **MONGO_USER** = **admin**<br/>
 > **MONGO_PASS** = **admin**<br/>
 > **MONGO_DB** = whatever_you_want<br/>
 > **MONGO_COLLECTION** = whatever_you_want
 
 > **EMAIL** = your_email_address ( I am using outlook smtp service so it must be outlook mail )<br/>
 > **EMAIL_PASS** = your_email_password

### For your beta or production environment, set these variables 
> **GEMINI_API_KEY** =  [Gemini api key.](https://aistudio.google.com/app/apikey)

> **SECRET** = something ( you can generate with openssl or take it from online )	

> **APP_MODE** = **BETA** or **PROD** 
 
 > **MONGO_HOST** = your_mongodb_host_url<br/>
 > **MONGO_USER** = your_mongodb_user<br/>
 > **MONGO_PASS** = your_mongodb_password<br/>
 > **MONGO_DB** = whatever_you_want<br/>
 > **MONGO_COLLECTION** = whatever_you_want
 
 > **EMAIL** = your_email_address ( I am using outlook smtp service so it must be outlook mail )<br/>
 > **EMAIL_PASS** = your_email_password

### Finally install dependencies using [poetry](https://python-poetry.org/docs/)
	> poetry install

### Run server
	> poetry run uvicorn main:app
