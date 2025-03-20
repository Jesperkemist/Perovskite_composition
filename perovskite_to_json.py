"""
Functionality for converting perovskite data to a .Json file

Written by:
T. Jesper Jacobsson 2024 10
The background is described in the paper ...
"""

import math
import os
from itertools import zip_longest

import pandas as pd
import numpy as np
import json

from Utilities import filepaths

class PerovskiteToJson:
    def __init__(
        self,
        composition_estimate="",
        sample_type="",
        dimensionality="",
        bandgap="",
        additives = [],
        impurities = [],
        additives_abbreviations = [],
        additives_concentrations = [],
        additives_mass_fractions = [],
        impurities_abbreviations = [],
        impurities_concentrations = [],
        impurities_mass_fractions = [],
        a_ions_abbreviations=[], 
        a_coefficients=[], 
        b_ions_abbreviations=[], 
        b_coefficients=[], 
        x_ions_abbreviations=[], 
        x_coefficients=[],
        path_to_reference_data='local',       
        save_path="",
        save=True):

        # initiate variables
        self.composition_estimate = composition_estimate
        self.sample_type = sample_type
        self.dimensionality = dimensionality
        self.bandgap = bandgap
        self.additives = additives
        self.impurities = impurities
        self.additives_abbreviations = additives_abbreviations
        self.additives_concentrations = additives_concentrations
        self.additives_mass_fractions = additives_mass_fractions
        self.impurities_abbreviations = impurities_abbreviations
        self.impurities_concentrations = impurities_concentrations
        self.impurities_mass_fractions = impurities_mass_fractions            
        self.a_ions_abbreviations = a_ions_abbreviations
        self.a_coefficients = a_coefficients
        self.b_ions_abbreviations = b_ions_abbreviations
        self.b_coefficients = b_coefficients
        self.x_ions_abbreviations = x_ions_abbreviations
        self.x_coefficients = x_coefficients 
        self.path_to_reference_data = path_to_reference_data
        self.save_path = save_path
        self.a_ions = []
        self.b_ions = []
        self.x_ions = []

        # Enforce proper formatting of the ions
        self.a_ions_abbreviations = self.clean_ions(self.a_ions_abbreviations)
        self.b_ions_abbreviations = self.clean_ions(self.b_ions_abbreviations)
        self.x_ions_abbreviations = self.clean_ions(self.x_ions_abbreviations)
        
        # Enforce proper formatting of the coefficients
        self.a_coefficients = self.clean_coefficients(self.a_coefficients)
        self.b_coefficients = self.clean_coefficients(self.b_coefficients)
        self.x_coefficients = self.clean_coefficients(self.x_coefficients)
        
        # Enforce proper formatting additives and impurities
        self.additives_abbreviations = self.clean_ions(self.additives_abbreviations)
        self.additives_concentrations = self.format_list_of_numbers(self.additives_concentrations)
        self.additives_mass_fractions = self.format_list_of_numbers(self.additives_mass_fractions)
        self.impurities_abbreviations = self.clean_ions(self.impurities_abbreviations)
        self.impurities_concentrations = self.format_list_of_numbers(self.impurities_concentrations)
        self.impurities_mass_fractions = self.format_list_of_numbers(self.impurities_mass_fractions)       
    
        self.additives_sort()
        self.impurities_sort()
        
        # Sort ions in alphabetic order
        self.a_ions_abbreviations, self.a_coefficients = self.sort_ions(self.a_ions_abbreviations, self.a_coefficients)
        self.b_ions_abbreviations, self.b_coefficients = self.sort_ions(self.b_ions_abbreviations, self.b_coefficients)
        self.x_ions_abbreviations, self.x_coefficients = self.sort_ions(self.x_ions_abbreviations, self.x_coefficients)
        
        # Get perovskite short composition
        self.short_form = self.get_short_formula()
        
        # Get perovskite long composition
        self.long_form = self.get_long_formula()

        # Read in file paths to reference data  
        path_a_ions, path_b_ions, path_x_ions, path_additives = filepaths.paths_to_data(origin=self.path_to_reference_data)

        # Read in reference data for the ions
        self.reference_data_a_ions = pd.read_excel(path_a_ions)
        self.reference_data_b_ions = pd.read_excel(path_b_ions)
        self.reference_data_x_ions = pd.read_excel(path_x_ions)
        self.reference_data_additive_and_impurities = pd.read_excel(path_additives)

        # Format the dimensionality
        self.dimensionality = self.format_singel_string_values(self.dimensionality)
        
        # Format the composition_estimate
        self.composition_estimate = self.format_singel_string_values(self.composition_estimate)
        
        # Format the sample_type
        self.sample_type = self.format_singel_string_values(self.sample_type)                     
        
        # Format the bandgap
        self.format_bandgap()
        
        # Format the data for the ions and complement with reference data
        # A ions
        self.format_ions_with_complementary_data(self.a_ions, self.a_ions_abbreviations, self.reference_data_a_ions, self.a_coefficients)

        # B ions
        self.format_ions_with_complementary_data(self.b_ions, self.b_ions_abbreviations, self.reference_data_b_ions, self.b_coefficients)

        # X ions
        self.format_ions_with_complementary_data(self.x_ions, self.x_ions_abbreviations, self.reference_data_x_ions, self.x_coefficients)
    
        # Format the additives
        self.format_additives_with_complementary_data(self.additives, 
                                                    self.additives_abbreviations, 
                                                    self.reference_data_additive_and_impurities, 
                                                    self.additives_concentrations,
                                                    self.additives_mass_fractions,                                                     
                                                    )
    
        # Format the impurities
        self.format_additives_with_complementary_data(self.impurities, 
                                                    self.impurities_abbreviations, 
                                                    self.reference_data_additive_and_impurities, 
                                                    self.impurities_concentrations, 
                                                    self.impurities_mass_fractions,
                                                    )
    
        # Convert data to a Json-file
        self.json = self.convert_to_json()
        
        if save == True:
            # Save Json file
            self.save_data(file_path = self.save_path)

    def add_parentheses(self, ions, n=2):
        # Enclose every ion with three letters or more with a parenthesis
        new_list = []
        for i, ion in enumerate(ions):
            if len(ion) > n:
                new_list.append("".join(["(", ion, ")"]))
            else:
                new_list.append(ion)
        return new_list

    def additives_sort(self):
        "Ensure that all additive list have the same length"
        if len(self.additives_concentrations) < len(self.additives_abbreviations):
            self.additives_concentrations.extend(["nan"] * (len(self.additives_abbreviations) - len(self.additives_concentrations)))   
        if len(self.additives_mass_fractions) < len(self.additives_abbreviations):
            self.additives_mass_fractions.extend(["nan"] * (len(self.additives_abbreviations) - len(self.additives_mass_fractions)))   
        
    def impurities_sort(self):
        "Ensure that all additive list have the same length"
        if len(self.impurities_concentrations) < len(self.impurities_abbreviations):
            self.impurities_concentrations.extend(["nan"] * (len(self.impurities_abbreviations) - len(self.impurities_concentrations)))   
        if len(self.impurities_mass_fractions) < len(self.impurities_abbreviations):
            self.impurities_mass_fractions.extend(["nan"] * (len(self.impurities_abbreviations) - len(self.impurities_mass_fractions))) 

    def clean_coefficients(self, coefficients):
        "Ensure proper formatting of the coefficients"
        # Enforce that coefficients are strings
        coefficients = [str(coef) for coef in coefficients]
        
        # Remove trailing blank spaces
        coefficients = [coef.strip() for coef in coefficients]

        for i, coff in enumerate(coefficients):
            # Set missing coefficients to 1 as default
            if coff == "":
                coefficients[i] = "1"
            # Enforce decimal points
            if "," in coff:
                coefficients[i] = coff.replace(",", ".")
        
        return coefficients         

    def clean_ions(self, ions):
        "Ensure proper formatting of the ions"
        # Enforce that ions are strings
        ions = [str(ion) for ion in ions]
        
        # Remove trailing blank spaces
        ions = [ion.strip() for ion in ions]
        
        # Remove any enclosing parenthesizes 
        for i, ion in enumerate(ions):
            if (ion[0] == "(" and ion[-1] == ")"):
                ions[i] = ion[1:-1]   
        
        return ions   

    def convert_to_json(self):
        "Convert to Json"
        
        # Combine data into a dictionary
        perovskite_data = {
            "m_def":"perovskite_solar_cell_database.composition.PerovskiteComposition",     # For NOMAD compatibility
            "long_form": self.long_form,
            "short_form": self.short_form,
            "composition_estimate": self.composition_estimate,
            "sample_type": self.sample_type,
            "dimensionality": self.dimensionality,
            "band_gap": self.bandgap,     
        }
        
        # Remove empty values
        perovskite_data = {key: value for key, value in perovskite_data.items() if value not in ["", "nan", pd.isna(value)]} 
        
        if len(self.a_ions) > 0:
            perovskite_data["ions_a_site"] = self.a_ions
        if len(self.b_ions) > 0:
            perovskite_data["ions_b_site"] = self.b_ions
        if len(self.x_ions) > 0:
            perovskite_data["ions_x_site"] = self.x_ions       
        if len(self.additives) > 0:
            perovskite_data["additives"] = self.additives
        if len(self.impurities) > 0:
            perovskite_data["impurities"] = self.impurities
        
        # Add a top level named data
        data = {
            "data": perovskite_data
        }    
        
        # Convert to json
        return json.dumps(data, indent=4)

    def format_additives_with_complementary_data(self, additives, abbreviations, reference_data, concentration, mass_fraction):
        ""
        for i, element in enumerate(abbreviations):
            additives.append(self.get_additive_complementary_data(
                element, 
                additive_data=reference_data, 
                additive_conc = concentration[i],
                additive_mass_fraction = mass_fraction[i],
                ))  

    def format_list_of_numbers(self, num_list):
        "Ensures that the values are numbers"
        # convert to string, remove trailing blank spaces, and replace comma with points
        
        num_list = [str(x) for x in num_list]
        num_list = [x.replace(",", ".") for x in num_list]
        num_list = [x.strip() for x in num_list]
        
        # Convert back to floating point number
        new_num_list = []
        for x in num_list:
            try:
                new_num_list.append(float(x))
            except:
                new_num_list.append(np.nan)

        return new_num_list

    def format_bandgap(self):
        "Ensures that the band gap is a number"
        # convert to string, remove trailing blank spaces, and replace comma with points
        temp = str(self.bandgap)
        temp = temp.replace(",", ".")
        temp = temp.strip()
        
        # Convert back to floating point number  
        try:
            self.bandgap = float(temp)
        except:
            # self.bandgap = np.nan
            self.bandgap = ""

    def format_ions_with_complementary_data(self, ions, abbreviations, reference_data, coefficients):
        ""
        for i, ion in enumerate(abbreviations):
            ions.append(self.get_ion_complementary_data(
                ion, 
                ion_data=reference_data, 
                coef=coefficients[i]))            
            
    def format_singel_string_values(self, item):
        "format a single string"
        item = str(item)
        item = item.strip()
        
        return item
        
    def format_list_of_strings(self, itemlist):
        "Format a simple list of strings"
        
        # Enforce that items are strings
        itemlist = [str(item) for item in itemlist]
        
        # Remove trailing blank spaces
        itemlist = [item.strip() for item in itemlist]
        
        return itemlist

    def get_additive_complementary_data(self, abbreviation, additive_data, additive_conc, additive_mass_fraction):
        "Get complementary data about additives and impurities from file"
        data_dict = {}

        # Get data
        data_dict["abbreviation"] = abbreviation
        data_dict["concentration"] = additive_conc
        data_dict["mass_fraction"] = additive_mass_fraction
        data_dict["molecular_formula"] = self.get_data_from_ion_datatables(abbreviation, additive_data, column="Molecular_formula")
        data_dict["smiles"] = self.get_data_from_ion_datatables(abbreviation, additive_data, column="SMILE")
        data_dict["common_name"] = self.get_data_from_ion_datatables(abbreviation, additive_data, column="Common_name")
        data_dict["iupac_name"] = self.get_data_from_ion_datatables(abbreviation, additive_data, column="IUPAC_name")
        data_dict["cas_number"] = self.get_data_from_ion_datatables(abbreviation, additive_data, column="CAS")       
        data_dict["source_compound_smiles"] = self.get_data_from_ion_datatables(abbreviation, additive_data, column="Parent_SMILE")
        data_dict["source_compound_iupac_name"] = self.get_data_from_ion_datatables(abbreviation, additive_data, column="Parent_IUPAC")
        data_dict["source_compound_cas_number"] = self.get_data_from_ion_datatables(abbreviation, additive_data, column="Parent_CAS")
    
        if not isinstance(data_dict["concentration"], str):
            if math.isnan(data_dict["concentration"]):
                data_dict["concentration"] = "nan"

        if not isinstance(data_dict["mass_fraction"], str):
            if math.isnan(data_dict["mass_fraction"]):
                data_dict["mass_fraction"] = "nan"            
        
        # Remove keys with "nan" values
        data_dict = {key: value for key, value in data_dict.items() if value not in ["", "nan", "NaN", pd.isna(value)]}   
                
        return data_dict

    def get_data_from_ion_datatables(self, ion, ion_data, column):
        "Fetch data for ions using the abbreviation as the key"
        
        data = ion_data.loc[ion_data["Abbreviation"] == ion, column].values
                
        if len(data) == 0: # If not in database
            value = "nan"    
        elif len(data) > 1: # If not unique, chose the first one
            value = str(data[0])                  
        else: # The value provided in the database
            value = str(data[0])   
            
        # Remove any trailing blank spaces
        value = value.strip()
        
        return value
        
    def get_ion_complementary_data(self, ion, ion_data, coef):
        "Get complementary data about ions from file"        
        data_dict = {}
        
        # Get data
        data_dict["abbreviation"] = ion
        data_dict["coefficient"] = coef
        # data_dict["ion_type"] = type
        data_dict["molecular_formula"] = self.get_data_from_ion_datatables(ion, ion_data, column="Molecular_formula")
        data_dict["smiles"] = self.get_data_from_ion_datatables(ion, ion_data, column="SMILE")
        data_dict["common_name"] = self.get_data_from_ion_datatables(ion, ion_data, column="Common_name")
        data_dict["iupac_name"] = self.get_data_from_ion_datatables(ion, ion_data, column="IUPAC_name")
        data_dict["cas_number"] = self.get_data_from_ion_datatables(ion, ion_data, column="CAS")       
        data_dict["source_compound_smiles"] = self.get_data_from_ion_datatables(ion, ion_data, column="Parent_SMILE")
        data_dict["source_compound_iupac_name"] = self.get_data_from_ion_datatables(ion, ion_data, column="Parent_IUPAC")
        data_dict["source_compound_cas_number"] = self.get_data_from_ion_datatables(ion, ion_data, column="Parent_CAS")
        
        # Remove keys with "nan" values
        data_dict = {key: value for key, value in data_dict.items() if value != "nan"}
        
        return data_dict

    def get_long_formula(self):      
        "The compleat perovskite formula"
        
        # The ions
        a_list = self.a_ions_abbreviations
        b_list = self.b_ions_abbreviations
        c_list = self.x_ions_abbreviations
        
        # Enclose every ion with three letters or more with a parenthesis
        a_list = self.add_parentheses(a_list, n=2)
        b_list = self.add_parentheses(b_list, n=2)
        c_list = self.add_parentheses(c_list, n=2)
            
        # The coefficients
        a_coefficients_list = self.a_coefficients
        b_coefficients_list = self.b_coefficients
        x_coefficients_list = self.x_coefficients
        
        # # Convert coefficients to strings
        a_coefficients_list = [str(x) for x in a_coefficients_list]
        b_coefficients_list = [str(x) for x in b_coefficients_list]
        x_coefficients_list = [str(x) for x in x_coefficients_list]
        
        # Replace ones with empty strings
        a_coefficients_list = ['' if x in [' 1', '1', '1 '] else x for x in a_coefficients_list]
        b_coefficients_list = ['' if x in [' 1', '1', '1 '] else x for x in b_coefficients_list]
        x_coefficients_list = ['' if x in [' 1', '1', '1 '] else x for x in x_coefficients_list]

        # Replace nan  with x 
        a_coefficients_list = ['x' if x in ['nan'] else x for x in a_coefficients_list]
        b_coefficients_list = ['x' if x in ['nan'] else x for x in b_coefficients_list]
        x_coefficients_list = ['x' if x in ['nan'] else x for x in x_coefficients_list]
        
        # Zip together the lists
        a_compleat = list(zip_longest(a_list, a_coefficients_list, fillvalue = ''))
        b_compleat = list(zip_longest(b_list, b_coefficients_list, fillvalue = ''))
        c_compleat = list(zip_longest(c_list, x_coefficients_list, fillvalue = ''))
        
        # Flatten the list of tuples generated by the zip function
        a_compleat = [item for sublist in a_compleat for item in sublist]
        b_compleat = [item for sublist in b_compleat for item in sublist]
        c_compleat = [item for sublist in c_compleat for item in sublist]
        
        # Merge the lists
        LongCompList = a_compleat + b_compleat + c_compleat

        # Concatenate the ions
        LongComp = ''.join(LongCompList)

        return LongComp
        
    def get_short_formula(self):
        "The perovskite family"
        # The ions
        a_list = self.a_ions_abbreviations
        b_list = self.b_ions_abbreviations
        c_list = self.x_ions_abbreviations
        
        # Enclose every ion with three letters or more with a parenthesis
        a_list = self.add_parentheses(a_list, n=2)
        b_list = self.add_parentheses(b_list, n=2)
        c_list = self.add_parentheses(c_list, n=2)
        
        # Merge the lists
        shortCompList = a_list + b_list + c_list

        # Concatenate the ions
        shortComp = ''.join(shortCompList)

        return shortComp

    def sort_ions(self, ions, coef):
        "Sort ions in alphabetic order"      
        # Check if coefficients are given for all ions, and if not, add nan in the last positions   
        if len(coef) < len(ions):
            # coef.extend(list(np.ones(len(ions)-len(coef))*np.nan))
            coef.extend(["nan"] * (len(ions) - len(coef)))
        
        # Update the order of the ions
        order = np.argsort(ions) 
        ion_list = [ions[i] for i in order]
        
        # Update the order of the coefficients
        coef_list = [coef[i] for i in order]
        
        return ion_list, coef_list
    
    def save_data(self, file_path):
        "Save data"
        # Check file ending
        if file_path[-4:] == ".txt":
            file_path = file_path[:-4]
        if file_path[-5:] != ".json":
            file_path = file_path + ".json"
        
        # Save the file    
        # with open("test.json", "w") as outfile:
        #     outfile.write(self.json)       
        with open(file_path, "w") as outfile:
            outfile.write(self.json)


            
