from abc import ABC, abstractmethod
import hashlib

class Usuario(ABC):
    def __init__(self, nombre: str, correo: str, numDoc: str, password: str, es_hash: bool = False):
        self._nombre = nombre
        self._correo = correo
        self._numDoc = numDoc
        # Si ya viene del TXT (es_hash=True), lo guardamos directo. Si es nuevo, lo hasheamos.
        if es_hash:
            self._passwordHash = password
        else:
            self._passwordHash = self._hashPasword(password)

    def verificarPassword(self, password: str) -> bool:
        # Comparamos el hash de la contraseña ingresada con el hash guardado
        return self._hashPasword(password) == self._passwordHash

    def cambiarPassword(self, oldPassword: str, newPassword: str) -> bool:
        if self.verificarPassword(oldPassword):
            self._passwordHash = self._hashPasword(newPassword)
            return True
        return False

    def getNumDoc(self) -> str:
        return self._numDoc

    def getNombre(self) -> str:
        return self._nombre
    
    def getCorreo(self) -> str:
        return self._correo
    
    def getPasswordHash(self) -> str:
        return self._passwordHash

    @abstractmethod
    def getTipo(self) -> str:
        pass

    def _hashPasword(self, password: str):
        return hashlib.sha256(password.encode()).hexdigest()