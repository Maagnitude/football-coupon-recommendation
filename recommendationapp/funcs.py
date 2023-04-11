from flask import request, jsonify
from recommendationapp import db
from recommendationapp.models import User, Event, Coupon
from recommendationapp.validators import validate_user, validate_event, validate_coupon
   
##########################################################################################

def get_event():
    user = User.query.filter_by(user_id=1900273).first()
    events = Event.query.all()
    print(events)
    return user, events

def get_a_coupon():
    user = User.query.filter_by(user_id=1900273).first()           # IT WORKS
    coupon = Coupon.query.filter_by(user_id=user.user_id).first()  # IT WORKS
    return user, coupon

def create_coupon():
    
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
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4cv",
                "league": "Extraliga",
                "participants": "Milan",
                "sport": "handball"
            },
            {
                "begin_timestamp": "2020-02-10 19:00:00+00",
                "country": "Spain",
                "end_timestamp": "2099-01-01 00:00:00+00",
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4cw",
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
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4cv",
                "odds": 3.97
            },
            {
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4cw",
                "odds": 2.9
            }
            ]
        
        # coupon = random.sample(coupon, 1)   # Gives a random coupon
        
        # if user_data['user_id'] % 2 == 0: # Gives a coupon according to user's id (even or odd)
        #     coupon = [coupon[0]]
        # else:
        #     coupon = [coupon[1]]
        
        output_data = {
            "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ai",
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