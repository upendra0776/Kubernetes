# DB Connector

## Build
```
docker build -t kunchalavikram/db-connector:1.0 .2
```
## Using with Docker
### Without Docker Networks
```
docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=my_secret -e MYSQL_DATABASE=test mysql:latest
docker run --rm --name db-connector -e DB_HOST=172.17.0.2 -e DB_USER=root  -e DB_PASSWORD=my_secret -e DATABASE=test kunchalavikram/db-connector:1.0 
```

### With Docker Networks
```
docker network create my_net
docker run -d --net my_net --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=my_secret -e MYSQL_DATABASE=test mysql:latest
docker run --rm --net my_net --name db-connector -e DB_HOST=mysql -e DB_USER=root  -e DB_PASSWORD=my_secret -e DATABASE=test kunchalavikram/db-connector:1.0 
```

## Using with K8s
```
kubectl create secret generic db-secret --from-literal=DB_HOST="192.168.99.111" --from-literal=DB_USER=root \
--from-literal=DB_PASSWORD=my_secret --from-literal=DATABASE=test
kubectl delete secret db-secret
```
