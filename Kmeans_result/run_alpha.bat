@echo off

set iter=20
set k=10

@REM python alpha_experiment_kmeans.py --err 0.1 --numIter %iter% --dataset 20newsgroups --k %k% --overwrite
@REM python alpha_experiment_kmeans.py --err 0.2 --numIter %iter% --dataset 20newsgroups --k %k%
@REM python alpha_experiment_kmeans.py --err 0.3 --numIter %iter% --dataset 20newsgroups --k %k%
@REM python alpha_experiment_kmeans.py --err 0.4 --numIter %iter% --dataset 20newsgroups --k %k%
@REM python alpha_experiment_kmeans.py --err 0.5 --numIter %iter% --dataset 20newsgroups --k %k%

@REM python alpha_experiment_kmeans.py --err 0.1 --numIter %iter% --dataset mnist --k %k% --overwrite
@REM python alpha_experiment_kmeans.py --err 0.2 --numIter %iter% --dataset mnist --k %k%
@REM python alpha_experiment_kmeans.py --err 0.3 --numIter %iter% --dataset mnist --k %k%
@REM python alpha_experiment_kmeans.py --err 0.4 --numIter %iter% --dataset mnist --k %k%
@REM python alpha_experiment_kmeans.py --err 0.5 --numIter %iter% --dataset mnist --k %k%
@REM
@REM python alpha_experiment_kmeans.py --err 0.1 --numIter %iter% --dataset cifar10 --k %k% --overwrite
@REM python alpha_experiment_kmeans.py --err 0.2 --numIter %iter% --dataset cifar10 --k %k%
@REM python alpha_experiment_kmeans.py --err 0.3 --numIter %iter% --dataset cifar10 --k %k%
@REM python alpha_experiment_kmeans.py --err 0.4 --numIter %iter% --dataset cifar10 --k %k%
@REM python alpha_experiment_kmeans.py --err 0.5 --numIter %iter% --dataset cifar10 --k %k%

python alpha_experiment_kmeans.py --err 0.1 --numIter %iter% --dataset phy --k %k% --overwrite
python alpha_experiment_kmeans.py --err 0.2 --numIter %iter% --dataset phy --k %k%
python alpha_experiment_kmeans.py --err 0.3 --numIter %iter% --dataset phy --k %k%
python alpha_experiment_kmeans.py --err 0.4 --numIter %iter% --dataset phy --k %k%
python alpha_experiment_kmeans.py --err 0.5 --numIter %iter% --dataset phy --k %k%