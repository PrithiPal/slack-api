docker ps | awk '{print $1}' | xargs -n1 docker kill
sleep 5
docker run -d -p 27017:27017 --network=slack mongo
sleep 10
docker run -p 3000:3000 -v ~/Desktop/stem:/data/db --network=slack -e MONGO_URL="mongodb://localhost:27017/pymongo_db" mongoclient/mongoclient
