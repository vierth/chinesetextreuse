'''
This script takes in the aggregated corpus created by compile_and_filter_results.py
and transforms them into a format that is compatible with the popular network
analysis program Gephi. This will allow you to identify communities of texts 
that are closely related with each other that can then be studied using the chord
visualizer.
'''




#*********************#
# START OF MAIN LOGIC #
#*********************#

def createNetwork(inputFile, outputFile, scoreLimit, setEncoding="utf8"):
    # Containers for corpus information
    edge_info = {}
    edges = []

    # open datafile
    with open(inputFile,'r') as f:
        contents = f.read().split("\n")
        contents = contents[1:]
        for line in contents:
            info = line.split("\t")
            
            # create an edge id
            edge = (info[0], info[1])
            # get a quote score (length of quote times similarity)
            score = int(info[2]) * float(info[3])
            # track the cumulative score of an edge by adding quote scores together
            # also keep track of how many quotes are shared among documents
            try:
                stored_info = edge_info[edge]
                edge_info[edge] = [stored_info[0]+score, stored_info[1]+1]
            except:
                edge_info[edge] = [score, 1]
                edges.append(edge)

    # Output the data as a table compatible with Gephi
    edges_for_gephi = ["Source,Target,EdgeScore,TotalQuotes"]
    for edge in edges:
        info = edge_info[edge]
        # If the edge is at or above the score limit, save the edge
        if info[0] >= scoreLimit:
            edges_for_gephi.append(",".join([edge[0],edge[1],str(info[0]),str(info[1])]))

    # save data
    with open(outputFile,'w', encoding=setEncoding) as wf:
        wf.write("\n".join(edges_for_gephi))

if __name__ == "__main__":
    #************#
    # PARAMETERS #
    #************#

    # Set a minimum threshold for similarity. 100 means one 100-character quote
    # or alternatively ten 10-character quotes (or something like that)
    SCORELIMIT = 100

    #************************#
    # INPUT AND OUTPUT FILES #
    #************************#

    # Input
    INPUTFILE = 'corpus_results.txt'
    # Output
    OUTPUTFILE = 'edgetable.csv'
    createNetwork(INPUTFILE, OUTPUTFILE, SCORELIMIT, setEncoding="utf8")
