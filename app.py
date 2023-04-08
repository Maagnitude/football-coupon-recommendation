from flask import Flask, render_template, request, jsonify 
import jsonschema

app = Flask(__name__)

def validate_user(data):
    
    schema = {
        "type": "object",
        "properties": {
            "birth_year": {"type": "integer"},
            "country": {"type": "string"},
            "currency": {"type": "string"},
            "gender": {"type": "string", "enum":["Male", "Female", "male", "female", "other"]},
            "registration_date": {"type": "string"},
            "user_id": {"type": "integer"}
        },
        "required": ["birth_year", "country", "currency", "gender", "registration_date", "user_id"]
    }
    jsonschema.validate(data, schema)
    return data


def validate_coupon(data):
    
    schema = {
        "type": "object",
        "properties": {
            "coupon_id": {"type": "string"},
            "selections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "event_id": {"type": "string"},
                        "odds": {"type": "float"}}
                    }
                },
            "stake": {"type": "float"},
            "timestamp": {"type": "string"},
            "user_id": {"type": "integer"}
        },
        "required": ["event_id", "odds", "stake", "timestamp", "user_id"]
    }
    jsonschema.validate(data, schema)
    return data


def validate_event(data):
    
    schema = {
        "type": "object",
        "properties": {
            "events": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "begin_timestamp": {"type": "string"},
                        "country": {"type": "string"},
                        "end_timestamp": {"type": "string"},
                        "event_id": {"type": "integer"},
                        "league": {"type": "string"},
                        "participants": {"type": "array", "items": {"type": "string"}},
                        "sport": {"type": "string"}
                    },
                    "required": ["begin_timestamp", "country", "end_timestamp", "event_id", "league", "participants", "sport"]
                }
            }
        }
    }
    jsonschema.validate(data, schema)
    return data
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/coupons', methods=['POST'])
def get_coupons():
    
    try:
        user_data = validate_user(request.json)
        
        event = [
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
        
        output_data = {
            "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
            "selections": coupon,
            "stake": 40.8,
            "timestamp": "2020-01-01T01:05:01",
            "user_id": user_data["user_id"]
            }
        
        # if user_data["user_id"] % 2 == 0:
        #     output_data = output_data["selections"][0]
        # else:
        #     output_data = output_data["selections"][1]
        
        
    
        # validate the output data
        output_data = validate_coupon(output_data)
        
        # return the output data
        return jsonify(output_data), 200
    
    except Exception as e:
        # return an error response if any exception occurs
        error_message = str(e)
        return jsonify({"error": error_message}), 400
        
    
    
if __name__ == '__main__':
    app.run(debug=True)