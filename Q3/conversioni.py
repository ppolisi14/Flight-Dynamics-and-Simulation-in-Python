# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 21:39:29 2024
Conversioni.py permette di effettuare le conversioni tra unità di misura
grandezze maggiormente usate in ambito aeronautico.
@author: ppoli
"""

from math import pi 

def convvel(quantity: float, from_unit: str, to_unit: str) -> float:
    """
    Converte una quantità di velocità da un'unità ad un'altra.
    
    Parametri:
    - quantity (float): La quantità di velocità da convertire.
    - from_unit (str): L'unità di partenza (ad esempio, "km/h", "m/s", "mph").
    - to_unit (str): L'unità di destinazione (ad esempio, "km/h", "m/s", "mph").
    
    Unità supportate:
    - "km/h": chilometri all'ora
    - "m/s": metri al secondo
    - "mph": miglia orarie
    
    Restituisce:
    - float: La quantità di velocità convertita nell'unità di destinazione.
    
    Solleva:
    - ValueError: Se la conversione tra le unità specificate non è supportata.
    
    Esempi:
    >>> convvel(100, "km/h", "m/s")
    27.77777777777778
    
    >>> convvel(60, "mph", "km/h")
    96.56064
    """
    
    # Definire i fattori di conversione per diverse unità
    conversion_factors = {
        ("km/h", "m/s"): 1 / 3.6,
        ("m/s", "km/h"): 3.6,
        ("mph", "km/h"): 1.60934,
        ("km/h", "mph"): 1 / 1.60934,
        ("mph", "m/s"): 0.44704,
        ("m/s", "mph"): 1 / 0.44704
    }

    # Verificare se la combinazione di unità è supportata
    if (from_unit, to_unit) in conversion_factors:
        return quantity * conversion_factors[(from_unit, to_unit)]
    else:
        raise ValueError(f"Conversione da {from_unit} a {to_unit} non supportata.")



def convangvel(quantity: float, from_unit: str, to_unit: str) -> float:
    """
    Converte una quantità di velocità angolare da un'unità ad un'altra.

    Parametri:
    - quantity (float): La quantità di velocità angolare da convertire.
    - from_unit (str): L'unità di partenza (ad esempio, "deg/s" o "rad/s").
    - to_unit (str): L'unità di destinazione (ad esempio, "deg/s" o "rad/s").

    Restituisce:
    - float: La quantità di velocità angolare convertita nell'unità di destinazione.

    Solleva:
    - ValueError: Se la conversione tra le unità specificate non è supportata.
    
    Esempio:
    >>> convangvel(180, "deg/s", "rad/s")
    3.141592653589793

    >>> convangvel(1, "rad/s", "deg/s")
    57.29577951308232
    """
    if from_unit == "deg/s" and to_unit == "rad/s":
        conversion_factor = pi / 180
        return quantity * conversion_factor
    elif from_unit == "rad/s" and to_unit == "deg/s":
        conversion_factor = 180 / pi
        return quantity * conversion_factor
    else:
        raise ValueError(f"Conversione da {from_unit} a {to_unit} non supportata.")