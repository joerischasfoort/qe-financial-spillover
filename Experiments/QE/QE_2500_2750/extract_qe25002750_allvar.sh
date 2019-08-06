#!/bin/sh

######################################################################################################
#                                                                                                    #
# This example submission script contains several important directives, please examine it thoroughly #
#                                                                                                    #
######################################################################################################

# The line below indicates which accounting group to log your job against
#SBATCH --account=aifmrm

# The line below selects the group of nodes you require
#SBATCH --partition=ada

# The line below means you need 1 worker node and a total of 2 cores
#SBATCH --nodes=1 --ntasks=30

# The line below indicates the wall time your job will need, 10 hours for example. NB, this is a mandatory directive!
#SBATCH --time=72:00:00

# A sensible name for your job, try to keep it short
#SBATCH --job-name="Tina_extract_25002750"
#Modify the lines below for email alerts. Valid type values are NONE, BEGIN, END, FAIL, REQUEUE, ALL 
#SBATCH --mail-user=kzltin001@myuct.ac.za
#SBATCH --mail-type=BEGIN,END,FAIL

 
 
 
###########################
 

module load python/anaconda-python-2.7


export PYTHONPATH=/scratch/kzltin001/ENV/lib/python2.7/site-packages:

export OMP_NUM_THREADS=2 # this is important to prevent numpy from grabbing more cores than assigned

python /scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_2500_2750/extract_all_mean.py


 
 

