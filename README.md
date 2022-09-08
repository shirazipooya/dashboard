# Install PostgreSQL and PostGIS on Ubuntu
- 1. sudo apt-get update && sudo apt-get upgrade -y
- 2. sudo apt -y install gnupg2
- 3. wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
- 4. sudo apt install postgresql postgresql-contrib postgis postgresql-postgis 
- 5. sudo apt install postgis postgresql-14-postgis-3
- 6. sudo service postgresql start
- 7. sudo -u postgres psql
- 8. ALTER USER postgres PASSWORD '1234';

# Install psycopg2 on Ubuntu
- 1. sudo apt-get install build-essential libpq-dev python3-dev

# Creation of Virtual Environments
- 1. python -m venv .venv
- 2. source .venv/bin/activate
- 3. python -m pip install --upgrade pip
- 4. pip install -r requirements.txt