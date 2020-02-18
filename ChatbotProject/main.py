import train
import generate_metadata

if __name__ == "__main__":
    TokenizerWrap=generate_metadata.TokenizerWrap
    train.read_model()
    while True:
        query = input(">> ")
        top_answers = 1
        for i in range(top_answers):
            sentence = train.answer(query, top_answers)
            print(" >", ' '.join(sentence))
