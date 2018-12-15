'''
This is a centralized location from which to run all of the analyses. This
prevents mistakes in the order in which the code needs to run.
'''

from prepare_corpus import createCorpus
from index_corpus import formIndex
from detect_intertexuality import detectIntertextuality
from compile_and_filter_results import compileFilter
from align_quotes import alignQuotes

####################
# ANALYSIS OPTIONS #
####################

# Define the analysis characteristics
# set the seed length
seedLength = 4

# How long is the minimal match?
matchLength = 10

# How similar is the minimum similarity?
threshhold = .8

# Set this to limit the similarity comparison to last n characters
# Set to None for no limit. Setting a limit significantly
# speeds the calculations up.
maxComp = 100

############################
# CORPUS AND FILE CREATION #
############################

# Name of the folder that contains the corpus
corpusFolder = "corpus"

# Name of corpus save file.
pickleFile = "corpus.pickle"

# where should the results be saved
resultsCorpus="results"

# What should the final output file be called?
resultsFile="corpus_results.txt"

# What should the aligned output file be called?
alignedFile = "corpus_alignment.txt"

# What should the network output file be called?
networkFile = "edgetable.csv"

#################
# INDEX OPTIONS #
#################

# Would you like to build an index? If so, set buildIndex to True. 
buildIndex = True

# Output corpus file (should end with .db). Can be None if buildIndex is false
indexFile = 'index.db'


#####################
# FILTERING OPTIONS #
#####################
# Do you want to filter the most common quotes?
filterCommon=True

# Do you want to filter quotes that are similar to the common quotes 
# (increases) processing time.
filterSimilar=True

# How often does a quote need to appear to be "common"?
minimumQuoteThresh = 400

# How similar does a quote need to be to be filtered?
minimumSimilarityThreshold = .6

#####################
# ALIGNMENT OPTIONS #
#####################

# Which documents do you want to align? 
alignmentDocs = ["KR2a0018 梁書-唐-姚思廉_10","KR2a0024 南史-唐-李延壽_54","KR2a0018 梁書-唐-姚思廉_11"]

# How would you like to score the alignment?
matchingChars = 1
mismatchingChars = -1
gap = -1

# The following options speed up the alignment process. The results are divided
# into chunks and then joined back together
chunkLim = 200 # limits the number of characters to align at once
overlap = 10 # how long of an overlap to fuse chunks
rangeMatch = 6 # how many characters must match to fuse

###################
# NETWORK OPTIONS #
###################

# How much matching should there be to produce an edge between documents?
scoreLimit = 100

###############
# VIZ OPTIONS #
###############



##################
# CORPUS DETAILS #
##################
# what is the character encoding of your files
characterEncoding = "utf8"

################
# RUN FUNCTION #
################

def run():
    # Create the corpus file. You can optionally specify if you want to remove
    # whitespace removeWS (set to True or False), and a list of characters to 
    # remove removeChars (set to a list)
    # createCorpus(corpusFolder, pickleFile, CORPUS_ENCODING=characterEncoding)

    # Create an index if desired:
    #if buildIndex:
    #    print("Creating Index")
    #    formIndex(seedLength, pickleFile, indexFile)

    # Run the main intertextuality algorithm
    
    # Other options are  maxChildTasks=250,  frontLoading=True, 
    # textsToAnalyze="filename.txt", corpusComposition="filename.txt"
    # setEncoding='utf8', resultsDirectory="results"
    # detectIntertextuality(seedLength, matchLength, threshhold, maxComp, 
    #                      pickleFile, hasPreppedIndex=buildIndex, 
    #                      indexFile=indexFile, DEBUG= False,
    #                      setEncoding=characterEncoding)

    # Compile and filter the results
    # Other options are setEncoding='utf8'
    # compileFilter(resultsCorpus=resultsCorpus, filterCommon=filterCommon, 
    #               outputFile=resultsFile, threshold=minimumQuoteThresh, 
    #               filtersimilar=filterSimilar, 
    #               simthresh=minimumSimilarityThreshold,
    #               setEncoding=characterEncoding)

    # align the results
    # alignQuotes(resultsFile, alignedFile, matchingChars, gap, mismatchingChars,
    #             chunkLim, overlap, rangeMatch, alignmentDocs=alignmentDocs,
    #             setEncoding=characterEncoding)
    
    # create a network from the results
    # createNetwork(resultsFile, networkFile, scoreLimit, 
    #               setEncoding=characterEncoding)

    # create a visualization of the intertextuality
    # createViz()

if __name__ == "__main__":
    run()