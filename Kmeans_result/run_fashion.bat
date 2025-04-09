@echo off

set iter=10
set k=10

python alpha_experiment_kmeans.py --err 0.1 --numIter %iter% --dataset fashion --k %k% --overwrite
python alpha_experiment_kmeans.py --err 0.2 --numIter %iter% --dataset fashion --k %k%
python alpha_experiment_kmeans.py --err 0.3 --numIter %iter% --dataset fashion --k %k%
python alpha_experiment_kmeans.py --err 0.4 --numIter %iter% --dataset fashion --k %k%
python alpha_experiment_kmeans.py --err 0.5 --numIter %iter% --dataset fashion --k %k%