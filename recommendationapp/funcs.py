from flask import jsonify
from recommendationapp.models import User, Event, Coupon, Odd
from recommendationapp.validators import validate_user, validate_event, validate_coupon
from typing import Tuple, Union, List
from sqlalchemy.orm import Session
import datetime
import uuid
import random

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
        # user_ids = [str(user_data['user_id']) for user_data in users]
        # print(f"Users with IDs: {', '.join(user_ids)} have been created.")
        user_objects.append("Users created successfully")
        return user_objects, 200
    except Exception as e:
        error_message = str(e)
        if error_message.__contains__("UNIQUE constraint failed"):
            return f"User creation failed! There is a user with the same ID! (user_id={user_data['user_id']})", 400
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
            return user_dict, 200
        else: 
            return jsonify(f"User with ID: {wanted_user['user_id']} doesn't exist!"), 400
    except Exception as e:
        error_message = str(e)
        return error_message, 400

def find_all_users()-> Tuple[str, Union[dict, User]]:
    users = User.query.all()
    users_list=[]
    for user in users:
        user_dict = {
                    "user_id": user.user_id,
                    "birth_year": user.birth_year,
                    "country": user.country,
                    "currency": user.currency,
                    "gender": user.gender,
                    "registration_date": user.registration_date
                }
        users_list.append(user_dict)
    return users_list, 200

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
        db_session.add_all(event_objects)
        db_session.commit()
        
        # event_matches = [str(f'{event_data["home"]} vs {event_data["away"]}') for event_data in events]
        # print(f"Events: {', '.join(event_matches)} have been created.")
        event_objects.append("Events created successfully")
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
                    "begin_timestamp": event.begin_timestamp,
                    "country": event.country,
                    "end_timestamp": event.end_timestamp,
                    "event_id": event.event_id,
                    "league": event.league,
                    "participants": event.participants,
                    "sport": event.sport
            }
        events_list.append(event_dict)
    return events_list, 200

# ODDS FUNCTIONS
def create_odds(odds: List[dict], db_session: Session)-> Tuple[str, Union[dict, List[Odd]]]:
    try:
        odd_objects = []
        for odd in odds:
            odd_obj = Odd(
                odd_id=odd['odd_id'], 
                event_id=odd['event_id'],
                odds = odd["odds"]
            )
            odd_objects.append(odd_obj)
        db_session.add_all(odd_objects)
        db_session.commit()
        odd_ids = [str(odd_data['event_id']) for odd_data in odds]
        # print(f"Odds with IDs: {', '.join(odd_ids)} have been created.")
        odd_objects.append("Odds created successfully")
        return odd_objects, 200
    except Exception as e:
        print(e)
        error_message = str(e)
        if error_message.__contains__("UNIQUE constraint failed"):
            return f"Odd creation failed! There is an odd with the same ID! (odd_id={odd['odd_id']})", 400
        return f"Odd creation failed! More details: {error_message}", 400
    
def find_all_odds()-> Tuple[str, Union[dict, Odd]]:
    odds = Odd.query.all()
    odds_list=[]
    for i, odd in enumerate(odds):
        odd_dict = {
                    "odd_id": odd.odd_id,
                    "event_id": odd.event_id,
                    "odds": odd.odds
                }
        odds_list.append(odd_dict) 
    return odds_list, 200    

# COUPON MEGA FUNCTION
def create_coupon(user_info: dict, db_session: Session)-> Tuple[str, Union[dict, List[Coupon]]]:
    try:
        wanted_user = User.query.filter_by(user_id=user_info['user_id']).first()
        if wanted_user is None:
            return jsonify(f"User with ID: {user_info['user_id']} doesn't exist!"), 400
        odds = Odd.query.all()
        if odds is None:
            return jsonify("There are no odds in the database!"), 400
        stake = user_info['stake']
        user_id = user_info['user_id']
        mode = user_info['mode']
        number_of_matchers = user_info['matches']
        
        odds_list=[]
        for odd in odds:
            odd_dict = {
                        "odd_id": odd.odd_id,
                        "event_id": odd.event_id,
                        "odds": odd.odds
                    }
            odds_list.append(odd_dict)

        selections = []
        if mode == "random":
            for _ in range(number_of_matchers):
                random_odds = random.choice(odds_list)
                selections.append({"event": random_odds["event_id"], "odd": random_odds["odds"]})
        elif mode == "high":
            for _ in range(number_of_matchers):
                max_odd = max(odds_list, key=lambda x: x['odds'])
                selections.append({"event": max_odd["event_id"], "odd": max_odd["odds"]})
                odds_list.remove(max_odd)
        elif mode == "low":
            for _ in range(number_of_matchers):
                min_odd = min(odds_list, key=lambda x: x['odds'])
                selections.append({"event": min_odd["event_id"], "odd": min_odd["odds"]})
                odds_list.remove(min_odd)
        else:
            return "Invalid mode!", 400
        
        coupons = {
            "coupon_id": str(uuid.uuid4()),
            "selections": selections,
            "stake": stake,
            "timestamp": str(datetime.datetime.now()),
            "user_id": user_id
        }
        coupons = validate_coupon(coupons)
        new_coupon = Coupon(coupon_id=coupons['coupon_id'],
                            selections=coupons['selections'],
                            stake=coupons['stake'],
                            timestamp=coupons['timestamp'],
                            user_id=coupons['user_id'])
        
        db_session.add(new_coupon)
        db_session.commit()
        return coupons, 200
    except Exception as e:
        error_message = str(e)
        return error_message, 400
    
def find_coupons(user_id):
    wanted_user = User.query.filter_by(user_id=user_id).first()
    if wanted_user is None:
        return jsonify(f"User with ID: {user_id} doesn't exist!"), 400
    coupons = Coupon.query.filter_by(user_id=user_id).all()
    coupons_list=[]
    for coupon in coupons:
        coupon_dict = {
                    "coupon_id": coupon.coupon_id,
                    "selections": coupon.selections,
                    "stake": coupon.stake,
                    "timestamp": coupon.timestamp,
                    "user_id": coupon.user_id
                }
        coupons_list.append(coupon_dict) 
    return coupons_list, 200