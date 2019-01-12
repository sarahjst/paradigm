import cobra
import os
import pandas as pd
import numpy as np
import glob
from cobra.core import Gene, Metabolite, Reaction

#model_dict = dict()
#path = "/home/mac9jc/paradigm/models/"
#os.chdir(path)
#for filename in glob.glob(os.path.join(path, 'final_denovo_*.json')):
#    key = filename.split('/')[len(filename.split('/'))-1]
#    key = key[:-5]
#    key = key[13:]
##    print(key)
#    model_dict[key] = cobra.io.load_json_model(filename)
## for filename in glob.glob(os.path.join(path, 'ortho_*.json')):
#  #  key = filename.split('/')[len(filename.split('/'))-1]
#   # key = key[:-5]
#  #  key = key[6:]
#  #  print(key)
#  #  model_dict[key] = cobra.io.load_json_model(filename)
#
## these metabolites are transported INTO the cell
#imported_mets_dict = dict()
#for species, model in model_dict.items():
#    reactants = list()
#    for rxn in model.reactions:
#        reactants.append([x.id for x in rxn.reactants])
#    reactants = [val for sublist in reactants for val in sublist]
#    transported_mets = list()
#    for x in model.metabolites:
#        if x.id.endswith('_e') and x.id in reactants:
#            transported_mets.append(x.id[:-2])
#    imported_mets_dict[species] = list(set(transported_mets))
#
## all transported mets
#met_list = list()
#for species, imported_mets in imported_mets_dict.items():
#    met_list.append(imported_mets)
#met_list = list(set([val for sublist in met_list for val in sublist]))
#
## get matrix of imported mets
#presence_matrix_of_transporters = pd.DataFrame(index = met_list,columns=model_dict.keys())
#for species, imported_mets in imported_mets_dict.items():
#    for met in met_list:
#        if met in imported_mets:
#            presence_matrix_of_transporters.loc[met,species] = 1
#        else:
#            presence_matrix_of_transporters.loc[met,species] = 0
#presence_matrix_of_transporters.to_csv("/home/mac9jc/paradigm/data/transporter_presence_before_gapfilling_jan.csv")
#
## get matrix of reactions
#reactions_in_model = dict()
#list_o_reactions = list()
#for species, model in model_dict.items():
#    reactions_in_model[species] = [x.id for x in model.reactions]
#    list_o_reactions.append([x.id for x in model.reactions])
#list_o_reactions = [val for sublist in list_o_reactions for val in sublist]
#list_o_reactions = list(set(list_o_reactions))
#presence_matrix_of_reactions = pd.DataFrame(index = list_o_reactions,columns=model_dict.keys())
#for species, rxn_list in reactions_in_model.items():
#    for rxn in rxn_list:
#        if rxn in list_o_reactions:
#            presence_matrix_of_reactions.loc[rxn,species] = 1
#        else:
#            presence_matrix_of_reactions.loc[rxn,species] = 0
#presence_matrix_of_reactions.to_csv("/home/mac9jc/paradigm/data/rxn_presence_before_gapfilling_jan.csv")

