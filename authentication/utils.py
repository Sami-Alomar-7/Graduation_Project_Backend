def message(en,ar,status):
    return {
        "message":{
            "status":str(status),
            "en":str(en),
            "ar":str(ar),
        }
    }

def generate_random_otp() -> str:
    import random
    otp = random.randint(100000, 999999)
    return otp