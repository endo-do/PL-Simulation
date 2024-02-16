from Table import Table
import json
import random

#HashtagForBob

# Path for the stats file
PATH = "Team_stats.json"

# Defining a League Class where will be defining all the functions we'll need
class League():
    
    # The league class has to be defined with the var 'data_path'
    def __init__(self, data_path):
        self.data_path = data_path
        
        # self.teams is defined as empty dict. We'll be storing all the data for the teams in this dict
        self.teams = {}
        self.season = 1

    # Function to update the data in the json file. -> Recalculate attack and defence score based on games played, goals scored and conceded
    def update_data(self):
        
        # Open the json file and read all the data and save it as self.data
        with open(self.data_path, 'r') as file:
            self.data = json.load(file)

        # calculate the avg defence score based on the read data
        total_goals_conceded = sum([int(team["goals_conceded"]) / int(team["games_played"]) for team in self.data.values()])
        total_teams = len(self.data)
        avg_defence = total_goals_conceded / total_teams
        
        # for each team calculate attack and defence score and add those to the self.data dict
        for team in self.data:
            
            defence_score = avg_defence - self.data[team]["goals_conceded"] / self.data[team]["games_played"]
            self.data[team]["defence"] = defence_score / 90
            
            attack_score = self.data[team]["goals_scored"] / self.data[team]["games_played"]
            self.data[team]["attack"] = attack_score / 90

        # write the self.data dict back into the json file with the updated attack and defence scores for each team
        with open(PATH, 'w') as f:
            json.dump(self.data, f, indent=4)

        # save the data as self.teams
        self.teams = self.data

    # Function for matching 2 teams and letting them play
    def match(self, team1, team2):
        
        # set scored goals to 0
        team1_goals = 0
        team2_goals = 0
        
        # for each minute
        for i in range(90):
            
            # calculate if team1 will score a goal. If True add a goal the team1's goals
            team1_attempt = random.random()
            if team1["attack"] - team2["defence"] >= team1_attempt:
                team1_goals += 1
            
            # same for team2
            team2_attempt = random.random()
            if team2["attack"] - team1["defence"] >= team2_attempt:
                team2_goals += 1

        # define which team has won 
        if team1_goals > team2_goals:
            win_team = team1
            lose_team = team2

        elif team2_goals > team1_goals:
            win_team = team2
            lose_team = team1
        
        # If draw set win and lose team to team1 detect later on a draw
        else:
            win_team = team1
            lose_team = team1
        
        # If one team has won
        if win_team != lose_team:

            # get current wins from winning team from the table
            score = int(self.results.get_cell(self.team_names.index(win_team["name"]), self.season))
            # add 1 to the wins
            self.results.replace_cell(self.team_names.index(win_team["name"]), self.season, score + 3)

            # same for losing team and losses
            score = int(self.results.get_cell(self.team_names.index(lose_team["name"]), self.season))
            # add 1 to losses
            self.results.replace_cell(self.team_names.index(lose_team["name"]), self.season, score + 0)

        # if draw
        else:
            # for both teams get current draw score and add 1
            
            score = int(self.results.get_cell(self.team_names.index(team1["name"]), self.season))
            self.results.replace_cell(self.team_names.index(team1["name"]), self.season, score + 1)

            score = int(self.results.get_cell(self.team_names.index(team2["name"]), self.season))
            self.results.replace_cell(self.team_names.index(team2["name"]), self.season, score + 1)
    
    
    # simulate a league with every team playing 2 times against each other team
    def play(self):

        # set a list with all the teams which we'll need later for calculations
        self.team_names = [team for team in self.teams.keys()]
        
        # setting up the table
        self.results = Table([[team["name"], 0, 0, 0] for team in self.teams.values()])
        self.results.conf_header("row", "add", ["Team",  "Points1", "Points2", "Points3"])
        self.results.conf_header("col", "add", ["#default"])

        # calculate amount of games
        amount_of_games = int((len(self.teams) * (len(self.teams))))

        for i in range (amount_of_games):
            t1 = i // 20
            t2 = i % 20
            if t1 != t2:
                self.match(self.teams[self.team_names[t1]], self.teams[self.team_names[t2]])

        # display results
        self.results.display()
            
# create a League
PremierLeague= League(PATH)

# update its data -> calculate each teams attack and defence score
PremierLeague.update_data()

# let them play and print out the results in a table
for i in range (3):
    PremierLeague.play()
    PremierLeague.season += 1