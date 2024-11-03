import fasttext

word_model = fasttext.train_unsupervised(
    input='file.txt',
    model='skipgram',
    dim=200,
    epoch=20,
    minCount=10,
    minn=1,
    maxn=5,
    neg=5
)
word_model.save('keyboard.bin')
