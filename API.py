import webview
import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, date

# Imports de clases (ajusta según tu estructura de carpetas si es necesario)
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
        self.__vuelos: List[Dict] = [] 
        
        # 2. SEPARACIÓN DE USUARIOS EN VARIABLES APARTE
        self.__clientes: List[Cliente] = []
        self.__administradores: List[Administrador] = []
        
        self.__reservas: List[Reserva] = []
        self.__persistencia: Optional[IPersistencia] = GestorTxt()

    def iniciar(self) -> None:
        # 1. Cargar Vuelos
        self.__vuelos = self.__persistencia.cargarDatos("vuelos.txt", ["id","origen","destino", "fechaDiaSalida", "fechaHoraSalida","asientosEco","asientosPref"])
        
        # 2. Cargar Administradores
        admins_data = self.__persistencia.cargarDatos("administradores.txt", ["nombre", "correo", "num_doc", "password_hash"])
        self.__administradores = [] # Reiniciar lista
        for admin in admins_data:
            obj_admin = Administrador(
                admin["nombre"], 
                admin["correo"], 
                admin["num_doc"], 
                admin["password_hash"], 
                es_hash=True
            )
            self.__administradores.append(obj_admin)

        # 3. Cargar Clientes
        clientes_data = self.__persistencia.cargarDatos("clientes.txt", ["nombre", "correo", "num_doc", "password_hash", "millas"])
        self.__clientes = [] # Reiniciar lista
        for cli in clientes_data:
            try:
                millas = int(cli.get("millas", 0))
            except:
                millas = 0
                
            obj_cliente = Cliente(
                cli["nombre"], 
                cli["correo"], 
                cli["num_doc"], 
                cli["password_hash"], 
                miles=millas,
                es_hash=True
            )
            self.__clientes.append(obj_cliente)

        print(f"Sistema iniciado: {len(self.__vuelos)} vuelos, {len(self.__administradores)} admins, {len(self.__clientes)} clientes.")

    def guardar_datos_cierre(self) -> None:
        """
        Este método se llama solo al cerrar la aplicación (desde el finally de init.py).
        Convierte los objetos en memoria a diccionarios y sobreescribe los TXT.
        """
        print("Guardando datos en disco...")

        # 1. Guardar Clientes
        lista_clientes_dicts = []
        for c in self.__clientes:
            lista_clientes_dicts.append({
                "nombre": c.getNombre(),
                "correo": c.getCorreo(),
                "num_doc": c.getNumDoc(),
                "password_hash": c.getPasswordHash(),
                "millas": c.getMillas()
            })
        self.__persistencia.guardarDatos("clientes.txt", lista_clientes_dicts)

        # 2. Guardar Administradores
        lista_admins_dicts = []
        for a in self.__administradores:
            lista_admins_dicts.append({
                "nombre": a.getNombre(),
                "correo": a.getCorreo(),
                "num_doc": a.getNumDoc(),
                "password_hash": a.getPasswordHash()
            })
        self.__persistencia.guardarDatos("administradores.txt", lista_admins_dicts)
        
        # Aquí también podrías guardar vuelos o reservas si los mantuviste en memoria

    def obtenerVuelosIniciales(self) -> List[Dict]:
        return self.__vuelos

    def buscarVuelos(self, filtros: Dict) -> List[Dict]:
        # (Lógica de búsqueda se mantiene igual...)
        resultado = []
        id_b = filtros.get("id", "").strip()
        origen_b = filtros.get("origen", "").lower().strip()
        destino_b = filtros.get("destino", "").lower().strip()
        dia_b = filtros.get("dia", "").upper().strip() 
        hora_inicio_str = filtros.get("horaInicio", "")
        hora_fin_str = filtros.get("horaFin", "")

        for v in self.__vuelos:
            if id_b and v["id"] != id_b: continue
            if origen_b and origen_b not in v["origen"].lower(): continue
            if destino_b and destino_b not in v["destino"].lower(): continue
            if dia_b and dia_b != "TODOS" and dia_b != v["fechaDiaSalida"].upper(): continue
            
            try:
                if hora_inicio_str or hora_fin_str:
                    hora_vuelo = datetime.strptime(v["fechaHoraSalida"], "%H:%M").time()
                    if hora_inicio_str:
                        hora_min = datetime.strptime(hora_inicio_str, "%H:%M").time()
                        if hora_vuelo < hora_min: continue
                    if hora_fin_str:
                        hora_max = datetime.strptime(hora_fin_str, "%H:%M").time()
                        if hora_vuelo > hora_max: continue
            except ValueError:
                continue

            resultado.append(v)
        return resultado


    def login(self, doc: str, password: str) -> Dict:
        # 1. Buscar en Administradores
        for admin in self.__administradores:
            if admin.getNumDoc() == doc:
                if admin.verificarPassword(password):
                    self.__usuarioSesion = admin
                    return {
                        "success": True, 
                        "user": {
                            "nombre": admin.getNombre(),
                            "tipo_usuario": "Admin"
                        }
                    }
                else:
                    return {"success": False, "message": "Contraseña incorrecta (Admin)."}

        # 2. Buscar en Clientes
        for cliente in self.__clientes:
            if cliente.getNumDoc() == doc:
                if cliente.verificarPassword(password):
                    self.__usuarioSesion = cliente
                    return {
                        "success": True, 
                        "user": {
                            "nombre": cliente.getNombre(),
                            "tipo_usuario": "Cliente",
                            "millas": cliente.getMillas()
                        }
                    }
                else:
                    return {"success": False, "message": "Contraseña incorrecta."}
        
        return {"success": False, "message": "Usuario no encontrado."}

    def registro(self, datos: Dict) -> Dict:
        # 1. Verificar existencia (revisar ambas listas para evitar duplicados de documento)
        for admin in self.__administradores:
            if admin.getNumDoc() == datos["numDoc"]:
                return {"success": False, "message": "El documento ya pertenece a un administrador."}
        
        for cli in self.__clientes:
            if cli.getNumDoc() == datos["numDoc"]:
                return {"success": False, "message": "El número de documento ya está registrado."}

        # 2. Crear objeto Cliente (es_hash=False para encriptar aquí)
        nuevo_cliente = Cliente(
            nombre=datos["nombre"],
            correo=datos["correo"],
            numDoc=datos["numDoc"],
            password=datos["password"],
            miles=0,
            es_hash=False 
        )

        # 3. GUARDAR EN MEMORIA (Lista) - NO EN TXT TODAVÍA
        self.__clientes.append(nuevo_cliente)

        return {"success": True, "message": "Registro exitoso (Temporal en memoria)"}

    # ... Resto de métodos (crearReserva, realizarCheckIn, adminGetReporte) se mantienen ...
    
    def adminGetReporte(self, filtros: Dict) -> Dict:
        if not self.__usuarioSesion or self.__usuarioSesion.getTipo() != "Admin":
            return {"error": "No autorizado"}
        admin: Administrador = self.__usuarioSesion 
        ventas = admin.verSillasVendidas(filtros)
        datos_pasajeros = []
        if filtros.get("codigo_vuelo"):
             datos_pasajeros = admin.verDatosPasajeros(filtros["codigo_vuelo"])
        return {"ventas_por_vuelo": ventas, "pasajeros": datos_pasajeros}

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