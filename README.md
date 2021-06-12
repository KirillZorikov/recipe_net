# recipe_net

Backend for the project recipe_net.
Vue 3 frontend is here: [front](https://github.com/KirillZorikov/recipe_net_front).

Production version on a running server: http://kz-projects.tk/recipe_net

Admin panel: https://kz-api.tk/admin_panel

recipe_net is an online service where users can publish recipes, 
subscribe to other users, add favorite recipes to the favorites list, 
and download a summary list of products needed to prepare one or more selected dishes before going to the store.

You can download docker images from the following link:
[backend](https://hub.docker.com/repository/docker/kzorikov/recipe_net_back),
[frontend](https://hub.docker.com/repository/docker/kzorikov/recipe_net_front).

There are also tests that cover most of the project endpoints.

## Run tests
```
pytest
```


# A few steps to fully run and setup the project:

## Project setup
```
docker-compose build
```

## Create HTTPS certificates
```
chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh
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
