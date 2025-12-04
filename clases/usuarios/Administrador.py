from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.usuarios.Usuario import Usuario
from clases.vuelos.Vuelo import Vuelo

class Administrador(Usuario):
    def __init__(self, nombre: str, correo: str, numDoc: str, passwordHash: str):
        super().__init__(nombre, correo, numDoc, passwordHash)

    def modificarVuelo(self, idVuelo: str, data: Dict) -> bool:

        pass

    def agregarVuelo(self, vuelo: 'Vuelo') -> bool:
        pass

    def verSillasVendidas(self, filtro: Dict) -> Dict:
            
        pass

    def verDatosPasajeros(self, idVuelo: str) -> List[Any]:
        pass

    def getTipo(self) -> str:
        return "Admin"