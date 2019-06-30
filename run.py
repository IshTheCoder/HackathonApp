# Use the attached data and instructions to calculate offensive rating and defensive rating for each player in each game from the 2018 Playoffs. Offensive Rating is defined as the team points scored per 100 possessions while the player is on the court. Defensive Rating is defined as the number of points per 100 possessions that the team allows while that individual player is on the court. A possession is ended by (1) made field goal attempts, (2) made final free throw attempt, (3) missed final free throw attempt that results in a defensive rebound, (4) missed field goal attempt that results in a defensive rebound, (5) turnover, or (6) end of time period. Note: When a player is substituted before or during a set of free throws but was on the court at the time of the foul that caused the free throw, he is considered to be on the court for the free throws for the purposes of offensive and defensive rating. A player substituted in before a free throw but after a foul is not considered to be on the court until after the conclusion of the free throws. Please submit a .csv file titled “Your_Team_Name_Q1_BBALL.csv” substituting in the name of your team for "Your_Team_Name". Please save as a .csv. The final product should have 4 columns. Column 1: Game_ID, Column 2: Player_ID, Column 3: OffRtg, Column 4: DefRtg. Please note that each question is permitted a maximum of two file attachments. Please submit your answer in a .csv file and save your code, spreadsheets, and all other work in a zip file.

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

for i in range(len(play)):
    if game != play.Game_id[i]:
        game = play.Game_id[i]

    if period != play.Period[i]:
        period = play.Period[i]
        lineup = hf.get_lineup(lineup,game,period)

