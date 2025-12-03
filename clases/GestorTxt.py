from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.IPersistencia import IPersistencia

class GestorTxt(IPersistencia):
    def __init__(self, rutaBase: str):
        self.__rutaBase = rutaBase

    def cargarDatos(self, ruta: str) -> List[Any]:
        pass

    def guardarDatos(self, ruta: str, datos: List[Any]) -> bool:
        pass

    def _parsearLinea(self, linea: str) -> Dict:
        pass

