import pandas as pd
import helper_functions as hf

play = pd.read_csv("Play_by_Play.txt",delimiter="\t")
lineup = pd.read_csv("Game_Lineup.txt",delimiter="\t")
codes = pd.read_csv("Event_Codes.txt",delimiter="\t")

period = 0
game = 0
stats = lineup[lineup['Period']==0][['Game_id','Person_id']]
stats['Points_made'] = stats.shape[0]*[0]
stats['Points_given'] = stats.shape[0]*[0]
stats['Number_possessions'] = stats.shape[0]*[0]



looper=(len(play.index))
for i in range(looper):

	event=play.iloc[i,:]

	#print(i)
	if game != event['Game_id']:
		game=event['Game_id']
		lineup_list = hf.get_starting_lineup(lineup,game,event['Period'])


	if period != event['Period']:
		period = event['Period']
    	lineup_list = hf.get_starting_lineup(lineup,game,period)
        #print(lineup_list)
	hf.update_lineup(lineup_list,event)

