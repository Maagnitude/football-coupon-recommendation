import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

###################################################
###################### APP ########################
###################################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geokaz'

###################################################
#################### DATABASE #####################
###################################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# api = Api(app)

# APIs
# api.add_resource(Coupon, '/coupons')
# api.add_resource(User, '/users')
# api.add_resource(Event, '/events')

###################################################
################### BLUEPRINTS ####################
###################################################

from recommendationapp.core.views import core
from recommendationapp.events.views import events
from recommendationapp.coupons.views import coupons

app.register_blueprint(core)
app.register_blueprint(events)
app.register_blueprint(coupons)