export FLASK_APP=server
export FLASK_ENV=production
#./uwsgi --http 0.0.0.0:7873 --module server:run_server_api
#./uwsgi --http-socket 0.0.0.0:7873 --wsgi-file server.py
python3 server.py