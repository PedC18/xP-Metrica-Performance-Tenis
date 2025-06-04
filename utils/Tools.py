import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os
import csv

def Victor(points, matches):
    Winners = []

    for id in matches['match_id']:
        # print(id)
        m_points = points[points['match_id'] == id]
        Victor = m_points.iloc[len(m_points) - 1]['PtWinner']
        if(Victor == 1):
            Winners.append(matches[matches['match_id'] == id]['Player 1'].unique())
        else:
            Winners.append(matches[matches['match_id'] == id]['Player 2'].unique())

    matches['Winner'] = Winners

def ServStats(Serves,player_name,player_games):
    serves = pd.DataFrame(columns=['match_id'])
    serves['match_id'] = player_games['match_id']

    ServesTotal = Serves[(Serves['row'] == 'Total') & (Serves['player'] == player_name)].reset_index(drop=True)
    ServesFirst = Serves[(Serves['row'] == '1') & (Serves['player'] == player_name)].reset_index(drop=True)
    ServesSecond = Serves[(Serves['row'] == '2') & (Serves['player'] == player_name)].reset_index(drop=True)

    serves['Total'] = ServesTotal['pts']
    serves[['1st','Won1']] = ServesFirst[['pts','pts_won']]
    serves[['2nd','Won2 ']] = ServesSecond[['pts','pts_won']]


    return serves

def PtWinner(points,player,games):
    result = pd.DataFrame()
    for id in games['match_id']:
        game = games[games['match_id'] == id]
        gamePts = points[points['match_id'] == id]
        Player1 = game['Player 1'].unique()

        if(Player1 == player):
            gamePts['PtWinner'] = gamePts['PtWinner'] == 1
        else:
            gamePts['PtWinner'] = gamePts['PtWinner'] == 2
        
        result = pd.concat([result,gamePts],axis=0)

    
    return result['PtWinner']

def Server(points,player,games):
    result = pd.DataFrame()
    for id in games['match_id']:
        game = games[games['match_id'] == id]
        gamePts = points[points['match_id'] == id]
        Player1 = game['Player 1'].unique()

        if(Player1 == player):
            gamePts['Svr'] = gamePts['Svr'] == 1
        else:
            gamePts['Svr'] = gamePts['Svr'] == 2
        
        result = pd.concat([result,gamePts],axis=0)

    
    return result['Svr']


def Shots(data,rows):
    result = pd.DataFrame(columns=rows)
    result['match_id'] = data['match_id'].unique()
    i = 0
    for id in data['match_id'].unique():
        game = data[data['match_id'] == id]
        for idx,row in game.iterrows():
            result.loc[i,row['row']] = row['shots']
        
        i += 1
        

    
    return result

def PtEnding(points,dict):
    
    for idx,row in points.iterrows():
        if row['2nd'] == None:
            rally = row['1st']
        else:
            rally = row['2nd']
        
        symbol = rally[len(rally) - 1]
        
        if symbol == "*":
            if(len(rally) == 2):
                points.loc[(idx),[dict["*"][1]]] = True
            else:
                points.loc[(idx),[dict["*"][0]]] = True

        elif symbol == "@":
            points.loc[(idx),[dict['@']]] = True

        elif symbol == '#':
            points.loc[(idx),[dict['#']]] = True
        
        else:
            points.loc[(idx),['Double Fault']] = True

def Rallys(data,rows):
    result = pd.DataFrame(columns=rows)
    result['match_id'] = data['match_id'].unique()
    i = 0
    for id in data['match_id'].unique():
        game = data[data['match_id'] == id]
        for idx,row in game.iterrows():
            result.loc[i,row['row']] = row['pts']
        
        i += 1
        

    
    return result

def GetMatches(Matches,years):     
    Num_years = years[1] - years[0]
    Division = Num_years/3
    middle_l = str(years[0] + Division)
    middle_h = str(years[1] - Division
)
    matches_start = Matches[(Matches['Date'].astype(str).str[:4] >= str(years[0])) & (Matches['Date'].astype(str).str[:4] < middle_l)]
    matches_middle = Matches[(Matches['Date'].astype(str).str[:4] >= middle_l) & (Matches['Date'].astype(str).str[:4] < middle_h)]
    matches_end = Matches[(Matches['Date'].astype(str).str[:4] >= middle_h) & (Matches['Date'].astype(str).str[:4] <= str(years[1]))]

    return matches_start, matches_middle, matches_end

def GetSetsResults(Points):
    NewPoints = pd.DataFrame(columns=Points.columns)
    
    for id in Points['match_id'].unique():
        Match = Points[Points['match_id'] == id]
        size = int(max(Match['Set#']))
        for i in Match['Set#'].unique():
            Set = Match[Match['Set#'] == i]
            if Set.iloc[-1]['Victor'] == False:
                Set['SetWinner'] = False
            else:
                Set['SetWinner'] = True

            NewPoints = pd.concat([NewPoints,Set],axis=0)
    
    return NewPoints

