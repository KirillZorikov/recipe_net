# recipe_net

Backend for the project recipe_net.

Recipe_net is an online service where users can publish recipes, 
subscribe to other users, add favorite recipes to the favorites list, 
and download a summary list of products needed to prepare one or more selected dishes before going to the store.

With this project, I learned about the features of Django 3.2 and consolidated my knowledge in DRF.

Also, I learned about:
* [Certbot](https://certbot.eff.org/)
* [Let's Encrypt](https://letsencrypt.org/)
* [Celery](https://docs.celeryproject.org/en/stable/index.html)
* [Flower](https://flower.readthedocs.io/en/latest/)
* [Redis](https://redis.io/)

For celery, the project has two tasks:
* Sending emails for password recovery,
* Informing administrators about new users. Every day at midnight

### Project links:

* Project site: https://kz-projects.tk/recipe_net
* Vue 3 frontend: https://github.com/KirillZorikov/recipe_net_front
* Api: https://kz-api.tk/recipe_net/api/v1
* Admin panel: https://kz-api.tk/recipe_net/admin_panel
* Flower: https://kz-projects.tk/recipe_net/flower
* Docker images: [backend](https://hub.docker.com/repository/docker/kzorikov/recipe_net_back), [frontend](https://hub.docker.com/repository/docker/kzorikov/recipe_net_front)

There are also the [tests](https://github.com/KirillZorikov/recipe_net/tree/master/tests) that cover most of the project endpoints.

### Run tests:

```
pytest
```

### Tech:

Backend side:

* [Python 3.8.5](https://www.python.org/)
* [Django 3.2.3](https://www.djangoproject.com/) 
* [DRF](https://www.django-rest-framework.org/)
* [Nginx](https://www.nginx.com/)
* [Gunicorn](https://gunicorn.org/)
* [Docker](https://www.docker.com/)
* [reCAPTCHA v2](https://developers.google.com/recaptcha/docs/display)

*See the full list of backend dependencies here: [requirements.txt](https://github.com/KirillZorikov/recipe_net/blob/master/requirements.txt)*

Frontend side:

* [Vue 3](https://v3.vuejs.org/)
* [Bootstrap.js 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
* [CKEditor 5](https://ckeditor.com/docs/ckeditor5/latest/builds/guides/integration/frameworks/vuejs-v3.html)

*See the full list of frontend dependencies here: [package.json](https://github.com/KirillZorikov/recipe_net_front/blob/master/package.json)*

## Project deployment

There is a [docker-compose.all_projects.yaml](https://github.com/KirillZorikov/recipe_net/blob/master/docker-compose.all_projects.yaml) file that will allow you to run several projects on the same server:
recipe_net, 
[blog](https://github.com/KirillZorikov/blog_back),
[yamdb](https://github.com/KirillZorikov/yamdb_final)

If this is your intention, then in the following instructions, replace 
```
docker-compose
```
with 
```
docker-compose -f docker-compose.all_projects.yaml
```

### Create HTTPS certificates
```
chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh
```

### Project run
```
docker-compose up
```

### Apply migrations
```
docker-compose exec recipe_net_prod python manage.py migrate
```

### Create superuser
```
docker-compose exec recipe_net_prod python manage.py createsuperuser
```

### Fill the database with dummy data
```
docker-compose exec recipe_net_prod python manage.py loaddata dummy_data/db.json
```
