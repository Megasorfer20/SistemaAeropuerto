from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime, date

from clases.usuarios.Usuario import Usuario

if TYPE_CHECKING:
    from clases.vuelos.Reserva import Reserva


class Cliente(Usuario):
    def __init__(self, nombre: str, correo: str, numDoc: str, passwordHash: str):
        super().__init__(nombre, correo, numDoc, passwordHash)
        self.__millas: int = 0
        self.__historialReservas: List['Reserva'] = []

    def acumularMillas(self, cantidad: int) -> None:
        self.__millas += cantidad
        return
    
    def gastarMillas(self, cantidad: int) -> bool:
        if cantidad > self.__millas:
            return False
        self.__millas -= cantidad
        return True

    def puedeMejorarClase(self) -> bool:
        if self.__millas >= 2000:
            return True

    def getMillas(self) -> int:
        return self.__millas

    def getTipo(self) -> str:
        return "Cliente"
        