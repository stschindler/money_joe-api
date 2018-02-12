# MoneyJoe API

## Development environment setup

The MoneyJoe API project comes with configuration files for both Vagrant and
Docker Compose. The following steps show you how to get an initial environment
up and running.

  1. `vagrant up && vagrant ssh`
  2. `cd /vagrant && sudo docker-compose up`
  3. Open 2nd session: `vagrant ssh`
  4. `cd /vagrant && sudo docker-compose exec --user 1000:1000 api sh`
  5. `python3 manage.py migrate && python3 manage.py load_demo_data`

The demo data includes the following accounts: (in case you change passwords at
any time, reloading demo data won't touch them!)

  * :bust_in_silhouette: stsch :key: roflcopter
  * :bust_in_silhouette: tisch :key: miabambina
  * :bust_in_silhouette: johndoe :key: jonnydonny

## Continuing development

After initializing the dev environment as described above, you only have to do
the following steps to continue development, e.g. after rebooting:

  1. `vagrant up && vagrant ssh`
  2. `cd /vagrant && sudo docker-compose up`

## Accessing the admin and API

Access the admin panel by going to http://localhost:8000/admin/

The GraphiQL interface can be reached at http://localhost:8000/graphql

## Cheatsheet

Shell access (run at Vagrant machine):

`docker-compose exec --user 1000:1000 api sh`

Migrate database:

`python3 manage.py migrate`

Load demo data:

`python3 manage.py load_demo_data`

Create superuser account:

`python3 manage.py createsuperuser`
