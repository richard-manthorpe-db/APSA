# apiserver #
This is a useful Flask ApiServer containing enpoints for:

1. hello world
2. hello <name>
3. return small json array
4. git pull force/reset for commit hook call used for dags for airflow
5. return large json text


# To Run..

export FLASK_ENV=development
export FLASK_APP=myAPIServer.py
myAPIServernohup flask run --host=0.0.0.0 --port=7999 &