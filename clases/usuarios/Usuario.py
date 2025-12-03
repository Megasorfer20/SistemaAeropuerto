from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date

class Usuario(ABC):
    def __init__(self, nombre: str, correo: str, numDoc: str, passwordHash: str):
        self._nombre = nombre
        self._correo = correo
        self._numDoc = numDoc
        self._passwordHash = passwordHash

    def verificarPassword(self, password: str) -> bool:
        if password == self._passwordHash:
            return True
        pass

    def cambiarPassword(self, newPassword: str) -> bool:
        if self.verificarPassword:
            self._passwordHash = newPassword
            return True
        
        pass

    @abstractmethod
    def getTipo(self) -> str:
        pass