# get essential reactions
#os.chdir("/home/mac9jc/paradigm/models")
#essentiality_screen_models = dict()
#essentiality_screen_models['TgondiiRH'] = cobra.io.load_json_model('gf_TgondiiRH.json')
#essentiality_screen_models['TgondiiME49'] = cobra.io.load_json_model('gf_TgondiiME49.json')
#essentiality_screen_models['Pfalciparum3D7'] = cobra.io.load_json_model('gf_Pfalciparum3D7.json')
#essentiality_screen_models['PbergheiANKA'] = cobra.io.load_json_model('gf_PbergheiANKA.json')
#essentiality_screen_models['PvivaxSal1'] = cobra.io.load_json_model('gf_PvivaxSal1.json')
#essentiality_screen_models['ChominisTU502_2012'] = cobra.io.load_json_model('gf_ChominisTU502_2012.json')
#essentiality_screen_models['CparvumIowaII'] = cobra.io.load_json_model('gf_CparvumIowaII.json')
#
#essentiality_screen_results_raw= dict()
#essentiality_screen_results_interpreted = dict()
#
#for species, model in essentiality_screen_models.items():
#    raw_results = dict()
#    interpreted_results = dict()
#
#    # set objective
#    model.objective = "generic_biomass"
#
#    # don't accidentally use other biomass reaction
#    if 'biomass' in [rxn.id for rxn in model.reactions]:
#        model.reactions.get_by_id('generic_biomass').upper_bound = 1000.
#        model.reactions.get_by_id('generic_biomass').lower_bound = 0.
#        model.reactions.get_by_id('biomass').upper_bound = 0.
#        model.reactions.get_by_id('biomass').lower_bound = 0.
#
#    max_biomass = model.slim_optimize()
#
#    # knockout and record growth
#    for rxn in model.reactions:
#        if rxn.id == 'generic_biomass' or rxn.id == 'biomass':
#            continue
#        with model as cobra_model:
#            cobra_model.reactions.get_by_id(rxn.id).knock_out()
#            f = cobra_model.slim_optimize()
#            if f < 0.1*max_biomass:
#                interpreted_results[rxn.id] = 'lethal'
#            else:
#                interpreted_results[rxn.id] = 'nonlethal'
#            raw_results[rxn.id] = f
#
#    # save
#    essentiality_screen_results_raw[species+'_generic_biomass'] = raw_results
#    essentiality_screen_results_interpreted[species+'_generic_biomass'] = interpreted_results
#
#    if species.startswith('P'):
#        # set objective
#        model.objective = "biomass"
#
#        # don't accidentally use other biomass reaction
#        model.reactions.get_by_id('biomass').upper_bound = 1000.
#        model.reactions.get_by_id('biomass').lower_bound = 0.
#        model.reactions.get_by_id('generic_biomass').upper_bound = 0.
#        model.reactions.get_by_id('generic_biomass').lower_bound = 0.
#
#        max_biomass = model.slim_optimize()
#
#        # knockout and record growth
#        for rxn in model.reactions:
#            if rxn.id == 'generic_biomass' or rxn.id == 'biomass':
#                continue
#            with model as cobra_model:
#                cobra_model.reactions.get_by_id(rxn.id).knock_out()
#                f = cobra_model.slim_optimize()
#                if f < 0.1*max_biomass:
#                    interpreted_results[rxn.id] = 'lethal'
#                else:
#                    interpreted_results[rxn.id] = 'nonlethal'
#                raw_results[rxn.id] = f
#
#        # save
#        essentiality_screen_results_raw[species+'_species_biomass'] = raw_results
#        essentiality_screen_results_interpreted[species+'_species_biomass'] = interpreted_results
#
#import json
#
#with open('essentiality_data.json', 'w') as fp:
#    json.dump(essentiality_screen_results_interpreted, fp)
#
#list_o_reactions2 = list()
#for species, model in essentiality_screen_models.items():
#    list_o_reactions2.append([x.id for x in model.reactions])
#list_o_reactions2 = [val for sublist in list_o_reactions2 for val in sublist]
#list_o_reactions2 = list(set(list_o_reactions2))
#
#print(essentiality_screen_results_raw.keys())
#
#matrix_of_essentiality = pd.DataFrame(index = list_o_reactions2,columns=essentiality_screen_results_raw.keys())
#matrix_interpreted = pd.DataFrame(index = list_o_reactions2,columns=essentiality_screen_results_interpreted.keys())
#for species_long, rxn_list in essentiality_screen_results_raw.items():
#    print(species_long)
#    if '_generic' in species_long:
#        species = species_long.split('_generic')[0]
#    elif '_species' in species_long:
#        species = species_long.split('_species')[0]
#    else:
#        print('ERROR, what biomass are we using?')
#    for rxn in list_o_reactions2:
#        if rxn in essentiality_screen_results_raw[species_long].keys():
#            matrix_of_essentiality.loc[rxn,species_long] = essentiality_screen_results_raw[species_long][rxn]
#            matrix_interpreted.loc[rxn,species_long] = essentiality_screen_results_interpreted[species_long][rxn]
#        else:
#            matrix_of_essentiality.loc[rxn,species_long] = 'NA'
#            matrix_interpreted.loc[rxn,species_long] = 'NA'
#matrix_of_essentiality.to_csv("/home/mac9jc/paradigm/data/rxn_essentiality_matrix_jan.csv")
#matrix_interpreted.to_csv("/home/mac9jc/paradigm/data/rxn_essentiality_matrix_interpreted_jan.csv")

