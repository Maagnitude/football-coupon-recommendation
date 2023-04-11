from recommendationapp import db

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