teams = [f"Team {i}" for i in range(1, 11)]

def Hinrunde(teams):
    for team in teams:
        team1 = team
        for team2 in teams[teams.index(team1):]:
            if team1 != team2:
                print(f"Heim: {team1} | Aus: {team2}")
