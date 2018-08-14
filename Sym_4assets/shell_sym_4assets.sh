#PBS -q UCTlong
#PBS -l nodes=1:ppn=10:series600
#PBS -N Sym_4_assets

module load python/anaconda-python-2.7

source activate

export PYTHONPATH=/home/kzltin001/ENV/lib/python2.7/site-packages:


python /home/kzltin001/qe-financial-spillover/Experiments/Sym_4_assets/sym_4_assets_exp.py 

