data = 'password:hjasdiebk456jhaccount:smytzek'

def store_data(payload: str):
    global data
    data = payload + data

def get_data(length: int) -> str:
    return data[:min(length, len(data) + 1)]
    
def heartbeat(length: int, payload: str) -> str:
    """Pre conditions"""
    assert length == len(payload), 'String lenght Cant be less or more than length'
    store_data(payload)
    assert data.startswith(payload) 
    """"Post conditions"""
    request = get_data(length)
    assert payload == request, 'Request -> Reply Missmatch'
    return request

