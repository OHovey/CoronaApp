from flask import Flask 
from flask_cors import CORS 
from flask_graphql import GraphQLView 
from apscheduler.scheduler import Scheduler

import atexit

from models import db_session 
from schema import schema 

from update import main as main_update

# ------------------------------

app = Flask(__name__) 
cors = CORS(app, resource = {r'/graphql/*': {'origins': "http://localhost:3000"}})
# crontab = Crontab(app)
app.debug = True 

# ------------------------------

# CRON JOBS HERE
cron = Scheduler(deamon = True) 
cron.start() 

@cron.interval_schedule(hours = 6)
def database_update():
    main_update()

# shutdown cron thread after web process is ended 
atexit.register(lambda: cron.shutdown(wait = False))
# -----------------------------

# Graphql setup
app.add_url_rule('/graphql',view_func = GraphQLView.as_view(
    'graphql',
    schema = schema,
    graphiql = True 
))

# ----------------------------- 

# app cleanup
@app.teardown_appcontext 
def shutdown_session(execption = None):
    db_session.remove() 

# -----------------------------

# main start
if __name__ == '__main__':
    app.run() 