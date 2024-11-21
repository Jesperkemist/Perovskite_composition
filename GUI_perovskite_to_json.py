"""
A simple GUI for generating a .json file describing a perovskite
Written by T. Jesper Jacobsson 2024 10
The background is described in the paper ...
"""
import os

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

from perovskite_to_json import PerovskiteToJson
from Utilities import default_values
from Utilities.CTkScrollableDropdown import *
from Utilities.filepaths import config

# Initialize the customtkinter theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
new_font = ('TkDefaultFont', 15)

# Read in list of ions there is data for
a_ions_from_database = default_values.get_a_ions()
b_ions_from_database = default_values.get_b_ions()
x_ions_from_database = default_values.get_x_ions()

# Read in additives there is data for
additives_from_database = default_values.get_additives()

class CompoundData(ctk.CTkFrame):
    def __init__(self, master, row, type="", values=[]):
        super().__init__(master)
        self.values = values
        self.type = type

        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.frame.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="ew")        

        self.title = ctk.CTkLabel(self.frame, text=f"{self.type} {row + 1}", fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")        

        self.compound = ctk.CTkEntry(self.frame, width=200, font=new_font, placeholder_text="")
        self.compound.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

class GetAdditivesData(ctk.CTkFrame):
    def __init__(self, master, title="Title", values=[]):
        super().__init__(master) 
        self.title = title
        self.values = values

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")

        # Buttons to add and remove input fields
        # self.add_button = ctk.CTkButton(self, text="Add Input Field", command=self.add_input_field)
        self.add_button = ctk.CTkButton(self, text="+", width=30, command=self.add_input_field)
        self.add_button.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="ew")

        # self.remove_button = ctk.CTkButton(self, text="Remove Input Field", command=self.remove_input_field)
        self.remove_button = ctk.CTkButton(self, text="-", width=30, command=self.remove_input_field)
        self.remove_button.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="ew")
        
        # Frame for adding additives        
        self.entries_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entries_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.entries_frame.grid_columnconfigure(0, weight=1)
        
        # List to keep track of input fields
        self.input_fields = []               

        # Add first row
        self.add_input_field()

    def add_input_field(self):
        row = len(self.input_fields)
        input_field = AdditiveData(self.entries_frame, row, self.values)
        self.input_fields.append(input_field)

    def remove_input_field(self):
        if self.input_fields:
            input_field = self.input_fields.pop()
            input_field.frame.destroy()

    def get(self):
        additives = []
        concentration = []
        mass_fractions = []
        for element in self.input_fields:
            if element.abbreviation.get().strip() != "":
                additives.append(element.abbreviation.get().strip())
                mass_fractions.append(element.mass_fractions.get().strip())
                concentration.append(element.concentration.get().strip())

        for i, conc in enumerate(concentration):
            if "," in conc:
                concentration[i] = conc.replace(",", ".")

        return additives, concentration, mass_fractions
    
    def clear(self):
        for element in self.input_fields:
            element.abbreviation.set("")
            element.concentration.delete(0, tk.END)
            element.mass_fractions.delete(0, tk.END)  
    
