from Table import Table
import json

PATH = "Team_stats.json"

class Team():
    def __init__(self, attack, defence):
        self.attack = attack
        self.defence = defence

class League():
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = {}

    def handle_data(self):
        with open(self.data_path, 'r') as file:
            self.data = json.load(file)
        self.cleaned_data = {}
        for team in list(self.data.keys()):
            self.cleaned_data[self.data[team]["name"]] = self.data[team]
        for team in self.cleaned_data.values():
            del team["name"]
        print(self.cleaned_data)
        total_goals_conceded = sum([int(team["goals_conceded"]) * int(team["games_played"]) for team in self.cleaned_data.values()])
        total_teams = len(self.cleaned_data)
        avg_defence = total_goals_conceded / total_teams
        print(avg_defence)
        for team in self.cleaned_data:
            # defence_score = avg + conceded/game
            defence_score = avg_defence + self.cleaned_data[team]["goals_conceded"] / self.cleaned_data[team]["games_played"]

l1 = League(PATH)
l1.handle_data()