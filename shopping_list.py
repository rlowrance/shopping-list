import math
import pdb
import numpy as np
import collections


if False:
    pdb.set_trace()


def decision_rule_template(days_between):
    '''Return function that decides what should be on the shopping list

    ARGS
    days_between: np.array 1d of mean days between purchases

    RETURNS
    on_list: lambda(n)->boolean, for n >= 1
             whether the item is on the shopping list
    '''


def decision_rule_always(days_between):
    '''Always say yes'''
    def on_list(n):
        return True

    return on_list


def decision_rule_never(days_between):
    '''Always say no'''
    def on_list(n):
        return False

    return on_list


def decision_rule_poisson(days_between):
    '''Assume data follow poisson distribution

    Fit a Poisson distribution and use threshold p >= .5 to say yes
    '''
    mean_days_between = np.mean(days_between)
    threshold = 0.5

    def poisson_df(k, lambda_):
        '''Probability of exactly k given parameter lambda_'''
        assert k >= 0
        assert lambda_ > 0
        result = math.pow(lambda_, k) * math.exp(-lambda_) / math.factorial(k)
        return result

    def poisson_cdf(k, lambda_):
        '''Probability of <= k given parameter lambda_'''
        p = 0.0
        for test_k in xrange(1, k + 1):
            p += poisson_df(test_k, lambda_)
        return p

    def on_list(n):
        '''Return whether to run ad on day n'''
        p = poisson_cdf(n, mean_days_between)
        return p >= threshold

    return on_list


def decision_rule_last(days_between):
    '''Assume last days_between is always true going forward'''
    threshold = days_between[-1]

    def on_list(n):
        return n >= threshold

    return on_list


def decision_rule_last_2(days_between):
    '''Assume average of last 2 is always true going forward'''
    if len(days_between) >= 2:
        threshold = (days_between[-1] + days_between[-2]) * 0.5
    else:
        threshold = days_between[-1]

    def on_list(n):
        return n >= threshold

    return on_list


def loss(predictions, actuals, debug=False):
    '''Return fraction incorrect

    ARGS
    predictions: list of predictions (True or False)
    actuals    : list of actuals (True or False)
    '''

    num_incorrect = 0
    for i in xrange(len(predictions)):
        num_incorrect += 0 if predictions[i] == actuals[i] else 1

    if debug:
        pdb.set_trace()
    fraction_incorrect = (1.0 * num_incorrect) / len(predictions)
    return fraction_incorrect


def generate_data(n, mean_value):
    result = np.zeros(n)
    for i in xrange(n):
        draw = np.random.poisson(mean_value)
        result[i] = draw
    return result


def summarize(cv_result):
    summary = {}
    for model_name, losses in cv_result.iteritems():
        total_loss = 0.0
        count = 0.0
        for loss in losses:
            total_loss += loss
            count += 1
        summary[model_name] = total_loss / count
    return summary


def main():
    mean_value = 7
    n = 50
    data = generate_data(n, mean_value)
    min_len = 1
    models = {'always': decision_rule_always,
              'never': decision_rule_never,
              'poisson': decision_rule_poisson,
              'last': decision_rule_last,
              'last_2': decision_rule_last_2}
    cv_result = collections.defaultdict(list)  # default value is an empty list
    for test_index in xrange(min_len, len(data)):
        train = data[:test_index]
        test = data[test_index]
        for model_name, model in models.iteritems():
            fitted = model(train)
            actuals = []
            predictions = []
            # predict each day for one month
            for d in xrange(1, 31):
                actuals.append(test < d)
                predictions.append(fitted(d))
            cv_result[model_name].append(loss(predictions, actuals))

    summary = summarize(cv_result)
    for model_name, summary_loss in summary.iteritems():
        print model_name, summary_loss


if __name__ == '__main__':
    main()
