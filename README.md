# Blimp Boards Backend

![wercker status](https://app.wercker.com/status/eee8e64a497f80d5367f9012fd2aff4a "wercker status")

## Install

```
git clone git@github.com:GetBlimp/boards-backend.git
cd boards-backend/
pip install -r requirements.txt
```

## First time setup

```
./manage.py syncdb --noinput
./manage.py loaddata blimp/users/fixtures/users.json
```

## Running web server

```
./manage.py runserver_plus
```

## Running websockets server

```
python ws.py --debug
```
