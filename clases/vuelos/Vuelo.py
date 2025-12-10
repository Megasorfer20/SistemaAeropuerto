from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.asientos.Asiento import Asiento

class Vuelo:
    def __init__(self, codigo: str, origen: str, destino: str, fechaHoraSalida: datetime, precioBaseEco: float, precioBasePref: float):
        self.__codigo = codigo
        self.__origen = origen
        self.__destino = destino
        self.__fechaHoraSalida = fechaHoraSalida
        self.__mapaAsientos: List[Asiento] = []
        self.__precioBaseEco = precioBaseEco
        self.__precioBasePref = precioBasePref

    # --- GETTERS ---
    def getCodigo(self) -> str:
        return self.__codigo

    def getOrigen(self) -> str:
        return self.__origen

    def getDestino(self) -> str:
        return self.__destino

    def getFechaHoraSalida(self) -> datetime:
        return self.__fechaHoraSalida

    def getMapaAsientos(self) -> List[Asiento]:
        return self.__mapaAsientos

    def getPrecioBaseEco(self) -> float:
        return self.__precioBaseEco

    def getPrecioBasePref(self) -> float:
        return self.__precioBasePref

    # --- MÉTODOS DE LÓGICA ---

    def generarMapaAsientos(self) -> None:
        pass

    def buscarAsientosLibres(self) -> int:
        pass

    def calcularSobreventaPermitida(self) -> float:
        pass

    def obtenerAsientoAleatorio(self, tipo: str) -> Asiento:
        pass

    def verificarDisponibilidad(self, cantidad: int) -> bool:
        pass