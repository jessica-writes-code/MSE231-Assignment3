import sys

if __name__=='__main__':
    f = open(sys.argv[1], 'r')
    countLines = 0
    for line in f:
        countLines += 1
    f.close()
    f = open(sys.argv[1], 'r')
    fTrain = open('train_tweets.tsv', 'w')
    fTest = open('test_tweets.tsv', 'w')
    count = 0
    for line in f:
        if count < countLines/5:
            fTest.write(line)
        else:
            fTrain.write(line)
        count += 1
    fTest.close()
    fTrain.close()
