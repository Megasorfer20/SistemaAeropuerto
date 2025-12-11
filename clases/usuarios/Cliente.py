from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime, date

from clases.usuarios.Usuario import Usuario

if TYPE_CHECKING:
    from clases.vuelos.Reserva import Reserva

class Cliente(Usuario):
    def __init__(self, nombre: str, correo: str, numDoc: str, password: str, miles: int = 0, es_hash: bool = False):
        super().__init__(nombre, correo, numDoc, password, es_hash)
        self.__millas: int = miles
        self.__historialReservas = []

    def acumularMillas(self, cantidad: int) -> None:
        self.__millas += cantidad

    def gastarMillas(self, cantidad: int) -> bool:
        if cantidad <= self.__millas:
            self.__millas -= cantidad
            return True
        return False

    def puedeMejorarClase(self) -> bool:
        return self.__millas >= 2000

    def getMillas(self) -> int:
        return self.__millas

    def getTipo(self) -> str:
        return "Cliente"