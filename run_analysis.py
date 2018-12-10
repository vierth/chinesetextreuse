'''
This is a centralized location from which to run all of the analysis. This
prevents mistakes in the order in which the code needs to run.
'''

from prepare_corpus import createCorpus
from index_corpus import formIndex
from detect_intertexuality import detectIntertextuality
from compile_and_filter_results import compileFilter

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
outputFile="corpus_results.txt"

# What should the aligned output file be called?


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

################
# RUN FUNCTION #
################

def run():
    # Create the corpus file. You can optionally specify if you want to remove
    # whitespace removeWS (set to True or False), and a list of characters to 
    # remove removeChars (set to a list)
    # createCorpus(corpusFolder, pickleFile)

    # Create an index if desired:
    #if buildIndex:
    #    print("Creating Index")
    #    formIndex(seedLength, pickleFile, indexFile)

    # Run the main intertextuality algorithm
    
    # Other options are  maxChildTasks=250,  frontLoading=True, 
    # textsToAnalyze="filename.txt", corpusComposition="filename.txt"
    # setEncoding='utf8', resultsDirectory="results"
    #detectIntertextuality(seedLength, matchLength, threshhold, maxComp, 
    #                      pickleFile, hasPreppedIndex=buildIndex, 
    #                      indexFile=indexFile, DEBUG= False)

    # Compile and filter the results
    # compileFilter(resultsCorpus=resultsCorpus, filterCommon=filterCommon, 
    #               outputFile=outputFile, threshold=minimumQuoteThresh, 
    #               filtersimilar=filterSimilar, 
    #               simthresh=minimumSimilarityThreshold)

if __name__ == "__main__":
    run()