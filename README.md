# Blimp Boards Backend

[![Build Status](https://travis-ci.org/GetBlimp/boards-backend.svg?branch=dev)](https://travis-ci.org/GetBlimp/boards-backend) [![Dependency Status](https://gemnasium.com/GetBlimp/boards-backend.svg)](https://gemnasium.com/GetBlimp/boards-backend)

## Install

```
$ git clone git@github.com:GetBlimp/boards-backend.git
$ cd boards-backend/
$ pip install -r requirements.txt
```

## Environment
Create an `.env` file in the root of the project based on `.env.example`.

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
