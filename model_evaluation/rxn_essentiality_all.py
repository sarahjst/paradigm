import cobra
import os
import pandas as pd
import numpy as np
import glob
from cobra.core import Gene, Metabolite, Reaction
from datetime import datetime

day = datetime.now().strftime('%d_%m_%Y')

## ##### get essential reactions
model_dict = dict()
path = "/home/mac9jc/paradigm/models/"
os.chdir(path)
for filename in glob.glob(os.path.join(path, 'gf_P*.xml')):
    key = filename.split('/')[len(filename.split('/'))-1]
    key = key[:-5]
    key = key[4:]
    #    print(key)
    if key is not 'PconfusumCUL13' and key is not 'PneurophiliaMK1':
        i = i+1
        model_dict[key] = cobra.io.read_sbml_model(filename)

for filename in glob.glob(os.path.join(path, 'gf_no_ortho_*.xml')):
    key = filename.split('/')[len(filename.split('/'))-1]
    key = key[:-5]
    key = key[12:]
    #    print(key)
    if key.startswith('P'):
        if key is 'PconfusumCUL13' or key is 'PneurophiliaMK1':
            i = i+1
            model_dict[key] = cobra.io.read_sbml_model(filename)
    else:
        i = i+1
        model_dict[key] = cobra.io.read_sbml_model(filename)
    
print(i)
    
essentiality_screen_models = model_dict.copy()
essentiality_screen_results_raw= dict()
essentiality_screen_results_interpreted = dict()

for species, model in essentiality_screen_models.items():
    raw_results = dict()
    interpreted_results = dict()
    
    print(species+', rxn essenitality screen')
    
    use_second_biomass = False
    if species.startswith('P') and key is not 'PconfusumCUL13' and key is not 'PneurophiliaMK1':
        model.objective = 'generic_biomass'
        model.reactions.get_by_id('generic_biomass').upper_bound = 1000.
        model.reactions.get_by_id('generic_biomass').lower_bound = 0.
    else:
        model.objective = "generic_biomass"
        model.reactions.get_by_id('generic_biomass').upper_bound = 1000.
        model.reactions.get_by_id('generic_biomass').lower_bound = 0.
        # don't accidentally use other biomass reaction
        model.reactions.get_by_id('biomass').upper_bound = 0.
       	model.reactions.get_by_id('biomass').lower_bound = 0.

    print('set biomass')

    max_biomass = model.slim_optimize()
    if max_biomass < 0.01:
        print('model doesnt grow')
        print(species)

    # knockout and record growth
    for rxn in model.reactions:
        if rxn.id == 'generic_biomass' or rxn.id == 'biomass':
            continue
        with model as cobra_model:
            cobra_model.reactions.get_by_id(rxn.id).knock_out()
            f = cobra_model.slim_optimize()
            if max_biomass < 0.01:
                print(species)
            else:
                if f < 0.1*max_biomass:
                    interpreted_results[rxn.id] = 'lethal'
                else:
                    interpreted_results[rxn.id] = 'nonlethal'
                raw_results[rxn.id] = f/max_biomass

    # save
        
    essentiality_screen_results_raw[species] = raw_results
    essentiality_screen_results_interpreted[species] = interpreted_results
     
    #pd.DataFrame.from_dict(essentiality_screen_results_raw[species], orient='index').to_csv("/home/mac9jc/paradigm/data/results/rxn_essentiality/rxn_essentiality_matrix_{}_{}.csv".format(species,day))
    #pd.DataFrame.from_dict(essentiality_screen_results_interpreted[species], orient='index').to_csv("/home/mac9jc/paradigm/data/results/rxn_essentiality/rxn_essentiality_matrix_interpreted_{}_{}.csv".format(species,day))
        

list_o_reactions2 = list()
for species, model in essentiality_screen_models.items():
    list_o_reactions2.append([x.id for x in model.reactions])
list_o_reactions2 = [val for sublist in list_o_reactions2 for val in sublist]
list_o_reactions2 = list(set(list_o_reactions2))

matrix_of_essentiality = pd.DataFrame(index = list_o_reactions2,columns=essentiality_screen_results_raw.keys())
matrix_interpreted = pd.DataFrame(index = list_o_reactions2,columns=essentiality_screen_results_interpreted.keys())
for species_long, rxn_list in essentiality_screen_results_raw.items():
    print(species_long)
    if '_generic' in species_long:
        species = species_long.split('_generic')[0]
    else:
        species = species_long
    for rxn in list_o_reactions2:
        if rxn in essentiality_screen_results_raw[species_long].keys():
            matrix_of_essentiality.loc[rxn,species_long] = essentiality_screen_results_raw[species_long][rxn]
            matrix_interpreted.loc[rxn,species_long] = essentiality_screen_results_interpreted[species_long][rxn]
        else:
            matrix_of_essentiality.loc[rxn,species_long] = 'NA'
            matrix_interpreted.loc[rxn,species_long] = 'NA'

matrix_of_essentiality.to_csv("/home/mac9jc/paradigm/data/results/rxn_essentiality/all_rxn_essentiality_matrix_{}.csv".format(day))
matrix_interpreted.to_csv("/home/mac9jc/paradigm/data/results/rxn_essentiality/all_rxn_essentiality_matrix_interpreted_{}.csv".format(day))


