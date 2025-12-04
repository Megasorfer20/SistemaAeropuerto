from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date

class Equipaje(ABC):
    def __init__(self, peso: float, volumen: float):
        self._peso = peso
        self._volumen = volumen

    @abstractmethod
    def calcularCosto(self, claseVuelo: str) -> float:
        pass