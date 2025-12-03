from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.asientos.Asiento import Asiento
from clases.equipajes.Equipaje import Equipaje
from clases.usuarios.Cliente import Cliente
from clases.vuelos.Vuelo import Vuelo
from clases.vuelos.Pasajero import Pasajero

class Reserva:
    def __init__(self, idReserva: str, titular: Cliente, vuelo: Vuelo, fechaReserva: date):
        self.__idReserva = idReserva
        self.__titular = titular
        self.__vuelo = vuelo
        self.__pasajeros: List[Pasajero] = []
        self.__fechaReserva = fechaReserva
        self.__totalPagado = 0.0
        self.__estado = "Pendiente" # Estado inicial por defecto
        self.__checkInRealizado = False

    def agregarPasajero(self, pasajero: Pasajero) -> None:
        pass

    def confirmarReserva(self) -> bool:
        pass

    def cancelarReserva(self) -> bool:
        pass

    def realizarCheckIn(self, datosEquipaje: List) -> Dict:
        pass