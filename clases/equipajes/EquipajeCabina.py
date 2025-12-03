from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.equipajes.Equipaje import Equipaje


class EquipajeCabina(Equipaje):
    def calcularCosto(self, claseVuelo: str) -> float:
        if claseVuelo == "ECO":
            costo = 40000
        elif claseVuelo == "PREF":
            costo = 0
        return costo