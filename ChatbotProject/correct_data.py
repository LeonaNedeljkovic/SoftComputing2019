import nltk
from nltk.corpus import words
from tqdm import tqdm
import re as reg
nltk.download()

detected_irregular_words = ["bo","wo","ho","m","yes","oh","no"]
detected_regular_words = ["looks","totally","subreddit","off","fall","gonna","typically","reddit"]
regular_words = []
pattern = reg.compile(r"(.)\1{1,}", reg.DOTALL)

from_file = "data\\train_from_filtered"
to_file = "data\\train_to_filtered"

corrected_from_file = 'data\\train_from_corrected'
corrected_to_file = 'data\\train_to_corrected'

from_list = []
to_list = []

def initialize_regular_words():
    word_list = words.words()
    double_letters = ["aa","ww","ee","rr","tt","yy","uu","ii","oo","pp","ss","dd","ff","gg","hh","jj","kk","ll","zz","xx","cc","vv","bb","nn","mm"]
    for word in word_list:
        for letter in double_letters:
            if letter in word:
                regular_words.append(word)

def correct_sentence(content):
    new_content = ""
    content = content.split(" ")
    for word in content:
        word = word.strip()
        if word not in regular_words:
            word = pattern.sub(r"\1", word)
            word = word.strip("'")
        if "haha" in word:
            word = "haha"
        if word != "" and word != " ":
            new_content = new_content + " " + word
    return new_content.strip()

def create_from_file():
    f = open(corrected_from_file, 'w', encoding='utf-8')
    for seed in from_list:
        f.write(seed+'\n')
    f.close()

def create_to_file():
    f = open(corrected_to_file, 'w', encoding='utf-8')
    for seed in to_list:
        f.write(seed+'\n')
    f.close()



if __name__ == "__main__":
    initialize_regular_words()
    for line in tqdm(open(from_file, encoding="utf-8"), desc="Reading 'from' lines"):
        sentence = line
        sentence = correct_sentence(sentence)
        from_list.append(sentence)
    print("Finished with 'from' lines\n")

    for line in tqdm(open(to_file, encoding="utf-8"), desc="Reading 'from' lines"):
        sentence = line
        sentence = correct_sentence(sentence)
        to_list.append(sentence)
    print("Finished with 'to' lines\n")

    create_from_file()
    create_to_file()

