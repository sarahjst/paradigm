import cobra
import os
import pandas as pd
import glob
from cobra.core import Gene, Metabolite, Reaction
from datetime import datetime
import sys
sys.path.append(os.path.abspath("/home/mac9jc/paradigm/"))
import helper_functions as hf

day = datetime.now().strftime('%d_%m_%Y')

##### get what mets are produced or consumed by each organism
model_dict = dict()
path = "/home/mac9jc/paradigm/models/"
os.chdir(path)
for filename in glob.glob(os.path.join(path, 'gf_*.xml')):
    key = filename.split('/')[len(filename.split('/'))-1]
    key = key[:-3]
    key = key[3:]
    model_dict[key] = cobra.io.read_sbml_model(filename)
    model_dict[key].repair()
    model_dict[key], unused_mets = hf.prune_unused_metabolites2(model_dict[key])

mets_consumed_in_model = dict()
mets_produced_in_model = dict()
mets_in_model = dict()
list_o_mets = list()

for species, model in model_dict.items():
    
    reactants = [[met.id for met in rxn.reactants] for rxn in model.reactions]
    products = [[met.id for met in rxn.products] for rxn in model.reactions]
    reactants = [val for sublist in reactants for val in sublist]
    products = [val for sublist in products for val in sublist]

    list_o_mets = list_o_mets.append([met.id for met in model.metabolites])

    # screen reactants for extracellular
    imported_mets = [hf.met_ids_without_comp(model,met.id) for met in model.metabolites if met.id.endswith('_e') and met.id in reactants]
    # screen products for synthesized, not imported
    produced_mets = list()
    for met in model.metabolites:
        if met.id in products and not met.id.endswith('_e'):
            for rxn in met.reactions:
                rxn_reactants_ids = [m.id for m in rxn.reactants]
                if hf.met_ids_without_comp(model,met.id)+'_e' not in rxn_reactants_ids:
                    if met.id not in rxn_reactants_ids:
                        produced_mets.append(hf.met_ids_without_comp(model,met.id))

    mets_consumed_in_model[species] = list(set(imported_mets))
    mets_produced_in_model[species] = list(set(produced_mets))
list_o_mets = list(set([val for sublist in list_o_mets for val in sublist]))

# get matrix of mets
matrix_of_mets = pd.DataFrame(index = list_o_mets,columns=model_dict.keys())
for species, model in model_dict.items():
    for met_id in list_o_mets:
        if met_id in [m.id for m in model.metabolites]:
            
            if hf.met_ids_without_comp(model,met_id) in mets_consumed_in_model[species]:
                if hf.met_ids_without_comp(model,met_id) in mets_produced_in_model[species]:
                    matrix_of_mets.loc[met_id,species] = 'both'
                else:                
                    matrix_of_mets.loc[met_id,species] = 'consumed'
            else:
                if hf.met_ids_without_comp(model,met_id) in mets_produced_in_model[species]:
                    matrix_of_mets.loc[met_id,species] = 'produced'
                else:
                    matrix_of_mets.loc[met_id,species] = 'neither'
                    print({species:met_id})
        else:
            matrix_of_mets.loc[met_id,species] = 'not present in model'
pd.DataFrame.from_dict(mets_consumed_in_model, orient='index').to_csv("/home/mac9jc/paradigm/data/results/mets_consumed_{}.csv".format(day))
matrix_of_mets.to_csv("/home/mac9jc/paradigm/data/results/met_presence_after_gapfilling_{}.csv".format(day))




