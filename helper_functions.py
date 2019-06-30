def get_lineup(lineup,gameID,gamePeriod):
    # This function pulls the starting lineup for a given game and period from Game_Lineup.txt
    ## Inputs:
    ### lineup: game lineup data from Game_Lineup.txt
    ### gameID: Game_id from Play_by_Play.txt
    ### gamePeriod: Period from Play_by_Play.txt
    ## Outputs:
    ### lineup_dict: dictionary with Team_id as keys and Person_id as values

    subset = lineup[(lineup['Game_id']==gameID) & (lineup['Period']==gamePeriod)]
    teams = subset.Team_id.unique().tolist()
    lineup_dict = {}
    for i in range(2):
        lineup_dict[teams[i]] = subset[subset['Team_id']==teams[i]].Person_id.tolist()
    return lineup_dict

def update_lineup(lineup_dict,team,player1,player2):
    # This function substitutes in player2 for player1.
    ## Inputs:
    ### lineup_dict: dictionary with Team_id as keys and Person_id as values
    ### team: Team_id from Play_by_Play.txt
    ### player1: Person_id from Play_by_Play.txt
    ### player2: Person_id from Play_by_Play.txt
    ## Outputs:
    ### lineup_dict: dictionary with Team_id as keys and Person_id as values
    lineup_dict[team].remove(player1)
    lineup_dict[team].append(player2)
    return lineup_dict