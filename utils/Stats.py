import pandas as pd

def Stats(Points,Matches,surface= None,result=None,pt_results= None,serve =None):
    
    if result != None:
        Matches = Matches[Matches['Winner'] == result]
    if surface != None:
        Matches = Matches[Matches['Surface'] == surface]

    data = Points[Points['match_id'].isin(Matches['match_id'])]

    if pt_results != None:
        data = data[data['Victor'] == pt_results]
    
    if serve != None:
        data = data[data['Server'] == serve]

    WinRate = round(data['Winner'].value_counts(normalize=True),4)
    AceRate = round(data['Ace'].value_counts(normalize=True),4)
    DoubleFRate = round(data['Double Fault'].value_counts(normalize=True),4)
    FERate = round(data['Forced Error'].value_counts(normalize=True),4)
    UFERate = round(data['Unforced Error'].value_counts(normalize=True),4)

    # print(f'Aces => {float(AceRate[True])}')
    # print(f'Winners => {float(WinRate[True])}')
    # print(f'Forced Errors => {float(FERate[True])}')
    # print(f'Unforced Errors => {float(UFERate[True])}')
    # if(pt_results==False):
    #     print(f'Double Faults => {float(DoubleFRate[not pt_results])} \n')
    
    # print('\n')

    return {'Winners': float(WinRate[True]), 'Aces' : float(AceRate[True]), 'Forced Error' : float(FERate[True]),'Unforced Error' : float(UFERate[True])} 

    

def KeyPointsData(data):
    GamePoints   = pd.DataFrame()
    BreakPoints  = pd.DataFrame()
    DeucePoints  = pd.DataFrame()

    KP = data[data['Pts'].str.contains('40', na=False)]

    ServingKP = data[data['Server'] == True]
    RecpKP = data[data['Server'] == False]

    GamePoints = pd.concat([GamePoints, ServingKP[ServingKP['Pts'].str.startswith(('40','AD') ,na=False)]], axis=0)
    GamePoints = pd.concat([GamePoints, RecpKP[~RecpKP['Pts'].str.startswith(('40','AD'),na=False)]], axis=0)

    BreakPoints = pd.concat([BreakPoints, ServingKP[~ServingKP['Pts'].str.startswith(('40','AD') ,na=False)]], axis=0)
    BreakPoints = pd.concat([BreakPoints, RecpKP[RecpKP['Pts'].str.startswith(('40','AD'),na=False)]], axis=0)

    GamePoints = GamePoints[GamePoints['Pts'] != '40-40']
    BreakPoints = BreakPoints[BreakPoints['Pts'] != '40-40']
    DeucePoints = KP[KP['Pts'] == '40-40']

    # Dpoints = ['40-40','AD-40','40-AD']
    # Dispute = KP[KP['Pts'].isin(Dpoints)]

    return GamePoints,BreakPoints,DeucePoints

def BuildRally(data,PlayerGames,Player):
    rows = ['Total','1-3','4-6','7-9','10']

    PlayerRallyServe = data[data['server'] == Player].drop(columns=['server','returner'])
    PlayerRallyServe = PlayerRallyServe[PlayerRallyServe['match_id'].isin(PlayerGames['match_id'].unique())]
    PlayerRallyServe = PlayerRallyServe[~PlayerRallyServe['row'].isin(rows)]
    PlayerRallyServe[['pl1_unforced','pl2_unforced']] = PlayerRallyServe[['pl2_unforced','pl1_unforced']]
    PlayerRallyServe['row'] = PlayerRallyServe['row'].str[:3]
    
    PlayerRallyReturn = data[data['returner'] == Player].drop(columns=['server','returner'])
    PlayerRallyReturn = PlayerRallyReturn[PlayerRallyReturn['match_id'].isin(PlayerGames['match_id'].unique())]
    PlayerRallyReturn = PlayerRallyReturn[~PlayerRallyReturn['row'].isin(rows)]
    PlayerRallyReturn[['pl1_unforced','pl2_unforced']] = PlayerRallyReturn[['pl2_unforced','pl1_unforced']]
    PlayerRallyReturn['row'] = PlayerRallyReturn['row'].str[:3]

    return PlayerRallyServe,PlayerRallyReturn

