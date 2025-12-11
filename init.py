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

class API:
    def __init__(self):
        self.__usuarioSesion: Optional[Usuario] = None
        self.__vuelos: List[Vuelo] = []
        self.__usuariosRegistrados: List[Usuario] = []
        self.__reservas: List[Reserva] = []
        self.__persistencia: Optional[IPersistencia] = GestorTxt()

    def iniciar(self) -> None:
        self.__vuelos = self.__persistencia.cargarDatos("vuelos.txt", ["id","origen","destino", "fechaDiaSalida", "fechaHoraSalida","asientosEco","asientosPref"])
        
        pass
        if not os.path.exists("database"):
            os.makedirs("database")
        print("Sistema iniciado y listo para usar :).")

    def login(self, doc: str, password: str) -> Dict:
        # 1. BUSCAR EN ADMINISTRADORES
        admins = self.__gestor.cargarDatos("administradores.txt", ["nombre", "correo", "num_doc", "password_hash"])
        for admin_data in admins:
            user = Administrador(admin_data["nombre"], admin_data["correo"], admin_data["num_doc"], admin_data["password_hash"])
            # Asumiendo que Administrador tiene verifyPassword o verificarPassword (según tu clase Usuario)
            if user.getNumDoc() == doc and user.verificarPassword(password): 
                self.__usuarioSesion = user
                return {"success": True, "user": {"nombre": user._nombre, "tipo_usuario": "Administrador"}}
                
        # 2. BUSCAR EN CLIENTES
        clientes = self.__gestor.cargarDatos("clientes.txt", ["nombre", "correo", "num_doc", "password_hash", "millas"])
        for cli_data in clientes:
            user_temp = Cliente(cli_data["nombre"], cli_data["correo"], cli_data["num_doc"], cli_data["password_hash"], int(cli_data.get("millas", 0)))
            if user_temp.verificarPassword(password): # Usar el método estándar de la clase
                self.__usuarioSesion = user_temp
                return {"success": True, "user": {"nombre": user_temp._nombre, "tipo_usuario": "Cliente", "millas": user_temp.getMillas()}}
                
        # 3. NO SE ENCONTRÓ
        return {"success": False, "message": "Credenciales inválidas."}

    def registro(self, datos: Dict) -> bool:
        clientes = self.__gestor.cargarDatos("clientes.txt", ["nombre", "correo", "num_doc", "password_hash", "millas"])
        
        for c in clientes:
            if c["num_doc"] == datos["numDoc"]:
                return {"success": False, "message": "El usuario ya existe"}

        nuevo_cliente = Cliente(datos["nombre"], datos["correo"], datos["numDoc"], datos["password"])
        
        nuevo_dict = {
            "nombre": datos["nombre"],
            "correo": datos["correo"],
            "num_doc": datos["numDoc"],
            "password_hash": nuevo_cliente._passwordHash,
            "millas": 0
        }
        
        clientes.append(nuevo_dict)
        if self.__gestor.guardarDatos("clientes.txt", clientes):
            return {"success": True, "message": "Registro exitoso"}
        return {"success": False, "message": "Error al guardar"}

    def buscarVuelos(self, filtros: Dict) -> List[Vuelo]:
        keys = ["codigo", "origen", "destino", "dia", "hora", "sillas_pref", "sillas_eco"]
        vuelos = self.__gestor.cargarDatos("vuelos.txt", keys)
        resultado = []

        origen_b = filtros.get("origen", "").lower()
        destino_b = filtros.get("destino", "").lower()

        for v in vuelos:
            match_origen = not origen_b or origen_b in v["origen"].lower()
            match_destino = not destino_b or destino_b in v["destino"].lower()

            if match_origen and match_destino:
                v["sillas_pref"] = int(v["sillas_pref"])
                v["sillas_eco"] = int(v["sillas_eco"])
                resultado.append(v)
        
        return resultado

    def obtenerDetalleVuelo(self, idVuelo: str) -> Dict:
        keys = ["codigo", "origen", "destino", "dia", "hora", "sillas_pref", "sillas_eco"]
        vuelos = self.__gestor.cargarDatos("vuelos.txt", keys)
        for v in vuelos:
            if v["codigo"] == idVuelo:
                return v
        return {}

    def crearReserva(self, idVuelo: str, pasajerosData: List) -> Dict:
        pass

    def realizarCheckIn(self, idReserva: str, configEquipaje: Dict) -> Dict:
        pass

    def _actualizarMillasCliente(self, cliente_obj: Cliente):
        cli_keys = ["nombre", "correo", "num_doc", "password_hash", "millas"]
        clientes = self.__gestor.cargarDatos("clientes.txt", cli_keys)
        for c in clientes:
            if c["num_doc"] == cliente_obj._numDoc:
                c["millas"] = str(cliente_obj.getMillas())
                break
        self.__gestor.guardarDatos("clientes.txt", clientes)

    def adminGetReporte(self, filtros: Dict) -> Dict:
        if not self.__usuarioSesion or self.__usuarioSesion.getTipo() != "Admin":
            return {"error": "No autorizado"}
        
        admin: Administrador = self.__usuarioSesion 
        
        ventas = admin.verSillasVendidas(filtros)
        
        datos_pasajeros = []
        if filtros.get("codigo_vuelo"):
             datos_pasajeros = admin.verDatosPasajeros(filtros["codigo_vuelo"])

        return {
            "ventas_por_vuelo": ventas,
            "pasajeros": datos_pasajeros
        }
    
    
def main():
    try:
        # Pruebas en consola
        
        prueba = API()
        
        prueba.iniciar()
        prueba.login("1001", "12345")
        
        
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
        
        # webview.start(debug=True, http_server=True)
        # webview.start( http_server=True)
    finally:
        ## PRUEBAS EN CONSOLA
        
        
        
        
        
        ## ESTO ES LO QUE SE VA A PRESENTAR A LA PROFESORA MAÑANA
        # Cerrar la aplicación
        print("Cerrando la aplicación...")

if __name__ == "__main__":
    main()