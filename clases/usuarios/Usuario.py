from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import hashlib

class Usuario(ABC):
    def __init__(self, nombre: str, correo: str, numDoc: str, password: str):
        self._nombre = nombre
        self._correo = correo
        self._numDoc = numDoc
        self._passwordHash = self._hashPasword(password)

    def verificarPassword(self, password: str) -> bool:
        if self._hashPasword(password) == self._passwordHash:
            return True

    def cambiarPassword(self, newPassword: str) -> bool:
        if self.verificarPassword:
            self._passwordHash = self._hashPasword(newPassword)
            return True

    @abstractmethod
    def getTipo(self) -> str:
        
        pass

    def _hashPasword(self, password: str):
        return hashlib.sha256(password.encode()).hexdigest()
