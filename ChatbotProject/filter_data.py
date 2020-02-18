from string import digits
import re as reg
from tqdm import tqdm


pattern = reg.compile(r"(.)\1{1,}", reg.DOTALL)

puncList = ["&gt","amp","%",'newlinechar',"~",".","\t","\n", "^", "_", "*", "<", ">", ";", ":", "!", "?", "/", "\\", ",", "#", "@", "$", "&", ")", "(", "\"", "]", "[", "|", "{", "}","=","-","+","\""]
links = ["http", "https", "htp", "www", "com"]
detected_irregular_words = ["bo","wo","ho","m","yes","oh","no"]
detected_regular_words = ["looks","totally","subreddit","off","fall","gonna","typically","reddit"]
filtered_sentences_from_index = []
filtered_sentences_to_index = []
common_index = []

from_file = "data\\from.txt"
to_file = "data\\to.txt"

filtered_from_file = 'data\\train_from_filtered'
filtered_to_file = 'data\\train_to_filtered'

from_lines = []
to_lines = []

isascii = lambda s: len(s) == len(s.encode())
remove_digits = str.maketrans('', '', digits)
regular_words = []

def remove_numbers(content):
    return content.translate(remove_digits)

def remove_inerpunction_and_nonascii_chars(content):
    new_content = ""
    content = content.split(" ")
    for word in content:
        word = word.strip()
        for punc in puncList:
            word = ''.join(word.split(punc))
        if word != "" and word != " " and isascii(word):
            new_content = new_content + " " + word
    return new_content.strip()

def content_is_link(content):
    for link in links:
        if link in content:
            return True
    return False

def acceptable_size(content):
    content.strip()
    if content == "" or content == " ":
        return False
    _content = content.split(" ")
    if len(_content) > 20 or len(_content) == 0:
        return False
    elif len(_content) == 1 and len(_content[0]) == 1:
        return False
    return True

def filter_index():
    for i in filtered_sentences_from_index:
        if i in filtered_sentences_to_index:
            common_index.append(i)
    new_to = []
    new_from = []
    for j in common_index:
        new_to.append(to_lines[j])
        new_from.append(from_lines[j])
    return new_from, new_to

def create_from_file():
    f = open(filtered_from_file, 'w', encoding='utf-8')
    for seed in from_lines:
        f.write(seed+'\n')
    f.close()

def create_to_file():
    f = open(filtered_to_file, 'w', encoding='utf-8')
    for seed in to_lines:
        f.write(seed+'\n')
    f.close()

if __name__ == "__main__":
    index = 0
    for line in tqdm(open(from_file, encoding="utf-8"), desc="Reading 'from' lines"):
        sentence = line.lower()
        sentence = remove_numbers(sentence)
        link = content_is_link(sentence)
        sentence = remove_inerpunction_and_nonascii_chars(sentence)
        if not link and acceptable_size(sentence):
            from_lines.append(sentence)
            filtered_sentences_from_index.append(index)
        else:
            from_lines.append(0)
        index += 1
    print("Finished with 'from' lines\n")

    index = 0
    for line in tqdm(open(to_file, encoding="utf-8"), desc="Reading 'to' lines"):
        sentence = line.lower()
        sentence = remove_numbers(sentence)
        link = content_is_link(sentence)
        sentence = remove_inerpunction_and_nonascii_chars(sentence)
        if link == False and acceptable_size(sentence):
            to_lines.append(sentence)
            filtered_sentences_to_index.append(index)
        else:
            to_lines.append(0)
        index += 1
    print("Finished with 'to' lines\n")

    from_lines, to_lines = filter_index()
    print("\nFrom lines length: ", len(from_lines))
    print("\nTo lines length: ", len(to_lines))
    print("\nWriting to files...")
    create_from_file()
    create_to_file()