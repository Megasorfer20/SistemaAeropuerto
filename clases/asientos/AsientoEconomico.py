from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.asientos.Asiento import Asiento

class AsientoEconomico(Asiento):
    def calcularPrecio(self, esPasajeroFrecuente: bool) -> float:
        self._precioBase = 235000
        if self._seleccionManual:
            precio += 0.15*self._precioBase
        return precio 
    
