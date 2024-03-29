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

def update_lineup(lineup,roster,event):
    # Substitutes in player2 for player1.
    ## Inputs:
    ### lineup: dictionary with Team_id as keys and Person_id as values
    ### roster: dataframe of all the players from the given game
    ### event: the event to look at for the updates
    ## Outputs:
    ### lineup_dict: dictionary with Team_id as keys and Person_id as values

    if event['Event_Msg_Type']==8:
        #lineup_list.remove(event['Person1'])
        # lineup_list_final = list(map(lambda b: b.replace(event['Person1'],event['Person2']), lineup.keys()))
        # if event['Person1'] not in lineup.keys():
        #     print(event)
        #     #print(lineup_dict.keys())

        try:
            lineup[event['Person2']]=lineup.pop(event['Person1'])
        except:
            lineup[event['Person2']]=roster[(roster['Game_id']==event['Game_id']) & (roster['Person_id']==event['Person2'])].Team_id.tolist()[0]


       


        return lineup
    else:
        return lineup
    


def update_possessions(stats,lineup_dict,event,prev_team,prevPlayerTeam):
    # Updates the possessions for each player on the court in the instance of a change of possession.
    ## Inputs:
    ### stats: stats is a dataframe that maps gameID and PlayerId onto the number of possessions and other stats
    ### lineup: dictionary with Team_id as keys and Person_id as values
    ### prev_team: This looks at the previous team that took a missed shot to figure out if the rebound is defensive
    ### prevPlayerTeam: looks at the team of the previous player
    ### event: the event to look at for the updates
    ## Outputs:
    ### stats: stats is a dataframe that maps gameID and PlayerId onto the number of possessions and other stats

    lineup_list=lineup_dict.keys()
    if (event['Event_Msg_Type']== 1) or (event['Event_Msg_Type']==5) or (event['Event_Msg_Type']==3 and event['Option1']==1 and (event['Action_Type'] in [10,12,15,16,19,20,22,26,29])) or (event['Event_Msg_Type']==13):
        #Consider edge case, event code 5,0 i.e. Turnover- No turnover, what does it mean?
        for each_player in lineup_list:
            stats.loc[(stats['Game_id']==event['Game_id'])&(stats['Person_id']==each_player),'Possessions']+=1
            # stats[each_player]['Possessions']+=1
        #print(stats)
    elif event['Event_Msg_Type']==4 and event['Action_Type']!=2:
        if prevPlayerTeam != event['Team_id']:
        # if prev_team != event['Team_id']:
            for each_player in lineup_list:
                stats.loc[(stats['Game_id']==event['Game_id'])&(stats['Person_id']==each_player),'Possessions']+=1
                # stats[each_player]['Possessions']+=1
            #print(stats)

    return 0

def get_team1(lineup_dict,event):
	### Helper function that just partitions the lineup_dict into team1 and team2
	### Input:
	### lineup_dict: dictionary of current on-court players mapped on to their teams
	### event: dataframe of the current event
	###Output:
	### team1_lineup: the list of players on the court of the same team as Person1
	### team2_lineup: the list of players from the opposite team on the court.

    lineup_players=lineup_dict.keys()
    team1=lineup_dict[event['Person1']]
    # lineup_teams=lineup_dict.values()

    team1_lineup=[]
    team2_lineup=[]

    # print(lineup_dict)
    for each_key in lineup_players:
        if lineup_dict[each_key]==team1:
            team1_lineup.append(each_key)
        else:
            team2_lineup.append(each_key)

    return team1_lineup, team2_lineup



def update_stats(stats,lineup_dict,event):

    # Updates the stats for each player on the court in the instance of a made shot or freethrow.
    ## Inputs:
    ### stats: stats is a dataframe that maps gameID and PlayerId onto the number of possessions and other stats
    ### lineup: dictionary with Team_id as keys and Person_id as values
    ### event: the event to look at for the updates
    ## Outputs:
    ### stats: stats is a dataframe that maps gameID and PlayerId onto the number of possessions and other stats



    # print(event)
    if event['Person1']=='0370a0d090da0d0edc6319f120187e0e':
        return stats



    if event['Event_Msg_Type']==1:
        team1_lineup,team2_lineup=get_team1(lineup_dict,event)
        if event['Option1']==3:
            # index=0
            for each_player in team1_lineup:
                stats.loc[(stats['Game_id']==event['Game_id'])&(stats['Person_id']==each_player),'PSc']+=3
                # stats[each_player]['PSc']+=3
            for each_player in team2_lineup:
                stats.loc[(stats['Game_id']==event['Game_id'])&(stats['Person_id']==each_player),'PAg']+=3
                # stats[each_player]['PAg']+=3
                # stats[team2_lineup[index]]['PAg']+=3
                # index+=1

        elif event['Option1']==2:
            # index=0
            for each_player in team1_lineup:
                stats.loc[(stats['Game_id']==event['Game_id'])&(stats['Person_id']==each_player),'PSc']+=2
                # stats[each_player]['PSc']+=2
            for each_player in team2_lineup:
                stats.loc[(stats['Game_id']==event['Game_id'])&(stats['Person_id']==each_player),'PAg']+=2
                # stats[each_player]['PAg']+=2
                # stats[team2_lineup[index]]['PAg']+=2
                # index+=1


    elif event['Event_Msg_Type']==3 and event['Option1']==1:
        team1_lineup,team2_lineup=get_team1(lineup_dict,event)

        # index=0
        for each_player in team1_lineup:
            stats.loc[(stats['Game_id']==event['Game_id'])&(stats['Person_id']==each_player),'PSc']+=1
            # stats[each_player]['PSc']+=1
        for each_player in team2_lineup:
            stats.loc[(stats['Game_id']==event['Game_id'])&(stats['Person_id']==each_player),'PAg']+=1
            # stats[each_player]['PAg']+=1
            # stats[team2_lineup[index]]['PAg']+=1
            # index+=1

    # Uses the event and action as they pertain to person1 and person2 to update the stats according to the current lineup.
    return stats
