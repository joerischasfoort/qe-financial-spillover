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
#SBATCH --nodes=1 --ntasks=2

# The line below indicates the wall time your job will need, 10 hours for example. NB, this is a mandatory directive!
#SBATCH --time=10:00:00

# A sensible name for your job, try to keep it short
#SBATCH --job-name="MAT_exp"

#Modify the lines below for email alerts. Valid type values are NONE, BEGIN, END, FAIL, REQUEUE, ALL 
#SBATCH --mail-user=jesper.riedler@uct.ac.za
#SBATCH --mail-type=BEGIN,END,FAIL

# NB, for more information read https://computing.llnl.gov/linux/slurm/sbatch.html

# Use module to gain easy access to software, typing module avail lists all packages.
# Example:
# module load python/anaconda-python-2.7


#SBATCH --array=0-10


module load python/anaconda-python-2.7


export PYTHONPATH=/home/jriedler/ENV/lib/python2.7/site-packages:


python /home/jriedler/qe-financial-spillover/Experiments/Maturity/MAT_exp.py 

