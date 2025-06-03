import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from utils.Tools import Victor,ServStats,PtWinner,Server,Shots, PtEnding, Rallys, GetMatches, GetSetsResults, GetGamesResults


def BuildDirectory(directory_name):
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


# --------------------------------------------------------------------------------------------------------------------------------- #

def BuildPoints(PlayerGames,Points,Player,player_name,directory_name,period):
    EndDict = {"*": ("Winner","Ace"),
           "@": "Unforced Error",
           "#" : "Forced Error"
           }

    PlayerAux = PlayerGames[['match_id','Player 1', 'Player 2','Surface']]

    PointsPlayer = pd.merge(Points,PlayerAux, on='match_id')

    Victor(Points,PlayerGames)
    PlayerGames['Winner'] = PlayerGames['Winner'].apply(lambda x: True if x == Player else False)

    PointsPlayer['Victor'] = PtWinner(PointsPlayer,Player, PlayerGames)

    PointsPlayer['Server'] = Server(PointsPlayer,Player, PlayerGames)

    PointsPlayer['Gm#'] = PointsPlayer['Gm#'].interpolate('nearest')

    PointsPlayer = GetGamesResults(PointsPlayer)
    PointsPlayer = GetSetsResults(PointsPlayer)
    
    PointsPlayer[['Ace','Winner','Unforced Error','Forced Error','Double Fault']] = None

    PointsPlayer.loc[(PointsPlayer['2nd'].isna()), ['2nd']] = None

    PtEnding(PointsPlayer,EndDict)

    PointsPlayer = PointsPlayer.fillna(False)


    PointsPlayer.to_csv(directory_name+'/Points'+ player_name + period +'.csv',index=False)

    PlayerGames.to_csv(directory_name+'/'+ player_name + period +'.csv',index=False)


# --------------------------------------------------------------------------------------------------------------------------------- #

def BuildRallys(PlayerGamesRally, directory_name,Player,player_name,period):

    rowsServe = ['Total','1-3','4-6','7-9','10']
    rowsIndx = ['match_id','1-3','4-6','7-9','10-']
    
    PlayerRallyServe = PlayerGamesRally[PlayerGamesRally['server'] == Player].drop(columns=['server','returner'])
    PlayerRallyServe = PlayerRallyServe[~PlayerRallyServe['row'].isin(rowsServe)]
    PlayerRallyServe['row'] = PlayerRallyServe['row'].str[:3]
    PlayerRallyServe = Rallys(PlayerRallyServe,rowsIndx)

    PlayerRallyServe.to_csv(directory_name +'/'+player_name +'ServesRally_' + period + '.csv',index=False)

    PlayerRallyReturn = PlayerGamesRally[PlayerGamesRally['returner'] == Player].drop(columns=['server','returner'])
    PlayerRallyReturn = PlayerRallyReturn[~PlayerRallyReturn['row'].isin(rowsServe)]
    PlayerRallyReturn['row'] = PlayerRallyReturn['row'].str[:3]
    PlayerRallyReturn = Rallys(PlayerRallyReturn,rowsIndx)

    PlayerRallyReturn.to_csv(directory_name +'/'+player_name +'Returns_'+ period +'.csv',index=False)

# --------------------------------------------------------------------------------------------------------------------------------- #

def BuildShotTypes(PlayerGames, PlayerGamesShotTypes,directory_name,Player,player_name,period):

    SymbolsDictionary = {"F" : "Forehand", 
                     "B" : "Backhand", 
                     "R" :"FH Slice", 
                     "S" : "BH Slice", 
                     "V" : "FH Volley", 
                     "Z" : "BH Volley"
                     }

    rowsST = ['match_id','Total', 'F', 'B', 'R', 'S', 'V','Z']

    PlayerGamesShotTypes = PlayerGamesShotTypes[PlayerGamesShotTypes['row'].isin(rowsST)].reset_index(drop=True)
    PlayerShotTypes = PlayerGamesShotTypes[PlayerGamesShotTypes['player'] == Player]

    PlayerShotStats = Shots(PlayerShotTypes,rows=rowsST)
    PlayerShotStats = PlayerShotStats.rename(columns=SymbolsDictionary)
    PlayerShotStats = PlayerShotStats.fillna(0)

    PlayerShotStats['Win'] = PlayerGames['Winner']
    
    PlayerShotStats.to_csv(directory_name +'/'+player_name +'ShotType_'+ period +'.csv',index=False)

# --------------------------------------------------------------------------------------------------------------------------------- #

