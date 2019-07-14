def invert(d):
    return dict( (v,k) for k in d for v in d[k] )

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

    for i in range(2):
        lineup_dict[teams[i]] = subset[subset['Team_id']==teams[i]].Person_id.tolist()

    lineup_dict_new=invert(lineup_dict)
    return lineup_dict_new

def update_lineup(lineup,event):
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
        lineup_list_final = list(map(lambda b: b.replace(event['Person1'],event['Person2']), lineup.keys()))
        # if event['Person1'] not in lineup.keys():
        #     print(event)
        #     #print(lineup_dict.keys())

        lineup[event['Person2']]=lineup.pop(event['Person1'])

        #print(lineup_dict)
        #print('boom')


        #Changes required: WE HAVE TO ADD IN THE BEFORE AFTER FREE THROW CAVEAT TO THE SUBSTITUTION
       

        # print(event)
        # print(event['Person1'])
        # print(lineup_list)
        # print(lineup_list_final)

    #lineup_dict[team].remove(player1)
    #lineup_dict[team].append(player2)
        return lineup
    else:
        return lineup
    


def update_possessions(stats,lineup_dict,event,prev_team,prevPlayer):

    lineup_list=lineup_dict.keys()
    if event['Event_Msg_Type']== 1 or event['Event_Msg_Type']==5 or event['Event_Msg_Type']==3:

        #Consider edge case, event code 5,0 i.e. Turnover- No turnover, what does it mean?
        for each_player in lineup_list:
            stats[each_player]['Possessions']+=1
        #print(stats)
    elif event['Event_Msg_Type']==4 and event['Action_Type']!=2:
        #print('Rebound')
        #print(event['Event_Num'])
        # if lineup_dict[prevPlayer] != event['Team_id']:
        print(event)
        print(lineup_dict[prevPlayer]==prev_team)
        # if lineup_dict[prevPlayer] != event['Team_id']:
        if prev_team != event['Team_id']:
            for each_player in lineup_list:
                stats[each_player]['Possessions']+=1
            #print(stats)

    return 0

def update_stats(stats,lineup_dict,event,action,person1,person2):
    # Uses the event and action as they pertain to person1 and person2 to update the stats according to the current lineup.
    return
