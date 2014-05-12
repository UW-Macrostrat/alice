#! /bin/bash

# Database Configuration
export DB_USER=john
export DB_PASSWORD=
export DB_PORT=5439
export DB_HOST=localhost

psql --set 'user='$DB_USER -p $DB_PORT -U $DB_USER -f alice.sql

python setup_db.py