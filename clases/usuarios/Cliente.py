from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime, date

from clases.usuarios.Usuario import Usuario

if TYPE_CHECKING:
    # Solo importamos Reserva para el chequeo de tipos, no para la ejecución
    from clases.vuelos.Reserva import Reserva


class Cliente(Usuario):
    def __init__(self, nombre: str, correo: str, numDoc: str, passwordHash: str):
        super().__init__(nombre, correo, numDoc, passwordHash)
        self.__millas: int = 0
        # Usamos 'Reserva' como string para evitar error de referencia circular
        self.__historialReservas: List['Reserva'] = []

    def acumularMillas(self, cantidad: int) -> None:
        #if self.checkin == True:
        self.__millas += cantidad
        return

    def puedeMejorarClase(self) -> bool:
        if self.__millas >= 2000:
            return True

        pass

    def getTipo(self) -> str:
        return "Cliente"
        