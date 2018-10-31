#PBS -q UCTlong
#PBS -l nodes=1:ppn=8:series600
#PBS -N QE_WASRA_exp

module load python/anaconda-python-2.7

source activate

export PYTHONPATH=/home/jriedler/ENV/lib/python2.7/site-packages:


python /home/jriedler/qe-financial-spillover/Experiments/QE_wASRA/QE_wASRA_exp.py 