def met_ids_without_comp(model,met_id):
    
    # print list of metabolites without the compartment associated
    # this needs to be updated if you have different compartments than those listed below
    if met_id in [met.id for met in model.metabolites]:
        for m in [model.metabolites.get_by_id(met_id)]:
            if m.id.endswith('_c') or m.id.endswith('_e') or m.id.endswith('_f') or \
            m.id.endswith('_g') or m.id.endswith('_h') or m.id.endswith('_i') or \
            m.id.endswith('_l') or m.id.endswith('_m') or m.id.endswith('_n') or \
            m.id.endswith('_p') or m.id.endswith('_r') or m.id.endswith('_s') or \
            m.id.endswith('_u') or m.id.endswith('_v') or m.id.endswith('_x'):
                id_withou_c = m.id[:-2]
            elif m.id.endswith('_cx') or m.id.endswith('_um') or m.id.endswith('_im') \
            or m.id.endswith('_ap') or m.id.endswith('_fv'):
                id_withou_c = m.id[:-3]
            else:
                print('unknown compartment')
                print(m.id)
                id_withou_c = ''
    else:
        id_withou_c = ''
    return(id_withou_c)

def get_comp(model,met_id):
    
    # get compartment associated with a metabolite(s)
    if met_id in [met.id for met in model.metabolites]:
        for m in [model.metabolites.get_by_id(met_id)]:
            if m.id.endswith('_c') or m.id.endswith('_e') or m.id.endswith('_f') or \
            m.id.endswith('_g') or m.id.endswith('_h') or m.id.endswith('_i') or \
            m.id.endswith('_l') or m.id.endswith('_m') or m.id.endswith('_n') or \
            m.id.endswith('_p') or m.id.endswith('_r') or m.id.endswith('_s') or \
            m.id.endswith('_u') or m.id.endswith('_v') or m.id.endswith('_x'):
                id_withou_c = m.id[-2:]
            elif m.id.endswith('_cx') or m.id.endswith('_um') or m.id.endswith('_im') or \
                m.id.endswith('_ap') or m.id.endswith('_fv'):
                    id_withou_c = m.id[-3:]
            else:
                print('unknown compartment')
                print(m.id)
                id_withou_c = ''
    else:
        id_withou_c = ''
    return(id_withou_c)

## get what mets are produced or consumed by each organism
model_dict = dict()
path = "/home/mac9jc/paradigm/models/"
os.chdir(path)
for filename in glob.glob(os.path.join(path, 'gf_*.json')):
    key = filename.split('/')[len(filename.split('/'))-1]
    key = key[:-5]
    key = key[4:]
    print(key)
    model_dict[key] = cobra.io.load_json_model(filename)


# these metabolites are transported INTO the cell
imported_mets_dict = dict()
for species, model in model_dict.items():
    reactants = list()
    for rxn in model.reactions:
        reactants.append([x.id for x in rxn.reactants])
    reactants = [val for sublist in reactants for val in sublist]
    transported_mets = list()
    for x in model.metabolites:
        if x.id.endswith('_e') and x.id in reactants:
            transported_mets.append(x.id[:-2])
    imported_mets_dict[species] = list(set(transported_mets))

# all transported mets
met_list = list()
for species, imported_mets in imported_mets_dict.items():
    met_list.append(imported_mets)
met_list = list(set([val for sublist in met_list for val in sublist]))

# get matrix of imported mets
presence_matrix_of_transporters = pd.DataFrame(index = met_list,columns=model_dict.keys())
for species, imported_mets in imported_mets_dict.items():
    for met in met_list:
        if met in imported_mets:
            presence_matrix_of_transporters.loc[met,species] = 1
        else:
            presence_matrix_of_transporters.loc[met,species] = 0
presence_matrix_of_transporters.to_csv("/home/mac9jc/paradigm/data/transporter_presence_before_gapfilling_jan.csv")


