#PBS -q UCTlong
#PBS -l nodes=1:ppn=24:series600
#PBS -N qe_parallel

module load python/anaconda-python-2.7

source activate

export PYTHONPATH=/home/kzltin001/qe/lib/python2.7/site-packages:/


python /home/kzltin001/qe/elasticity_experiment.py 

