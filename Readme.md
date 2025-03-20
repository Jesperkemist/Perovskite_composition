## About The Project
This repo is associated to a paper with the title:

Towards an Interoperable Perovskite Description,
Or How to Keep Track of Close to 300 Organic Ions Used in Hybrid Perovskites
in ...

## Resources
*The file **perovskite_composition_schema.json** defines the data schema for perovskite compositions
*The file **ion_schema.json** defines the data schema for perovskite ions 
*The folder **Data_ions** contains excel files with data for all perovskite ions identified in the projects.
*The folder **Perovskite composition files** contains example files of perovskite composition files
*The file **perovskite_to_json.py** contains the class PerovskiteToJson with functionality for converting perovskite data to a perovskite composition json file.
*The file **GUI_perovskite_to_json.py** is a graphical user interface  for simplified data entry and for converting data to a perovskite composition json file 
*The file **demo_notebook.ipynb** demonstrates how to format the required data in order to be able to convert it to a perovskite composition json file
*The file **demo_notebook_NOMAD.ipynb** demonstrates how to access and manipulate data for perovskite compositions and perovskite ions stored in the NOMAD database

## Requirements
The scripts have been tested on Windows 11 running python 3.11

Requires: customtkinter, ipython, json, Numpy, Openpyxl, Pandas, tkinter


## How to cite
If you use this code in your research, we kindly ask that you cite the published paper:

Ayman Maqsood, Hampus Näsström, Chen Chen, Li Qiutong, Jingshan Luo, Rayan Chakraborty, Volker Blum, Eva Unger, Claudia Draxl, José A Márquez*, T. Jesper Jacobsson*, Towards an Interoperable Perovskite Description, Or How to Keep Track of Close to 300 Organic Ions Used in Hybrid Perovskites, XXX, 2024

---

## License
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons
Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a><br />

This code is licensed under the terms of the [Creative Commons Attribution 4.0 International
License](http://creativecommons.org/licenses/by/4.0/).