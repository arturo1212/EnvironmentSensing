# EnvironmentSensing
Demo project for environment variable sensing using Docker, Angular, Flask and Arduino


docker run -v /db/:/db/ senseme_store
docker run -d -p 5000:5000 -v /db/:/db/ senseme_api
