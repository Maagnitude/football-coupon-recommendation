import jsonschema

def validate_user(data):    
    schema = {
        "type": "object",
        "properties": {
            "birth_year": {"type": "integer"},
            "country": {"type": "string"},
            "currency": {"type": "string"},
            "gender": {"type": "string", "enum":["Male", "Female", "male", "female", "other"]},
            "registration_date": {"type": "string"},
            "user_id": {"type": "string"}
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
                        "odds": {"type": "number"}}
                    }
                },
            "stake": {"type": "number"},
            "timestamp": {"type": "string"},
            "user_id": {"type": "string"}
        },
        "required": ["coupon_id", "selections", "stake", "timestamp"]
    }
    jsonschema.validate(data, schema)
    return data

def validate_event(data): 
    schema = {
        "type": "object",
        "properties": {
            "event": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "begin_timestamp": {"type": "string"},
                        "country": {"type": "string"},
                        "end_timestamp": {"type": "string"},
                        "event_id": {"type": "string"},
                        "league": {"type": "string"},
                        "participants": {"type": "string"},
                        "sport": {"type": "string"}
                    },
                    "required": ["begin_timestamp", "country", "end_timestamp", "event_id", "league", "participants", "sport"]
                }
            }
        }
    }
    jsonschema.validate(data, schema)
    return data