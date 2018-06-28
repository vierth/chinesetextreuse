This is a suite of tools that takes raw texts as input, cleans them, preps them, and then runs an intertextuality detection algorithm.

Additionally, it aligns the resulting quotes and can arrange the results in a network format for exploration in outside tools.

# Requirements
This suite has been tested on a machine running Ubuntu 16.04 with an i7 processor and 64GB of RAM

It requires the Anaconda distribution of Python 3 (minimum Python 3.6.3)

Additionally, it requires the Levenshtein library, which is not included in Anaconda. You can install this using pip install python-Levenshtein. 

Note that this suite of tools uses Pickle for object serialization. Be wary of unpickling files from untrusted sources!

As of June 22nd, 2018, this may not be compatible with Windows systems because of issues with the Python multiprocessing library. I plan to fix this in the near future.

# Step One
## prepare_corpus.py   
Cleans and preps corpus.
Outputs a pickle file containing the cleaned texts and file titles.
This script assumes that the files in the corpus have the following structure for their name:

Title-Era-Author_Section.txt

This will clean the documents by removing all punctuation and artifacts unnecessary for understanding intertexuality
in a pre 1911 Chinese corpus.

Creates a pickle file named "corpus.pickle" which contains a list with two items: a list of file names and a list of the text contents

### Demo corpus
The included corpus is derived from the Kanripo shadow repository at https://github.com/kr-shadow/KR2 It is a limited collection of historical documents to be used for testing the algorithm.

Thanks to Christian Wittern for the compilation of this dataset.

This is a corpus of 63 historical texts divided into their 4,100 constituent juan (scrolls or fascicles).

The corpus was chosen for a balance between size and speed of processing to demonstrate the code. It should stay under 16GB of RAM, but depending on your exact set up, it may exceed this.

## Optional
## index_corpus.py 
You can optionally create an index for the corpus. This will significantly speed up intertextuality detection. It will, however, also significantly increase disk space and memory usage. I recommend using this only if your corpus is over 10 texts and 1 million characters. Otherwise, the overhead of creating the index is not worth the savings it provides.

Here you can set the seed lenght used for identifying reuse. You can also set this in detect_intertextuality.py for when you create the corpus on the fly.

Creates a sqlite database called "index.db" with an "info" table with textid and data columns

Data is saved on a per text basis as a json string. The size of this index tends to be about 4 times the size of the prepared corpus file.


# Step Two
## detect_intertexuality.py
This is the most important script and where most of the work actually happens. detects intertexuality. There are several options when running this. If you are concerned with memory use, run without creating an index. Otherwise, you can create one on the fly by setting INDEXFILE = None.

Here you can set the seedlength, similarity threshold, and minimum match length You can also provide a file with specific texts to analyze (if you only want to compare several to the corpus). You can also limit the corpus against which you are comparing the texts.

If there is an index file, the index is loaded into memory and then analysis happens

The results are saved into a directory called results. The directory, if it exists, will be deleted if debug is set to true, so be careful! The results from each text are saved into an individual file.

# Step Three
## compile_and_filter_results.py
This script compiles the results in every file in the results directory. Here you can remove results that are common if you like by setting FILTERCOMMON to True. You can also remove similar quotes, but this is quite slow.

Results are saved in the corpus_results.txt file.

# Step Four
## form_quote_system.py
This creates an network visualization of the quote system. This is so you can import the data into a tool like Gephi to identify closely related texts. You can set the minimum necessary similarity for saving by changing SCORELIMIT. 

Outputs a gephi compatible edge list titled "edges.csv"

# Step Five
## align_quotes.py 
You can align the quotes using the Needleman Wunsch algorithm with this script. There are several speed optimizations in the code itself, but it is based almost entirely on algorithms. Here you can specify the documents you are interested in. It is generally not necessary to align EVERYTHING, though you can if you want by specifying
alignment_docs = None
Normally, you shoud provide a list of document names as the purpose is to aid in reading alignment_docs = ["doc1", "doc2"] You can also adjust the scores given to tweak your prefered alignment type. This outputs a file called "corpus_alignment.txt"

# Step Six
## build_chord_viz.py
This simply converts information found in corpus_alignment.txt and corpus_text_lengths.txt to a format that is loaded into viz.html, a simple chord viewer and intertextuality explorer written in d3js.
outputs "edge_data.js"

# Step Seven
## viz.html
Simply open this file in your browser. Click on an chord to see the aligned text.
