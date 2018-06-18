from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, levenshtein, distance_and_ok
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import math
import random

def writeText(text, fileName): 
    image = Image.open('real_effort/background.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('real_effort/Roboto-Regular.ttf', size=12)
    imageChars = 40
    numLines = len(text) / imageChars
    numLines = math.ceil(numLines)
    lines = []

    for i in range(numLines):
        if(imageChars * (i + 1) < len(text)):
            lines.append(text[imageChars * i : imageChars * (i+1)])
        else:
            lines.append(text[imageChars * i : len(text)])

    for i in range(numLines):
        (x, y) = (10, 20 * i)
        message = lines[i]
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), message, fill=color, font=font)

    image.save(fileName)

def getPageCode(self):
    config = Constants.config
    t_code = 0
    auth_code = config[0][self.round_number - 1]["mode"]

    if config[0][self.round_number - 1]["transcription"] == True:
        t_code = 1

    return "R" + str(self.round_number) + "_" + "T" + str(t_code) + "_" + "A" + str(auth_code)


class Introduction(Page):
    form_model = 'player'
    form_fields = ['spanish']
    """Description of the game: How to play and returns expected"""

    def is_displayed(self):
        if (self.round_number == 1):
            return True

        return False

class Transcribe(Page):
    form_model = 'player'
    form_fields = ['transcribed_text']

    # Don't display this Transcribe page if the "transcription" value in
    # the dictionary representing this round in config.py is False
    def is_displayed(self):
        if (Constants.config[0][self.round_number - 1]["transcription"] == False):
            return False

        # Don't display this Transcribe page for each player who has completed
        # the first transcription task
        for p in self.player.in_all_rounds():
            if(p.transcriptionDone):
                return False

        return True

    def vars_for_template(self):
        writeText("test for transcribe page #21983401-29384-129834-1283-4182-304981-2384-12348", 'real_effort/static/real_effort/paragraphs/{}.png'.format(2))
        pgCode = getPageCode(self)

        return {
            'image_path': 'real_effort/paragraphs/{}.png'.format(2), 
            'reference_text': Constants.reference_texts[1],
            'debug': settings.DEBUG,
            'required_accuracy': 100 * (1 - Constants.allowed_error_rates[1]),
            'pgCode': pgCode
        }

    def transcribed_text_error_message(self, transcribed_text):
        """Determines the player's transcription accuracy."""

        reference_text = Constants.reference_texts[1]
        allowed_error_rate = Constants.allowed_error_rates[1]
        distance, ok = distance_and_ok(transcribed_text, reference_text,
                                       allowed_error_rate)
        if ok:
            self.player.levenshtein_distance = distance
            self.player.ratio = 1 - distance / Constants.maxdistance2
        else:
            if allowed_error_rate == 0:
                return "The transcription should be exactly the same as on the image."
            else:
                return "This transcription appears to contain too many errors."

    def before_next_page(self):
        """Initialize payoff to have a default value of 0"""
        self.player.payoff = 0

        config = Constants.config
        self.player.income = config[0][self.round_number - 1]["end"]

        for prev_player in self.player.in_all_rounds():
            # Income calculation done here
            if prev_player.transcribed_text == None:
                prev_player.transcribed_text = ""
                prev_player.levenshtein_distance = 0

            self.player.ratio = 1 - prev_player.levenshtein_distance / Constants.maxdistance2
            self.player.income *= self.player.ratio
            print("inside transcribe results, player income is")

        self.player.transcriptionDone = True


class Transcribe2(Page):
    form_model = 'player'
    form_fields = ['transcribed_text2']

    def is_displayed(self):
        # Don't display this Transcribe page if the "transcription" value in
        # the dictionary representing this round in config.py is False
        if (Constants.config[0][self.round_number - 1]["transcription"] == False):
            self.player.ratio = 1
            return False

        # Don't display this Transcribe page for each player who has completed
        # the second transcription task
        for p in self.player.in_all_rounds():
            if(p.transcriptionDone): 
                return False

        return True


    def vars_for_template(self):
        pgCode = getPageCode(self)
        writeText("Test for transcribe page #1 lak;sjdfl;aksjdfl;aksjdfl;kjasdl;fkjals;dkfja;sldkjf;alskjdf;ajksdf;lajk;", 'real_effort/static/real_effort/paragraphs/{}.png'.format(1))

        return {
            'image_path': 'real_effort/paragraphs/{}.png'.format(1),
            'reference_text': Constants.reference_texts[0],
            'debug': settings.DEBUG,
            'required_accuracy': 100 * (1 - Constants.allowed_error_rates[0]),
            'pgCode': pgCode
        }

    def before_next_page(self):
        """Initialize payoff to have a default value of 0"""
        self.player.payoff = 0