class GetFileName(ctk.CTkFrame):
    def __init__(self, master, title, text):
        super().__init__(master) 
        self.title = title
        self.text = text

        self.title = ctk.CTkLabel(self, width=140, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        
        self.entrybox = ctk.CTkEntry(self, width=500, placeholder_text=self.text, font=new_font)
        self.entrybox.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

    def clear(self):
        self.entrybox.delete(0, tk.END)
        
    def get(self):
        return self.entrybox.get().strip() 

class GetIonsData(ctk.CTkFrame):
    def __init__(self, master, title="Title", values=[]):
        super().__init__(master) 
        self.title = title
        self.values = values

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")

        # Buttons to add and remove input fields
        # self.add_button = ctk.CTkButton(self, text="Add Input Field", command=self.add_input_field)
        self.add_button = ctk.CTkButton(self, text="+", width=30, command=self.add_input_field)
        self.add_button.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="ew")

        # self.remove_button = ctk.CTkButton(self, text="Remove Input Field", command=self.remove_input_field)
        self.remove_button = ctk.CTkButton(self, text="-", width=30, command=self.remove_input_field)
        self.remove_button.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="ew")

        # Frame for adding ion data        
        self.entries_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entries_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.entries_frame.grid_columnconfigure(0, weight=1)
        
        # List to keep track of input fields
        self.input_fields = []

        # Add first row
        self.add_input_field()

    def add_input_field(self):
        row = len(self.input_fields)
        input_field = IonData(self.entries_frame, row, self.values)
        self.input_fields.append(input_field)

    def remove_input_field(self):
        if self.input_fields:
            input_field = self.input_fields.pop()
            input_field.frame.destroy()

    def get(self):
        ions = []
        coefficients = []
        for element in self.input_fields:
            if element.abbreviation.get().strip() != "":
                ions.append(element.abbreviation.get().strip())
                coefficients.append(element.coefficient.get().strip())

        for i, coff in enumerate(coefficients):
            # Set missing coefficients (where ions are given) to 1 as default
            if coff == "":
                coefficients[i] = "1"
            if "," in coff:
                coefficients[i] = coff.replace(",", ".")
        
        return ions, coefficients
    
    def clear(self):
        for element in self.input_fields:
            element.abbreviation.set("")
            element.coefficient.delete(0, tk.END) 

class GetListOfCompounds(ctk.CTkFrame):
    def __init__(self, master, title="", text=""):
        super().__init__(master) 
        self.title = title
        self.text = text    

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        # Buttons to add and remove input fields
        # self.add_button = ctk.CTkButton(self, text="Add Input Field", command=self.add_input_field)
        self.add_button = ctk.CTkButton(self, text="+", width=30, command=self.add_input_field)
        self.add_button.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="ew")

        # self.remove_button = ctk.CTkButton(self, text="Remove Input Field", command=self.remove_input_field)
        self.remove_button = ctk.CTkButton(self, width=30, text="-", command=self.remove_input_field)
        self.remove_button.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="ew")

        # Frame for adding compound names        
        self.entries_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entries_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.entries_frame.grid_columnconfigure(0, weight=1)
        
        # List to keep track of input fields
        self.input_fields = []

        # Add first row
        self.add_input_field()

    def add_input_field(self):
        row = len(self.input_fields)
        input_field = CompoundData(self.entries_frame, row, type=self.text)
        self.input_fields.append(input_field)

    def remove_input_field(self):
        if self.input_fields:
            input_field = self.input_fields.pop()
            input_field.frame.destroy()
            
    def get(self):
        compounds = []
        for element in self.input_fields:
            if element.compound.get().strip() != "":
                compounds.append(element.compound.get().strip())                
        compounds.sort()        
        return compounds
        
    def clear(self):
        for element in self.input_fields:
            element.compound.delete(0, tk.END)

