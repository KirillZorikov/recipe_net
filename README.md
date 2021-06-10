# recipe_net

Backend for the project recipe_net.
Vue 3 frontend is here: [front](https://github.com/KirillZorikov/recipe_net_front)

Production version on a running server: http://84.252.132.216:8080
Admin panel: http://84.252.132.216/admin_panel

recipe_net is an online service where users can publish recipes, 
subscribe to other users, add favorite recipes to the favorites list, 
and download a summary list of products needed to prepare one or more selected dishes before going to the store.

You can download docker images from the following link:
[backend](https://hub.docker.com/repository/docker/kzorikov/recipe_net_back),
[frontend](https://hub.docker.com/repository/docker/kzorikov/recipe_net_front),

## Project setup
```
docker-compose build
```

## Project run
```
docker-compose up
```

## Apply migrations
```
docker-compose exec recipe_net_prod python manage.py migrate
```

## Create superuser
```
docker-compose exec recipe_net_prod python manage.py createsuperuser
```

## Fill the database with dummy data
```
docker-compose exec recipe_net_prod python manage.py loaddata dummy_data/db.json
```