"""
class TranscribeResults(Page):
    form_model = 'player'
    form_fields = []

    def is_displayed(self):
        # Don't display the TranscribeResults page listing each player's transcription
        # accuracy (levenshtein value) if the "transcription" value in
        # the dictionary representing this round in config.py is False
        if (Constants.config[0][self.round_number - 1]["transcription"] == False):
            return False

        # Don't display this TranscribeResults page for each player who has completed
        # the second transcription task
        for p in self.player.in_all_rounds():
            if(p.transcriptionDone):
                return False

        return True

    def vars_for_template(self):
        table_rows = []
        config = Constants.config
        self.player.income = config[0][self.round_number - 1]["end"]

        for prev_player in self.player.in_all_rounds():
        # Income calculation done here
            if prev_player.transcribed_text == None:
                prev_player.transcribed_text = ""
                prev_player.levenshtein_distance = 0

            row = { 
                'round_number': prev_player.round_number,
                'reference_text_length': len(Constants.reference_texts[1]),
                'transcribed_text_length': len(prev_player.transcribed_text),
                'distance': prev_player.levenshtein_distance,
                'ratio':   1 - prev_player.levenshtein_distance / Constants.maxdistance2,
            }

            self.player.ratio = 1 - prev_player.levenshtein_distance / Constants.maxdistance2
            self.player.income *= self.player.ratio
            print("inside transcribe results, player income is")

            table_rows.append(row)

        print("inside transcriberesults varsfortemplate")
        return {'table_rows': table_rows}

    def before_next_page(self):
        # Disables transcription for the rest of the game
        self.player.transcriptionDone = True
"""

