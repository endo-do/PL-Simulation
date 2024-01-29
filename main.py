from Table import Table
import json
import random

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
        
        team1_goals = 0
        team2_goals = 0
        
        for i in range(90):
            
            team1_attempt = random.random()
            if team1["attack"] - team2["defence"] >= team1_attempt:
                team1_goals += 1
            
            team2_attempt = random.random()
            if team2["attack"] - team1["defence"] >= team2_attempt:
                team2_goals += 1

        if team1_goals > team2_goals:
            win_team = team1
            lose_team = team2
        elif team2_goals > team1_goals:
            win_team = team2
            lose_team = team1
        else:
            win_team = team1
            lose_team = team1

        if win_team != lose_team:

            score = int(self.results.get_cell(self.team_names.index(win_team["name"]), 1))
            self.results.replace_cell(self.team_names.index(win_team["name"]), 1, score + 1)

            score = int(self.results.get_cell(self.team_names.index(lose_team["name"]), 3))
            self.results.replace_cell(self.team_names.index(lose_team["name"]), 3, score + 1)

        else:
            score = int(self.results.get_cell(self.team_names.index(team1["name"]), 2))
            self.results.replace_cell(self.team_names.index(team1["name"]), 2, score + 1)

            score = int(self.results.get_cell(self.team_names.index(team2["name"]), 2))
            self.results.replace_cell(self.team_names.index(team2["name"]), 2, score + 1)
        
        print(f"{team1["name"]} {team1_goals} : {team2_goals} {team2["name"]}")
    
    
    def play(self):

        self.team_names = [team for team in self.teams.keys()]
        self.results = Table([[team["name"], 0, 0, 0] for team in self.teams.values()])
        self.results.conf_header("row", "add", ["Team",  "W", "D", "L"])
        self.results.conf_header("col", "add", ["#default"])
        self.results.display()

        amount_of_games = int((len(self.teams) * (len(self.teams))))

        for i in range (amount_of_games):
            t1 = i // 20
            t2 = i % 20
            if t1 != t2:
                self.match(self.teams[self.team_names[t1]], self.teams[self.team_names[t2]])

        self.results.display()
            
PremierLeague= League(PATH)
PremierLeague.update_data()
PremierLeague.play()