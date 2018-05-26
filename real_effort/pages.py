from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, levenshtein, distance_and_ok
from django.conf import settings
from . import config as config_py


class Transcribe(Page):
    form_model = 'player'
    form_fields = ['transcribed_text']

        

    def vars_for_template(self):
        config = Constants.config


        return {
            'image_path': 'real_effort/paragraphs/{}.png'.format(
                self.round_number),
            'reference_text': Constants.reference_texts[self.round_number - 1],
            'debug': settings.DEBUG,
            'required_accuracy': 100 * (1 - Constants.allowed_error_rates[self.round_number - 1]),
            'placeholder': config[0][0]["end"]
        }

    def transcribed_text_error_message(self, transcribed_text):
        reference_text = Constants.reference_texts[self.round_number - 1]
        allowed_error_rate = Constants.allowed_error_rates[
            self.round_number - 1]
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


class Results(Page):
    form_model = 'player'
    form_fields = []
    
    def is_displayed(self):
        return self.round_number == Constants.number_game_rounds

    def vars_for_template(self):
        table_rows = []
        config = config_py.export_data()

        for prev_player in self.player.in_all_rounds():
            row = {
                'round_number': prev_player.round_number,
                'reference_text_length': len(Constants.reference_texts[prev_player.round_number - 1]),
                'transcribed_text_length': len(prev_player.transcribed_text),
                'distance': prev_player.levenshtein_distance,
                'ratio':   1 - prev_player.levenshtein_distance / Constants.maxdistance,
            }
            self.player.ratio = 1 - prev_player.levenshtein_distance / Constants.maxdistance
            print("flag")
            print(self.round_number)
            self.player.income = config[0][self.round_number-2]["end"] * self.player.ratio
            



            
            table_rows.append(row)

        return {'table_rows': table_rows}


class part2(Page):
    form_model = 'player'
    form_fields = ['contribution']
    def vars_for_template(self):
        config = config_py.export_data()



        self.player.ratio = round(self.player.ratio,5)
        displaytax = config[0][self.round_number-2]["tax"] * 100


        return{'ratio': self.player.ratio, 'income': self.player.income, 'tax': displaytax}
        




    def is_displayed(self):
        return self.round_number == 2

class resultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.contribution != -1



    def after_all_players_arrive(self):
        config = config_py.export_data()

        group = self.group
        players = group.get_players()
        contributions = [p.contribution * config[0][self.round_number-2]["tax"] for p in players]
        group.total_contribution = sum(contributions)
        group.total_earnings = config[0][self.round_number-2]["multiplier"] * group.total_contribution
        group.individual_share = group.total_earnings / Constants.players_per_group
        for p in players:
            p.payoff = p.income - ( config[0][self.round_number-2]["tax"] * p.contribution) + group.individual_share

class results2(Page):
    def is_displayed(self):
        return self.player.payoff != 0
    def vars_for_template(self):
        config = config_py.export_data()
        share = self.group.total_earnings / Constants.players_per_group
        return{
            'total_earnings': self.group.total_contribution * config[0][self.round_number-2]["multiplier"], 'player_earnings': share
        }














page_sequence = [Transcribe, Results, part2, resultsWaitPage, results2]
