### What is PSP
It's a short for People shaping people.
It's simply a platform where people can share stories of how friends or loved ones have shaped their lives.
Read more [here](https://www.peopleshapingpeople.com/AboutUs/)

### Live
https://www.peopleshapingpeople.com


## Development
Built with Django stack.

### Features

    - Asyncronous chat system using sockets
    - Custom CMS (In retrospect, this might be an overkill, headless CMS would have been great)
    - Frontend using jinja

## Running App locally
Steps

- Create a virtual environment (Recommended, not required). [See how](https://www.javatpoint.com/django-virtual-environment-setup).
- Install dependencies - 
    `pip install -r requirements.txt`
- Make database migration - `python manage.py makemigrations`
- Migrate database - `python manage.py migrate`
- Run App - `python manage.py runserver`


### Possible Errors During setup

### Unable to install Twisted: [Ref here](https://github.com/cowrie/cowrie/issues/668)
 - `apt install python3-dev` To enabe compilation of package.
 - I did include the package on root directory, to allow me run app on heroku, you can also remove `Twisted` from `requirements.txt` file and install other packages. That works too.

## Env variables you need

### Email SMTP server (you could simply use django's console EmailBackend for local test puposes)
- EMAIL_BACKEND
- EMAIL_HOST
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
- EMAIL_PORT
- EMAIL_USE_TLS
- EMAIL_USE_SSL
- DEFAULT_FROM_EMAIL

### Django app variables
- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS

### Cloudinary credentials, used for accessing data storage
- cloud_name
- api_key
- api_secret

### Database credentials (you could simply use the sqlite dev db)
- DB_ENGINE
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT