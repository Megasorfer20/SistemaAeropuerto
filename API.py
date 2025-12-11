import webview
import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta

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
        self.__vuelos: List[Vuelo] = [] 
        
        # 2. SEPARACIÓN DE USUARIOS EN VARIABLES APARTE
        self.__clientes: List[Cliente] = []
        self.__administradores: List[Administrador] = []
        
        self.__reservas: List[Reserva] = []
        self.__persistencia: Optional[IPersistencia] = GestorTxt()
        
    def _obtener_fecha_desde_str(self, dia_texto: str, hora_texto: str) -> datetime:
        """
        Intenta convertir el día y hora a datetime.
        Soporta formato 'YYYY-MM-DD' y 'LUNES', 'MARTES', etc.
        """
        dia_texto = dia_texto.upper().strip()
        
        # 1. Intentar formato fecha completa (YYYY-MM-DD)
        try:
            return datetime.strptime(f"{dia_texto} {hora_texto}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass # No es fecha, probamos día de la semana

        # 2. Intentar formato Día de Semana (LUNES, MARTES...)
        dias_semana = {
            "LUNES": 0, "MARTES": 1, "MIERCOLES": 2, "MIÉRCOLES": 2, 
            "JUEVES": 3, "VIERNES": 4, "SABADO": 5, "SÁBADO": 5, "DOMINGO": 6
        }
        
        if dia_texto in dias_semana:
            today = datetime.now()
            target_day_index = dias_semana[dia_texto]
            current_day_index = today.weekday()
            
            # Calcular cuántos días faltan para el próximo día deseado
            days_ahead = target_day_index - current_day_index
            if days_ahead <= 0: # Si ya pasó esta semana, buscar la próxima
                days_ahead += 7
                
            future_date = today + timedelta(days=days_ahead)
            fecha_str = f"{future_date.strftime('%Y-%m-%d')} {hora_texto}"
            return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")

        # 3. Si falla todo, devolvemos la fecha de hoy para que no explote el sistema
        print(f"Advertencia: No se pudo parsear la fecha '{dia_texto}', usando fecha actual.")
        return datetime.now()

    def iniciar(self) -> None:
        # --- CARGAR ADMINISTRADORES ---
        admins_data = self.__persistencia.cargarDatos("administradores.txt", ["nombre", "correo", "num_doc", "password_hash"])
        self.__administradores = []
        for admin in admins_data:
            obj_admin = Administrador(
                admin["nombre"], 
                admin["correo"], 
                admin["num_doc"], 
                admin["password_hash"], 
                es_hash=True
            )
            self.__administradores.append(obj_admin)

        # --- CARGAR CLIENTES ---
        clientes_data = self.__persistencia.cargarDatos("clientes.txt", ["nombre", "correo", "num_doc", "password_hash", "millas"])
        self.__clientes = []
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

        # --- CARGAR VUELOS ---
        vuelos_data = self.__persistencia.cargarDatos("vuelos.txt", ["id","origen","destino", "fechaDiaSalida", "fechaHoraSalida","asientosPref","asientosEco"])
        self.__vuelos = []
        
        for v in vuelos_data:
            try:
                # CORRECCIÓN DE FECHAS:
                # Intentamos parsear la fecha. Si viene como "LUNES", calculamos una fecha futura real.
                dia_str = v['fechaDiaSalida']
                hora_str = v['fechaHoraSalida']
                
                fecha_dt = self._obtener_fecha_desde_str(dia_str, hora_str)
                
                precio_eco = 235000.0
                precio_pref = 850000.0
                
                nuevo_vuelo = Vuelo(
                    codigo=v["id"],
                    origen=v["origen"],
                    destino=v["destino"],
                    fechaHoraSalida=fecha_dt,
                    asientosEco=int(v["asientosEco"]),
                    asientosPref=int(v["asientosPref"]),
                    precioBaseEco=precio_eco,
                    precioBasePref=precio_pref
                )
                self.__vuelos.append(nuevo_vuelo)
            except Exception as e:
                print(f"Error cargando vuelo {v.get('id')}: {e}")

        print(f"Sistema iniciado: {len(self.__vuelos)} vuelos, {len(self.__administradores)} admins, {len(self.__clientes)} clientes.")
    
    def guardar_datos_cierre(self) -> None:
        """
        Guarda Clientes, Admins y Vuelos desde la memoria a los archivos TXT.
        Se ejecuta en el finally de init.py
        """
        print("Guardando datos en disco...")

        # 1. Guardar Clientes
        lista_clientes = []
        for c in self.__clientes:
            lista_clientes.append({
                "nombre": c.getNombre(),
                "correo": c.getCorreo(),
                "num_doc": c.getNumDoc(),
                "password_hash": c.getPasswordHash(),
                "millas": c.getMillas()
            })
        self.__persistencia.guardarDatos("clientes.txt", lista_clientes)

        # 2. Guardar Administradores
        lista_admins = []
        for a in self.__administradores:
            lista_admins.append({
                "nombre": a.getNombre(),
                "correo": a.getCorreo(),
                "num_doc": a.getNumDoc(),
                "password_hash": a.getPasswordHash()
            })
        self.__persistencia.guardarDatos("administradores.txt", lista_admins)

        # 3. Guardar Vuelos (NUEVO)
        # Convertimos objetos Vuelo -> Diccionarios formato TXT
        lista_vuelos = []
        for v in self.__vuelos:
            # Separamos datetime en Dia y Hora
            dt = v.getFechaHoraSalida()
            dia_str = dt.strftime("%Y-%m-%d")
            hora_str = dt.strftime("%H:%M")
            
            lista_vuelos.append({
                "id": v.getCodigo(),
                "origen": v.getOrigen(),
                "destino": v.getDestino(),
                "fechaDiaSalida": dia_str,
                "fechaHoraSalida": hora_str,
                "asientosEco": v.getAsientosEco(),
                "asientosPref": v.getAsientosPref()
            })
        self.__persistencia.guardarDatos("vuelos.txt", lista_vuelos)
        # Aquí también podrías guardar vuelos o reservas si los mantuviste en memoria
    
    def admin_agregar_vuelo(self, datos: Dict) -> Dict:
        """Agrega un vuelo a la memoria."""
        if not self.__usuarioSesion or self.__usuarioSesion.getTipo() != "Admin":
            return {"success": False, "message": "No autorizado"}

        for v in self.__vuelos:
            if v.getCodigo() == datos["codigo"]:
                return {"success": False, "message": "El código ya existe."}

        try:
            fecha_str = f"{datos['dia']} {datos['hora']}"
            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
            
            nuevo = Vuelo(
                codigo=datos["codigo"],
                origen=datos["origen"],
                destino=datos["destino"],
                fechaHoraSalida=fecha_dt,
                asientosEco=int(datos["sillas_eco"]),
                asientosPref=int(datos["sillas_pref"]),
                precioBaseEco=235000.0,
                precioBasePref=850000.0
            )
            self.__vuelos.append(nuevo)
            return {"success": True, "message": "Vuelo creado exitosamente"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def admin_eliminar_vuelo(self, idVuelo: str) -> Dict:
        """Elimina un vuelo de la memoria."""
        if not self.__usuarioSesion or self.__usuarioSesion.getTipo() != "Admin":
            return {"success": False, "message": "No autorizado"}
            
        index_a_borrar = -1
        for i, v in enumerate(self.__vuelos):
            if v.getCodigo() == idVuelo:
                index_a_borrar = i
                break
        
        if index_a_borrar != -1:
            self.__vuelos.pop(index_a_borrar)
            return {"success": True, "message": "Vuelo eliminado"}
        
        return {"success": False, "message": "Vuelo no encontrado"}

    def admin_modificar_vuelo(self, idVuelo: str, datos: Dict) -> Dict:
        """Modifica un vuelo existente."""
        if not self.__usuarioSesion or self.__usuarioSesion.getTipo() != "Admin":
            return {"success": False, "message": "No autorizado"}

        vuelo_encontrado = next((v for v in self.__vuelos if v.getCodigo() == idVuelo), None)
        
        if not vuelo_encontrado:
            return {"success": False, "message": "Vuelo no encontrado"}

        try:
            # Actualizamos atributos usando name mangling (acceso a privados)
            # Idealmente Vuelo debería tener métodos setOrigen, etc.
            if "origen" in datos and datos["origen"]:
                vuelo_encontrado._Vuelo__origen = datos["origen"]
            if "destino" in datos and datos["destino"]:
                vuelo_encontrado._Vuelo__destino = datos["destino"]
            
            if "dia" in datos and "hora" in datos and datos["dia"] and datos["hora"]:
                nuevo_dt = datetime.strptime(f"{datos['dia']} {datos['hora']}", "%Y-%m-%d %H:%M")
                vuelo_encontrado._Vuelo__fechaHoraSalida = nuevo_dt

            if "sillas_eco" in datos and datos["sillas_eco"]:
                vuelo_encontrado._Vuelo__asientosEco = int(datos["sillas_eco"])
            if "sillas_pref" in datos and datos["sillas_pref"]:
                vuelo_encontrado._Vuelo__asientosPref = int(datos["sillas_pref"])

            return {"success": True, "message": "Vuelo modificado"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}

    def obtenerVuelosIniciales(self) -> List[Dict]:
        """
        Retorna la lista de vuelos convertida a diccionarios para el frontend.
        """
        resultado = []
        for v in self.__vuelos:
            resultado.append(self._vuelo_to_dict(v))
        return resultado

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
    
    def _vuelo_to_dict(self, v: Vuelo) -> Dict:
        """Helper para convertir objeto Vuelo a Dict para el frontend"""
        dt = v.getFechaHoraSalida()
        return {
            "id": v.getCodigo(),
            "origen": v.getOrigen(),
            "destino": v.getDestino(),
            "fechaDiaSalida": dt.strftime("%Y-%m-%d"),
            "fechaHoraSalida": dt.strftime("%H:%M"),
            "asientosEco": v.getAsientosEco(),
            "asientosPref": v.getAsientosPref()
        }


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

    def crearReserva(self, idVuelo: str, pasajerosData: List) -> Dict:
        pass

    def buscarReservaPorId(self, idReserva: str) -> Dict:
        # Nota: Asegúrate de tener cargadas las reservas en self.__reservas o leer el TXT aquí
        reservas = self.__persistencia.cargarDatos("reservas.txt", ["codigo_reserva", "codigo_vuelo", "num_doc", "tipo_asiento", "fecha_reserva"])
        
        # Filtramos las líneas que coinciden con el ID
        reserva_match = [r for r in reservas if r["codigo_reserva"] == idReserva]
        
        if not reserva_match:
            return {"success": False, "message": "Reserva no encontrada"}

        # Tomamos datos generales del primer pasajero/linea (asumiendo mismo vuelo para el grupo)
        first = reserva_match[0]
        
        # Necesitamos info del vuelo para mostrar origen/destino
        vuelo_info = next((v for v in self.__vuelos if v.getCodigo() == first["codigo_vuelo"]), None)
        
        # Construimos la lista de pasajeros
        pasajeros_list = []
        for r in reserva_match:
            # Buscar nombre del cliente (opcional, si tienes el num_doc)
            nombre_cliente = "Pasajero" # Default
            for c in self.__clientes:
                if c.getNumDoc() == r["num_doc"]:
                    nombre_cliente = c.getNombre()
                    break
            
            pasajeros_list.append({
                "num_doc": r["num_doc"],
                "nombre": nombre_cliente,
                "clase_asiento": r["tipo_asiento"] # 'ECO' o 'PREF'
            })

        data_response = {
            "codigo_reserva": idReserva,
            "vuelo": {
                "codigo": vuelo_info.getCodigo() if vuelo_info else "N/A",
                "origen": vuelo_info.getOrigen() if vuelo_info else "N/A",
                "destino": vuelo_info.getDestino() if vuelo_info else "N/A",
                "fecha": vuelo_info.getFechaHoraSalida().strftime("%Y-%m-%d") if vuelo_info else "",
                "hora": vuelo_info.getFechaHoraSalida().strftime("%H:%M") if vuelo_info else ""
            },
            "pasajeros": pasajeros_list
        }

        return {"success": True, "data": data_response}

    def realizarCheckIn(self, payload: Dict) -> Dict:
        id_reserva = payload.get("idReserva")
        pasajeros_data = payload.get("pasajeros") # Lista con cabina/bodega
        
        # 1. Validar Reserva
        # 2. Calcular costos finales (Python debe ser la autoridad del precio)
        # 3. Marcar reserva como "Check-In Completo" (en memoria o txt)
        
        # 4. Acumular Millas al titular (Buscar titular de esa reserva)
        # Nota: Aquí deberías buscar quién hizo la reserva originalmente.
        # Si no tienes guardado el titular en reserva.txt, asume el usuario logueado o el primer pasajero.
        
        if self.__usuarioSesion and isinstance(self.__usuarioSesion, Cliente):
            self.__usuarioSesion.acumularMillas(500)
            # Recordar: esto actualiza memoria, se guarda al cerrar ventana.
        
        return {"success": True, "millas_ganadas": 500}

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
    
    # --- MÉTODOS DE DATOS (DASHBOARD) ---

    def obtener_dashboard_stats(self) -> Dict:
        """Retorna estadísticas para las cards del dashboard."""
        tipo = self.__usuarioSesion.getTipo() if self.__usuarioSesion else "Cliente"
        
        stats = {
            "vuelos_activos": len(self.__vuelos),
            "destinos": len(set(v.getDestino() for v in self.__vuelos)),
            "reservas_count": 0, # Placeholder hasta implementar Reservas reales
            "millas": 0
        }

        if tipo == "Cliente" and isinstance(self.__usuarioSesion, Cliente):
            stats["millas"] = self.__usuarioSesion.getMillas()
            # Aquí filtrarías self.__reservas por el documento del cliente
            
        elif tipo == "Admin":
            # Admin ve total de reservas
            stats["reservas_count"] = len(self.__reservas) # Placeholder

        return stats

    def obtener_mis_reservas(self) -> List[Dict]:
        """
        Retorna la lista de reservas. 
        Si es Admin, retorna todas. Si es Cliente, solo las suyas.
        NOTA: Como la clase Reserva no está 100% implementada en el input,
        esto retornará una lista vacía o mock por ahora para que el front no falle.
        """
        if not self.__usuarioSesion:
            return []

        reservas_fmt = []
        # Lógica futura: iterar self.__reservas y convertir a dict
        # for r in self.__reservas: ...
        
        return reservas_fmt