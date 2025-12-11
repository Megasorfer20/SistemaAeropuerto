import random
import string
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
from clases.equipajes.EquipajeCabina import EquipajeCabina
from clases.equipajes.EquipajeBodega import EquipajeBodega

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
        # 1. CARGAR ADMINISTRADORES (Faltaba esto)
        admins_data = self.__persistencia.cargarDatos("administradores.txt", ["nombre", "correo", "num_doc", "password_hash"])
        self.__administradores = []
        for admin in admins_data:
            if admin.get("nombre"): # Validación simple para no cargar vacíos
                obj_admin = Administrador(
                    admin["nombre"], 
                    admin["correo"], 
                    admin["num_doc"], 
                    admin["password_hash"], 
                    es_hash=True
                )
                self.__administradores.append(obj_admin)

        # 2. CARGAR CLIENTES (Faltaba esto)
        clientes_data = self.__persistencia.cargarDatos("clientes.txt", ["nombre", "correo", "num_doc", "password_hash", "millas"])
        self.__clientes = []
        for cli in clientes_data:
            if cli.get("nombre"):
                try:
                    millas = int(cli.get("millas", 0) if cli.get("millas") else 0)
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

        # 3. CARGAR VUELOS
        # Aquí estaba el error principal: cargabas los datos pero no creabas los objetos
        vuelos_data = self.__persistencia.cargarDatos("vuelos.txt", [
            "id",
            "origen",
            "destino", 
            "fechaDiaSalida", 
            "fechaHoraSalida",
            "asientosPref",
            "asientosEco"
        ])
        
        self.__vuelos = [] # Reiniciar lista
        for v in vuelos_data:
            if v.get("id"): # Validar que tenga ID
                try:
                    # Parsear fecha
                    fecha_dt = self._obtener_fecha_desde_str(v["fechaDiaSalida"], v["fechaHoraSalida"])
                    
                    # Convertir strings a int (con fallback a 0 si falla)
                    sillas_eco = int(v["asientosEco"]) if v["asientosEco"] else 0
                    sillas_pref = int(v["asientosPref"]) if v["asientosPref"] else 0

                    nuevo_vuelo = Vuelo(
                        codigo=v["id"],
                        origen=v["origen"],
                        destino=v["destino"],
                        fechaHoraSalida=fecha_dt,
                        asientosEco=sillas_eco,
                        asientosPref=sillas_pref,
                        precioBaseEco=235000.0,
                        precioBasePref=850000.0
                    )
                    self.__vuelos.append(nuevo_vuelo)
                except Exception as e:
                    print(f"Error procesando vuelo {v.get('id')}: {e}")

        # 4. CARGAR RESERVAS
        reservas_data = self.__persistencia.cargarDatos("reservas.txt", ["codigo_reserva", "codigo_vuelo", "doc_titular", "fecha", "checkin", "pasajeros_raw"])
        self.__reservas = []
        
        for r_data in reservas_data:
            if not r_data.get("codigo_reserva"): continue
            
            try:
                vuelo_obj = next((v for v in self.__vuelos if v.getCodigo() == r_data["codigo_vuelo"]), None)
                titular_obj = next((c for c in self.__clientes if c.getNumDoc() == r_data["doc_titular"]), None)
                
                if vuelo_obj and titular_obj:
                    nueva_reserva = Reserva(
                        idReserva=r_data["codigo_reserva"],
                        titular=titular_obj,
                        vuelo=vuelo_obj,
                        fechaReserva=r_data["fecha"]
                    )
                    
                    if r_data.get("checkin") == "True":
                        nueva_reserva.setCheckInRealizado(True)
                    
                    raw_pax = r_data.get("pasajeros_raw", "")
                    if raw_pax:
                        lista_pax = raw_pax.split("|")
                        for p_str in lista_pax:
                            if p_str:
                                datos_p = p_str.split(";") 
                                if len(datos_p) >= 3:
                                    # Determinar tipo de asiento dummy para lógica de equipaje
                                    es_eco = (datos_p[2] == "ECO")
                                    # Precio 0 porque ya está reservado
                                    asiento_obj = AsientoEconomico("X",0,"X",False,0) if es_eco else AsientoPreferencial("X",0,"X",False,0)
                                    
                                    pax = Pasajero(datos_p[0], datos_p[1], "email@dummy.com", asiento_obj)
                                    nueva_reserva.getPasajeros().append(pax)

                    self.__reservas.append(nueva_reserva)
            except Exception as e:
                print(f"Error cargando reserva {r_data.get('codigo_reserva')}: {e}")
        
        print(f"SISTEMA INICIADO: {len(self.__administradores)} Admins, {len(self.__clientes)} Clientes, {len(self.__vuelos)} Vuelos.")

    def buscarReservaPorId(self, idReserva: str) -> Dict:
        # Buscar en memoria
        reserva: Reserva = next((r for r in self.__reservas if r.getId() == idReserva), None)
        
        if not reserva:
            return {"success": False, "message": "Reserva no encontrada."}
        
        if reserva.getCheckInRealizado():
             return {"success": False, "message": "El Check-In para esta reserva ya fue realizado."}

        vuelo = reserva.getVuelo()
        
        # Construir respuesta para el Frontend
        pasajeros_data = []
        for pax in reserva.getPasajeros():
            # Determinar tipo de asiento para reglas de equipaje
            # (Asumimos que Pasajero tiene un objeto Asiento o una forma de saberlo)
            # Aquí usamos un truco: miramos la clase del objeto asiento
            es_pref = isinstance(pax._Pasajero__asiento, AsientoPreferencial) # Acceso a atributo privado name mangling si es necesario o getter
            
            pasajeros_data.append({
                "nombre": pax._Pasajero__nombre, # Usar Getters en tu clase real
                "num_doc": pax._Pasajero__numDoc,
                "clase_asiento": "PREF" if es_pref else "ECO"
            })

        response = {
            "codigo_reserva": reserva.getId(),
            "vuelo": {
                "codigo": vuelo.getCodigo(),
                "origen": vuelo.getOrigen(),
                "destino": vuelo.getDestino(),
                "fecha": vuelo.getFechaHoraSalida().strftime("%Y-%m-%d"),
                "hora": vuelo.getFechaHoraSalida().strftime("%H:%M")
            },
            "pasajeros": pasajeros_data
        }
        
        return {"success": True, "data": response}

    def realizarCheckIn(self, payload: Dict) -> Dict:
        """
        Recibe payload del Vue con la configuración de maletas.
        Calcula costos finales, asigna millas y cierra el check-in.
        """
        id_reserva = payload.get("idReserva")
        pasajeros_config = payload.get("pasajeros") # Lista [{num_doc, maleta_cabina, maleta_bodega...}]

        reserva: Reserva = next((r for r in self.__reservas if r.getId() == id_reserva), None)
        if not reserva:
            return {"success": False, "message": "Reserva no encontrada"}

        total_costo_equipaje = 0.0

        # Procesar Equipaje y Costos
        for p_conf in pasajeros_config:
            doc = p_conf.get("num_doc")
            # Buscar el objeto pasajero en la reserva
            # (Simplificación: iteramos para encontrar coincidencia)
            pasajero_obj = next((p for p in reserva.getPasajeros() if p._Pasajero__numDoc == doc), None)
            
            if pasajero_obj:
                # Determinar clase
                es_pref = isinstance(pasajero_obj._Pasajero__asiento, AsientoPreferencial)
                clase_str = "PREF" if es_pref else "ECO"

                # 1. Maleta Cabina
                if p_conf.get("maleta_cabina"):
                    eq_cabina = EquipajeCabina(10, 0) # Peso estándar
                    total_costo_equipaje += eq_cabina.calcularCosto(clase_str)
                    pasajero_obj.agregarEquipaje(eq_cabina)

                # 2. Maleta Bodega
                bodega_data = p_conf.get("maleta_bodega")
                peso = float(bodega_data.get("peso", 0))
                vol = float(bodega_data.get("volumen", 0))

                if peso > 0:
                    eq_bodega = EquipajeBodega(peso, vol)
                    costo = eq_bodega.calcularCosto(clase_str)
                    
                    # REGLA: 1 incluida en Preferencial
                    # Si es PREF, asumimos que el usuario ingresó el peso TOTAL.
                    # El sistema podría descontar la primera maleta, o asumir que el input
                    # son maletas ADICIONALES.
                    # Dado el enunciado "maletas adicionales... tienen costo", asumiremos:
                    # Si es PREF y solo lleva 1, el frontend o usuario pone 0 costo.
                    # Para simplificar backend: Calculamos costo full según fórmula.
                    # Si quieres aplicar descuento: 
                    # if es_pref: costo = max(0, costo - costo_una_maleta_promedio)
                    
                    total_costo_equipaje += costo
                    pasajero_obj.agregarEquipaje(eq_bodega)

        # Actualizar estado de Reserva
        reserva.setCheckInRealizado(True)

        # REQUERIMIENTO 6: ACUMULAR MILLAS
        # Por cada reserva acumula 500 millas (al titular)
        titular = reserva.getTitular()
        if titular:
            titular.acumularMillas(500)
            print(f"Millas acumuladas para {titular.getNombre()}. Total: {titular.getMillas()}")

        return {
            "success": True, 
            "millas_ganadas": 500,
            "costo_equipaje": total_costo_equipaje
        }
                
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
            dt = v.getFechaHoraSalida()
            lista_vuelos.append({
                "id": v.getCodigo(),
                "origen": v.getOrigen(),
                "destino": v.getDestino(),
                "fechaDiaSalida": dt.strftime("%Y-%m-%d"),
                "fechaHoraSalida": dt.strftime("%H:%M"),
                # OJO AL ORDEN AQUÍ TAMBIÉN:
                "asientosPref": v.getAsientosPref(),
                "asientosEco": v.getAsientosEco()
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
        """
        Filtra los vuelos (Objetos) y retorna diccionarios.
        """
        resultado = []
        
        # Obtener filtros y limpiar strings
        id_b = filtros.get("id", "").strip()
        origen_b = filtros.get("origen", "").lower().strip()
        destino_b = filtros.get("destino", "").lower().strip()
        dia_b = filtros.get("dia", "").upper().strip() 
        hora_inicio_str = filtros.get("horaInicio", "")
        hora_fin_str = filtros.get("horaFin", "")

        # Mapeo de números de día (datetime.weekday()) a nombres en español
        dias_semana_map = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]

        for v in self.__vuelos:
            # v es un OBJETO Vuelo, usamos getters
            
            # 1. Filtro ID
            if id_b and v.getCodigo() != id_b:
                continue

            # 2. Filtro Origen
            if origen_b and origen_b not in v.getOrigen().lower():
                continue
            
            # 3. Filtro Destino
            if destino_b and destino_b not in v.getDestino().lower():
                continue

            # Obtenemos el objeto datetime del vuelo una sola vez
            dt_vuelo = v.getFechaHoraSalida()

            # 4. Filtro Día
            if dia_b and dia_b != "TODOS":
                # Convertimos el día del vuelo (0-6) a texto (LUNES-DOMINGO)
                dia_vuelo_str = dias_semana_map[dt_vuelo.weekday()]
                
                # Manejo especial para tildes si es necesario o comparaciones directas
                if dia_b == "MIERCOLES" and dia_vuelo_str == "MIÉRCOLES": pass # Ajuste opcional
                elif dia_b != dia_vuelo_str:
                    continue

            # 5. Filtro Rango Horario
            try:
                if hora_inicio_str or hora_fin_str:
                    hora_vuelo = dt_vuelo.time()
                    
                    if hora_inicio_str:
                        hora_min = datetime.strptime(hora_inicio_str, "%H:%M").time()
                        if hora_vuelo < hora_min:
                            continue
                    
                    if hora_fin_str:
                        hora_max = datetime.strptime(hora_fin_str, "%H:%M").time()
                        if hora_vuelo > hora_max:
                            continue
            except ValueError:
                print(f"Error comparando horas para vuelo {v.getCodigo()}")
                continue

            # SI PASA TODOS LOS FILTROS:
            # Convertimos el objeto Vuelo a diccionario para enviarlo al Frontend
            resultado.append(self._vuelo_to_dict(v))
        
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
                            "correo": admin.getCorreo(),   # AGREGADO
                            "doc": admin.getNumDoc(),      # AGREGADO
                            "tipo_usuario": "Admin"
                        }
                    }

        # 2. Buscar en Clientes
        for cliente in self.__clientes:
            if cliente.getNumDoc() == doc:
                if cliente.verificarPassword(password):
                    self.__usuarioSesion = cliente
                    return {
                        "success": True, 
                        "user": {
                            "nombre": cliente.getNombre(),
                            "correo": cliente.getCorreo(), # AGREGADO
                            "doc": cliente.getNumDoc(),    # AGREGADO
                            "tipo_usuario": "Cliente",
                            "millas": cliente.getMillas()
                        }
                    }
        
        return {"success": False, "message": "Credenciales inválidas."}
    
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

    def crearReserva(self, payload: Dict) -> Dict:
        """
        Crea una reserva real en memoria.
        Recibe: { "vuelo_id": "...", "asientos": [...], "pasajeros": [...] }
        """
        try:
            vuelo_id = payload.get("vuelo_id")
            pasajeros_data = payload.get("pasajeros") # Lista con datos de personas
            asientos_data = payload.get("asientos")   # Lista con info de asientos

            # 1. Buscar Vuelo
            vuelo = next((v for v in self.__vuelos if v.getCodigo() == vuelo_id), None)
            if not vuelo:
                return {"success": False, "message": "Vuelo no encontrado"}

            # 2. Identificar Titular (Usamos el usuario logueado o el primer pasajero)
            titular = self.__usuarioSesion
            if not titular or not isinstance(titular, Cliente):
                # Si no hay sesión o es admin, intentamos buscar si el primer pasajero ya es cliente
                doc_primer_pax = pasajeros_data[0]["documento"]
                titular = next((c for c in self.__clientes if c.getNumDoc() == doc_primer_pax), None)
                
                # Si aun así no existe, creamos un cliente "fantasma" temporal para que no falle el sistema
                if not titular:
                    titular = Cliente(pasajeros_data[0]["nombre"], pasajeros_data[0]["email"], pasajeros_data[0]["documento"], "temp123", 0, False)
                    self.__clientes.append(titular) # Lo agregamos para que persista

            # 3. Generar Código Reserva (6 caracteres alfanuméricos)
            codigo_res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            fecha_actual = datetime.now().strftime("%Y-%m-%d")

            # 4. Crear la Reserva
            nueva_reserva = Reserva(codigo_res, titular, vuelo, fecha_actual)

            # 5. Crear y Asignar Pasajeros
            for i, p_data in enumerate(pasajeros_data):
                # Determinar asiento correspondiente
                info_asiento = asientos_data[i]
                es_vip = (info_asiento["tipo"] == "vip")
                
                # Crear objeto Asiento (Simulado para cumplir con la clase Pasajero)
                # Precio 0 aquí porque ya se calculó en el front, solo nos importa el tipo
                if es_vip:
                    asiento_obj = AsientoPreferencial(info_asiento["id"], 0, "A", True, 0)
                else:
                    asiento_obj = AsientoEconomico(info_asiento["id"], 0, "A", True, 0)
                
                nuevo_pasajero = Pasajero(
                    p_data["nombre"],
                    p_data["documento"],
                    p_data["email"],
                    asiento_obj
                )
                
                # Guardamos el pasajero dentro de la reserva
                nueva_reserva.getPasajeros().append(nuevo_pasajero)

            # 6. Guardar en la lista maestra de la API
            self.__reservas.append(nueva_reserva)
            print(f"Reserva creada exitosamente: {codigo_res} con {len(pasajeros_data)} pasajeros.")

            return {
                "success": True, 
                "codigo": codigo_res, 
                "message": "Reserva creada exitosamente"
            }

        except Exception as e:
            print(f"Error creando reserva: {e}")
            return {"success": False, "message": f"Error interno: {str(e)}"}

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
    
    def obtener_sillas_ocupadas(self, id_vuelo: str) -> List[str]:
        sillas_ocupadas = []
        # Recorremos todas las reservas en memoria
        for reserva in self.__reservas:
            # Si la reserva es de este vuelo
            if reserva.get("codigo_vuelo") == id_vuelo:
                # reserva["asientos"] debe ser una lista de IDs de asientos (ej: ["A1", "B1"])
                sillas_ocupadas.extend(reserva.get("asientos", []))
        return sillas_ocupadas

    def crearReserva(self, datos: Dict) -> Dict:
        """
        Recibe: { idVuelo, pasajeros: [], asientos: [], total: float, titular_doc: str }
        """
        import random
        import string

        try:
            # Generar código de reserva único
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            # Crear estructura de reserva (Diccionario simple para este ejercicio)
            nueva_reserva = {
                "codigo_reserva": codigo,
                "codigo_vuelo": datos["idVuelo"],
                "documento_cliente": datos.get("titular_doc"), # Doc del usuario logueado
                "asientos": [a["id"] for a in datos["asientos"]], # Guardamos solo IDs ["1A", "1B"]
                "detalles_asientos": datos["asientos"], # Guardamos detalle completo si quieres
                "pasajeros": datos["pasajeros"],
                "total": datos["total"],
                "fecha_reserva": datetime.now().strftime("%Y-%m-%d")
            }

            # Guardar en memoria
            self.__reservas.append(nueva_reserva)
            
            # (Opcional) Aquí deberías llamar a self.__persistencia.guardarDatos("reservas.txt", ...) 
            # si quieres persistencia inmediata, pero con tenerlo en memoria basta para que el flujo funcione.

            return {"success": True, "codigo": codigo}
        except Exception as e:
            print(f"Error creando reserva: {e}")
            return {"success": False, "message": str(e)}