#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --time=2-00:00:00
#SBATCH --partition=standard
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=9000
#SBATCH --account=csblrivanna
#SBATCH --output=%x-%j.out

module purge
module load anaconda/5.2.0-py3.6
source activate annotation_env # this has the newer cobrapy
python3 model_refinement/add_annot_iPfal19.py 
