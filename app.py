from flask import Flask 
from flask_cors import CORS 
from flask_graphql import GraphQLView 
# from flask_crontab import Crontab
# from crontab import CronTab 
from celery import Celery

from models import db_session 
from schema import schema 

app = Flask(__name__) 
cors = CORS(app, resource = {r'/graphql/*': {'origins': "http://localhost:3000"}})
# crontab = Crontab(app)
app.debug = True 

# def make_celery(app):
#     celery = Celery(app.import_name, backend = app.config['CELERY_RESULT'])

# cron job 
# @crontab.job(minute=0, hour=24)
# def retrieve_and_update_data():
#     cron = CronTab(user = 'root') 
#     job = cron.new(command = 'python update.py') 
#     cron.write()


app.add_url_rule('/graphql',view_func = GraphQLView.as_view(
    'graphql',
    schema = schema,
    graphiql = True 
))

@app.teardown_appcontext 
def shutdown_session(execption = None):
    db_session.remove() 

if __name__ == '__main__':
    app.run() 