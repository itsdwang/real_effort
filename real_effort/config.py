import random

# Dictionary Format: endowment, multiplier, tax, transcription
# Each dictionary entry represents the data values for 1 round
data = [
    [ 
        {"end": 1000, "multiplier": 2, "tax": 0.1, "transcription": True, "mode": 1},
        {"end": 2000, "multiplier": 3, "tax": 0.2, "transcription": True, "mode": 2},
        {"end": 3000, "multiplier": 4, "tax": 0.3, "transcription": True, "mode": 1}
    ]
]

def shuffle(data):
    # random.sample does not shuffle data in place. random.shuffle would work in this case but
    # could lead to bugs if we are say trying to write the data to csv after having used
    # it in the experiment.
    return [random.sample(data[0], k=len(data[0]))]

def export_data():
    return shuffle(data)