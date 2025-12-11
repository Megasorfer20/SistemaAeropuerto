from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.equipajes.Equipaje import Equipaje
from clases.vuelos.Pasajero import Pasajero

class EquipajeBodega(Equipaje):
    def calcularCosto(self, claseVuelo: str, pasajero : Pasajero) -> float:
        if claseVuelo == "PREF" and len(pasajero.__equipajes) == 0:
            costo = (self._peso * 10000) + (self._volumen * 5000)
            return costo
            
