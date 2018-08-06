#PBS -q UCTlong
#PBS -l nodes=1:ppn=5:series600
#PBS -N RA_exp

module load python/anaconda-python-2.7

source activate

export PYTHONPATH=/home/jriedler/ENV/lib/python2.7/site-packages:


python /home/jriedler/qe-financial-spillover/Experiments/Risk_Aversion/RA_exp.py 

