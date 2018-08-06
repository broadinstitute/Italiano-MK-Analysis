#!/bin/bash
#SBATCH -c 12                               
#SBATCH -N 1                               
#SBATCH -t 7-00:00                         
#SBATCH -p long                          
#SBATCH --mem=3G                          

cd /n/data2/bwh/medicine/italiano/Inucycte_Analysis/
conda activate bioimg
python 180731_MS.py