def statsDiv(data):
    stats_dic = {}
    stats_dic['Totality'] = data
    for r in data['row'].unique():

        Type = data[data['row'] == r]
        stats_dic[r] = Type
    
    return stats_dic

def AllStats(data,Player = None):

    DirOutcome = pd.read_csv('BaseData/charting-m-stats-ShotDirOutcomes.csv')
    Overview = pd.read_csv('BaseData/charting-m-stats-Overview.csv')
    NetPoints = pd.read_csv('BaseData/charting-m-stats-NetPoints.csv')
    RallySize = pd.read_csv('BaseData/charting-m-stats-Rally.csv')
    KeyPServe = pd.read_csv('BaseData/charting-m-stats-KeyPointsServe.csv')
    KeyPReturn = pd.read_csv('BaseData/charting-m-stats-KeyPointsReturn.csv')

    DirOutcome = DirOutcome[DirOutcome['match_id'].isin(data['match_id'].unique())]

    Overview = Overview[Overview['match_id'].isin(data['match_id'].unique())]
    Overview.rename(columns={'set':'row'}, inplace=True)
    
    NetPoints = NetPoints[NetPoints['match_id'].isin(data['match_id'].unique())]

    KeyPServe = KeyPServe[KeyPServe['match_id'].isin(data['match_id'].unique())]

    KeyPReturn = KeyPReturn[KeyPReturn['match_id'].isin(data['match_id'].unique())]

    if Player != None:
        DirOutcome = DirOutcome[DirOutcome['player'] == Player]
        Overview = Overview[Overview['player'] == Player]
        NetPoints = NetPoints[NetPoints['player'] == Player]
        KeyPServe = KeyPServe[KeyPServe['player'] == Player]
        KeyPReturn = KeyPReturn[KeyPReturn['player'] == Player]

    ServingRally, ReceivingRally = BuildRally(RallySize,data,Player)

    S_Rally_dic = statsDiv(ServingRally)
    R_Rally_dic = statsDiv(ReceivingRally)
    Shots_dic = statsDiv(DirOutcome)
    Over_dic = statsDiv(Overview)
    Net_dic = statsDiv(NetPoints)
    KPS_dic = statsDiv(KeyPServe)
    KPR_dic = statsDiv(KeyPReturn)

    return [S_Rally_dic,R_Rally_dic,Shots_dic,Over_dic,Net_dic,KPS_dic,KPR_dic]

def SRally(data, Matches, surface = None, result = None):

    Stats = {}

    for c in data.keys():
        Data = data[c]

        if surface != None:
            Matches = Matches[Matches['Surface'] == surface]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]
        
        if result != None:
            Matches = Matches[Matches['Winner'] == result]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]

        aggregate = Data.sum()

        PtsWon = aggregate['pl1_won']
        PtsLost = aggregate['pl2_won']
        WinPer100 = aggregate['pl1_winners']/aggregate['pl1_won']
        ForcedPer100 = aggregate['pl1_forced']/aggregate['pl1_won']
        unForcedPer100 = aggregate['pl1_unforced']/aggregate['pl1_won']
        
        Stats[c] = {'PtsWon' : PtsWon, 'PtsLost' : PtsLost,'Winners' : WinPer100, 'Forced' : ForcedPer100, 'Unforced' : unForcedPer100}
        
    return Stats

def RRally(data, Matches, surface = None, result = None):

    Stats = {}

    for c in data.keys():
        Data = data[c]

        if surface != None:
            Matches = Matches[Matches['Surface'] == surface]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]
        
        if result != None:
            Matches = Matches[Matches['Winner'] == result]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]

        aggregate = Data.sum()

        PtsWon = aggregate['pl2_won']
        PtsLost = aggregate['pl1_won']
        WinPer100 = aggregate['pl2_winners']/aggregate['pl2_won']
        ForcedPer100 = aggregate['pl2_forced']/aggregate['pl2_won']
        unForcedPer100 = aggregate['pl2_unforced']/aggregate['pl2_won']
        
        Stats[c] = {'PtsWon' : PtsWon, 'PtsLost' : PtsLost,'Winners' : WinPer100, 'Forced' : ForcedPer100, 'Unforced' : unForcedPer100}
        
    return Stats

