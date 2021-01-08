# hotwire-django-realworld

A RealWorld Django app using Turbo. See [RealWorld](https://github.com/gothinkster/realworld).

## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py createdata 10
./manage.py runserver
```

## Tests

Run `pytest`.
