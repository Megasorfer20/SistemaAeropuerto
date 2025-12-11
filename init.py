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
from clases.GestorTxt import GestorTxt

class API:
    def __init__(self):
        self.__usuarioSesion: Optional[Usuario] = None
        self.__vuelos: List[Vuelo] = []
        self.__usuariosRegistrados: List[Usuario] = []
        self.__reservas: List[Reserva] = []
        self.__persistencia: Optional[IPersistencia] = GestorTxt()

    def iniciar(self) -> None:
        self.__vuelos = self.__persistencia.cargarDatos("vuelos.txt", ["id","origen","destino", "fechaDiaSalida", "fechaHoraSalida","asientosEco","asientosPref"])
        
        print("Vuelos cargados:", self.__vuelos)
        
        pass

    def login(self, doc: str, password: str) -> Dict:
        pass

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
    try:
        # Pruebas en consola

        
        # Activar la interfaz
        dist_dir = os.path.join(os.path.dirname(__file__), 'interface', 'dist')
        index_file = os.path.join(dist_dir, 'index.html')

        # if not os.path.exists(index_file):
        #     raise FileNotFoundError("¡Asegúrate de haber ejecutado 'npm run build' en Vue!")
        
        api = API()
        api.iniciar()

        # webview.create_window('Gestor de pacientes', index_file, js_api=api)
        webview.create_window("Dev", "http://localhost:5173", js_api=api)
        
        webview.start(debug=True, http_server=True)
        # webview.start( http_server=True)
    finally:
        #PRUEBAS EN CONSOLA
        
        
        # Cerrar la aplicación
        print("Cerrando la aplicación...")

if __name__ == "__main__":
    main()