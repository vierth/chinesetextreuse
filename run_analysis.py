'''
This is a centralized location from which to run all of the analysis. This
prevents mistakes in the order in which the code needs to run.
'''

from prepare_corpus import createCorpus
####################
# ANALYSIS OPTIONS #
####################

###################
# CORPUS CREATION #
###################

# Name of the folder that contains the corpus
corpusFolder = "corpus"

# Name of corpus save file.
pickleFile = "corpus.pickle"

#################
# INDEX OPTIONS #
#################




def run():
    # Create the corpus file. You can optionally specify if you want to remove
    # whitespace removeWS (set to True or False), and a list of characters to 
    # remove removeChars (set to a list)
    createCorpus(corpusFolder, pickleFile)


if __name__ == "__main__":
    run()