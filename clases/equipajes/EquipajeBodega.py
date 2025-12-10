from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.equipajes.Equipaje import Equipaje

class EquipajeBodega(Equipaje):
    def calcularCosto(self, claseVuelo: str) -> float:
        if claseVuelo == "PREF" :  #and pasajero.equipajes.lenght == 0
            costo = (self._peso * 10000) + (self._volumen * 5000)
            return costo
            
        pass