def NetStat(data, Matches, surface = None, result = None):
    Stats = {}

    for c in data.keys():
        dic = {}
        Data = data[c]

        if surface != None:
            Matches = Matches[Matches['Surface'] == surface]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]
        
        if result != None:
            Matches = Matches[Matches['Winner'] == result]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]

        aggregate = Data.sum()

        dic['Total Pts'] = aggregate['net_pts']
        dic['Pts_Won'] = aggregate['pts_won']/aggregate['net_pts']
        dic['Winner'] = aggregate['net_winner']/aggregate['pts_won']
        dic['Forced'] = (aggregate['induced_forced'] + aggregate['passing_shot_induced_forced'])/aggregate['pts_won']
        dic['AvgRallyLen'] = aggregate['total_shots'] / aggregate['net_pts']

        Stats[c] = dic
    
    return Stats

def KPServeStat(data, Matches, surface = None, result = None):
    Stats = {}

    for c in data.keys():
        dic = {}
        Data = data[c]

        if surface != None:
            Matches = Matches[Matches['Surface'] == surface]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]
        
        if result != None:
            Matches = Matches[Matches['Winner'] == result]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]

        aggregate = Data.sum()
        
        dic['Total Points'] = aggregate['pts']
        dic['Points Won'] = aggregate['pts_won']/ aggregate['pts']
        dic['Winners'] = aggregate['rally_winners']/ aggregate['pts_won']
        dic['Forced'] = aggregate['rally_forced']/ aggregate['pts_won']
        dic['Unforced'] = aggregate['unforced']/ aggregate['pts_won']
        dic['Aces'] = aggregate['aces']/ aggregate['pts_won']
        dic['FirstServe'] = aggregate['first_in']/ aggregate['pts']

        Stats[c] = dic
    
    return Stats

def KPReturnStat(data, Matches, surface = None, result = None):
    Stats = {}

    for c in data.keys():
        dic = {}
        Data = data[c]

        if surface != None:
            Matches = Matches[Matches['Surface'] == surface]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]
        
        if result != None:
            Matches = Matches[Matches['Winner'] == result]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]

        aggregate = Data.sum()
        
        dic['Total Points'] = aggregate['pts']
        dic['Points Won'] = aggregate['pts_won']/ aggregate['pts']
        dic['Winners'] = aggregate['rally_winners']/ aggregate['pts_won']
        dic['Forced'] = aggregate['rally_forced']/ aggregate['pts_won']
        dic['Unforced'] = aggregate['unforced']/ aggregate['pts_won']

        Stats[c] = dic
    
    return Stats

def ShotsStat(data, Matches, surface = None, result = None):

    Stats = {}

    for c in data.keys():
        dic = {}
        Data = data[c]

        if surface != None:
            Matches = Matches[Matches['Surface'] == surface]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]
        
        if result != None:
            Matches = Matches[Matches['Winner'] == result]
            Data = Data[Data['match_id'].isin(Matches['match_id'].unique())]
        
        aggregate = Data.sum()
        
        dic['Total_Shots'] = aggregate['shots']
        dic['Finished'] = aggregate['pt_ending'] / aggregate['shots']
        dic['WinPer100'] = aggregate['winners'] / aggregate['pt_ending']
        dic['InducedError'] = aggregate['induced_forced'] / aggregate['pt_ending']
        dic['Unforced'] = aggregate['unforced'] / aggregate['pt_ending']
        dic['Shots_in_PtWon'] = aggregate['shots_in_pts_won'] / aggregate['shots']
        dic['Shots_in_Ptlost'] = aggregate['shots_in_pts_lost'] / aggregate['shots']

        Stats[c] = dic
    
    return Stats

def AggregateStats(data,Matches,surface = None, result = None):
    
    RallyServeStats = SRally(data[0],Matches,surface=surface,result=result)
    RallyReceptionStats = RRally(data[1],Matches,surface=surface,result=result)

    ShotsStats = ShotsStat(data[2],Matches,surface=surface,result=result)
    NetStats = NetStat(data[4],Matches,surface=surface,result=result)
    KPServeStats = KPServeStat(data[5],Matches,surface=surface,result=result)
    KPReturnStats = KPReturnStat(data[6],Matches,surface=surface,result=result)

    return RallyServeStats,RallyReceptionStats,ShotsStats,NetStats,KPServeStats,KPReturnStats