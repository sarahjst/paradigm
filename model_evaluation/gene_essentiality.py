import cobra
import os
import pandas as pd
import numpy as np
import glob
from cobra.core import Gene, Metabolite, Reaction

## ##### get essential
os.chdir("/home/mac9jc/paradigm/models")
essentiality_screen_models = dict()
essentiality_screen_models['TgondiiGT1'] = cobra.io.load_json_model('gf_TgondiiGT1.json')
essentiality_screen_models['TgondiiME49'] = cobra.io.load_json_model('gf_TgondiiME49.json')
essentiality_screen_models['Pfalciparum3D7'] = cobra.io.load_json_model('gf_Pfalciparum3D7.json')
essentiality_screen_models['PbergheiANKA'] = cobra.io.load_json_model('gf_PbergheiANKA.json')
essentiality_screen_models['PcynomolgiB'] = cobra.io.load_json_model('gf_PcynomolgiB.json')
essentiality_screen_models['PvivaxSal1'] = cobra.io.load_json_model('gf_PvivaxSal1.json')
essentiality_screen_models['ChominisTU502_2012'] = cobra.io.load_json_model('gf_ChominisTU502_2012.json')
essentiality_screen_models['CparvumIowaII'] = cobra.io.load_json_model('gf_CparvumIowaII.json')
essentiality_screen_models['PknowlesiH'] = cobra.io.load_json_model('gf_PknowlesiH.json')
essentiality_screen_models['PcynomolgiB'] = cobra.io.load_json_model('gf_PcynomolgiB.json')

essentiality_screen_models['Pfalciparum3D7_without_ortho'] = cobra.io.load_json_model('no_ortho_gf_without_ortho_Pfalciparum3D7.json')
essentiality_screen_models['PbergheiANKA_without_ortho'] = cobra.io.load_json_model('no_ortho_gf_without_ortho_PbergheiANKA.json')
essentiality_screen_models['PcynomolgiB_without_ortho'] = cobra.io.load_json_model('no_ortho_gf_without_ortho_PcynomolgiB.json')
essentiality_screen_models['PvivaxSal1_without_ortho'] = cobra.io.load_json_model('no_ortho_gf_without_ortho_PvivaxSal1.json')
essentiality_screen_models['PknowlesiH_without_ortho'] = cobra.io.load_json_model('no_ortho_gf_without_ortho_PknowlesiH.json')
essentiality_screen_models['PcynomolgiB_without_ortho'] = cobra.io.load_json_model('no_ortho_gf_without_ortho_PcynomolgiB.json')

os.chdir("/home/mac9jc/paradigm/data/published_models")
model_dict['pfal2018'] = cobra.io.read_sbml_model('pfal2018_abdel_haleem.xml')
model_dict['pviv2018'] = cobra.io.read_sbml_model('pviv2018_abdel_haleem.xml')
model_dict['pber2018'] = cobra.io.read_sbml_model('pber2018_abdel_haleem.xml')
model_dict['pkno2018'] = cobra.io.read_sbml_model('pkno2018_abdel_haleem.xml')
model_dict['pcyn2018'] = cobra.io.read_sbml_model('pcyn2018_abdel_haleem.xml')
model_dict['ipfa2017'] = cobra.io.read_sbml_model('ipfa2017_chiappino_pepe.xml')
model_dict['tg2015'] = cobra.io.read_sbml_model('tg2015_tymoshenko.xml')

os.chdir("/home/mac9jc/paradigm/models")
model_dict['iPfal18'] = cobra.io.load_json_model('iPfal18.json')

gene_essentiality_screen_results_raw= dict()
gene_essentiality_screen_results_interpreted = dict()