def BuildShotDirection(PlayerGamesShotDir,Player,directory_name,player_name,period):
    
    PlayerShotDirTotal = PlayerGamesShotDir[PlayerGamesShotDir['player'] == Player]
    PlayerShotDirTotal = PlayerShotDirTotal[PlayerShotDirTotal['row'] == 'Total']
    PlayerShotDirTotal = PlayerShotDirTotal.drop(columns=['player','row'])

    PlayerShotDirTotal.to_csv(directory_name +'/'+player_name +'ShotDir_'+ period +'.csv',index=False)

# --------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------------------------------------------------------------------------------- #

def BuildDatasets(PlayerGames,Points,Player,player_name,directory_name,period):
    
    BuildPoints(PlayerGames,Points,Player,player_name,directory_name,period)

    Rally = pd.read_csv('BaseData/charting-m-stats-Rally.csv')
    ShotTypes = pd.read_csv('BaseData/charting-m-stats-ShotTypes.csv')
    Serves = pd.read_csv('BaseData/charting-m-stats-ServeBasics.csv')
    ShotDir = pd.read_csv('BaseData/charting-m-stats-ShotDirection.csv')

    PlayerGamesRally = Rally[Rally['match_id'].isin(PlayerGames['match_id'])]
    PlayerGamesServes = Serves[Serves['match_id'].isin(PlayerGames['match_id'])]
    PlayerGamesShotTypes = ShotTypes[ShotTypes['match_id'].isin(PlayerGames['match_id'])]
    PlayerGamesShotDir = ShotDir[ShotDir['match_id'].isin(PlayerGames['match_id'])]

    BuildRallys(PlayerGamesRally,directory_name,Player,player_name,period)
    BuildShotTypes(PlayerGames,PlayerGamesShotTypes,directory_name,Player,player_name,period)
    BuildShotDirection(PlayerGamesShotDir,Player,directory_name,player_name,period)

    PlayerServes = ServStats(Serves,Player,PlayerGames)

    PlayerServes.to_csv(directory_name +'/'+player_name +'Serve_'+ period +'.csv',index=False)

# --------------------------------------------------------------------------------------------------------------------------------- #

def Builder(Player,years):
    
    player_name = Player.split(' ',1)[1]
    
    directory_name = player_name +'_data'

    BuildDirectory(directory_name)

    matches = pd.read_csv('BaseData/charting-m-matches.csv', encoding='unicode_escape',quoting=csv.QUOTE_NONE)

    Start, Middle, End = GetMatches(matches,years)

    PlayerGamesStart = Start[(Start['Player 1'] == Player) | (Start['Player 2'] == Player)].reset_index(drop=True)
    PlayerGamesMiddle = Middle[(Middle['Player 1'] == Player) | (Middle['Player 2'] == Player)].reset_index(drop=True)
    PlayerGamesEnd = End[(End['Player 1'] == Player) | (End['Player 2'] == Player)].reset_index(drop=True)

    # PlayerGamesStart.to_csv(directory_name+'/'+ player_name + 'Start.csv',index=False)
    # PlayerGamesMiddle.to_csv(directory_name+'/'+ player_name + 'Middle.csv',index=False)
    # PlayerGamesEnd.to_csv(directory_name+'/'+ player_name + 'End.csv',index=False)

    Points = pd.read_csv('ProjData/Points.csv')

    BuildDatasets(PlayerGamesStart,Points,Player,player_name,directory_name,'Start')
    BuildDatasets(PlayerGamesMiddle,Points,Player,player_name,directory_name,'Middle')
    BuildDatasets(PlayerGamesEnd,Points,Player,player_name,directory_name,'End')



# def BuilderOld(Player,years):

#     SymbolsDictionary = {"F" : "Forehand", 
#                      "B" : "Backhand", 
#                      "R" :"FH Slice", 
#                      "S" : "BH Slice", 
#                      "V" : "FH Volley", 
#                      "Z" : "BH Volley"
#                      }

#     EndDict = {"*": ("Winner","Ace"),
#            "@": "Unforced Error",
#            "#" : "Forced Error"
#            }
    
#     player_name = Player.split(' ',1)[1]
    
#     directory_name = player_name +'_data'

#     matches = pd.read_csv('BaseData/charting-m-matches.csv', encoding='unicode_escape',quoting=csv.QUOTE_NONE)
#     matches_period =  matches[matches['Date'].astype(str).str[:4] == '2012']

#     PlayerGames = matches_period[(matches_period['Player 1'] == Player) | (matches_period['Player 2'] == Player)].reset_index(drop=True)

#     PlayerGames.to_csv(directory_name+'/'+ player_name + '.csv',index=False)

#     Points = pd.read_csv('ProjData/Points.csv')

#     PlayerAux = PlayerGames[['match_id','Player 1', 'Player 2','Surface']]

