# hotwire-django-realworld

A RealWorld Django app using Turbo. See [RealWorld](https://github.com/gothinkster/realworld). A live demo is [hosted on Heroku](https://hotwire-django-realworld.herokuapp.com/)

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

# License
hotwire-django-realworld is released under the MIT License to keep compatibility with both the Hotwire project and the [RealWorld starter kit](https://github.com/gothinkster/realworld-starter-kit).

If you submit a pull request. Remember to add yourself to CONTRIBUTORS.md!
