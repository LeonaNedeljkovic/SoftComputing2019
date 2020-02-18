import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle

MAX_NUM_WORDS = 25000

input_sentences = []
output_sentences = []

class TokenizerWrap(Tokenizer):

    def __init__(self, texts,num_words=None):
        Tokenizer.__init__(self, num_words=num_words)

        self.fit_on_texts(texts)

        self.index_to_word = dict(zip(self.word_index.values(),
                                      self.word_index.keys()))
        self.max_tokens = 20

    def texts_to_nums(self,texts):
        tokens = self.texts_to_sequences(texts)
        return tokens
    def pad_tokens(self,texts,padding):

        tokens_padded = pad_sequences(self.tokens,
                                           maxlen=self.max_tokens,
                                           padding=padding,
                                           truncating='post')
        return tokens_padded

    def token_to_word(self, token):
        word = " " if token == 0 else self.index_to_word[token]
        return word

    def tokens_to_string(self, tokens):
        words = [self.index_to_word[token]
                 for token in tokens
                 if token != 0]
        text = " ".join(words)

        return text

    def text_to_tokens(self, text, reverse=False, padding=False):
        tokens = self.texts_to_sequences([text])
        tokens = np.array(tokens)
        if reverse:
            tokens = np.flip(tokens, axis=1)
            truncating = 'pre'
        else:
            truncating = 'post'
        if padding:
            tokens = pad_sequences(tokens,
                                   maxlen=self.max_tokens,
                                   padding='pre',
                                   truncating=truncating)

        return tokens

def read_lines():
    for line in open('data\\train_from_corrected', encoding="utf-8"):
        input_sentences.append(line)

    for line in open('data\\train_to_corrected', encoding="utf-8"):
        output_sentences.append(line)

    trainX=input_sentences
    trainY=output_sentences

    tokenizer = TokenizerWrap(trainX+trainY,num_words=MAX_NUM_WORDS)

    print(tokenizer.word_index)


    metadata = {
        'tokens_src': tokenizer.texts_to_nums(trainX),
        'tokens_dest': tokenizer.texts_to_nums(trainY),
        'tokenizer':tokenizer,
    }


    with open('data\\metadataFirst.pkl', 'wb') as f:
        pickle.dump(metadata, f)


if __name__=='__main__':
    read_lines()



