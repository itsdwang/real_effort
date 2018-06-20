import random

# Dictionary Format: endowment, multiplier, tax, transcription
# Each dictionary entry represents the data values for 1 round
data = [
    [ 
        {"end": 1000, "multiplier": 2, "tax": 0.5, "transcription": True, "mode": 1, "difficulty": 1, "spanish": False, "penalty": 0.9, "appropriation_percent": 0.25},
        {"end": 2000, "multiplier": 2, "tax": 0.5, "transcription": True, "mode": 2, "difficulty": 2, "spanish": False, "penalty": 0.9,"appropriation_percent": 0.25},
        {"end": 3000, "multiplier": 2, "tax": 0.5, "transcription": False, "mode": 1, "difficulty": 3, "spanish": False, "penalty": 0.9, "appropriation_percent": 0.25},
        {"end": 4000, "multiplier": 2, "tax": 0.5, "transcription": True, "mode": 2, "difficulty": 4, "spanish": False, "penalty": 0.9, "appropriation_percent": 0.25}
    ]
]

def shuffle(data):
    # random.sample does not shuffle data in place. random.shuffle would work in this case but
    # could lead to bugs if we are say trying to write the data to csv after having used
    # it in the experiment.
    return [random.sample(data[0], k=len(data[0]))]

def export_data():
    return shuffle(data)
