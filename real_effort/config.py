# format: endowment, multiplier, tax, transcription
import random
data = [
    [ 
        {"end": 1000, "multiplier": 2, "tax": 0.1, "transcription": True },
        {"end": 2000, "multiplier": 2, "tax": 0.2, "transcription": False },
        {"end": 3000, "multiplier": 2, "tax": 0.3, "transcription": True }
    ]



    
]

def shuffle(data):
    # random.sample does not shuffle data in place. random.shuffle would work in this case but
    # could lead to bugs if we are say trying to write the data to csv after having used
    # it in the experiment.
    return [random.sample(data[0], k=len(data[0]))]

def export_data():
    return shuffle(data)

