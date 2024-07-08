
docker rmi ganesha-backend-web
docker rmi registry.digitalocean.com/ganesha/dev
docker-compose -f docker-compose.beta.yml build
docker image ls | grep ganesha-backend-web
doctl registry login
docker tag ganesha-backend-web registry.digitalocean.com/ganesha/dev
docker push registry.digitalocean.com/ganesha/dev
