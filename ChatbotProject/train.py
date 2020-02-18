#! /usr/bin/python
# -*- coding: utf-8 -*-
import tensorflow as tf
import tensorlayer as tl
from tensorlayer.cost import cross_entropy_seq_with_mask
from tqdm import tqdm
from sklearn.utils import shuffle
import pickle
from tensorlayer.models import Seq2seq
import keras.backend  as K
import itertools
import check_sentences
import generate_metadata

TokenizerWrap = generate_metadata.TokenizerWrap

VOCABULARY_SIZE=25000
emb_dim=1024

decoder_seq_length = 20
train_model = Seq2seq(
    decoder_seq_length=decoder_seq_length,
    cell_enc=tf.keras.layers.GRUCell,
    cell_dec=tf.keras.layers.GRUCell,
    n_layer=3,
    n_units=256,
    embedding_layer=tl.layers.Embedding(vocabulary_size=VOCABULARY_SIZE+3, embedding_size=emb_dim),
)

def train():
    batch_size, num_epochs, w2idx, idx2word, n_step, end_id, start_id,vocabulary_size,trainX,trainY=start_work()
    optimizer = tf.optimizers.Adam(learning_rate=0.001)  # bio 0.001
    train_model.train()
    for epoch in range(num_epochs):
        train_model.train()
        trainX, trainY = shuffle(trainX, trainY, random_state=0)
        total_loss, n_iter, accuracy = 0, 0, 0
        for X, Y in tqdm(tl.iterate.minibatches(inputs=trainX, targets=trainY, batch_size=batch_size, shuffle=False),
                         total=n_step, desc='Epoch[{}/{}]'.format(epoch + 1, num_epochs), leave=False):
            X = tl.prepro.pad_sequences(X, padding='pre')
            target_sequences = tl.prepro.sequences_add_end_id(Y, end_id=end_id)
            target_sequences = tl.prepro.pad_sequences(target_sequences, maxlen=decoder_seq_length)
            decode_sequences = tl.prepro.sequences_add_start_id(Y, start_id=start_id, remove_last=False)
            decode_sequences = tl.prepro.pad_sequences(decode_sequences, maxlen=decoder_seq_length)
            target_mask = tl.prepro.sequences_get_mask(target_sequences)

            with tf.GradientTape() as tape:
                output = train_model(inputs=[X, decode_sequences])
                output = tf.reshape(output, [-1, vocabulary_size])
                loss = cross_entropy_seq_with_mask(logits=output, target_seqs=target_sequences, input_mask=target_mask)
                grad = tape.gradient(loss, train_model.all_weights)
                optimizer.apply_gradients(zip(grad, train_model.all_weights))
                # accuracy += binary_accuracy(y_true, y_pred)

            total_loss += loss
            n_iter += 1

        print('\nEpoch [{}/{}]: loss {:.4f}'.format(epoch + 1, num_epochs, total_loss / n_iter))
        # validation()
        check_sentences.check()
        tl.files.save_npz(train_model.all_weights, name='data\\model.npz')

# def validation():
#     train_model.eval()
#     batch_size, num_epochs, w2idx, idx2word, n_step, end_id, start_id, vocabulary_size, trainX, trainY = start_work()
#     # Tacni odgovori
#     _validY_target = tl.prepro.sequences_add_end_id(validY, end_id=end_id)
#     _validY_target = tl.prepro.pad_sequences(_validY_target, maxlen=decoder_seq_length)
#     all = []
#     for seed in tqdm(validX, position=0, leave=True, desc='Validation:'):
#         if seed != []:
#             arr=[]
#             sentence_id = train_model(inputs=[[seed]], seq_length=20, start_token=start_id, top_n=1)
#             for el in sentence_id[0]:
#                 if (el != end_id):
#                     arr.append(el.numpy())
#                 if (el == end_id):
#                     arr.append(el.numpy())
#                     break
#             if len(arr) != 20:
#                 arr = arr + [0] * (20 - len(arr))
#             all.append(arr)
#         else:
#             all.append([0]*20)
#     accuracy = binary_accuracy(tf.convert_to_tensor(np.array(_validY_target), dtype=tf.int64),
#                                tf.convert_to_tensor(np.array(all), dtype=tf.int64))
#     print('\nAccuracy: ', accuracy / len(all))


def binary_accuracy(y_true, y_pred):
    '''Calculates the mean accuracy rate across all predictions for binary
    classification problems.
    '''
    return K.mean(K.equal(y_true, K.round(y_pred)))

def initial_setup():
    with open('data\\metadataFirst.pkl', 'rb') as f:
        metadata = pickle.load(f)
    trainX = metadata['tokens_src']
    trainY = metadata['tokens_dest']
    tokenizer = metadata['tokenizer']
    return tokenizer, trainX, trainY

def start_work():
    start_id = VOCABULARY_SIZE + 1
    end_id = VOCABULARY_SIZE + 2
    tokenizer, trainX, trainY = initial_setup()
    tokenizer.word_index = dict(itertools.islice(tokenizer.word_index.items(), VOCABULARY_SIZE))
    tokenizer.index_to_word = dict(itertools.islice(tokenizer.index_to_word.items(), VOCABULARY_SIZE))
    tokenizer.word_index.update({'start_id': start_id})
    tokenizer.word_index.update({'end_id': end_id})
    d1 = dict({'_': 0})
    d1.update(tokenizer.word_index)
    tokenizer.word_index = d1

    d2 = dict({0: '_'})
    d2.update(tokenizer.index_to_word)
    tokenizer.index_to_word = d2

    tokenizer.index_to_word.update({start_id: 'start_id'})
    tokenizer.index_to_word.update({end_id: 'end_id'})

    src_len = len(trainX)
    tgt_len = len(trainY)

    assert src_len == tgt_len
    batch_size = 32
    n_step = src_len // batch_size
    src_vocab_size = len(tokenizer.word_index.keys())

    num_epochs = 20
    vocabulary_size = src_vocab_size

    w2idx = tokenizer.word_index
    idx2word = list(tokenizer.index_to_word.values())
    return batch_size,num_epochs,w2idx,idx2word,n_step,end_id,start_id,vocabulary_size,trainX,trainY

def answer(input_sentence, top_answers):
    batch_size, num_epochs, w2idx, idx2word, n_step, end_id, start_id, vocabulary_size,trainX,trainY=start_work()
    train_model.eval()
    input_sentence = input_sentence.lower()
    puncList = [".", ";", ":", "!", "?", "/", "\\", ",", "#", "@", "$", "&", ")", "(", "\""]
    for punc in puncList:
        input_sentence = ' '.join(input_sentence.split(punc))
    new_input_sentence = input_sentence
    for el in input_sentence.split():
        if el not in w2idx.keys():
            new_input_sentence = ''.join(new_input_sentence.split(el))
    input_sentence = new_input_sentence
    input_sentence = ' '.join(input_sentence.split())
    if input_sentence != "":
        input_sentence_id = [w2idx.get(w) for w in input_sentence.split()]
        sentence_id = train_model(inputs=[[input_sentence_id]], seq_length=20, start_token=start_id,
                                  top_n=top_answers)
        sentence = []
        for w_id in sentence_id[0]:
            w = idx2word[w_id]
            if w == 'end_id':
                break
            sentence = sentence + [w]
        return sentence
    return ""


def read_model():
    initial_setup()
    load_weights = tl.files.load_npz(name='data\\model.npz')
    tl.files.assign_weights(load_weights, train_model)


if __name__ == "__main__":
    read_model()
    train()










