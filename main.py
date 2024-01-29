from Table import Table
import json
#HashtagForBob
PATH = "Team_stats.json"

class League():
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = {}

    def update_data(self):
        
        with open(self.data_path, 'r') as file:
            self.data = json.load(file)

        self.cleaned_data = self.data

        total_goals_conceded = sum([int(team["goals_conceded"]) / int(team["games_played"]) for team in self.cleaned_data.values()])
        total_teams = len(self.cleaned_data)
        avg_defence = total_goals_conceded / total_teams
        
        for team in self.cleaned_data:
            
            defence_score = avg_defence - self.cleaned_data[team]["goals_conceded"] / self.cleaned_data[team]["games_played"]
            self.cleaned_data[team]["defence"] = defence_score / 90
            
            attack_score = self.cleaned_data[team]["goals_scored"] / self.cleaned_data[team]["games_played"]
            self.cleaned_data[team]["attack"] = attack_score / 90

        with open(PATH, 'w') as f:
            json.dump(self.cleaned_data, f, indent=4)


l1 = League(PATH)