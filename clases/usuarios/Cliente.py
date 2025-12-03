from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.usuarios.Usuario import Usuario
from clases.vuelos.Reserva import Reserva

class Cliente(Usuario):
    def __init__(self, nombre: str, correo: str, numDoc: str, passwordHash: str):
        super().__init__(nombre, correo, numDoc, passwordHash)
        self.__millas: int = 0
        # Usamos 'Reserva' como string para evitar error de referencia circular
        self.__historialReservas: List['Reserva'] = []

    def acumularMillas(self, cantidad: int) -> None:
        pass

    def puedeMejorarClase(self) -> bool:
        pass

    def getTipo(self) -> str:
        pass