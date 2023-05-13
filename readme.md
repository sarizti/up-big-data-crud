Readme
======

Useful commands
---------------

Sometimes you need to execute commands in the pipenv directly instead of using the IDE gui. Open the terminal and use

```sh
pipenv shell
```

Django needs some db tables to make its own administration, just run migrate to make the initial setup.

```sh
python manage.py migrate
```

Sometimes this package is out of date in python installations, so the America/Mexico_City timezone is not found.

```sh
pip install pytz tzdata --upgrade
```

If for whatever reason you don't have pipenv installed, use this

```sh
python -m pip install --upgrade pip
python -m pip install --upgrade pipenv
```

SQL Scripts
-----------

After the initial migrate command, you should see the `db.sqlite3` file in your project files. If not, refresh the view.
Double-click the file. It should be added as a data source in the database section.

For this course, we need to have the tables found in `campus/sql`, so open those files and execute them in the sqlite
database that the `migrate` command created: `db.sqlite3`.
