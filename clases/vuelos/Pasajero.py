from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.asientos.Asiento import Asiento
from clases.equipajes.Equipaje import Equipaje

class Pasajero:
    def __init__(self, nombre: str, numDoc: str, correo: str, asiento: Asiento):
        self.__nombre = nombre
        self.__numDoc = numDoc
        self.__correo = correo
        self.__asiento = asiento
        self.__equipajes: List[Equipaje] = []

    def agregarEquipaje(self, eq: Equipaje) -> None:
        self.__equipajes.append(eq)

    def calcularTotalPasajero(self) -> float:
        return 0.0