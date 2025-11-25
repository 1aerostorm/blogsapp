## About project

All specified functionality has been implemented.

Stack used: Poetry, Django, DRF and MsSQL Server 2022. No cookie-cutter.

The "accounts" are not used from Django, but implemented by my own (and this decision is a bit controversial).

Security:
- Accounts in post views are "id+username+email", but email is for admin only, -> standard spam protection.
- "Limit" and "offset" have protection from too big (DoS vulnerability) or negative values.
- "Posts" using pure SQL queries (as in the task), but I think there is no SQL injections :)

Architecture:
- Strange :) and primitive. It is architecture built by person who sees Django first time in his life.
- But queries are separated from views, and validation separated, too. I think it is good.

## Production Usage

(note: port 8000 should be free)

```sh
docker compose up
```

http://127.0.0.1:8000/ - check running server

http://127.0.0.1:8000/admin - login with root:rootroot and create accounts, posts, comments

http://127.0.0.1:8000/api/posts - get posts
http://127.0.0.1:8000/api/posts?author_id=1 - by author
http://127.0.0.1:8000/api/posts?limit=2&offset=1 - pagination
http://127.0.0.1:8000/api/posts/?sort_by=title&sort_order=asc - sorting
http://127.0.0.1:8000/api/posts/?sort_by=created_at&sort_order=desc - sorting

http://127.0.0.1:8000/api/posts/1?comment_limit=1&comment_offset=0 - get post, with comment pagination

## Development

Start database in separate shell (note: expose 1433 port in docker-compose.yml):

```sh
docker compose up mssql initdb
```

Install MSSQL drivers (instruction for Ubuntu):

```sh
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
exit
sudo apt update
sudo ACCEPT_EULA=Y apt install msodbcsql18 unixodbc-dev
```

Install deps:

```sh
poetry install
```

Migrations:

```sh
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```
Undo migrations, clear database:
```sh
poetry run python manage.py migrate zero
```

How I created superuser:

```sh
poetry run python manage.py createsuperuser
root
root@root.ru
rootroot
```

Run server:

```sh
poetry run python manage.py runserver
```