#     PointsPlayer = pd.merge(Points,PlayerAux, on='match_id')

#     Victor(PointsPlayer,PlayerGames)

#     PlayerGames['Winner'] = PlayerGames['Winner'].apply(lambda x: True if x == "["+Player+"]" else False)

#     PointsPlayer['Victor'] = PtWinner(PointsPlayer,Player, PlayerGames)

#     PointsPlayer['Server'] = Server(PointsPlayer,Player, PlayerGames)

#     PointsPlayer[['Ace','Winner','Unforced Error','Forced Error','Double Fault']] = None

#     PointsPlayer.loc[(PointsPlayer['2nd'].isna()), ['2nd']] = None

#     PtEnding(PointsPlayer,EndDict)

#     PlayerGames.to_csv(directory_name+'/'+ player_name + '.csv',index=False)
#     PointsPlayer.to_csv(directory_name+'/Points'+ player_name + '.csv',index=False)

#     Rally = pd.read_csv('BaseData/charting-m-stats-Rally.csv')
#     ShotTypes = pd.read_csv('BaseData/charting-m-stats-ShotTypes.csv')
#     Serves = pd.read_csv('BaseData/charting-m-stats-ServeBasics.csv')
#     ShotDir = pd.read_csv('BaseData/charting-m-stats-ShotDirection.csv')

#     PlayerGamesRally = Rally[Rally['match_id'].isin(PlayerGames['match_id'])]
#     PlayerGamesServes = Serves[Serves['match_id'].isin(PlayerGames['match_id'])]
#     PlayerGamesShotTypes = ShotTypes[ShotTypes['match_id'].isin(PlayerGames['match_id'])]
#     PlayerGamesShotDir = ShotDir[ShotDir['match_id'].isin(PlayerGames['match_id'])]

#     rowsServe = ['Total','1-3','4-6','7-9','10']
#     rowsIndx = ['match_id','1-3','4-6','7-9','10-']
    
#     PlayerRallyServe = PlayerGamesRally[PlayerGamesRally['server'] == Player].drop(columns=['server','returner'])
#     PlayerRallyServe = PlayerRallyServe[~PlayerRallyServe['row'].isin(rowsServe)]
#     PlayerRallyServe['row'] = PlayerRallyServe['row'].str[:3]
#     PlayerRallyServe = Rallys(PlayerRallyServe,rowsIndx)

#     PlayerRallyServe.to_csv(directory_name +'/'+player_name +'ServesRally.csv',index=False)

#     PlayerRallyReturn = PlayerGamesRally[PlayerGamesRally['returner'] == Player].drop(columns=['server','returner'])
#     PlayerRallyReturn = PlayerRallyReturn[~PlayerRallyReturn['row'].isin(rowsServe)]
#     PlayerRallyReturn['row'] = PlayerRallyReturn['row'].str[:3]
#     PlayerRallyReturn = Rallys(PlayerRallyReturn,rowsIndx)
#     PlayerRallyReturn.to_csv(directory_name +'/'+player_name +'Returns.csv',index=False)

#     PlayerShotDirTotal = PlayerGamesShotDir[PlayerGamesShotDir['player'] == Player]
#     PlayerShotDirTotal = PlayerShotDirTotal[PlayerShotDirTotal['row'] == 'Total']
#     PlayerShotDirTotal = PlayerShotDirTotal.drop(columns=['player','row'])
#     PlayerShotDirTotal.to_csv(directory_name +'/'+player_name +'ShotDir.csv',index=False)

#     rowsST = ['match_id','Total', 'F', 'B', 'R', 'S', 'V','Z']
#     PlayerGamesShotTypes = PlayerGamesShotTypes[PlayerGamesShotTypes['row'].isin(rowsST)].reset_index(drop=True)
#     PlayerShotTypes = PlayerGamesShotTypes[PlayerGamesShotTypes['player'] == Player]

#     PlayerShotStats = Shots(PlayerShotTypes,rows=rowsST)
#     PlayerShotStats = PlayerShotStats.rename(columns=SymbolsDictionary)
#     PlayerShotStats = PlayerShotStats.fillna(0)
    


#     PlayerShotStats['Win'] = PlayerGames['Winner']
    
#     PlayerShotStats.to_csv(directory_name +'/'+player_name +'ShotType.csv',index=False)
#     # data = PlayerShotStats[[ 'Total', 'Forehand', 'Backhand', 'FH Slice', 'BH Slice',
#     #     'FH Volley', 'BH Volley', 'Win']]
    
#     PlayerServes = ServStats(Serves,Player,PlayerGames)

#     PlayerServes.to_csv(directory_name +'/'+player_name +'Serve.csv',index=False)