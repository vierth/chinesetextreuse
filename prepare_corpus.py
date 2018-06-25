'''
This script takes every file in a folder named 'corpus' and transforms it into
a serialized object that can be used to study intertextuality at a large level.
This is the first step in the analysis workflow. It removes unwanted punctuation
and other artifacts from the texts, parses metadata from the file titles and saves
it into a "pickle" file. Note that all pickle files in this workflow are generated
by these scripts. If you do not trust the source of your pickle files,  you should
never open them, as they can contain arbitrary code! This assumes you are using the
Anaconda distribution of Python 3.

Assumed Filename format is this:
Title-Era-Author_TextDivison.txt

TextDivision should be zero if the text has not been divided. Otherwise, it can be
chapter number, volume number, etc.
'''

import os, re, pickle, sys

#*****************#
# PREP PARAMETERS #
#*****************#

# Name of save file. Leave as "corpus.pickle" for best compatibility with other scripts
picklefile = "corpus.pickle"

# Items to remove from texts
toremove = ['』','。', '！', '，', '：', '、', '（', '）', '；', '？', '〉', '〈', '」', '「', '『', '“', '”', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '_', '`''{', '|', '}', '~', '¤', '±', '·', '×', 'à', 'á', 'è', 'é', 'ê', 'ì', 'í', 'ò', 'ó', '÷', 'ù', 'ú', 'ü', 'ā', 'ī', 'ń', 'ň', 'ō', 'ū', 'ǎ', 'ǐ', 'ǔ', 'ǖ', 'ǘ', 'ǚ', 'ǜ', 'ǹ', 'ɑ', 'ɡ', 'α', 'β', 'γ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω', 'а', 'б', 'в', 'г', 'д', 'е', 'к', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё', '—', '‖', '‘', '’', '…', '※', 'ⅰ', 'ⅲ', '∈', '∏', '∑', '√', '∠', '∥', '∧', '∩', '∪', '∫', '∮', '∶', '∷', '∽', '≈', '≌', '≡', '⊙', '⊥', '⌒', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑴', '⑵', '⑶', '⑷', '⑸', '⑹', '⑺', '⑻', '⑼', '⑽', '⑾', '⑿', '⒀', '⒁', '⒂', '⒃', '⒄', '⒅', '⒆', '⒈', '⒉', '⒊', '⒋', '⒌', '⒍', '⒎', '⒏', '⒐', '⒑', '⒒', '⒓', '⒔', '⒕', '⒖', '⒗', '⒘', '⒙', '⒚', '⒛', '─', '┅', '┋', '┌', '┍', '┎', '┏', '┐', '┑', '┒', '┓', '└', '┕', '┘', '┙', '┚', '┛', '├', '┝', '┞', '┠', '┡', '┢', '┣', '┤', '┥', '┦', '┧', '┩', '┪', '┫', '┬', '┭', '┮', '┯', '┰', '┱', '┲', '┳', '■', '□', '▲', '△', '◆', '◇', '○', '◎', '●', '★','︶', '﹑', '﹔', '﹖', '＂', '＃', '％', '＆', '＊','．', '／', '０', '１', '２', '３', '４', '５', '６', '７', '８', '９', '＜', '＝', '＞', '＠', '［', '＼', '］', '＿', '｀', 'ａ', 'ｂ', 'ｃ', 'ｄ', 'ｅ', 'ｆ', 'ｇ', 'ｈ', 'ｉ', 'ｊ', 'ｋ', 'ｌ', 'ｍ', 'ｎ', 'ｏ', 'ｐ', 'ｑ', 'ｒ', 'ｓ', 'ｔ', 'ｕ', 'ｖ', 'ｗ', 'ｘ', 'ｙ', 'ｚ', '｛', '｝', '～', '￥','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','《', '》', '〔', '〕', '【', '】', 'A',  'B',  'C',  'D',  'E',  'F',  'G',  'H', 'I', 'J', 'K', 'L', "M", 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',  'Ｗ',  'Ｘ',  'Ｙ',  'Ｚ',  '＾',  '｜', '￠',  '￡', '~']

#**********************#
# FUNCTION DEFINITIONS #
#**********************#

# clean the text. This will remove everything in the above list from the text
def clean(content,remove):
    # These two lines are useful for Chinese texts where there was no whitespace or punctuation
    # in the original documents
	content = re.sub('\s+', '', content)
	for item in remove:
		content = content.replace(item, "")
	return content

#*********************#
# START OF MAIN LOGIC #
#*********************#

# containers for the data. The final file will be a list of lists. The first item
# will be metadata, and the second item will be the texts themselves.
all_filenames = []
all_texts = []

# Track the total length of the corpus.
totalcharacters = 0

# Retrieve the directory information
for root, dirs, files in os.walk('corpus'):
    # remove license file if present
    files = [f for f in files if f != "LICENSE"]
    # Iterate through each file in the filelist
    for i,f in enumerate(files):

        # remove extension
        file_name = f[:-4]

        with open(f"{root}/{f}") as tf:
            # clean text, append it to all texts, and increment total length tracker
            text = clean(tf.read(),toremove)
            all_texts.append(text)
            totalcharacters += len(text)

            # Save metadata
            all_filenames.append(file_name)
        
        # print tracking statement
        sys.stdout.write(f"{i + 1} documents of {len(files)} completed\r")
        sys.stdout.flush()

# Print basic corpus information
print(f"\n{totalcharacters} from {len(all_texts)} documents.")

# Save data to pickle
pickle.dump([all_filenames, all_texts], open(picklefile, "wb"))