def GetGamesResults(Points):
    NewPoints = pd.DataFrame(columns=Points.columns)
    
    for id in Points['match_id'].unique():
        Match = Points[Points['match_id'] == id]
        size = int(max(Match['Gm#']))
        for i in Match['Gm#'].unique():
            Game = Match[Match['Gm#'] == i]
            if Game.iloc[-1]['Victor'] == False:
                Game['GameWinner'] = False
            else:
                Game['GameWinner'] = True

            NewPoints = pd.concat([NewPoints,Game],axis=0)
    
    return NewPoints

def Translate(s):
    chars_to_remove = "789+-^;=cg!CRSQ "  # Specify characters to remove
    translation_table = str.maketrans('', '', chars_to_remove)
    updated_text = s.translate(translation_table)

    return updated_text

def ServeTranslate(s):
    chars_to_remove = "+-^;=cq!CRS "  # Specify characters to remove
    translation_table = str.maketrans('', '', chars_to_remove)
    updated_text = s.translate(translation_table)

    return updated_text

def NetTranslate(s):
    chars_to_remove = "879-^;=c!CRS "  # Specify characters to remove
    translation_table = str.maketrans('', '', chars_to_remove)
    updated_text = s.translate(translation_table)

    return updated_text

def check_list_contained(A, B):
  # convert list A to string
    A_str = ' '.join(map(str, A))
    # convert list B to string
    B_str = ' '.join(map(str, B))
    # find all instances of A within B
    instances = re.findall(A_str, B_str)
 
    # return True if any instances were found, False otherwise
    return len(instances) > 0

def split_string(s):
    # Find matches from a letter to the next letter
    split = re.findall(r'[a-zA-Z][^a-zA-Z]*', s)
    if(len(s) <= 2):
        split.insert(0,s)
    else:
        split.insert(0,s[0])
    return split


def RallyParsing(s,dic):
    Sequence = []
    End = []
    text = Translate(s=s)
    serve = text[0]
    rally = text[1:len(text)-1]
    end = text[-1]

    Sequence.append(dic[serve])

    if rally != '':
        rallyShots = rally[::2]
        rallyDir = rally[1::2]
        for i in range(len(rallyShots)):
            if(i == len(rallyDir)):
                End.append(dic[rallyShots[i]] +'_'+str(((i+1)%2) + 1))
            else:
                Sequence.append(dic[rallyShots[i]] + dic[rallyDir[i]] +'_'+ str(((i+1)%2) + 1))

    End.append(dic[end])
    return Sequence, End

def RallyParsingCounter(s,dic):
    Sequence = []
    End = []
    text = Translate(s=s)
    serve = text[0]
    rally = text[1:len(text)-1]
    end = text[-1]

    Sequence.append(dic[serve])

    if rally != '':
        rallyShots = rally[::2]
        rallyDir = rally[1::2]
        for i in range(len(rallyShots)):
            if(i == len(rallyDir)):
                End.append(dic[rallyShots[i]])
            else:
                Sequence.append(dic[rallyShots[i]] + dic[rallyDir[i]])

    End.append(dic[end])
    return Sequence, End

def RallyExtraction(Points):
    Rallys = []
    for _,row in Points.iterrows():
            
        if(row['2nd'] == 'False'):
            Rallys.append(row['1st'])
        else:
            Rallys.append(row['2nd'])
    
    return Rallys

# def ResumePointsStats(data, columns):
#     total = len(data)
#     result = []
#     for column in columns:
#         aux = data[data[column] == True]

#         true = len(aux)

#         Percentage = true/total
#         Percentage = round(Percentage,2)

#         result.append(Percentage)
    
#     return result

# Make a function that calculates the way the point was won

# Make a function that specifically calculates serve stats

# def ResumeServeStats(data):
#     FirstIn = data[data['1stIn'] == True]
#     FirstOut = data[data['1stIn'] == False]

    
#     SecondIn = FirstOut[FirstOut['2ndIn'] == True]

   
#     FirstIn_Percent = len(FirstIn)/len(data)
#     SecondIn_Percent = len(SecondIn)/len(FirstOut)


#     print(f'1stIn percentage : {FirstIn_Percent}')
#     print(f'2ndIn percentage : {SecondIn_Percent}')

# def Surface(data):
#     print(f"Grass :  {len(data[data['Surface'] == 'Grass'])}")
#     print(f"Hard :  {len(data[data['Surface'] == 'Hard'])}")
#     print(f"Clay :  {len(data[data['Surface'] == 'Clay'])}")


