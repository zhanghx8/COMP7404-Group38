import numpy as np 
from _code_ import kmeans_cost_label, algo1, k_means_cost, detAlg, samplingResult, hard_noisy_oracle, unpickle 
from sklearn.cluster import KMeans
import random
import csv
from sklearn.datasets import load_digits
from sklearn.cluster import kmeans_plusplus as kpp
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.datasets import fashion_mnist

import time


import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--seed", type = int, help = "Seed", default = 2022)
parser.add_argument('--overwrite', action='store_true', help = "Whether to overwrite the output file")
parser.add_argument("--err", type = float, help = "True error rate", default = 0.2)
parser.add_argument("--nTrials", type = int, help = "NumTrials", default = 15)
parser.add_argument("--numIter", type = int, help = "Number of iterations for taking average", default = 10)
parser.add_argument("--dataset", type = str, help = "Datasets:phy, cifar10, mnist", default = 'phy')
parser.add_argument("--k", type = int, help = "Number of clusters", default = 10)
parser.add_argument("--nPortion", type = float, help = "Portion of the dataset used for clustering", default = 1)



args = parser.parse_args()

np.random.seed(args.seed)
random.seed(args.seed)
err = args.err
nTrials = args.nTrials
nIters = args.numIter
dataset = args.dataset
k = args.k

resultFileFormatted = dataset + 'KmeansResult.csv'
resultFileFormattedTime = dataset + 'KmeansResultTime.csv'

# load data
print('loading data')
if dataset == 'cifar10':
    data = unpickle("datasets/test")[b'data']
    np.random.shuffle(data)
    nPortion = int(len(data) * args.nPortion)
    test = data[-nPortion:].astype(np.float64)
    print(len(test[0]))
elif dataset == 'phy':
    data = np.loadtxt("datasets/phy.dat")
    nPortion = int(len(data) * args.nPortion)
    np.random.shuffle(data)
    test = data[-nPortion:,:]
elif dataset == 'mnist':
    data = load_digits().data
    nPortion = int(len(data) * args.nPortion)
    test = data[-nPortion:]
elif dataset == '20newsgroups':
    newsgroups_train = fetch_20newsgroups(subset='train')
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    test = vectorizer.fit_transform(newsgroups_train.data).toarray()
    # print("Dataset size:", type(test))
elif dataset == 'fashion':
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    X = train_images.reshape(-1, 28 * 28).astype(float)
    X /= 255.0
    n, d = X.shape  # n=60000, d=784
    nPortion = 10000
    test = X[:nPortion]
    print(len(test[0]))


start = time.time()
kmeans_scikit_10 = KMeans(n_clusters=k, random_state = args.seed).fit(test)
time_OPT = time.time() - start
true_labels_10 = kmeans_scikit_10.labels_

print('Predictor: {} corruption (avg over {} trials)'.format(err,nIters))

pvals_alg1 = np.linspace(.01, 1/5, nTrials)
pvals_det = np.linspace(.01, .5, nTrials)
cost_oracle = []
cost_sampling = []
cost_algo = []
det_cost_algo = []
baseline_10 = []

cost_opt = [kmeans_cost_label(test, true_labels_10,k)[1]]
noisy_orc_labels = hard_noisy_oracle(test, true_labels_10, err)


time_sampling = []
time_alg = []
det_time_alg = []
time_OPT = [time_OPT]

for i in range(nIters):
    baseline_10.append(k_means_cost(test, kpp(test, k, random_state = args.seed)[0])[1])
    cost_oracle.append(kmeans_cost_label(test, noisy_orc_labels, k)[1])
    
    start = time.time()
    SR = samplingResult(test, noisy_orc_labels, k)
    time_sampling.append(time.time() - start)
    cost_sampling.append(SR)
    lowest = float('inf')
    det_lowest = float('inf')
	
    alg1_time_count = 0
    det_time_count = 0
    for p_alg1, p_det in zip(pvals_alg1, pvals_det):
        
        start = time.time()
        cr = algo1(test, noisy_orc_labels.copy(), k, p_alg1)
        alg1_time_count += time.time() - start

        
        start = time.time()
        dr = detAlg(test, noisy_orc_labels.copy(), k, p_det)
        det_time_count += time.time() - start
        
        curr_cost = k_means_cost(test,cr )[1]
        det_curr_cost = k_means_cost(test, dr )[1]
        if det_curr_cost < det_lowest:
            det_lowest = det_curr_cost
        if curr_cost < lowest:
            lowest = curr_cost
    cost_algo.append(lowest)
    det_cost_algo.append(det_lowest)
    time_alg.append(alg1_time_count)
    det_time_alg.append(det_time_count)

    


    
print('k means ++', np.average(baseline_10), 'Noisy predictor:', np.average(cost_oracle), 'Sampling:', np.average(cost_sampling),  'Algo1:', np.average(cost_algo), 'Det:',np.average(det_cost_algo) )


cost_oracle = np.array(cost_oracle) 
cost_sampling = np.array(cost_sampling) 
cost_algo = np.array(cost_algo) 
det_cost_algo = np.array(det_cost_algo)
baseline_10 = np.array(baseline_10)
result = np.array([baseline_10, cost_oracle, cost_sampling, cost_algo, det_cost_algo]).T
mean = np.mean(result, axis = 0)
std = np.std(result, axis = 0)
result = np.expand_dims(np.append(mean, std), 0)
result = np.append(result, [[np.average(cost_opt)]], axis = 1)

header = ["Params", "k++" ,"Predictor", "Sampling" , "Ergun, Jon, et al.", "Ours", "k++EB" , "PredictorEB", "SamplingEB" ,"Ergun, Jon, et al.EB", "OursEB", "OPT"]
if args.overwrite:
    w = 'w'
else:
    w = 'a'
    
params = ["Error {} K {} Num Trials {}".format(args.err, args.k, args.nTrials)]
params_result = list(map(str, result[0].tolist()))
params.extend(params_result)

with open(resultFileFormatted,w) as fd:
    writer = csv.writer(fd, delimiter=',')
    if args.overwrite:
        writer.writerows([header, params])
    else:
        writer.writerows([params])
        

#######################################

result = np.array([cost_sampling, cost_algo, det_cost_algo]).T
mean = [np.mean(x) for x in [time_sampling, time_alg, det_time_alg]]
std = [np.std(x) for x in [time_sampling, time_alg, det_time_alg]]
result = np.expand_dims(np.append(mean, std), 0)
result = np.append(result, [[np.average(time_OPT)]], axis = 1)

header = ["Params",  "Sampling" , "Ergun, Jon, et al.", "Ours", "Sampling++EB" ,"Ergun, Jon, et al.EB", "OursEB", "OPT"]
if args.overwrite:
    w = 'w'
else:
    w = 'a'
    
params = ["Error {} K {} Num Trials {} Dataset Portion {}".format(args.err, args.k, args.nTrials, args.nPortion)]
params_result = list(map(str, result[0].tolist()))
params.extend(params_result)

with open(resultFileFormattedTime,w) as fd:
    writer = csv.writer(fd, delimiter=',')
    if args.overwrite:
        writer.writerows([header, params])
    else:
        writer.writerows([params])
