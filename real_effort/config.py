# format: endowment, multiplier, tax, transcription
import random
data = [
    [ 
        {"end": 1000, "multiplier": 2, "tax": 0.1, "transcription": True },
        {"end": 2000, "multiplier": 2, "tax": 0.2, "transcription": False },
        {"end": 3000, "multiplier": 2, "tax": 0.3, "transcription": True }
    ]



    
]

def export_data():
    data[0] = shuffle(data[0])
    return data

def shuffle(data):
    random.shuffle(data)
    return data
