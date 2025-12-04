from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.asientos.Asiento import Asiento

class AsientoEconomico(Asiento):
    def calcularPrecio(self, esPasajeroFrecuente: bool) -> float:
        pass
