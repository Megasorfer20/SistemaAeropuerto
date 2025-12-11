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
        self.__vuelos: List[Dict] = [] 
        # Esta lista contendrá objetos Cliente y Administrador mezclados
        self.__usuariosRegistrados: List[Usuario] = [] 
        self.__reservas: List[Reserva] = []
        self.__persistencia: Optional[IPersistencia] = GestorTxt()

    def iniciar(self) -> None:
        # 1. Cargar Vuelos
        self.__vuelos = self.__persistencia.cargarDatos("vuelos.txt", ["id","origen","destino", "fechaDiaSalida", "fechaHoraSalida","asientosEco","asientosPref"])
        
        # 2. Cargar Administradores
        admins_data = self.__persistencia.cargarDatos("administradores.txt", ["nombre", "correo", "num_doc", "password_hash"])
        for admin in admins_data:
            # Creamos el objeto indicando es_hash=True para que no vuelva a encriptar la clave
            obj_admin = Administrador(
                admin["nombre"], 
                admin["correo"], 
                admin["num_doc"], 
                admin["password_hash"], 
                es_hash=True
            )
            self.__usuariosRegistrados.append(obj_admin)

        # 3. Cargar Clientes
        clientes_data = self.__persistencia.cargarDatos("clientes.txt", ["nombre", "correo", "num_doc", "password_hash", "millas"])
        for cli in clientes_data:
            # Parseamos las millas a int, si falla asumimos 0
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
            self.__usuariosRegistrados.append(obj_cliente)

        print(f"Sistema iniciado: {len(self.__vuelos)} vuelos, {len(self.__usuariosRegistrados)} usuarios.")

    def obtenerVuelosIniciales(self) -> List[Dict]:
        return self.__vuelos

    def buscarVuelos(self, filtros: Dict) -> List[Dict]:
        """
        Filtra los vuelos según: id, origen, destino, dia, horaInicio, horaFin
        """
        resultado = []
        
        # 1. Obtenemos el ID del filtro (nuevo)
        id_b = filtros.get("id", "").strip()
        
        origen_b = filtros.get("origen", "").lower().strip()
        destino_b = filtros.get("destino", "").lower().strip()
        dia_b = filtros.get("dia", "").upper().strip() 
        hora_inicio_str = filtros.get("horaInicio", "")
        hora_fin_str = filtros.get("horaFin", "")

        for v in self.__vuelos:
            # --- NUEVA VALIDACIÓN: ID ---
            # Si hay un ID en el filtro y no coincide, saltamos
            if id_b and v["id"] != id_b:
                continue

            # 2. Filtro Origen
            if origen_b and origen_b not in v["origen"].lower():
                continue
            
            # 3. Filtro Destino
            if destino_b and destino_b not in v["destino"].lower():
                continue

            # 4. Filtro Día
            if dia_b and dia_b != "TODOS" and dia_b != v["fechaDiaSalida"].upper():
                continue

            # 5. Filtro Rango Horario
            try:
                if hora_inicio_str or hora_fin_str:
                    hora_vuelo = datetime.strptime(v["fechaHoraSalida"], "%H:%M").time()
                    
                    if hora_inicio_str:
                        hora_min = datetime.strptime(hora_inicio_str, "%H:%M").time()
                        if hora_vuelo < hora_min:
                            continue
                    
                    if hora_fin_str:
                        hora_max = datetime.strptime(hora_fin_str, "%H:%M").time()
                        if hora_vuelo > hora_max:
                            continue
            except ValueError:
                print(f"Error parseando horas en vuelo {v['id']}")
                continue

            resultado.append(v)
        
        return resultado


    def login(self, doc: str, password: str) -> Dict:
        # Buscamos en la lista cargada en memoria
        for usuario in self.__usuariosRegistrados:
            if usuario.getNumDoc() == doc:
                # Verificamos contraseña usando el método de la clase Usuario
                if usuario.verificarPassword(password):
                    self.__usuarioSesion = usuario
                    
                    respuesta = {
                        "nombre": usuario.getNombre(),
                        "tipo_usuario": usuario.getTipo()
                    }
                    
                    # Si es cliente, agregamos las millas a la respuesta
                    if isinstance(usuario, Cliente):
                        respuesta["millas"] = usuario.getMillas()
                        
                    return {"success": True, "user": respuesta}
                else:
                    return {"success": False, "message": "Contraseña incorrecta."}
        
        return {"success": False, "message": "Usuario no encontrado."}

    def registro(self, datos: Dict) -> Dict:
        # 1. Verificar si ya existe en memoria
        for usuario in self.__usuariosRegistrados:
            if usuario.getNumDoc() == datos["numDoc"]:
                return {"success": False, "message": "El número de documento ya está registrado."}

        # 2. Crear nuevo objeto Cliente (es_hash=False por defecto, encriptará la clave)
        nuevo_cliente = Cliente(
            nombre=datos["nombre"],
            correo=datos["correo"],
            numDoc=datos["numDoc"],
            password=datos["password"],
            miles=0,
            es_hash=False 
        )

        # 3. Agregar a la lista en memoria
        self.__usuariosRegistrados.append(nuevo_cliente)

        # 4. Guardar TODOS los clientes en el TXT (Reconstruimos la lista de dicts)
        # Filtramos solo los que son Cliente para guardarlos en clientes.txt
        lista_clientes_dicts = []
        for u in self.__usuariosRegistrados:
            if isinstance(u, Cliente):
                lista_clientes_dicts.append({
                    "nombre": u.getNombre(),
                    "correo": u.getCorreo(),
                    "num_doc": u.getNumDoc(),
                    "password_hash": u.getPasswordHash(),
                    "millas": u.getMillas()
                })

        # Usamos self.__persistencia en lugar de self.__gestor
        if self.__persistencia.guardarDatos("clientes.txt", lista_clientes_dicts):
            return {"success": True, "message": "Registro exitoso"}
        else:
            # Si falla el guardado, podríamos revertir el append en memoria, pero para este ejercicio basta con avisar
            return {"success": False, "message": "Error al guardar en base de datos"}

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