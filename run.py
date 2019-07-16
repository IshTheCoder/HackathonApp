import pandas as pd
import helper_functions as hf
from collections import defaultdict

play = pd.read_csv("Play_by_Play.txt",delimiter="\t")
play = play.sort_values(by=['Game_id','Period','PC_Time','WC_Time','Event_Num'],ascending=[True,True,False,True,True])
lineup = pd.read_csv("Game_Lineup.txt",delimiter="\t")
codes = pd.read_csv("Event_Codes.txt",delimiter="\t")

# move substitution to fix key error for specific game
temp = play.iloc[8754:8755]
play = pd.concat([play.iloc[:8754],play.iloc[8755:]],ignore_index=True)
play = pd.concat([play.iloc[:8751],temp,play.iloc[8751:]],ignore_index=True)

# play.to_csv('sortedPlay.txt',sep="\t")

period = 0
game = 0
stats = lineup[lineup['Period']==0][['Game_id','Person_id']]
stats['PSc'] = stats.shape[0]*[0]
stats['PAg'] = stats.shape[0]*[0]
stats['Possessions'] = stats.shape[0]*[0]
stats['OffRtg']= stats.shape[0]*[0]
stats['DefRtg']= stats.shape[0]*[0]

roster = lineup[lineup['Period']==0][['Game_id','Person_id','Team_id']]
looper=(len(play.index))

team=0
prevPlayerTeam=0
for i in range(looper):
	print(i)
	event=play.iloc[i,:]

	if event['Event_Msg_Type'] != 20:
		if game != event['Game_id']:
			game=event['Game_id']

		if period != event['Period']:
			lineup_list = hf.get_starting_lineup(lineup,event['Game_id'],event['Period'])
			period = event['Period']

		hf.update_lineup(lineup_list,roster,event)
		# hf.update_possessions(stats,lineup_list,event,team)

		if event['Event_Msg_Type']==6:
			lineup_copy = lineup_list

		if (event['Event_Msg_Type']==9) or (event['Event_Msg_Type']==8) or (event['Event_Msg_Type']==3) or (event['Event_Msg_Type']==6):
			flag_dead = 1
		else:
			flag_dead = 0

		if flag_dead==1:
			hf.update_possessions(stats,lineup_copy,event,team,prevPlayerTeam)
			hf.update_stats(stats,lineup_copy,event)
		else:
			hf.update_possessions(stats,lineup_list,event,team,prevPlayerTeam)
			hf.update_stats(stats,lineup_list,event)

		team=event['Team_id']
		# prevPlayer = event['Person1']

		if event['Event_Msg_Type']==2:
			prevPlayerTeam = lineup_list[event['Person1']]

# print(stats)
# print(len(stats.keys()))

stats.loc[stats['Possessions']>0,'OffRtg']+=stats['PSc']/stats['Possessions']
stats.loc[stats['Possessions']>0,'DefRtg']+=stats['PAg']/stats['Possessions']

stats_final = stats[['Game_id','Person_id','OffRtg','DefRtg']]
stats_final.to_csv('TEAMNAME_Q1_BBALL.csv',sep="\t")