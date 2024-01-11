# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 21:39:29 2024
Conversioni.py permette di effettuare le conversioni tra unità di misura
grandezze maggiormente usate in ambito aeronautico.
@author: ppoli
"""

from math import pi 

def convvel(quantity: float, from_unit : str, to_unit: str):
    if(from_unit == "km/h" and to_unit =="m/s"):
        return quantity/3.6
    elif(from_unit == "m/s" and to_unit =="km/h"):
        return quantity*3.6



def convangvel(quantity: float, from_unit : str, to_unit: str):
    if(from_unit == "deg/s" and to_unit =="rad/s"):
        conversion_factor = pi / 180
        return quantity*conversion_factor
    elif(from_unit == "rad/s" and to_unit =="deg/s"):
        conversion_factor = 180 / pi
        return quantity*conversion_factor