# Basic check        
if __name__ == "__main__":     
    # Path to where to save data
    path_json_file = os.path.join(os.getcwd(), "composition_standard_perovskite.json") 
    # path_json_file = os.path.join(path_json_files, "test.json")

    # Test data
    composition_estimate = "Estimated from precursor solutions"
    sample_type = "Polycrystalline film"
    dimensionality = "3D"
    bandgap = 1.55


    a_ions_abbreviations = ["Cs", "MA", "FA "]
    a_coefficients = [0.05, 0.79, 0.18]
    b_ions_abbreviations = ["Pb"]
    b_coefficients = [1]
    x_ions_abbreviations = ["Br", "I"]
    x_coefficients = [0.5, 2.5]

    a_ions_abbreviations = ["Cs", "MA", "FA "]
    a_coefficients = [0.05, 0.79, 0.18]
    b_ions_abbreviations = []
    b_coefficients = []
    x_ions_abbreviations = ["Br", "I"]
    x_coefficients = [0.5, 2.5]

    additives_abbreviations = ["PbI2"]
    additives_concentrations = []
    additives_mass_fractions = [0.03]

    impurities_abbreviations = []
    impurities_concentrations = []
    impurities_mass_fractions = []


    # bandgap = 2.38
    # dimensionality = "2D"
    # a_ions_abbreviations = ["PEA"]
    # a_coefficients = [2]
    # b_ions_abbreviations = ["Pb"]
    # b_coefficients = [1]
    # x_ions_abbreviations = ["I"]
    # x_coefficients = ["4"]    
    
    # additives_abbreviations = ["RbI"]
    # additives_concentrations = []
    # additives_mass_fractions = [0.001]

    # impurities_abbreviations = ["Fe+2"]
    # impurities_concentrations = [1e13]
    # impurities_mass_fractions = []

    # Generate the composition object
    perovskite = PerovskiteToJson(
        composition_estimate=composition_estimate,
        sample_type=sample_type,
        dimensionality=dimensionality, 
        bandgap=bandgap,        
        a_ions_abbreviations=a_ions_abbreviations, 
        a_coefficients=a_coefficients, 
        b_ions_abbreviations=b_ions_abbreviations, 
        b_coefficients=b_coefficients, 
        x_ions_abbreviations=x_ions_abbreviations, 
        x_coefficients=x_coefficients,     
        additives_abbreviations = additives_abbreviations,
        additives_concentrations = additives_concentrations,
        additives_mass_fractions = additives_mass_fractions,       
        impurities_abbreviations = impurities_abbreviations,
        impurities_concentrations = impurities_concentrations,
        impurities_mass_fractions = impurities_mass_fractions,                  
        path_to_reference_data='local', 
        save_path=path_json_file)
    
    # Print some test data
    print(f"band gap: {perovskite.bandgap}")
    print(perovskite.a_ions_abbreviations)
    print(perovskite.a_coefficients)
    print(perovskite.short_form)
    print(perovskite.long_form)
    
    # Save data
    perovskite.save_data(path_json_file)