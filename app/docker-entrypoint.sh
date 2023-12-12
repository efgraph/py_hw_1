#!/bin/sh
./wait-for-it.sh postgres:5432 -t 10 -- echo "postgres is up"
echo 'Load data'
python3 load_data.py
echo 'Run streamlit'
streamlit run app.py
exec "$@"