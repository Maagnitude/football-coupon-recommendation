from flask import request, jsonify
from recommendationapp import db
from recommendationapp.models import User, Event, Coupon
from recommendationapp.validators import validate_user, validate_event, validate_coupon
from typing import Tuple, Union, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

# USER FUNCTIONS
def create_user(users: List[dict], db_session: Session) -> Tuple[str, Union[dict, List[User]]]:
    try:
        user_objects = []
        for user in users:
            user_data = validate_user(user)
            user_obj = User(
                user_id=user_data['user_id'],
                birth_year=user_data['birth_year'],
                country=user_data['country'],
                currency=user_data['currency'],
                gender=user_data['gender'],
                registration_date=user_data['registration_date']
            )
            user_objects.append(user_obj)
        db_session.add_all(user_objects)
        db_session.commit()

        user_ids = [str(user_data['user_id']) for user_data in users]
        print(f"Users with IDs: {', '.join(user_ids)} have been created.")
        
        user_objects.append("Users created successfully")

        return user_objects, 200
    except Exception as e:
        error_message = str(e)
        return f"User creation failed! More details: {error_message}", 400

def find_user(wanted_user: dict)-> Tuple[str, Union[dict, User]]:
    try:
        user = User.query.filter_by(user_id=wanted_user['user_id']).first()
        if user is not None: 
            user_dict = {
                "user_id": user.user_id,
                "birth_year": user.birth_year,
                "country": user.country,
                "currency": user.currency,
                "gender": user.gender,
                "registration_date": user.registration_date
            }
            return jsonify("User found!", user_dict), 200
        else: 
            return jsonify(f"User with ID: {wanted_user['user_id']} doesn't exist!"), 400
    except Exception as e:
        error_message = str(e)
        return jsonify("User not found!", "More details: ", error_message), 400

def find_all_users()-> Tuple[str, Union[dict, User]]:
    users = User.query.all()
    users_list=[]
    for i, user in enumerate(users):
        user_dict = {
                f"User no. {i+1}": {
                    "user_id": user.user_id,
                    "birth_year": user.birth_year,
                    "country": user.country,
                    "currency": user.currency,
                    "gender": user.gender,
                    "registration_date": user.registration_date
                }
            }
        users_list.append(user_dict)
    return jsonify("List of all the users: ", users_list), 200

# EVENT FUNCTIONS
def create_event(events: List[dict], db_session: Session)-> Tuple[str, Union[dict, List[Event]]]:
    try:
        event_objects = []
        for event in events:
            event_data = validate_event(event)
            event_obj = Event(
                begin_timestamp=event_data['begin_timestamp'], 
                country=event_data['country'],
                end_timestamp=event_data['end_timestamp'],
                event_id=event_data['event_id'],
                league=event_data['league'],
                participants=f'{event_data["home"]} vs {event_data["away"]}',
                sport = event_data['sport']
            )
            event_objects.append(event_obj)
        db.session.add_all(event_objects)
        db.session.commit()
        
        event_ids = [str(event_data['user_id']) for event_data in events]
        print(f"Events with IDs: {', '.join(event_ids)} have been created.")
        
        event_objects.append("Users created successfully")
        return event_objects, 200
    except Exception as e:
        print(e)
        error_message = str(e)
        if error_message.__contains__("UNIQUE constraint failed"):
            return f"Event creation failed! There is an event with the same ID! (event_id={event_data['event_id']})", 400
        return f"Event creation failed! More details: {error_message}", 400

def find_event(wanted_event: dict)-> Tuple[str, Union[dict, Event]]:
    try:
        event = Event.query.filter_by(event_id=wanted_event['event_id']).first()
        if event is not None: 
            event_dict = {
                "begin_timestamp": event.begin_timestamp,
                "country": event.country,
                "end_timestamp": event.end_timestamp,
                "event_id": event.event_id,
                "league": event.league,
                "participants": event.participants,
                "sport": event.sport
            }
            return jsonify("Event found!", event_dict), 200
        else: 
            return jsonify(f"Event with ID: {wanted_event['event_id']} doesn't exist!"), 400
    except Exception as e:
        error_message = str(e)
        return jsonify("Event not found!", "More details: ", error_message), 400

def find_all_events()-> Tuple[str, Union[dict, Event]]:
    events = Event.query.all()
    events_list=[]
    for i, event in enumerate(events):
        event_dict = {
                f"Event no. {i+1}": {
                    "begin_timestamp": event.begin_timestamp,
                    "country": event.country,
                    "end_timestamp": event.end_timestamp,
                    "event_id": event.event_id,
                    "league": event.league,
                    "participants": event.participants,
                    "sport": event.sport
                }
            }
        events_list.append(event_dict)
    odds = Event.query.order_by(desc(Event.event_id)).all()[:5] # 5: number_of_matches, desc: descending order
    print(len(odds))  
    return jsonify("List of all the events: ", events_list), 200
        

# COUPON FUNCTIONS
def get_a_coupon():
    user = User.query.filter_by(user_id=1).first()           
    coupon = Coupon.query.filter_by(user_id=user.user_id).first()  
    events = Event.query.filter_by(event_id=coupon.event_id).all()
    # TODO : odds = Event.query.order_by(desc(Event.event_id)).all()[:5] # 5: number_of_matches, desc: descending order
    # TODO : odds = Event.query.order_by(Event.event_id).all()[:5] # 5: number_of_matches
    # TODO: random.choices(list, k=3) # 3: number_of_matches
    return user, coupon, events

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
                "begin_timestamp": "2020-02-09 18:00:00+00",
                "country": "England",
                "end_timestamp": "2099-01-01 00:00:00+00",
                "event_id": "event3",
                "league": "Premier League",
                "participants": "Liverpool",
                "sport": "football"
            },
            {
                "begin_timestamp": "2020-02-10 19:00:00+00",
                "country": "Italy",
                "end_timestamp": "2099-01-01 00:00:00+00",
                "event_id": "event4",
                "league": "Serie A",
                "participants": "Milan",
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
                "event_id": "event3",
                "odds": 3.34
            },
            {
                "event_id": "event4",
                "odds": 2.32
            }
            ]
        
        # coupon = random.sample(coupon, 1)   # Gives a random coupon
        
        # if user_data['user_id'] % 2 == 0: # Gives a coupon according to user's id (even or odd)
        #     coupon = [coupon[0]]
        # else:
        #     coupon = [coupon[1]]
        
        output_data = {
            "coupon_id": "coupon2",
            "selections": coupon,
            "stake": 32.8,
            "timestamp": "2020-01-09T01:05:01",
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