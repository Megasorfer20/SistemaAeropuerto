from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date

class Asiento(ABC):
    def __init__(self, id: str, fila: int, columna: str, esVentana: bool, precioBase: float):
        self._id = id
        self._fila = fila
        self._columna = columna
        self._esVentana = esVentana
        self._ocupado = False
        self._precioBase = precioBase
        self._seleccionManual = False

    @abstractmethod
    def calcularPrecio(self, esPasajeroFrecuente: bool) -> float:
        pass

    def reservar(self, manual: bool) -> None:
        self._ocupado = True 
        pass

    def liberar(self) -> None:
        self._ocupado = False
        pass