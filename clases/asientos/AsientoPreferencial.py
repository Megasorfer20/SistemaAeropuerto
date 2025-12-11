from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.asientos.Asiento import Asiento


class AsientoPreferencial(Asiento):
    def calcularPrecio(self, esPasajeroFrecuente: bool) -> float:
        self._precioBase = 850000
        precio = self._precioBase
        if esPasajeroFrecuente:
            precio = 235000
        if self._seleccionManual:
            precio += 0.15*precio
        return precio