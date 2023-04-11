import os
from flask import Flask, render_template, request, jsonify
from validators import validate_user, validate_event, validate_coupon
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random

##########################################################################################
####################################### APP ##############################################
##########################################################################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geokaz'

##########################################################################################
##################################### DATABASE ###########################################
##########################################################################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

# api = Api(app)

##########################################################################################
###################################### MODELS ############################################
##########################################################################################
class Coupon(db.Model):
    
    __tablename__ = 'coupons'
    
    coupon_id = db.Column(db.String(50), primary_key=True)
    event_id = db.Column(db.String(50), db.ForeignKey('events.event_id'))   # Connecting the keys (events)
    odds = db.Column(db.Float)
    stake = db.Column(db.Float)
    timestamp = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))         # Connecting the keys (users)
    
    events = db.relationship('Event', backref='coupon')                     # ONE TO MANY, one coupon has many events 
    
    def __init__(self, coupon_id, event_id, odds, stake, timestamp, user_id):
        self.coupon_id = coupon_id
        self.event_id = event_id
        self.odds = odds
        self.stake = stake
        self.timestamp = timestamp
        self.user_id = user_id
    
    def json(self):
        return {
            'coupon_id': self.coupon_id,
            'event_id': self.event_id,
            'odds': self.odds,
            'stake': self.stake,
            'timestamp': self.timestamp,
            'user_id': self.user_id
        }
    
    
class User(db.Model):
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    birth_year = db.Column(db.Integer)
    country = db.Column(db.String(3))
    currency = db.Column(db.String(3))
    gender = db.Column(db.String(6))
    registration_date = db.Column(db.String())
    
    coupon = db.relationship('Coupon', backref='user')  # ONE TO ONE - user to coupon (to test it)
    
    def __init__(self, user_id, birth_year, country, currency, gender, registration_date):
        self.user_id = user_id
        self.birth_year = birth_year
        self.country = country
        self.currency = currency
        self.gender = gender
        self.registration_date = registration_date
    
    def json(self):
        return {
            'user_id': self.user_id,
            'birth_year': self.birth_year,
            'country': self.country,
            'currency': self.currency,
            'gender': self.gender,
            'registration_date': self.registration_date
        }
    
    
class Event(db.Model):
    
    __tablename__ = 'events'
    
    begin_timestamp = db.Column(db.String(50))
    country = db.Column(db.String(20))
    end_timestamp = db.Column(db.String(50))
    event_id = db.Column(db.String(50), primary_key=True)
    league = db.Column(db.String(20))
    participants = db.Column(db.String(20))
    sport = db.Column(db.String(20))
    
    def __init__(self, event_id, begin_timestamp, country, end_timestamp, league, participants, sport):
        self.event_id = event_id
        self.begin_timestamp = begin_timestamp
        self.country = country
        self.end_timestamp = end_timestamp
        self.league = league
        self.participants = participants
        self.sport = sport
        
    def json(self):
        return {
            'begin_timestamp': self.begin_timestamp,
            'country': self.country,
            'end_timestamp': self.end_timestamp,
            'event_id': self.event_id,
            'league': self.league,
            'participants': self.participants     # To convert string back to list
        }
    
##########################################################################################    

# APIs
# api.add_resource(Coupon, '/coupons')
# api.add_resource(User, '/users')
# api.add_resource(Event, '/events')

##########################################################################################
###################################### END POINTS ########################################
##########################################################################################
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/coupons')
def get_coupons():
    user = User.query.filter_by(user_id=1900271).first()           # IT WORKS
    coupon = Coupon.query.filter_by(user_id=user.user_id).first()  # IT WORKS
    
    return render_template('coupons.html', user=user, coupon=coupon)

@app.route('/events')
def get_events():
    user = User.query.filter_by(user_id=1900271).first()
    events = Event.query.all()
    return render_template('events.html', user=user, events=events)


@app.route('/coupon', methods=['POST'])
def get_coupon():
    try:
        user_data = validate_user(request.json) 
        
        user = User(user_id=user_data['user_id'], 
                    birth_year=user_data['birth_year'],
                    country=user_data['country'],
                    currency=user_data['currency'],
                    gender=user_data['gender'],
                    registration_date=user_data['registration_date'])
        db.session.add(user)
        db.session.commit()
        
        print(f"User with ID: {user_data['user_id']} has validated schema.")
        
        events = [
            {
                "begin_timestamp": "2020-02-08 18:00:00+00",
                "country": "Czech Republic",
                "end_timestamp": "2099-01-01 00:00:00+00",
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4ca",
                "league": "Extraliga",
                "participants": "Milan",
                "sport": "handball"
            },
            {
                "begin_timestamp": "2020-02-10 19:00:00+00",
                "country": "Spain",
                "end_timestamp": "2099-01-01 00:00:00+00",
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4cb",
                "league": "LaLiga",
                "participants": "Barcelona",
                "sport": "football"
            }
        ]
        
        event = {"event": events}  
        event = validate_event(event) 
        
        new_event = Event(begin_timestamp=event['event'][0]['begin_timestamp'],
                          country=event['event'][0]['country'],
                          end_timestamp=event['event'][0]['end_timestamp'],
                          event_id=event['event'][0]['event_id'],
                          league=event['event'][0]['league'],
                          participants=event['event'][0]['participants'],
                          sport=event['event'][0]['sport'])
        db.session.add(new_event)
        db.session.commit()
        
        print(f"Event with ID: {event['event'][0]['event_id']} has validated schema.")
        
        coupon = [
            {
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4ca",
                "odds": 3.97
            },
            {
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4cb",
                "odds": 2.9
            }
            ]
        
        # coupon = random.sample(coupon, 1)   # Gives a random coupon
        
        # if user_data['user_id'] % 2 == 0: # Gives a coupon according to user's id (even or odd)
        #     coupon = [coupon[0]]
        # else:
        #     coupon = [coupon[1]]
        
        output_data = {
            "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278aa",
            "selections": coupon,
            "stake": 40.8,
            "timestamp": "2020-01-01T01:05:01",
            "user_id": user_data["user_id"]
            }        
        output_data = validate_coupon(output_data)    
        print(f"Coupon with ID: {output_data['coupon_id']} has validated schema.") 
        
        new_coupon = Coupon(coupon_id=output_data['coupon_id'],
                            event_id=output_data['selections'][0]['event_id'],
                            odds=output_data['selections'][0]['odds'],
                            stake=output_data['stake'],
                            timestamp=output_data['timestamp'],
                            user_id=user_data['user_id'])
        db.session.add(new_coupon)
        db.session.commit()

        return jsonify(output_data), 200
    
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 400
        
     
if __name__ == '__main__':
    app.run(debug=True)