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
from clases.asientos.AsientoEconomico import AsientoEconomico
from clases.asientos.AsientoPreferencial import AsientoPreferencial
from clases.equipajes.Equipaje import Equipaje
from clases.usuarios.Cliente import Cliente
from clases.usuarios.Administrador import Administrador
from clases.vuelos.Vuelo import Vuelo
from clases.vuelos.Pasajero import Pasajero
from clases.usuarios.Usuario import Usuario
from clases.vuelos.Reserva import Reserva
from clases.IPersistencia import IPersistencia
from clases.GestorTxt import GestorTxt
from API import API

def main():
    try:
        # Pruebas en consola
        
        prueba = API()
        
        asiento1 = AsientoPreferencial(
        id="A1",
        fila=10,
        columna="C",
        esVentana=True,
        precioBase=0     # Este valor luego es reemplazado en calcularPrecio
        )
        asiento1._seleccionManual = False
        print(asiento1.calcularPrecio(False))
        
        
        
        
        
        
        
        
        
        ## ESTO ES LO QUE SE VA A PRESENTAR A LA PROFESORA MAÑANA
        
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
        ## PRUEBAS EN CONSOLA
        
        
        
        
        
        ## ESTO ES LO QUE SE VA A PRESENTAR A LA PROFESORA MAÑANA
        # Cerrar la aplicación
        print("Cerrando la aplicación...")

if __name__ == "__main__":
    main()