for species, model in essentiality_screen_models.items():
    raw_results = dict()
    interpreted_results = dict()

    print(species+', gene essenitality screen')
    
    if species == 'tg2015':
        model.objective = "Biomass"
    elif species == 'ipfa2017':
        model.objective == 'Biomass_rxn_c'
    elif species in ['pfal2018','pviv2018','pber2018','pkno2018','pcyn2018']:
        model.objective = "biomass"
    else:
        model.objective = "generic_biomass"
        use_second_biomass = True

    # don't accidentally use other biomass reaction
    if 'biomass' in [rxn.id for rxn in model.reactions]:
        model.reactions.get_by_id('generic_biomass').upper_bound = 1000.
        model.reactions.get_by_id('generic_biomass').lower_bound = 0.
        model.reactions.get_by_id('biomass').upper_bound = 0.
        model.reactions.get_by_id('biomass').lower_bound = 0.

    max_biomass = model.slim_optimize()

    # knockout and record growth
    for gene in model.genes:
        with model as cobra_model:
            cobra.manipulation.delete_model_genes(cobra_model, [gene.id], cumulative_deletions=True)
            f = cobra_model.slim_optimize()
            if f < 0.1*max_biomass:
                interpreted_results[gene.id] = 'lethal'
            else:
                interpreted_results[gene.id] = 'nonlethal'
            raw_results[gene.id] = f/max_biomass
            cobra.manipulation.undelete_model_genes(cobra_model)

    # save
    if not use_second_biomass:

        gene_essentiality_screen_results_raw[species] = raw_results
        gene_essentiality_screen_results_interpreted[species] = interpreted_results
        cols = ['gene_id', 'normalized_growth']
        pd.DataFrame.from_dict(gene_essentiality_screen_results_raw[species], orient='index').to_csv("/home/mac9jc/paradigm/data/gene_essentiality_matrix_{}.csv".format(species))
        pd.DataFrame.from_dict(gene_essentiality_screen_results_interpreted[species], orient='index').to_csv("/home/mac9jc/paradigm/data/gene_essentiality_matrix_interpreted_{}.csv".format(species))

    else:
        gene_essentiality_screen_results_raw[species+'_generic_biomass'] = raw_results
        gene_essentiality_screen_results_interpreted[species+'_generic_biomass'] = interpreted_results
        cols = ['gene_id', 'normalized_growth']
        pd.DataFrame.from_dict(gene_essentiality_screen_results_raw[species+'_generic_biomass'], orient='index').to_csv("/home/mac9jc/paradigm/data/gene_essentiality_matrix_{}.csv".format(species+'_generic_biomass'))
        pd.DataFrame.from_dict(gene_essentiality_screen_results_interpreted[species+'_generic_biomass'], orient='index').to_csv("/home/mac9jc/paradigm/data/gene_essentiality_matrix_interpreted_{}.csv".format(species+'_generic_biomass'))

        print(species+', gene essenitality screen')
        # set objective
        model.objective = "biomass"

        # don't accidentally use other biomass reaction
        model.reactions.get_by_id('biomass').upper_bound = 1000.
        model.reactions.get_by_id('biomass').lower_bound = 0.
        model.reactions.get_by_id('generic_biomass').upper_bound = 0.
        model.reactions.get_by_id('generic_biomass').lower_bound = 0.

        max_biomass = model.slim_optimize()

        # knockout and record growth
        for gene in model.genes:
            with model as cobra_model:
                cobra.manipulation.delete_model_genes(cobra_model, [gene.id], cumulative_deletions=True)
                f = cobra_model.slim_optimize()
                if f < 0.1*max_biomass:
                    interpreted_results[gene.id] = 'lethal'
                else:
                    interpreted_results[gene.id] = 'nonlethal'
                raw_results[gene.id] = f/max_biomass
                cobra.manipulation.undelete_model_genes(cobra_model)

        # save
        gene_essentiality_screen_results_raw[species+'_species_biomass'] = raw_results
        gene_essentiality_screen_results_interpreted[species+'_species_biomass'] = interpreted_results

        cols = ['gene_id', 'normalized_growth']
        pd.DataFrame.from_dict(gene_essentiality_screen_results_raw[species+'_species_biomass'], orient='index').to_csv("/home/mac9jc/paradigm/data/gene_essentiality_matrix_{}.csv".format(species+'_species_biomass'))
        pd.DataFrame.from_dict(gene_essentiality_screen_results_interpreted[species+'_species_biomass'], orient='index').to_csv("/home/mac9jc/paradigm/data/gene_essentiality_matrix_interpreted_{}.csv".format(species+'_species_biomass'))


