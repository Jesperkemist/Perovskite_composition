"""
lists of values to be used in drop down menus in the graphical interface

Written by:
T. Jesper Jacobsson 2024 06
"""
import pandas as pd

try:
    import filepaths
except:
    from Utilities import filepaths
    
def collect_all_default_values():
    """Collects all default values defined here. 
    Read in the origin for the ions data from the configuration settings defined in the file filepath.py  """ 
    default_values = {
        "a_ions_options": get_a_ions(origin=filepaths.config["origin"]),
        "b_ions_options": get_b_ions(origin=filepaths.config["origin"]),
        "x_ions_options": get_x_ions(origin=filepaths.config["origin"]),
        "composition_estimates_options": composition_estimates(),
        "dimensionality_options": dimensionality(),
        "sample_type_options": sample_type(),
        }     
    return default_values

def composition_estimates():
    alternatives = [
        "Estimated from precursor solutions", 
        "Literature value", 
        "Estimated from XRD data", 
        "Estimated from spectroscopic data", 
        "Theoretical simulation", 
        "Hypothetical compound", 
        "Other",
        ]
    return alternatives

def dimensionality():
    alternatives = [
        "0D", 
        "1D", 
        "2D", 
        "3D", 
        "2D/3D", 
        "Unknown",
        ]
    return alternatives

def sample_type():
    alternatives = [
        "Polycrystalline film", 
        "Single crystal", 
        "Quantum dots", 
        "Nano rods", 
        "Colloidal solution",
        "Other",
    ]
    return alternatives

def additive_type():
    alternatives = [
        "Additive", 
        "Impurity", 
        "Dopant", 
        "Secondary phase", 
        "Other",
    ]
    return alternatives

def additive_concentration_metrics():
    alternatives = [
        "mol %", 
        "wt %", 
        "vol %", 
        "mol/dm^3", 
        "Other",
    ]
    return alternatives


def getIonAbbreviationsFromDatabase(file_path):
    """Get the abbreviations for all ions we have data on"""
    ion_data = pd.read_excel(file_path)
    ions = ion_data["Abbreviation"].values
    ions = ions.astype(str)
    ions.sort()
    return list(ions) 

def get_a_ions():
    # Read in file paths to reference data  
    path_a_ions, path_b_ions, path_x_ions, path_additives = filepaths.paths_to_data(origin=filepaths.config["origin"])
    a_ions_from_database = ["Cs", "FA", "MA"] + getIonAbbreviationsFromDatabase(path_a_ions)
    return a_ions_from_database

def get_b_ions():
    # Read in file paths to reference data  
    path_a_ions, path_b_ions, path_x_ions, path_additives = filepaths.paths_to_data(origin=filepaths.config["origin"])
    b_ions_from_database = ["Pb", "Sn"] + getIonAbbreviationsFromDatabase(path_b_ions)
    return b_ions_from_database

def get_x_ions():
    # Read in file paths to reference data  
    path_a_ions, path_b_ions, path_x_ions, path_additives = filepaths.paths_to_data(origin=filepaths.config["origin"])
    x_ions_from_database = ["Br", "I"] + getIonAbbreviationsFromDatabase(path_x_ions)
    return x_ions_from_database

def get_additives():
    # Read in file paths to reference data  
    path_a_ions, path_b_ions, path_x_ions, path_additives = filepaths.paths_to_data(origin=filepaths.config["origin"])
    additives_from_database = getIonAbbreviationsFromDatabase(path_additives)
    return additives_from_database
    