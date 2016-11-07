import argparse

def sign(x):
    return x/abs(x)

# Parse some args
parser = argparse.ArgumentParser(description='Evaluate accuracy')
parser.add_argument('-t','--truth', action="store", default = False)
parser.add_argument('-p','--predictions', action="store", default = False)
args = vars(parser.parse_args())

# Get truth
truth = []
truth_file = open(args['truth'], 'r')
for line in truth_file.readlines():
    line_split = line.split()
    truth.append(int(line_split[0]))

# Get prediction
predictions = []
prediction_file = open(args['predictions'], 'r')
for line in prediction_file.readlines():
    line_split = line.split()
    predictions.append(float(line_split[0]))

# Calculate accuracy
assert(len(truth) == len(predictions)), "What?!?"
correct = 0
total = 0
for i in xrange(len(truth)):
    total = total + 1
    if sign(truth[i]) == sign(predictions[i]):
        correct = correct + 1
print float(correct)/float(total)

# Confusion matrix
tp = 0
tn = 0
fp = 0
fn = 0
for i in xrange(len(truth)):
    true_direction = sign(truth[i])
    predicted_direction = sign(predictions[i])

    if true_direction > 0.0 and predicted_direction > 0.0:
        tp = tp + 1
    if true_direction > 0.0 and predicted_direction < 0.0:
        fn = fn + 1
    if true_direction < 0.0 and predicted_direction > 0.0:
        fp = fp + 1
    if true_direction < 0.0 and predicted_direction < 0.0:
        tn = tn + 1
print [tp, tn, fp, fn]