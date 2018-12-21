#!/bin/bash
# path = "/home/mac9jc/paradigm"

cd /home/mac9jc/paradigm
# SAVE ANNOTATIONS IN TABLE FORMAT
python3 ./data_acquistion/step_1_genome_annotation.py
echo "processed annotations"

# FINISH CURATION OF iPfal17
python3 ./model_refinement/step_2_curate_iPfal17.py
echo "finished iPfal17 curation"

