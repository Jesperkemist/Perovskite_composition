"""
Filepaths to where compiled data of known perovskite ions are found

Written by:
T. Jesper Jacobsson 2024 06
"""
import os

"""
config is a dictionary that could be read in to simplify where to get the data
The key-word origin has two values in the initial release
local: which means that data for ions are fetch from data files supplied with hte original release
online: which means that updated datafiles are fetch online
"""
config = {"origin": "local"}
# config = {"origin": "online"}


def paths_to_data(origin="local"):
    "file paths to resources. Options are: 'local' and 'online'"
    
    # Locally stored files (not updated after release) 
    if origin == "local":
        # path to locally stored data files
        path_data_ion_folder = os.path.join(os.getcwd(), "Data_ions")
        path_a_ions = os.path.join(path_data_ion_folder, "A-ion_data.xlsx")
        path_b_ions = os.path.join(path_data_ion_folder, "B-ion_data.xlsx")
        path_x_ions = os.path.join(path_data_ion_folder, "C-ion_data.xlsx")
        path_additives_and_impurities = os.path.join(path_data_ion_folder, "additives_and_impurities.xlsx")
        
        return path_a_ions, path_b_ions, path_x_ions, path_additives_and_impurities
    
    
    # Updated data stored in a Github repository
    if origin == "online":
        path_a_ions = "https://github.com/FAIRmat-NFDI/nomad-perovskite-solar-cells-database/raw/main/src/perovskite_solar_cell_database/schema_sections/ions/A-ion_data.xlsx"
        path_b_ions = "https://github.com/FAIRmat-NFDI/nomad-perovskite-solar-cells-database/raw/main/src/perovskite_solar_cell_database/schema_sections/ions/B-ion_data.xlsx"
        path_x_ions = "https://github.com/FAIRmat-NFDI/nomad-perovskite-solar-cells-database/raw/main/src/perovskite_solar_cell_database/schema_sections/ions/C-ion_data.xlsx"
    
        return path_a_ions, path_b_ions, path_x_ions
        
    