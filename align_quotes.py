'''
This script takes the compiled results compiles and aligns quotes
between documents that the scholar is interested in. If no documents
are listed, this operates on the entire corpus, but can be very slow
depending on corpus size.
'''

import pickle, os, time, sys, Levenshtein
import numpy as np
from multiprocessing import Pool
from itertools import repeat, chain

#********************#
# DOCUMENTS TO ALIGN #
#********************#

# Align quotes occuring between the following documents. Provide at least two. 
# If None, all quotes will be aligned. If your corpus contains signficant 
# reuse, this may be slow.
alignment_docs = ["KR2a0018 梁書-唐-姚思廉_10","KR2a0024 南史-唐-李延壽_54","KR2a0018 梁書-唐-姚思廉_11"]


#**********************#
# ALIGNMENT PARAMETERS #
#**********************#

class alignmentParameters:
    def __init__(self, matchScore, misalignScore, mismatchScore, chunkLim, 
                 overlap, rangeMatch):
        self.matchScore = matchScore
        self.misalignScore = misalignScore
        self.mismatchScore = mismatchScore
        self.chunkLim = chunkLim
        self.overlap = overlap
        self.rangeMatch = rangeMatch



#****************#
# GLOBAL TRACKER #
#****************#
# to track alignment progress
tracker = 0

#**********************#
# FUNCTION DEFINITIONS #
#**********************#

# Divide texts into smaller chunks of a certain maximum length
# To optimze for later alignment, divide texts in areas of high
# homology
def divtexts(quote1, quote2, aParams):
    chunks = len(quote1)//aParams.chunkLim
    qs1 = 0
    qs2 = 0
    chunkedTexts = []
    for chunk in range(chunks + 1):
        if chunk != chunks:
            tqe1 = (chunk+1)*aParams.chunkLim
            tqe2 = (chunk+1)*aParams.chunkLim
        
            # retreive the boundary region
            tqr1 = quote1[tqe1-aParams.rangeMatch:tqe1+aParams.rangeMatch]
            tqr2 = quote2[tqe2-aParams.rangeMatch:tqe2+aParams.rangeMatch]
            
            # identify a stretch of identical overlap and save the midpoint
            qe1 = None
            qe2 = None
            for i in range(len(tqr1)-aParams.overlap):
                for j in range(len(tqr2)-aParams.overlap):
                    if tqr1[i:i+aParams.overlap] == tqr2[j:j+aParams.overlap]:
                        qe1 = tqe1 - aParams.rangeMatch + i + aParams.overlap//2
                        qe2 = tqe2 - aParams.rangeMatch + i + aParams.overlap//2
            # If no region is identified, just cut at initial boundary
            if not qe1:
                qe1 = tqe1
                qe2 = tqe2
            
            # save the cut region
            chunkedTexts.append([quote1[qs1:qe1],quote2[qs2:qe2]])

            # move the start of the next chunk to the end of the last one
            qs1 = qe1
            qs2 = qe2
        else:
            if len(quote1[qs1:]) == 0 or len(quote2[qs2:]) == 0:
                chunkedTexts[-1][0] += quote1[qs1:]
                chunkedTexts[-1][1] += quote2[qs2:]
            else:
                chunkedTexts.append([quote1[qs1:],quote2[qs2:]])
    return chunkedTexts
        
