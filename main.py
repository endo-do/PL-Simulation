from FixedTable import Table
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

        # setting up the table
        self.results_table = Table([[team["name"], 0, 0, 0] for team in self.teams.values()], header={"row":["Team",  "Points"], "col":["#default"]})

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

        draw = False

        # define which team has won 
        if team1_goals > team2_goals:
            win_team = team1["name"]
            lose_team = team2["name"]

        elif team2_goals > team1_goals:
            win_team = team2["name"]
            lose_team = team1["name"]
        
        # If draw set win and lose team to team1 detect later on a draw
        else:
            win_team = team1["name"]
            lose_team = team2["name"]
            draw = True
        
        # If one team has won
        if draw is False:
            self.results[win_team][0] += 1
            self.results[win_team][3] += 3
            self.results[lose_team][2] += 1
        
        else:
            self.results[win_team][1] += 1
            self.results[win_team][3] += 1
            self.results[lose_team][1] += 1
            self.results[lose_team][3] += 1

        new_content = [[team, value[3]] for team, value in self.results.items()]

        self.results_table.replace_content(new_content)
    
    # simulate a league with every team playing 2 times against each other team
    def play(self):

        # calculate amount of games
        amount_of_games = int((len(self.teams) * (len(self.teams))))

        self.team_names = [team for team in self.teams.keys()]
        self.results = {team:[0, 0, 0, 0] for team in self.teams} # W D L Points

        for i in range (amount_of_games):
            t1 = i // 20
            t2 = i % 20
            if t1 != t2:
                self.match(self.teams[self.team_names[t1]], self.teams[self.team_names[t2]])

        # display results
        self.results_table.display()
            
# create a League
PremierLeague= League(PATH)

# update its data -> calculate each teams attack and defence score
PremierLeague.update_data()

# let them play and print out the results in a table
PremierLeague.play()