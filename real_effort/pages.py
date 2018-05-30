from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, levenshtein, distance_and_ok
from django.conf import settings
from . import config as config_py


class Transcribe(Page):
    form_model = 'player'
    form_fields = ['transcribed_text']
    def is_displayed(self):
        if(Constants.config[0][self.round_number-1]["transcription"] == False): #initial check for first round no transcribe
            self.player.ratio = 1 #sets up the game for no transcription
            return False
        for p in self.player.in_all_rounds(): #looks through the game history to see if transcription is done
            if(p.transcriptionDone):
                return False
        return True




        

    def vars_for_template(self): 
        config = Constants.config


        return {
            'image_path': 'real_effort/paragraphs/{}.png'.format(1), 
            'reference_text': Constants.reference_texts[0],
            'debug': settings.DEBUG,
            'required_accuracy': 100 * (1 - Constants.allowed_error_rates[0]),
        }

    def transcribed_text_error_message(self, transcribed_text): # Transcription accuracy check seems to work here

        reference_text = Constants.reference_texts[0]
        allowed_error_rate = Constants.allowed_error_rates[0]
        distance, ok = distance_and_ok(transcribed_text, reference_text,
                                       allowed_error_rate)
        if ok:
            self.player.levenshtein_distance = distance
            self.player.ratio = 1 - distance / Constants.maxdistance
        else:
            if allowed_error_rate == 0:
                return "The transcription should be exactly the same as on the image."
            else:
                return "This transcription appears to contain too many errors."

    def before_next_page(self):

        self.player.payoff = 0

class Transcribe2(Page): # Transcription task #2 (SHOULD be determining income)


    form_model = 'player'
    form_fields = ['transcribed_text2']
    def is_displayed(self):
        #basically same checks as transcribe 1
        if(Constants.config[0][self.round_number-1]["transcription"] == False): 
            return False
        for p in self.player.in_all_rounds():
            if(p.transcriptionDone): 
                return False
        return True


        

    def vars_for_template(self):
        config = Constants.config




        return {
            'image_path': 'real_effort/paragraphs/{}.png'.format(2),
            'reference_text': Constants.reference_texts[1],
            'debug': settings.DEBUG,
            'required_accuracy': 100 * (1 - Constants.allowed_error_rates[1]),
        }
        #  below function not working, always returns 1
    def transcribed_text_error_message(self, transcribed_text2): #where is this function being called? 
        reference_text = Constants.reference_texts[1]  
        allowed_error_rate = Constants.allowed_error_rates[1]
        distance, ok = distance_and_ok(self.player.transcribed_text2, reference_text,
                                       allowed_error_rate)
        if ok:
            self.player.levenshtein_distance = distance
            self.player.ratio = 1 - distance / Constants.maxdistance
        else:
            if allowed_error_rate == 0:
                return "The transcription should be exactly the same as on the image."
            else:
                return "This transcription appears to contain too many errors."

    def before_next_page(self):

        self.player.payoff = 0


class Results(Page):
    form_model = 'player'
    form_fields = []
    def is_displayed(self):
        if(Constants.config[0][self.round_number-1]["transcription"] == False): # same checks as transcribe 1
            return False
        for p in self.player.in_all_rounds():
            if(p.transcriptionDone):
                return False
        return True


    def vars_for_template(self):


        table_rows = []
        config = Constants.config
        self.player.income = config[0][self.round_number-1]["end"]
        print(self.player.income)

        for prev_player in self.player.in_all_rounds(): # may be causing the wrong ratio 
        #income calculation done here
            if prev_player.transcribed_text == None:
                prev_player.transcribed_text = ""
                prev_player.levenshtein_distance = 0


            row = { 
                'round_number': prev_player.round_number,
                'reference_text_length': len(Constants.reference_texts[1]),
                'transcribed_text_length': len(prev_player.transcribed_text),
                'distance': prev_player.levenshtein_distance,
                'ratio':   1 - prev_player.levenshtein_distance / Constants.maxdistance,
            }
            self.player.ratio = 1 - prev_player.levenshtein_distance / Constants.maxdistance
            self.player.income *= self.player.ratio
            
        
            



            
            table_rows.append(row)


        return {'table_rows': table_rows}
    def before_next_page(self):
        
        self.player.transcriptionDone = True #disables transcription for the rest of the game


class part2(Page):


    form_model = 'player'
    form_fields = ['contribution']

    
    def vars_for_template(self):

        config = Constants.config

        # for display purposes
        self.player.ratio = round(self.player.ratio,5) 
        displaytax = config[0][self.round_number-1]["tax"] * 100
        


        return{'ratio': self.player.ratio, 'income': self.player.income, 'tax': displaytax, 'flag': config[0][self.round_number-1]["transcription"]}
        





class resultsWaitPage(WaitPage):
    


    def after_all_players_arrive(self):
        #group income calculation
        config = Constants.config

        group = self.group
        players = group.get_players()
        contributions = [p.contribution * config[0][int(self.round_number-1)]["tax"] for p in players]
        group.total_contribution = sum(contributions)
        group.total_earnings = config[0][self.round_number-1]["multiplier"] * group.total_contribution
        group.individual_share = group.total_earnings / Constants.players_per_group
        for p in players:

            print("player income")
            print(type(p.income))
            print(p.income)


            p.payoff = p.income - ( config[0][int(self.round_number - 1)]["tax"] * p.contribution) + group.individual_share

class results2(Page):
    #basically only views
    
    def is_displayed(self): 
        return self.player.payoff != 0 #may cause problems, may change to something more direct later
    def vars_for_template(self):
        print("in results2")
        print(self.round_number)
        config = Constants.config
        share = self.group.total_earnings / Constants.players_per_group

        return{
            'total_earnings': self.group.total_contribution * config[0][int(self.round_number-1)]["multiplier"], 'player_earnings': share
        }














#page_sequence = [Transcribe, Results, part2, resultsWaitPage, results2,resetPage]
page_sequence = [Transcribe,Transcribe2,Results,part2,resultsWaitPage, results2]
# 