class part2(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def contribution_max(self):
        """Dynamically sets the maximum amount of each player's income that he/she can report"""
        return self.player.income

    def vars_for_template(self):
        # If transcription mode is set to true for this round, set the player's income according
        # to their transcription accuracy
        config = Constants.config
        pgCode = getPageCode(self)
        endowment = config[0][self.round_number - 1]["end"]
        transcribe_on = config[0][self.round_number - 1]["transcription"]

        """
        if self.player.ratio == 1 and Constants.config[0][self.round_number - 1]["transcription"] == False:
            for p in self.player.in_all_rounds():
                if p.ratio < 1:
                    self.player.ratio = p.ratio
                    print("player income before is:", self.player.income)
                    self.player.income *= self.player.ratio
                    break

                    print("player income after is:", self.player.income)
        """

        # Displays the tax as a percentage rather than as a decimal between 0 and 1
        self.player.ratio = round(self.player.ratio, 5)
        displaytax = config[0][self.round_number - 1]["tax"] * 100

        display_ratio = self.player.ratio * 100
        display_income = int(self.player.income)

        return {'ratio': self.player.ratio, 'income': self.player.income, 'tax': displaytax,
                'flag': config[0][self.round_number - 1]["transcription"],
                'mult': config[0][self.round_number - 1]["multiplier"],
                'display_ratio': display_ratio, 'endowment': endowment,
                'display_income': display_income, 'transcribe_on': transcribe_on,
                'pgCode': pgCode
        }


class resultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        group = self.group

        # Generate a random player ID to determine who will be the authority
        group.random_player = random.randint(1, Constants.players_per_group)

        print("Random player's ID is: ", group.random_player)


class Authority(Page):
    form_model = 'group'
    form_fields = ['authority_multiply']

    def is_displayed(self):
        config = Constants.config
        group = self.group

        mode_num = config[0][self.round_number - 1]["mode"]

        if (mode_num == 1 and self.player.id_in_group == group.random_player):
            return True

    def vars_for_template(self):
        config = Constants.config
        pgCode = getPageCode(self)

        return {
            'mult': config[0][self.round_number - 1]["multiplier"],
            'pgCode': pgCode
        }


class AuthorityInfo(Page):
    def is_displayed(self):
        config = Constants.config
        group = self.group

        if (self.player.id_in_group == group.random_player):
            return False
        else:
            return True

    def vars_for_template(self):
        config = Constants.config
        group = self.group
        pgCode = getPageCode(self)

        mode_num = config[0][self.round_number - 1]["mode"]
        if(mode_num == 1 and group.authority_multiply):
            decision = Constants.decisions[1] + " " + str(config[0][self.round_number - 1]["multiplier"]) + "."
        elif(mode_num == 1 and not group.authority_multiply):
            decision = Constants.decisions[0]
        elif(mode_num == 2 and not group.auth_appropriate):
            decision = Constants.decisions[1] + " " + str(config[0][self.round_number - 1]["multiplier"]) + " ."
        else:
            decision = Constants.decisions[1] + " " + str(config[0][self.round_number - 1]["multiplier"]) + Constants.decisions[2] + str(config[0][self.round_number - 1]["tax"] * 100) + Constants.decisions[3]

        return {"decision": decision, 'pgCode': pgCode}


class Authority2(Page):
    form_model = 'group'
    form_fields = ['auth_appropriate']

    def is_displayed(self):
        config = Constants.config
        group = self.group

        mode_num = config[0][self.round_number - 1]["mode"]

        if (mode_num == 2 and self.player.id_in_group == group.random_player):
            return True

    def vars_for_template(self):
        config = Constants.config
        pgCode = getPageCode(self)

        displaytax = config[0][self.round_number - 1]["tax"] * 100

        return {
            'mult': config[0][self.round_number - 1]["multiplier"],
            'tax': displaytax, 'pgCode': pgCode
        }


class AuthorityWaitPage(WaitPage):
    def after_all_players_arrive(self):
        config = Constants.config
        group = self.group
        players = group.get_players()

        mode_num = config[0][self.round_number - 1]["mode"]
        tax = config[0][int(self.round_number - 1)]["tax"]
        multiplier = config[0][self.round_number - 1]["multiplier"]

        # NOTE: the code below can definitely be refactored (get rid of duplicate code), but I just want to see if
        # the functionality is correct first
        if(mode_num == 1 and group.authority_multiply):
            contributions = [p.contribution * tax for p in players]

            group.total_contribution = multiplier * sum(contributions)
            group.total_earnings = group.total_contribution

            group.individual_share = group.total_earnings / Constants.players_per_group

            for p in players:
                p.payoff = p.income - (tax * p.contribution) + group.individual_share

        # This below else if statement should never be executed
        elif(mode_num == 1 and not group.authority_multiply):
            contributions = [p.contribution * tax for p in players]
            group.total_contribution = sum(contributions)
            group.total_earnings = multiplier * group.total_contribution
            group.individual_share = group.total_earnings / Constants.players_per_group

            for p in players:
                p.payoff = p.income - (tax * p.contribution) + group.individual_share

        elif(mode_num == 2 and not group.auth_appropriate):
            contributions = [p.contribution * tax for p in players]

            group.total_contribution = multiplier * sum(contributions)
            group.total_earnings = group.total_contribution

            group.individual_share = group.total_earnings / Constants.players_per_group

            for p in players:
                p.payoff = p.income - (tax * p.contribution) + group.individual_share

        # Mode 2, Authority 2, Button 2
        else:
            contributions = [p.contribution * tax for p in players]

            group.total_contribution = multiplier * sum(contributions)
            group.total_earnings = group.total_contribution

            group.appropriation = tax * group.total_contribution
            group.total_earnings -= group.appropriation
            group.individual_share = group.total_earnings / Constants.players_per_group

            for p in players:
                if (p.id_in_group == group.random_player):
                    p.payoff = p.income - (tax * p.contribution) + group.individual_share
                    p.payoff += group.appropriation
                else:
                    p.payoff = p.income - (tax * p.contribution) + group.individual_share


class TaxResults(Page):
    def is_displayed(self):
        # May cause a problem, may change to something more direct later
        return self.player.payoff != 0

    def vars_for_template(self):
        config = Constants.config
        group = self.group
        player = self.player
        players = group.get_players()
        share = self.group.total_earnings / Constants.players_per_group
        tax = config[0][int(self.round_number - 1)]["tax"]
        multiplier = config[0][self.round_number - 1]["multiplier"]
        display_tax = tax * 100
        others_avg_income = 0
        pgCode = getPageCode(self)

        total_tax_contribution = sum([p.contribution * tax for p in players])

        for p in players:
            others_avg_income += p.contribution

        others_avg_income -= player.contribution
        others_avg_income /= (Constants.players_per_group - 1)

        return {
            'total_earnings': self.group.total_earnings, 'player_earnings': share,
            'avg_income': others_avg_income, 'num_other_players': Constants.players_per_group - 1,
            'total_tax_contribution': total_tax_contribution, 'multiplier': multiplier,
            'appropriation': group.appropriation,'tax': tax, 'display_tax': display_tax,
            'pgCode': pgCode
        }

"""
page_sequence = [Introduction, Transcribe2, Transcribe, TranscribeResults, part2, resultsWaitPage,
                 Authority,  Authority2, AuthorityWaitPage, AuthorityInfo, TaxResults]
"""

page_sequence = [Introduction, Transcribe2, Transcribe, part2, resultsWaitPage,
                 Authority,  Authority2, AuthorityWaitPage, AuthorityInfo, TaxResults]