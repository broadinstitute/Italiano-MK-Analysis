#!/bin/bash
#SBATCH -c 8                               
#SBATCH -N 1                               
#SBATCH -t 7-00:00                         
#SBATCH -p long                          
#SBATCH --mem=4G

cd /n/data2/bwh/medicine/italiano/Inucycte_Analysis/
conda activate bioimg
python HumanMK.py
