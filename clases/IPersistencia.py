from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date

class IPersistencia(ABC):
    @abstractmethod
    def cargarDatos(self, ruta: str) -> List[Any]:
        pass

    @abstractmethod
    def guardarDatos(self, ruta: str, datos: List[Any]) -> bool:
        pass
