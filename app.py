from flask import Flask, render_template, request, jsonify 
from validators import validate_user, validate_event, validate_coupon

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/coupons', methods=['POST'])
def get_coupons():
    try:
        user_data = validate_user(request.json) 
        print(f"User with ID: {user_data['user_id']} has validated schema.")
        
        events = [
            {
                "begin_timestamp": "2020-02-08 18:00:00+00",
                "country": "Czech Republic",
                "end_timestamp": "2099-01-01 00:00:00+00",
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4cf",
                "league": "Extraliga",
                "participants": [
                    "HC Zubri",
                    "HBC Ronal Jicin"
                ],
                "sport": "handball"
            },
            {
                "begin_timestamp": "2020-02-10 19:00:00+00",
                "country": "Spain",
                "end_timestamp": "2099-01-01 00:00:00+00",
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4ce",
                "league": "LaLiga",
                "participants": [
                    "FC Barcelona",
                    "Sevilla FC"
                ],
                "sport": "football"
            }
        ]
        
        event = {"event": events}  
        event = validate_event(event) 
        print(f"Event with ID: {event['event'][0]['event_id']} has validated schema.")
        
        coupon = [
            {
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4ce",
                "odds": 3.97
            },
            {
                "event_id": "2ff91a-09b3-41a2-a8c4-4a78ba85f4cf",
                "odds": 2.9
            }
            ]
        
        if user_data['user_id'] % 2 == 0:
            coupon = [coupon[0]]
        else:
            coupon = [coupon[1]]
        
        output_data = {
            "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
            "selections": coupon,
            "stake": 40.8,
            "timestamp": "2020-01-01T01:05:01",
            "user_id": user_data["user_id"]
            }        
        output_data = validate_coupon(output_data)    
        print(f"Coupon with ID: {output_data['coupon_id']} has validated schema.") 
        return jsonify(output_data), 200
    
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 400
        
     
if __name__ == '__main__':
    app.run(debug=True)