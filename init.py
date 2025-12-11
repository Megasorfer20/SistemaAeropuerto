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
    # Instanciamos la API fuera del try para que sea accesible en el finally
    api = API()
    
    try:
        # Pruebas en consola (Opcional)
        asiento1 = AsientoPreferencial(id="A1", fila=10, columna="C", esVentana=True, precioBase=0)
        asiento1._seleccionManual = False
        # print(asiento1.calcularPrecio(False))
        
        # INICIO DEL SISTEMA
        # Carga los datos de los txt a las listas en memoria (__clientes, __administradores)
        api.iniciar()

        ## CONFIGURACIÓN DE LA INTERFAZ
        dist_dir = os.path.join(os.path.dirname(__file__), 'interface', 'dist')
        # index_file = os.path.join(dist_dir, 'index.html') 
        
        # Para desarrollo suele usarse localhost, para prod index_file
        webview.create_window("Sistema de Reservas", "http://localhost:5173", js_api=api)
        
        webview.start(debug=True, http_server=True)

    finally:
        ## 1. GUARDADO DE DATOS AL CERRAR
        # Aquí se cumple el requerimiento: guardar solo al cerrar la ventana
        if api:
            print("\n--- Ejecutando cierre del sistema ---")
            api.guardar_datos_cierre()
            
        print("Aplicación cerrada correctamente.")

if __name__ == "__main__":
    main()