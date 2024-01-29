from Table import Table
import json
#HashtagForBob
PATH = "Team_stats.json"

class League():
    def __init__(self, data_path):
        self.data_path = data_path
        self.teams = {}

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

        self.teams = self.cleaned_data

    def match(self, team1, team2):
        print(f"{team1["name"]} vs {team2["name"]}")

    def play(self):
        amount_of_games = int((len(self.teams) * (len(self.teams))))

        team_names = [team for team in self.teams.keys()]
        for i in range (amount_of_games):
            t1 = i // 20
            t2 = i % 20
            if t1 != t2:
                self.match(self.teams[team_names[t1]], self.teams[team_names[t2]])
            


PremierLeague= League(PATH)
PremierLeague.update_data()
PremierLeague.play()