from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime, date
# Imports que NO causan conflicto
from clases.asientos.Asiento import Asiento
from clases.equipajes.Equipaje import Equipaje
from clases.vuelos.Vuelo import Vuelo
from clases.vuelos.Pasajero import Pasajero

# Bloque especial para evitar el ciclo
if TYPE_CHECKING:
    from clases.usuarios.Cliente import Cliente
    # Si Equipaje también causa conflicto, muévelo aquí también

class Reserva:
    # Gracias a 'from __future__ ...', ahora puedes usar Cliente sin comillas
    # aunque no esté importado realmente en tiempo de ejecución.
    def __init__(self, idReserva: str, titular: Cliente, vuelo: Vuelo, fechaReserva: date):
        self.__idReserva = idReserva
        self.__titular = titular
        self.__vuelo = vuelo
        self.__pasajeros: List[Pasajero] = []
        self.__fechaReserva = fechaReserva
        self.__totalPagado = 0.0
        self.__estado = "Pendiente"
        self.__checkInRealizado = False

    def agregarPasajero(self, pasajero: Pasajero) -> None:
        pass

    def confirmarReserva(self) -> bool:
        pass

    def cancelarReserva(self) -> bool:
        pass

    def realizarCheckIn(self, datosEquipaje: List) -> Dict:
        pass