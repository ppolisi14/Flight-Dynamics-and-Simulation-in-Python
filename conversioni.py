# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 21:39:29 2024
Conversioni.py permette di effettuare le conversioni tra unità di misura
grandezze maggiormente usate in ambito aeronautico.
@author: ppoli
"""

def convvel(quantity: float, from_unit : str, to_unit: str):
    if(from_unit == "km/h" and to_unit =="m/s"):
        return quantity/3.6
    elif(from_unit == "m/s" and to_unit =="km/h"):
        return quantity*3.6

