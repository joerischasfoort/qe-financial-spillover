#PBS -q UCTlong
#PBS -l nodes=2:ppn=10:series600
#PBS -N hex_test_simulation

module load python/anaconda-python-2.7


python /home/kzltin001/qe-financial-spillover/parallel_simulation.py 

