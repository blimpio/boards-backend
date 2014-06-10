# Blimp Boards Backend

[![Build Status](https://travis-ci.org/GetBlimp/boards-backend.svg?branch=dev)](https://travis-ci.org/GetBlimp/boards-backend)

## Install

```
$ git clone git@github.com:GetBlimp/boards-backend.git
$ cd boards-backend/
$ pip install -r requirements.txt
```

## Environment
Create an .env file in the root of the project.

```
ENVIRONMENT=DEVELOPMENT
DJANGO_SECRET_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
BLIMP_PREVIEWS_ACCOUNT_ID=
BLIMP_PREVIEWS_SECRET_KEY=
BLIMP_PREVIEWS_URL=
```

## First time setup

```
$ ./manage.py syncdb --noinput
$ ./manage.py migrate apps.users
$ ./manage.py migrate
$ ./manage.py loaddata blimp_boards/users/fixtures/users.json
```

## Running web server

```
$ ./manage.py runserver_plus
```

## Running tests

```
$ ./manage.py test --configuration=Testing
```

## Running tests with tox

```
$ pip install tox
$ tox
```

## Code coverage

```
$ pip install coverage
$ coverage run --source='.' manage.py test --configuration=Testing
$ coverage report --show-missing --omit='*migrations*'
```
