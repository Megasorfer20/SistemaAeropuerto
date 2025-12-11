import webview
import sys
import os
from difflib import get_close_matches
from datetime import datetime
from difflib import SequenceMatcher
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.asientos.Asiento import Asiento
from clases.equipajes.Equipaje import Equipaje
from clases.usuarios.Cliente import Cliente
from clases.vuelos.Vuelo import Vuelo
from clases.vuelos.Pasajero import Pasajero
from clases.usuarios.Usuario import Usuario
from clases.vuelos.Reserva import Reserva
from clases.IPersistencia import IPersistencia

class API:
    def __init__(self):
        self.__usuarioSesion: Optional[Usuario] = None
        self.__vuelos: List[Vuelo] = []
        self.__usuariosRegistrados: List[Usuario] = []
        self.__reservas: List[Reserva] = []
        self.__persistencia: Optional[IPersistencia] = None

    def iniciar(self) -> None:
        if not os.path.exists("database"):
            os.makedirs("database")
        print("Sistema iniciado y listo para usar :).")

    def login(self, doc: str, password: str) -> Dict:
        admins = self.__gestor.cargarDatos("administradores.txt", ["nombre", "correo", "num_doc", "password_hash"])
        for admin_data in admins:
            user = Administrador(admin_data["nombre"], admin_data["correo"], admin_data["num_doc"], admin_data["password_hash"])
            if user.getNumDoc() == doc and user.verifyPassword(password):
                self.__usuarioSesion = user
                return {"success": True, "user": {"nombre": user-_nombre, "tipo_usuario": "Administrador"}}
        clientes = self.__gestor.cargarDatos("clientes.txt", ["nombre", "correo", "num_doc", "password_hash", "millas"])
        for cli_data in clientes:
            user_temp = Cliente(cli_data["nombre"], cli_data["correo"], cli_data["num_doc"], cli_data["password_hash"], int(cli_data.get("millas", 0)))
            if user_temp._passwordHash == password or user_temp.verificarPassword(password):
                self.__usuarioSesion = user_temp
                return {"success": True, "user": {"nombre": user_temp._nombre, "tipo_usuario": "Cliente, "millas": user_temp.getMillas()}}
        return {"success": False, "message": "Credenciales inválidas."}}}

    def registro(self, datos: Dict) -> bool:
        pass

    def buscarVuelos(self, filtros: Dict) -> List[Vuelo]:
        pass

    def obtenerDetalleVuelo(self, idVuelo: str) -> Dict:
        pass

    def crearReserva(self, idVuelo: str, pasajerosData: List) -> Dict:
        pass

    def realizarCheckIn(self, idReserva: str, configEquipaje: Dict) -> Dict:
        pass

    def adminGetReporte(self, filtros: Dict) -> Dict:
        pass
        

def main():
    dist_dir = os.path.join(os.path.dirname(__file__), 'interface', 'dist')
    index_file = os.path.join(dist_dir, 'index.html')

    # if not os.path.exists(index_file):
    #     raise FileNotFoundError("¡Asegúrate de haber ejecutado 'npm run build' en Vue!")
    
    api = API()

    # webview.create_window('Gestor de pacientes', index_file, js_api=api)
    webview.create_window("Dev", "http://localhost:5173", js_api=api)

    try:
        # Pruebas en consola
        
        
        # Activar la interfaz
        
        webview.start(debug=True, http_server=True)
        # webview.start( http_server=True)
    finally:
        #PRUEBAS EN CONSOLA
        
        
        # Cerrar la aplicación
        print("Cerrando la aplicación...")

if __name__ == "__main__":
    main()