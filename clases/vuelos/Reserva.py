from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime, date
# Imports que NO causan conflicto
from clases.asientos.Asiento import Asiento
from clases.equipajes.Equipaje import Equipaje
from clases.vuelos.Vuelo import Vuelo
from clases.vuelos.Pasajero import Pasajero

if TYPE_CHECKING:
    from clases.usuarios.Cliente import Cliente
    from clases.vuelos.Vuelo import Vuelo
    from clases.vuelos.Pasajero import Pasajero

class Reserva:
    def __init__(self, idReserva: str, titular: Cliente, vuelo: Vuelo, fechaReserva: str, pasajeros: List[Pasajero] = None):
        self.__idReserva = idReserva
        self.__titular = titular
        self.__vuelo = vuelo
        self.__fechaReserva = fechaReserva
        # Si pasamos pasajeros en el init, los usamos, si no, lista vacía
        self.__pasajeros: List[Pasajero] = pasajeros if pasajeros else []
        self.__totalPagado = 0.0
        self.__estado = "Confirmada" # Pendiente, Confirmada, Cancelada
        self.__checkInRealizado = False

    # --- GETTERS ---
    def getId(self) -> str:
        return self.__idReserva

    def getTitular(self) -> Cliente:
        return self.__titular
    
    def getVuelo(self) -> Vuelo:
        return self.__vuelo

    def getPasajeros(self) -> List[Pasajero]:
        return self.__pasajeros

    def getCheckInRealizado(self) -> bool:
        return self.__checkInRealizado

    def getFechaReserva(self) -> str:
        return self.__fechaReserva

    # --- LÓGICA ---
    def setCheckInRealizado(self, estado: bool):
        self.__checkInRealizado = estado

    def realizarCheckIn(self) -> bool:
        if self.__estado == "Cancelada":
            return False
        self.__checkInRealizado = True
        return True