class GetNumberAsString(ctk.CTkFrame):
    def __init__(self, master, title, text):
        super().__init__(master) 
        self.title = title
        self.text = text

        self.title = ctk.CTkLabel(self, width=160, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        
        self.entrybox = ctk.CTkEntry(self, width=140, placeholder_text=self.text, font=new_font)
        self.entrybox.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

    def clear(self):
        self.entrybox.delete(0, tk.END)
        
    def get(self):
        x = self.entrybox.get()
        x = x.replace(",", ".")
        x = x.strip()
        return x

class IonData(ctk.CTkFrame):
    def __init__(self, master, row, values):
        super().__init__(master)
        self.values = values
        
        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.frame.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.title = ctk.CTkLabel(self.frame, text=f"Abbreviation. Ion {row + 1}", fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")        

        self.abbreviation = ctk.CTkComboBox(self.frame, font=new_font, variable="")
        self.abbreviation.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        values = [""] + self.values
        CTkScrollableDropdown(self.abbreviation, values=values, justify="left", button_color="transparent", autocomplete=True) 

        self.coefficient = ctk.CTkEntry(self.frame, placeholder_text="Coefficient", font=new_font)
        self.coefficient.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="w")

class AdditiveData(ctk.CTkFrame):
    def __init__(self, master, row, values):
    # def __init__(self, master, row, values, functions, conc_metrics):
        super().__init__(master)
        self.values = values

        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.frame.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="ew")
    
        self.title = ctk.CTkLabel(self.frame, text=f"Abbriviation {row + 1}", fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew") 
        
        self.abbreviation = ctk.CTkComboBox(self.frame, font=new_font, variable="")
        self.abbreviation.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        values = [""] + self.values
        CTkScrollableDropdown(self.abbreviation, values=values, justify="left", button_color="transparent", autocomplete=True) 

        self.mass_fractions = ctk.CTkEntry(self.frame, placeholder_text="Mass fraction", font=new_font)
        self.mass_fractions.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="w")
        
        self.concentration = ctk.CTkEntry(self.frame, placeholder_text=f"Cons. [/cm³]", font=new_font)
        self.concentration.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="w")

class SaveFolder(ctk.CTkFrame):
    def __init__(self, master, button_text, text, command):
        super().__init__(master) 
        self.text = text

        self.button = ctk.CTkButton(self, text=button_text, command=command, font=new_font)
        self.button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.entrybox = ctk.CTkEntry(self, width=500, placeholder_text=self.text, font=new_font)
        self.entrybox.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
    
    def get(self):
        return self.entrybox.get().strip() 
        
    def update_textbox(self, text):
        self.entrybox.delete(0, tk.END)
        self.entrybox.insert(0, text)

class StandardButton(ctk.CTkFrame):
    def __init__(self, master, text, command):
        super().__init__(master) 
        
        self.button = ctk.CTkButton(self, text=text, command=command, font=new_font)
        self.button.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="w")

