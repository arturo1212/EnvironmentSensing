# EnvironmentSensing
Demo project for environment variable sensing using Docker, Angular, Flask and Arduino

docker build --network=host -t senseme/api -f DockerfileAPI ./
docker build --network=host -t senseme/store -f DockerfileStore ./

docker run -d --network=host -v /db/:/db/ senseme/store
docker run -d -p 5000:5000 -v /db/:/db/ senseme/api

