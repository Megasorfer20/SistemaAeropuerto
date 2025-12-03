from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.equipajes.Equipaje import Equipaje


class EquipajeMano(Equipaje):
    def calcularCosto(self, claseVuelo: str) -> float:
        pass