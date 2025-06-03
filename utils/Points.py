import pandas as pd
from utils.Tools import Translate,ServeTranslate,RallyParsing,RallyExtraction
from utils.SeqMining import Sequencer,GetStrokes
   
def DivisionSets(Points,ids):
    SetPerMatches = {}
    for id in ids:
        Match = Points[Points['match_id'] == id]
        Sets_Matrix = []
        size = int(max(Match['Set#']))

        for i in Match['Set#'].unique():
            Set = Match[Match['Set#'] == i]

            Rallys = []
            for _,row in Set.iterrows():
            
                if(row['2nd'] == 'False'):
                    Rallys.append(row['1st'])
                else:
                    Rallys.append(row['2nd']) 
                    
            Sets_Matrix.append(Rallys)
        
        SetPerMatches[id] = Sets_Matrix
    
    return SetPerMatches

def DivisionGames(Points,ids):
    GamesPerMatches = {}
    for id in ids:
        Match = Points[Points['match_id'] == id]
        
        Games_Matrix = []
        size = int(max(Match['Gm#']))
        
        for i in Match['Gm#'].unique():
            Game = Match[Match['Gm#'] == i]

            Rallys = []
            for _,row in Game.iterrows():
            
                if(row['2nd'] == 'False'):
                    Rallys.append(row['1st'])
                else:
                    Rallys.append(row['2nd'])

            Games_Matrix.append(Rallys)
        
        GamesPerMatches[id] = Games_Matrix
    
    return GamesPerMatches


def SnVPoints(data, result = None, surface = None):

    StrokesDictionary = GetStrokes()
    
    data = data[data['Server'] == True]
    
    Rally = RallyExtraction(data)
    count = 0
    for n in Rally:
        if n[1] == '+':
            count+=1

    if result != None:
        data = data[data['Victor'] == result]

    if surface != None:
        data = data[data['Surface'] == surface]

    Rally = RallyExtraction(data)
    
    SnV = []
    for n in Rally:
        if n[1] == '+':
            SnV.append(n)

    RallyS = [RallyParsing(d,StrokesDictionary) for d in SnV]

    Sequences = []
    Endings = []
    for seq, end in RallyS:
        Sequences.append(seq)
        Endings.append(end)

    dicS = {'Total' : count,'Vencidos' : 0}
    for e in Endings:
        dicS['Vencidos']+=1
        if(e[-1] in dicS):
            dicS[e[-1]] += 1
        else:
            dicS[e[-1]] = 1
    
    return dicS

def FindRallyLenght(Points,result= None, surface = None):

    if result != None:
        Points = Points[Points['Victor'] == result]

    if surface != None:
        Points = Points[Points['Surface'] == surface]
    
    First = Points[(Points['2nd'] == 'False')]
    Second = Points[~(Points['2nd'] == 'False')]

    Sequences,_ = Sequencer(First)

    First['1st'] = Sequences

    Sequences,_ = Sequencer(Second)

    Second['2nd'] = Sequences

    print(First['1st'].apply(lambda x : len(x)).mean())
    print(Second['2nd'].apply(lambda x : len(x)).mean())

def FindNetPoints(data,server=None, result = None, surface = None):
    
    StrokesDictionary = GetStrokes()

    if server != None:
        data = data[data['Server'] == server]

    if result != None:
        data = data[data['Victor'] == result]

    if surface != None:
        data = data[data['Surface'] == surface]

    Rally = RallyExtraction(data)
    
    Net = []
    for r in Rally:
        if r.find('+') != -1:
            Net.append(r)

    RallyS = [RallyParsing(d,StrokesDictionary) for d in Net]

    Sequences = []
    Endings = []
    for seq, end in RallyS:
        Sequences.append(seq)
        Endings.append(end)

    dic = {}
    for e in Endings:
        if(e[-1] in dic):
            dic[e[-1]] += 1
        else:
            dic[e[-1]] = 1
    
    return dic

def Service(Points):

    Points = Points[Points['Server'] == True]
    
    FirstServe = Points[(Points['2nd'] == 'False')] 
    SecondServe = Points[~(Points['2nd'] == 'False')] 

    return FirstServe,SecondServe

def ServeData(data, result = None):
    Serve = []
    Wide = {'Total' : 0}
    Middle = {'Total' : 0}
    DownTheT = {'Total' : 0}

    data = data[data['Server'] == True]
    
    if result != None:
        data = data[data['Victor'] == result]

    Rallys = RallyExtraction(data)

    for r in Rallys:
        r = ServeTranslate(r)
        Serve.append((r[0],r[-1]))
    
    for s in Serve:
        if s[0] == '4':
            Wide['Total'] += 1
            if(s[1] in Wide):
                Wide[s[1]] +=1
            else:
                Wide[s[1]] = 1
        elif s[0] == '5':
            Middle['Total'] += 1
            if(s[1] in Middle):
                Middle[s[1]] +=1
            else:
                Middle[s[1]] = 1
        else:
            DownTheT['Total'] += 1
            if(s[1] in DownTheT):
                DownTheT[s[1]] +=1
            else:
                DownTheT[s[1]] = 1
    

    return Wide,Middle,DownTheT


