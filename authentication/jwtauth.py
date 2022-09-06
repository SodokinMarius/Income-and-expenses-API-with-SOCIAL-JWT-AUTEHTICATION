import jwt 

def encode(token,key,algorithm=['HS256']):
    try:
        encode=jwt.encode(token,key,algorithm)
            
        return encode    

    except jwt.InvalidAlgorithmError:
        raise  jwt.exceptions ("Used algorithm error")
    except jwt.InvalidKeyError:
        raise jwt.exceptions ("Invalid key !!")
    except jwt.InvalidTokenError:
        raise jwt.exceptions ("Token Invalid  !!")


def encode(token,key,algorithm=['HS256']):
    try:
        decode=jwt.decode(token,key,algorithm)
            
        return decode    

    except jwt.InvalidAlgorithmError:
        raise  jwt.exceptions ("Used algorithm error")
    except jwt.InvalidKeyError:
        raise jwt.exceptions ("Invalid key !!")
    except jwt.InvalidTokenError:
        raise jwt.exceptions ("Token Invalid  !!")
     


