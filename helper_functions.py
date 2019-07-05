

def get_starting_lineup(lineup,gameID,gamePeriod):
    # Pulls the starting lineup for a given game and period from Game_Lineup.txt
    ## Inputs:
    ### lineup: game lineup data from Game_Lineup.txt
    ### gameID: Game_id from Play_by_Play.txt
    ### gamePeriod: Period from Play_by_Play.txt
    ## Outputs:
    ### lineup_dict: dictionary with Team_id as keys and Person_id as values

    subset = lineup[(lineup['Game_id']==gameID) & (lineup['Period']==gamePeriod)]
    teams = subset.Team_id.unique().tolist()
    lineup_dict = {}

    lineup_list=[]

    for i in range(2):
        lineup_dict[teams[i]] = subset[subset['Team_id']==teams[i]].Person_id.tolist()
        lineup_list.extend(subset[subset['Team_id']==teams[i]].Person_id.tolist())
    return lineup_list

def update_lineup(lineup_list,event):
    # Substitutes in player2 for player1.
    ## Inputs:
    ### lineup_dict: dictionary with Team_id as keys and Person_id as values
    ### team: Team_id from Play_by_Play.txt
    ### player1: Person_id from Play_by_Play.txt
    ### player2: Person_id from Play_by_Play.txt
    ## Outputs:
    ### lineup_dict: dictionary with Team_id as keys and Person_id as values

    if event['Event_Msg_Type']==8:
        #lineup_list.remove(event['Person1'])
        lineup_list_final = list(map(lambda b: b.replace(event['Person1'],event['Person2']), lineup_list))

        # print(event)
        # print(event['Person1'])
        # print(lineup_list)
        # print(lineup_list_final)



    #lineup_dict[team].remove(player1)
    #lineup_dict[team].append(player2)
        return lineup_list_final
    else:
        return lineup_list
    

def update_stats(stats,lineup_dict,event,action,person1,person2):
    # Uses the event and action as they pertain to person1 and person2 to update the stats according to the current lineup.
    return


