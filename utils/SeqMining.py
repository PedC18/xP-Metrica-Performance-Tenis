from prefixspan import PrefixSpan
from utils.Tools import RallyExtraction,RallyParsing,RallyParsingCounter
from pymining import itemmining, seqmining
from collections import Counter
import re

StrokesDictionary = {
    '0' : 'Serve',
    '4' : 'Wide Serve',
    '5' : 'Body Serve',
    '6' : 'Down The T Serve',
    '7' : 'shallow',
    '8' : 'middle',
    '9' : 'deep',
    'f' : 'Forehand',
    'b' : 'Backhand',
    'r' : 'FH Slice',
    's' : 'BH Slice',
    'v' : 'FH Volley',
    'z' : 'BH Volley',
    '1' : ' Cruzado',
    '2' : ' Meio',
    '3' : ' Paralelo',
    '*' : 'Winner',
    '@' : 'Unforced Error',
    '#' : 'Forced Error',
    'o' :'standard overhead/smash',
    'p' :'backhand overhead/smash',
    'u' :'forehand drop shot',
    'y' :'backhand drop shot',
    'l' :'forehand lob',
    'm' :'backhand lob',
    'h' :'forehand half-volley',
    'i' :'backhand half-volley',
    'j' :'forehand swinging volley',
    'k' :'backhand swinging volley',
    'n' : 'net',
    'w' : 'wide' ,
    'd' : 'deep',
    'x' : 'both wide and deep',
    'g' : 'foot faults',
    't' : 'trick shot',
    'q' : 'unknown',
    'e' : 'any',
    '+' : 'net',
    'No Return' : 'No Return'
}

def GetStrokes():
    return StrokesDictionary


def Sequencer(Points):
    Rally = RallyExtraction(Points)

    data = [RallyParsing(d,StrokesDictionary) for d in Rally]

    Sequences = []
    Endings = []
    for seq, end in data:
        Sequences.append(seq)
        Endings.append(end)
    
    return Sequences, Endings

def SequencerShots(Points):
    Rally = RallyExtraction(Points)

    data = [RallyParsingCounter(d,StrokesDictionary) for d in Rally]

    Sequences = []
    Endings = []
    for seq, end in data:
        Sequences.append(seq)
        Endings.append(end)
    
    return Sequences, Endings

def SequencerServe(Points):
    Rally = RallyExtraction(Points)

    data = [RallyParsing(d,StrokesDictionary) for d in Rally]

    Sequences = []
    Endings = []
    for seq, end in data:
        Sequences.append(seq[-3:])
        Endings.append(end)
    
    return Sequences, Endings

# Initialize the PrefixSpan algorithm
def CallPrefixSpan(Sequences, min_support, k = 0):
    ps = PrefixSpan(Sequences)

    # Find frequent subsequences
    frequent_patterns = ps.frequent(min_support)
    filtered_pattern = [(sup,seq) for sup, seq in frequent_patterns if len(seq) >= k]


    return filtered_pattern

def SortPatterns(patterns):
    sorted_values = sorted(patterns, key=lambda x : x[0],reverse=True)

    return sorted_values

def check_list_contained(A, B):
  # convert list A to string
    A_str = ' '.join(map(str, A))
    # convert list B to string
    B_str = ' '.join(map(str, B))
    # find all instances of A within B
    instances = re.findall(A_str, B_str)
 
    # return True if any instances were found, False otherwise
    return len(instances) > 0


# Non-contiguos sequence mining
def Seqmining(Sequences, k ):
    freq_seqs = seqmining.freq_seq_enum(Sequences, min_support=100)

    k = 4
    # Exibir resultados
    filtered_seq = [(seq,sup) for seq, sup in freq_seqs if len(seq) >= k]

    sorted_values = sorted(filtered_seq, key=lambda x : x[1],reverse=True)

    return sorted_values[:10]

def find_contiguous_patterns(sequences, min_support, k=5, max_length=None):
    
    if max_length is None:
        max_length = float('inf')  # No maximum length constraint
    
    # Counter to store pattern frequencies
    pattern_counts = Counter()

    # Generate all contiguous subsequences
    for sequence in sequences:
        seq_len = len(sequence)
        for start in range(seq_len):
            for length in range(k, min(max_length, seq_len - start) + 1):
                subsequence = tuple(sequence[start:start + length])
                pattern_counts[subsequence] += 1

    # Filter patterns by minimum support
    frequent_patterns = [(count, pattern) for pattern, count in pattern_counts.items() if count >= min_support]
    
    return frequent_patterns

# def SortByOcurrence(Sequences, Patterns):
#     idx = []
#     for S in Patterns:
#         count = 0
#         result = [check_list_contained(S[1],s) for s in Sequences]
#         for i in range(len(result)):
#             if result[i] == True:
#                 # print(Endings[i])
#                 count+=1
        
#         idx.append(count)
#         S += (count)
    
#     sorted_values = [x for _, x in sorted(zip(idx, Patterns),reverse=True)]

#     return sorted_values

def FindSeq(data,k,Stat,serve=None,result=None):

    Stats = data[data[Stat] == True]

    if serve != None:
        Stats = Stats[Stats['Server'] == serve]

    if result != None:
        Stats = Stats[Stats['Victor'] == result]

    min_support = int(len(Stats)/200)

    Sequences, _ = Sequencer(Stats)
    Stats_Patterns = find_contiguous_patterns(Sequences,min_support,k)
    SortedPatterns = SortPatterns(Stats_Patterns)

    return SortedPatterns

def FindSeqFinal(data,k,Stat,serve=None,result=None,surface = None):

    Stats = data[data[Stat] == True]

    if serve != None:
        Stats = Stats[Stats['Server'] == serve]

    if result != None:
        Stats = Stats[Stats['Victor'] == result]

    if surface != None:
        Stats = Stats[Stats['Surface'] == surface]

    min_support = int(len(Stats)/200)

    Sequences, _ = SequencerServe(Stats)
    Stats_Patterns = find_contiguous_patterns(Sequences,min_support,k)
    SortedPatterns = SortPatterns(Stats_Patterns)

    return SortedPatterns


def PatternsByStat(Stat, Points, min_support, k):
    Stats = Points[Points[Stat] == True]

    Sequences, _ = Sequencer(Stats)
    Stats_Patterns = find_contiguous_patterns(Sequences,min_support,k)
    SortedPatterns = SortPatterns(Stats_Patterns)

    return SortedPatterns


