import requests
import json 
def consume():

    response = requests.get('http://127.0.0.1:5000/filter')
    # print(response.json())
    responses = response.json
    
    x = []

    for artist in responses:
        
        data = ('id', 'album', 'artist', 'track')
        if len(artist) == len(data):
            res = {data[i] : artist[i] for i, _ in enumerate(artist)}
            x.append(res)
    print(x)  
            
    
    return x