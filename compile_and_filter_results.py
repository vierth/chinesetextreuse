'''
This script takes each file in the results directory and compiles them
into a single file. It also filters out common results (and results that
are highly similar to the common quotes) if the user chooses to do so.
'''

import pickle, os, Levenshtein, time, sys
from multiprocessing import Pool
from itertools import repeat, chain

#**********************#
# FILTERING PARAMETERS #
#**********************#

# Filter the common, short quotes?
FILTERCOMMON = True
# What length constitutes "short"?
SHORTQUOTELENGTH = 20
# How many repetitions consitute common?
REPMAX = 400

# Should similar to the common ones be filtered?
# This will add significant slowdown depending on how many
# quotes are included
FILTERSIMILAR = True
# What is the similarity threshold?
SIMILARITYTHRESHOLD = .6
# Limit check? If this is true, similarity will only be checked
# for quotes that start with the same characters. This speeds the
# code up significantly
LIMITCHECK = True
LIMEXTENT = 2

#************************#
# Input and output files #
#************************#

# Input directory
QUOTERESULTCORPUS = "results"
# Output
OUTPUTFILE = "corpus_results.txt"

#**********************#
# FUNCTION DEFINITIONS #
#**********************#


# This function removes common quotes, and similar quotes as requested
def remove_common(quoteinfo, threshold=REPMAX,filtersimilar=FILTERSIMILAR,simthresh=SIMILARITYTHRESHOLD):
    # Identify common quotes
    print(f"\nCounting short quotes")
    quote_scores = {}
    for line in quoteinfo:
        info = line.split("\t")
        # remove alignment information
        relevant_quote = info[6]
        # Calculate short quote frequency
        if len(relevant_quote) < SHORTQUOTELENGTH:
            try:
                quote_scores[relevant_quote] += 1
            except:
                quote_scores[relevant_quote] = 1


    print(f"Identifying high incidence quotes")
    # return quotes that should be discarded
    to_discard = set([q for q,v in quote_scores.items() if v > threshold])
    
    if filtersimilar:
        print("Removing high incidence and similar results")
    else:
        print("Removing high incidence quotes")

    temptime = time.time()
    totaltime = 0
    save = []
    total_quotes = len(quoteinfo)

    # Iterate through the information and discard unwanted information
    for line in quoteinfo:
        add = True
        info = line.split("\t")
        relevant_quote = info[6]
        # Save the quote if it is longer than the cutoff
        if relevant_quote in to_discard:
            add = False
        # Otherwise, check its length. If it is shorter than the cuttoff 
        # and filtersimilar is set to true, check to see if it is similar
        # to discarded quotes quotes.
        elif len(relevant_quote) < SHORTQUOTELENGTH and filtersimilar:
            for common in to_discard:
                if LIMITCHECK:
                    if common[0:LIMEXTENT]==relevant_quote[0:LIMEXTENT]:
                        if Levenshtein.ratio(relevant_quote, common) >= simthresh:
                            add = False
                            break
                else:
                    if common[0]==relevant_quote[0]:
                        if Levenshtein.ratio(relevant_quote, common) >= simthresh:
                            add = False
                            break
        if add:
            save.append(line)
        total_quotes -= 1
        if total_quotes % 10000 == 0:
            ft = time.time() - temptime
            totaltime += ft
            sys.stdout.write(f"{total_quotes} quotes remaining. {ft:.2f}/{totaltime:.2f} secs                \r")
            sys.stdout.flush()
            temptime = time.time()
        
    quoteinfo = save
    return quoteinfo

#*********************#
# START OF MAIN LOGIC #
#*********************#
def compileFilter(resultsCorpus="results", filterCommon=True, outputFile="corpus_results.txt", threshold=400, filtersimilar=True,simthresh=.6):
    # Start timer
    gs = time.time()

    # Container for the resulting information
    results = []

    # Compile results into a single list
    for root, dirs, files in os.walk(resultsCorpus):
        for i,f in enumerate(files):
            with open(os.path.join(root, f), "r") as rf:
                contents = rf.read().split("\n")
                for line in contents:
                    if line[:11] != "TargetTitle" and len(line) > 0:
                        results.append(f"{f[:-4]}\t{line}")
            sys.stdout.write(f"{i + 1} results of {len(files)} processed.\r")
            sys.stdout.flush()

    # Filter empty results (just in case)
    results = [r for r in results if len(r) > 0]

    # Filter out common quotes if desired
    if filterCommon:
        results = remove_common(results, threshold=threshold,filtersimilar=filtersimilar,simthresh=simthresh)

    # Write results to file
    with open(outputFile, "w") as wf:
        wf.write("SourceTitle\tTargetTitle\tLength\tRatio\tSourcePlace\tTargetPlace\tSourceText\tTargetText\n")
        wf.write("\n".join(results))

    ge = time.time()
    gt = ge-gs
    print(f"Global Operation completed in {gt:.2f} seconds")

if __name__ == "__main__":

    compileFilter()