#PBS -q UCTlong
#PBS -l nodes=2:ppn=10:series600
#PBS -N hex_spillover_simulation

module load python/anaconda-python-3.4


python /home/kzltin001/qe-financial-spillover/spillover_simulation.py 

