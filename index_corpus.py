'''
Pre index the corpus for faster intertextuality processing.
Non-duplicate seeds are removed from the index as per
Smith et al and Holston. This uses a sqlite database to store
the resulting index.
'''

import pickle, os, json, sqlite3, time, sys

#******************#
# INDEX PARAMETERS #
#******************#

# Set seed length to track
seedLength = 4

# Input file
dataFile = 'corpus.pickle'

# Output corpus file
indexFile = 'index.db'

#*********************#
# START OF MAIN LOGIC #
#*********************#

def formIndex(seedLength, dataFile, indexFile):
    s = time.time()

    # Load data
    data = pickle.load(open(dataFile,"rb"))




    # Delete any old indices
    if os.path.isfile(indexFile):
        os.remove(indexFile)

    # Connect to the database
    connection = sqlite3.connect(indexFile)
    c = connection.cursor()

    # Create a table for the index information
    c.execute('CREATE TABLE info (textid integer, data text)')

    # Get texts from data
    texts = data[1]

    # Container for a numerical ID for each seed. I do this to save space in 
    # the created index.
    seed_to_id = {}
    # Tracks which seed id to assign a seed.
    seed_id_to_assign = 0

    # Container for each text index
    text_index = []

    # Container to track how many documents a given seed appears in
    # This is so we can remove seeds that only appear in a single document
    seed_doc_counts = {}

    # Iterate through each text
    for tnum,text in enumerate(texts):
        # Create a dictionary for index
        local_index = {}

        # Iterate through the text dividing it into overlaping n-grams
        # of the input seedLength
        for i in range(len(text)-seedLength):
            seed = text[i:i+seedLength]
            
            # Retrieve the seed id for the given seed. If none exist, create one
            # and incremete the seed id to assign
            try:
                current_seed_id = seed_to_id[seed]    
            except:
                seed_to_id[seed] = seed_id_to_assign
                current_seed_id = seed_id_to_assign
                seed_id_to_assign += 1
            
            # Save the location of the current seed. Append it to the existing
            # locations if seen. If not, create a new list. If it is the first
            # time seeing a seed, increment the number of seen docs.
            try:
                local_index[current_seed_id].append(i)
            except:

                local_index[current_seed_id] = [i]
                try:
                    seed_doc_counts[current_seed_id] += 1
                except:
                    seed_doc_counts[current_seed_id] = 1

        # Save index to text list
        text_index.append(local_index)
        
        # Print out current status
        sys.stdout.write(f"First pass {tnum + 1} of {len(texts)}\r")
        sys.stdout.flush()
    print("\nFirst pass complete")

    # Take a second pass through the data to save seeds that appear more than once
    for i,local_index in enumerate(text_index):

        # This list will contain a list of indices for each seed
        local_list = []
        # This tracks where in the local list a given seed's indices appear
        seed_index = 0
        # This dictionary takes a seed and returns the index in the local list
        local_dictionary = {}

        # Go through each seed in the saved index
        for seed in local_index.keys():
            # If the seed appears in more than one document, save its indices.
            if seed_doc_counts[seed] > 1:
                locations = local_index[seed]
                local_list.append(locations)
                # Here the seed id is saved as a string because of quirks of the
                # json serialization
                local_dictionary[str(seed)] = seed_index
                seed_index += 1            

        # Convert data into a json object for storage in database
        seeddata = json.dumps([local_dictionary,local_list,list(local_dictionary.keys())])
        # Insert the data into the database
        c.execute(f"INSERT INTO info VALUES('{i}','{seeddata}')")
        
        # Write the status of the script
        sys.stdout.write(f"Single seeds removed from {i + 1} texts\r")
        sys.stdout.flush()
    print("\nSecond pass complete")

    # Commit index to database
    connection.commit()

    # Close database connection
    connection.close()

    # Measure time usage and print final status
    e = time.time()
    t = e-s
    print(f"Operation completed in {t:.2f} seconds")

if __name__ == "__main__":
    formIndex(seedLength, dataFile, indexFile)