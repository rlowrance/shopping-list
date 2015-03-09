def f_score(predictions, actuals):
    '''Return F_1 score

    ARGS
    predictions: list of predictions (True or False)
    actuals    : list of actuals (True or False)

    RETURNS
    f1 : 2 * precision * recall / (precision + recall)
    '''
    # beta converns whether recall is more important than precision
    # beta == 2  ==> recall is more valuable than precision
    # beta == .5 ==> precision is more valuable than recall
    verbose = True
    beta = 1  # equally value precision and recall

    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_negative = 0

    for i in xrange(len(predictions)):
        if predictions[i]:
            if actuals[i]:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if actuals[i]:
                false_negative += 1
            else:
                true_negative += 1

    if verbose:
        print 'actuals', actuals
        print 'predictions', predictions
        print 'true_positive', true_positive
        print 'false_positive', false_positive
        print 'false_negative', false_negative
        print 'true_negative', true_negative

    precision = (1.0 * true_positive) / (true_positive + false_positive)
    recall = (1.0 * true_positive) / (true_positive + false_negative)

    beta2 = beta * beta
    f = (1.0 + beta2) * precision * recall / (beta2 * precision + recall)

    if verbose:
        print 'precision', precision
        print 'recall', recall
        print 'f', f

    return f