# Algorithm used for quote alignment. Insights into how this work come from the 
# original Needleman-Wunsch article, but also from 
# http://www.biorecipes.com/DynProgBasic/code.html
def align(quote1, quote2, aParams):
    
    # The alignment algorithm is O(n^2) so only alinging short chunks speeds
    # the process up. Here I divide each sequence into smaller chunks for 
    # alignment and then recombine them at the end.
    if len(quote1) > aParams.chunkLim:
        textchunks = divtexts(quote1, quote2, aParams)
    else:
        textchunks = [[quote1, quote2]]
    
    # Empty strings to store the calculated quotes
    total_quote_1 = ""
    total_quote_2 = ""

    # Iterate through each of the divided texts
    for texts in textchunks:
        
        # Create alignment matrix
        matrix = np.zeros([len(texts[0])+1,len(texts[1])+1])
        # prep matrix:
        for i in range(len(texts[0])+1):
            matrix[i][0] = -i
        for j in range(len(texts[1])+1):
            matrix[0][j] = -j

        
        # Iterate through both texts and fill out the matrix
        for i in range(len(texts[0])):
            for j in range(len(texts[1])):
                # Get characters to compare
                c1 = texts[0][i]
                c2 = texts[1][j]

                # If they are the same, give them the matching score.
                # Otherwise, give them the mismatch score
                if c1 == c2:
                    score = aParams.matchScore
                else:
                    score = aParams.mismatchScore

                # get the pertinent matrix location (which will be both plus 
                # one)
                matrixrow = i+1
                matrixcolumn = j+1

                # Calculate scores from top, left, and diagnol
                upperscore = matrix[i][j+1] + aParams.misalignScore
                leftscore = matrix[i+1][j] + aParams.misalignScore
                diagonal = matrix[i][j] + score

                # Select the highest score and place it in the box
                currentscore = max([upperscore, leftscore, diagonal])
                matrix[matrixrow][matrixcolumn] = currentscore

        # Create two empty strings for the traceback
        stringa = ""
        stringb = ""

        # Traceback to get the best alignment
        # Begin at the bottom right corner
        i = len(matrix)-1
        j = len(matrix[0])-1

        # Get the final score
        finalscore = matrix[i][j]

        # While i or j is above zero, trace backwards
        while i > 0 or j > 0:
            # Get the maximum value from the adjacent squares
            upper = matrix[i][j - 1]
            left  = matrix[i-1][j]
            diagonal = matrix[i-1][j-1]
            maxval = max([upper, left, diagonal]) 
            
            # If the maximum value is the diagonal, move diagonally
            if maxval == diagonal:
                i -= 1
                j -= 1
                stringa = texts[0][i] + stringa
                try:
                    stringb = texts[1][j] + stringb
                except:
                    print(texts, i, j)
            # If the maximum value is above, insert gap into stringa    
            elif maxval == upper:
                j -= 1
                stringa = " "+stringa
                stringb = texts[1][j] + stringb
            # If the maximum value is left, insert gap into stringb
            elif maxval == left:
                i -= 1
                stringa = texts[0][i] + stringa
                stringb = " "+stringb

        # add all parts of the string together
        total_quote_1 += stringa
        total_quote_2 += stringb  

    # Trim the bits left over from searching algorithm. In certain edge cases
    # the ends are not the same
    while total_quote_1[-1] == " " or total_quote_2[-1] == " ": 
        total_quote_1 = total_quote_1[:-1]
        total_quote_2 = total_quote_2[:-1]
    while total_quote_1[-1] != total_quote_2[-1]:
        total_quote_1 = total_quote_1[:-1]
        total_quote_2 = total_quote_2[:-1]
        
    return total_quote_1, total_quote_2

# Run the process
def runalignment(content,totallength, aParams):
    global tracker
    info = content.split("\t")
    # If the quotes are identical, no need to align them
    if float(info[3]) != 1.0:
        # Run the alignment algorithm
        aligneda, alignedb = align(info[6], info[7], aParams)

        # Save the information
        info[6] = aligneda
        info[7] = alignedb
        content = "\t".join(info)
    tracker += 1
    if tracker % 1000 == 0:
        sys.stdout.write(f"{tracker} out of {totallength} aligned          \r")
        sys.stdout.flush()
    return content

#*********************#
# START OF MAIN LOGIC #
#*********************#

def alignQuotes(corpusResults, outputFile, matchScore, misalignScore, 
                mismatchScore, chunkLim, overlap, rangeMatch, 
                alignmentDocs=None, setEncoding="utf8"):

    # create alignment parameter object:
    aParams = alignmentParameters(matchScore, misalignScore, mismatchScore, chunkLim, 
    overlap, rangeMatch)

    # Start a global timer
    gs = time.time()

    # Initialize thread pool for parallel processing
    pool = Pool()
    runtimes = []
    save_contents = []


    # Results container
    results = []
    # Iterate through each line in the file aligning the results using map
    with open(corpusResults, "r") as rf:
        contents = rf.read().split("\n")
        contents = contents[1:]
        
        # If alignment_docs have beeen provided, extract the relevant quotes
        if alignmentDocs:
            use_contents = []
            pairs = set()
            for t1 in alignmentDocs:
                for t2 in alignmentDocs:
                    if t1 != t2:
                        pairs.add((t1, t2))

            for line in contents:
                info = line.split("\t")
                pair = (info[0], info[1])
                if pair in pairs:
                    use_contents.append(line)
            contents = use_contents

        results = pool.starmap(runalignment,
                               zip(contents,repeat(len(contents)), 
                                   repeat(aParams)))


    # Remove blank results and flatten the list    
    save_contents = [s for s in results if len(s) > 0]

    with open(outputFile, "w", encoding=setEncoding) as wf:
        wf.write("\n".join(save_contents))

    ge = time.time()
    gt = ge-gs
    print(f"Global Operation completed in {gt:.2f} seconds")

# Match, mismatch, and gap scores
MATCHSCORE = 1
MISALIGNSCORE = -1
MISMATCHSCORE = -1

# Limit the length of text that will be aligned
# This significantly speeds up the algorithm when
# aligning very long quotes. This divides the quotes
# into blocks of CHUNKLIM length. It tries to divide
# the chunks in places where the alignment is exact
# So OVERLAP looks at the 10 character before and after
# the proposed break. When it finds RANGEMATCH exact
# characters, it inserts a break in the middle.
CHUNKLIM = 200
OVERLAP = 10
RANGEMATCH = 6

if __name__ == "__main__":
    corpusResults = "corpus_results.txt"
    outputFile = "corpus_alignment.txt"
    alignmentDocs = ["KR2a0018 梁書-唐-姚思廉_10","KR2a0024 南史-唐-李延壽_54","KR2a0018 梁書-唐-姚思廉_11"]
    alignQuotes(corpusResults, outputFile, 1, -1, -1, 200, 10, 6, alignmentDocs=alignmentDocs)