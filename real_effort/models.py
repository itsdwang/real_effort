from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from . import config as config_py


doc = """
This is a task that requires real effort from participants.
Subjects are shown two images of incomprehensible text.
Subjects are required to transcribe (copy) the text into a text entry field.
The quality of a subject's transcription is measured by the
<a href="http://en.wikipedia.org/wiki/Levenshtein_distance">Levenshtein distance</a>.
"""


def levenshtein(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def distance_and_ok(transcribed_text, reference_text, max_error_rate):
    error_threshold = len(reference_text) * max_error_rate
    distance = levenshtein(transcribed_text, reference_text)
    ok = distance <= error_threshold
    return distance, ok


class Constants(BaseConstants):
    config = config_py.export_data()
    name_in_url = 'real_effort'

    number_game_rounds = len(config[0])
    players_per_group = 2
    instructions_template = 'real_effort/InstructionsPG.html'

    reference_texts = [
        "Revealed preference",
        "Hex ton satoha egavecen. Loh ta receso minenes da linoyiy xese coreliet ocotine! Senuh asud tu bubo tixorut sola, bo ipacape le rorisin lesiku etutale saseriec niyacin ponim na. Ri arariye senayi esoced behin? Tefid oveve duk mosar rototo buc: Leseri binin nolelar sise etolegus ibosa farare. Desac eno titeda res vab no mes!",
    ]

    '''
        NOTES TO DAN AND JEFF:

        you were getting the increasing round number error because you were increasing the round
        number when you weren't supposed to. In the transcription task, the there is a different
        transcription page every round. In this experiment, that is not the case. You might have 
        2 transcription pages, but they must all be in the same round.
        The best way to implement this is by having a set number of reference texts that cannot be
        changed across experiments. Then, you need a page for each one. For now, assume that there
        will always be 2 texts to transcribe in transcribe mode.

        In pages.py, the page_sequence list at the bottom determines which round you are in. You
        start in round 1, and when the player has gone thru all the pages, the round number
        increments. Since you had it set to display the part 2 pages only when the round number is
        even, it will do 1 transcription task, not display any other pages, then move on to round 2,
        displaying all pages.

        Fix this.

        Please start thoroughly documenting all your code as you write it. These files will be read
        and edited a lot more often by econ grad students and by Kristian than they will by you.

        Also: please only host the real_effort directory on github. You should have a copy of the 
        base otree directory (in this case named public_goodsv2, and which contains settings.py
        and other files, along with any and all experiment repos) on your local machine, not as
        a git repo. To repeat: a directory (which is not instantiated as a git repo) 
        on your computer, should hold all the shit that public_goodsv2/ holds rn. 
        real_effort should be a git repo stored on jeffrey's github. when you push and pull,
        you are only pushing and pulling the real_effort repo and all the shit in it.

        summary:

        page sequence
        initial instructions
        (transcription mode only, round 1 only) transcrption instructions
        (transcription mode only, round 1 only) transcription page 1
        (transcription mode only, round 1 only) transcription page 2
        (transcription mode only, round 1 only) transcription results
        tax instructions
        tax page 1
        tax page 2
        tax page 3
        ...
        tax page n, n = Constants.num_rounds
        (round Constants.num_rounds only) Results

    
        Transcription mode:
            2 pages, player transcribes a thing on each one.
            only the second one (longer one) determines their ratio and therefore their endowment
            all transcrition shit only happens on round 1, and players endowment afterward is 
            set in player.participant.vars. See the otree docs.

        Non-transcription mode/after transcription pages are gone thru
            tax pages, 1 per round
            results wait page after last tax page
            results after wait page, with payoffs set using a result from a randomly chosen
            round of taxes. same round for all players.

        0. Find a time to (both of u at same time) skype kristian and talk about this ASAP.
        1. implement transcription mode causing transcription pages to show or not.
        2. fix page sequence thing
        3. change how the experiment is hosted on github
        4. add documentation
        5. test and make sure it all works

        

    '''
    # num_rounds = len(reference_texts) * number_game_rounds    
    num_rounds = number_game_rounds
    maxdistance = len(reference_texts[1])
    allowed_error_rates = [0, 0.99]
    


class Subsession(BaseSubsession):
    
    # to create groups of size Constants.players_per_group every round by randomly selecting
    # Constants.players_per_group players from all players in the subsession and assigning them
    # to a group
    def creating_session(self):
        self.group_randomly()
        for p in self.get_players():
            p.participant.vars[0] = {}
            p.participant.vars[0]['transcribeDone'] = False
            p.participant.vars[self.round_number] = {}



class Group(BaseGroup): 
    total_report = models.CurrencyField()
    total_contribution = models.IntegerField()
    total_earnings = models.IntegerField()
    individual_share = models.FloatField()



class Player(BasePlayer):
    transcribed_text = models.LongStringField()
    transcribed_text2 = models.LongStringField()
    levenshtein_distance = models.IntegerField()
    ratio = models.FloatField()
    contribution = models.IntegerField(min=0, max=100000, initial = -1)
    income = models.FloatField()
    done = models.BooleanField()
    transcriptionDone = models.BooleanField()
    payoff = models.FloatField()
    def method(self):
        self.participant.vars['transcribeDone'] = False
