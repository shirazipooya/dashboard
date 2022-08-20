# KHRW Dashboard

## Creation of Virtual Environments

[]: python -m venv .venv
[]: source .venv/bin/activate
[]: python -m pip install --upgrade pip
[]: pip install -r requirements.txt

## Install PostgreSQL and PostGIS

- sudo apt update && sudo apt upgrade -y
- sudo apt -y install gnupg2
- wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
- echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee /etc/apt/sources.list.d/pgdg.list
- sudo apt install postgresql postgresql-contrib
  - psql --version
  - sudo service postgresql status
  - sudo service postgresql start
  - sudo service postgresql stope
  - sudo passwd postgres
    - 1234
    - ALTER USER postgres PASSWORD '1234';
  - sudo service postgresql start
  - sudo -u postgres psql
- sudo apt install postgis postgresql-14-postgis-3

## Create Database

- sudo -i -u postgres
- createdb layers -O postgres
- createdb hydrograph -O postgres
- createdb thiessen -O postgres
- psql -d layers
- CREATE EXTENSION postgis;
- \q
- psql -d thiessen
- CREATE EXTENSION postgis;
- \q

## Install psycopg2 on Ubuntu

- sudo apt-get install build-essential
- sudo apt-get install libpq-dev python3-dev