class StandardCombobox(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master) 
        self.title = title
        self.values = values 

        self.title = ctk.CTkLabel(self, width=160, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        
        self.entrybox = ctk.CTkComboBox(self, width=300, values=self.values, variable="", font=new_font)
        self.entrybox.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w") 

    def clear(self):
        self.entrybox.set("")     
        
    def get(self):
        return self.entrybox.get().strip()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Perovskite description to JSON")
        self.geometry("850x1200")
        
        # Configure the grid layout for the main window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create a frame for the main content and scrollbar
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew")                

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # self.canvas = tk.Canvas(self.main_frame, bg="#212121")
        # self.canvas = tk.Canvas(self.main_frame, bg=self.main_frame.cget("fg_color"))
        self.canvas = tk.Canvas(self.main_frame, bg="#000000")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.content_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")        

        # Bind the mouse wheel to scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        
        #### Input fields #############
        # Generate JSON button
        self.json_button = StandardButton(self.content_frame, text="Generate JSON file", command=self.generate_json)
        self.json_button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw") 

        # Clear user input button
        self.clear_button = StandardButton(self.content_frame, text="Clear user input", command=self.clear_user_input)
        self.clear_button.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsw")        

        # Get file folder
        self.save_folder = SaveFolder(self.content_frame, button_text="Save folder", 
                                            text="Give save folder (or browse by pressing the button)", 
                                            command=self.get_filepath)
        self.save_folder.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")

        # Get file name to save to
        self.file_name = GetFileName(self.content_frame, title="File name", text="Provide file name")
        self.file_name.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")

        # Composition estimate
        self.composition_estimate = StandardCombobox(self.content_frame, title="Composition estimate", values=default_values.composition_estimates())
        self.composition_estimate.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="nsw")   

        # Sample type
        self.sample_type = StandardCombobox(self.content_frame, title="Sample type", values=default_values.sample_type())
        self.sample_type.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="nsw")  

        # Dimensionality
        self.dimensionality = StandardCombobox(self.content_frame, title="Dimensionality", values=default_values.dimensionality())
        self.dimensionality.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="nsw")  

        # Band gap
        self.bandgap = GetNumberAsString(self.content_frame, title="Band gap [eV]", text="")
        self.bandgap.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="nsw")

        # A-ions
        self.A_ions = GetIonsData(self.content_frame, title="A-ions", values=a_ions_from_database)
        self.A_ions.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="nsw")

        # B-ions
        self.B_ions = GetIonsData(self.content_frame, title="B-ions", values=b_ions_from_database)
        self.B_ions.grid(row=9, column=0, padx=10, pady=(10, 0), sticky="nsw")
        
        # X-ions
        self.X_ions = GetIonsData(self.content_frame, title="X-ions", values=x_ions_from_database)
        self.X_ions.grid(row=10, column=0, padx=10, pady=(10, 0), sticky="nsw")        

        # Additives
        self.additives = GetAdditivesData(self.content_frame, title="Additives", 
                                        values=additives_from_database)
        self.additives.grid(row=11, column=0, padx=10, pady=(10, 0), sticky="nsw") 

        # Impurities
        self.impurities = GetAdditivesData(self.content_frame, title="Impurities", 
                                        values=additives_from_database)
        self.impurities.grid(row=12, column=0, padx=10, pady=(10, 0), sticky="nsw") 

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def clear_user_input(self):
        "Clear user input"
        self.composition_estimate.clear()
        self.sample_type.clear()
        self.dimensionality.clear()
        self.bandgap.clear()
        self.A_ions.clear()
        self.B_ions.clear()
        self.X_ions.clear()          
        self.additives.clear()
        self.impurities.clear()

    def generate_json(self):
        "Put user data together in a json file"
        # File path to save the data
        save_path = self.generate_save_path()
        
        # Categorical text data
        composition_estimate = self.composition_estimate.get()
        sample_type = self.sample_type.get()
        dimensionality = self.dimensionality.get()
        bandgap = self.bandgap.get()
    
        # Data for ions
        a_ions, a_coefficients = self.A_ions.get()
        b_ions, b_coefficients = self.B_ions.get()
        x_ions, x_coefficients = self.X_ions.get()

        # Additives
        # additives, function, concentration, concentration_metric = self.additives.get()
        additives, additives_concentrations, additives_mass_fractions = self.additives.get()

        # Impurities
        impurities, impurities_concentrations, impurities_mass_fractions = self.impurities.get() 

        # Generate and save the perovskite object as json
        perovskite = PerovskiteToJson(
            composition_estimate=composition_estimate,
            sample_type=sample_type,
            dimensionality=dimensionality, 
            bandgap=bandgap,       
            a_ions_abbreviations=a_ions, 
            a_coefficients=a_coefficients, 
            b_ions_abbreviations=b_ions, 
            b_coefficients=b_coefficients, 
            x_ions_abbreviations=x_ions, 
            x_coefficients=x_coefficients,          
            additives_abbreviations = additives,
            additives_concentrations = additives_concentrations,
            additives_mass_fractions = additives_mass_fractions,       
            impurities_abbreviations = impurities,
            impurities_concentrations = impurities_concentrations,
            impurities_mass_fractions = impurities_mass_fractions,         
            path_to_reference_data='local', 
            save_path=save_path,
            save=True)

    def generate_save_path(self):
        "Generate the compleat file path to where to save the data"
        folder_path = self.save_folder.get()
        file_name = self.file_name.get()
        
        # Check file ending
        if file_name[-4:] == ".txt":
            file_name = file_name[:-4]
        if file_name[-5:] != ".json":
            file_name = file_name + ".json"
            
        file_path = os.path.join(folder_path, file_name)
        
        return file_path
        
    def get_filepath(self):
        "Ask user for a path to the catalog to store the files"
        self.folder_selected = tk.filedialog.askdirectory()
        self.save_folder.update_textbox(text=self.folder_selected)

if __name__ == "__main__":
    app = App()
    app.mainloop()