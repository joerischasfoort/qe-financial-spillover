#PBS -q UCTlong
#PBS -l nodes=1:ppn=5:series600
#PBS -N Market_size

module load python/anaconda-python-2.7

source activate

export PYTHONPATH=/home/kzltin001/ENV/lib/python2.7/site-packages:


python /home/kzltin001/qe-financial-spillover/Experiments/Market_size/market_size_exp.py 

