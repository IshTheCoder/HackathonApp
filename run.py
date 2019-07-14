import pandas as pd
import helper_functions as hf
from collections import defaultdict

play = pd.read_csv("Play_by_Play.txt",delimiter="\t")
play = play.sort_values(by=['Game_id','Event_Num'])
lineup = pd.read_csv("Game_Lineup.txt",delimiter="\t")
codes = pd.read_csv("Event_Codes.txt",delimiter="\t")

period = 0
game = 0
#stats = lineup[lineup['Period']==0][['Game_id','Person_id']]
#stats['Points_made'] = stats.shape[0]*[0]
#stats['Points_given'] = stats.shape[0]*[0]
#stats['Number_possessions'] = stats.shape[0]*[0]

looper=(len(play.index))

team=0
prevPlayer=0
stats=defaultdict(lambda: defaultdict(int))
for i in range(looper):

	event=play.iloc[i,:]

	if game != event['Game_id']:
		game=event['Game_id']

	if period != event['Period']:
		lineup_list = hf.get_starting_lineup(lineup,event['Game_id'],event['Period'])
		period = event['Period']

	hf.update_lineup(lineup_list,event)
	# hf.update_possessions(stats,lineup_list,event,team)

	if event['Event_Msg_Type']==6:
		lineup_copy = lineup_list

	if (event['Event_Msg_Type']==9) or (event['Event_Msg_Type']==8) or (event['Event_Msg_Type']==3) or (event['Event_Msg_Type']==6):
		flag_dead = 1
	else:
		flag_dead = 0

	if flag_dead==1:
		hf.update_possessions(stats,lineup_copy,event,team,prevPlayer)
		hf.update_stats(stats,lineup_copy,event)
	else:
		hf.update_possessions(stats,lineup_list,event,team,prevPlayer)
		hf.update_stats(stats,lineup_list,event)

	team=event['Team_id']
	prevPlayer = event['Person1']

	if game != '006728e4c10e957011e1f24878e6054a':
		break
