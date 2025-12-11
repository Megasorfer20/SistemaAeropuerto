import random
import string
import webview
import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta

# Imports de clases
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
        self.__clientes: List[Cliente] = []
        self.__administradores: List[Administrador] = []
        self.__reservas: List[Reserva] = []
        self.__persistencia: Optional[IPersistencia] = GestorTxt()
        
    def _obtener_fecha_desde_str(self, dia_texto: str, hora_texto: str) -> datetime:
        dia_texto = dia_texto.upper().strip()
        try:
            return datetime.strptime(f"{dia_texto} {hora_texto}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass 

        dias_semana = {
            "LUNES": 0, "MARTES": 1, "MIERCOLES": 2, "MIÉRCOLES": 2, 
            "JUEVES": 3, "VIERNES": 4, "SABADO": 5, "SÁBADO": 5, "DOMINGO": 6
        }
        
        if dia_texto in dias_semana:
            today = datetime.now()
            target_day_index = dias_semana[dia_texto]
            current_day_index = today.weekday()
            days_ahead = target_day_index - current_day_index
            if days_ahead <= 0: days_ahead += 7
            future_date = today + timedelta(days=days_ahead)
            fecha_str = f"{future_date.strftime('%Y-%m-%d')} {hora_texto}"
            return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")

        return datetime.now()

    def iniciar(self) -> None:
        # 1. CARGAR ADMINISTRADORES
        admins_data = self.__persistencia.cargarDatos("administradores.txt", ["nombre", "correo", "num_doc", "password_hash"])
        self.__administradores = []
        for admin in admins_data:
            if admin.get("nombre"):
                obj_admin = Administrador(admin["nombre"], admin["correo"], admin["num_doc"], admin["password_hash"], es_hash=True)
                self.__administradores.append(obj_admin)

        # 2. CARGAR CLIENTES
        clientes_data = self.__persistencia.cargarDatos("clientes.txt", ["nombre", "correo", "num_doc", "password_hash", "millas"])
        self.__clientes = []
        for cli in clientes_data:
            if cli.get("nombre"):
                try:
                    millas = int(cli.get("millas", 0) if cli.get("millas") else 0)
                except:
                    millas = 0
                obj_cliente = Cliente(cli["nombre"], cli["correo"], cli["num_doc"], cli["password_hash"], miles=millas, es_hash=True)
                self.__clientes.append(obj_cliente)

        # 3. CARGAR VUELOS
        vuelos_data = self.__persistencia.cargarDatos("vuelos.txt", ["id","origen","destino", "fechaDiaSalida", "fechaHoraSalida","asientosPref","asientosEco"])
        self.__vuelos = []
        for v in vuelos_data:
            if v.get("id"):
                try:
                    fecha_dt = self._obtener_fecha_desde_str(v["fechaDiaSalida"], v["fechaHoraSalida"])
                    sillas_eco = int(v["asientosEco"]) if v["asientosEco"] else 0
                    sillas_pref = int(v["asientosPref"]) if v["asientosPref"] else 0
                    nuevo_vuelo = Vuelo(v["id"], v["origen"], v["destino"], fecha_dt, sillas_eco, sillas_pref, 235000.0, 850000.0)
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
                    nueva_reserva = Reserva(r_data["codigo_reserva"], titular_obj, vuelo_obj, r_data["fecha"])
                    if r_data.get("checkin") == "True":
                        nueva_reserva.setCheckInRealizado(True)
                    
                    raw_pax = r_data.get("pasajeros_raw", "")
                    if raw_pax:
                        lista_pax = raw_pax.split("|")
                        for p_str in lista_pax:
                            if p_str:
                                datos_p = p_str.split(";") 
                                if len(datos_p) >= 3:
                                    es_eco = (datos_p[2] == "ECO")
                                    asiento_obj = AsientoEconomico("X",0,"X",False,0) if es_eco else AsientoPreferencial("X",0,"X",False,0)
                                    pax = Pasajero(datos_p[0], datos_p[1], "email@dummy.com", asiento_obj)
                                    nueva_reserva.getPasajeros().append(pax)
                    self.__reservas.append(nueva_reserva)
            except Exception as e:
                print(f"Error cargando reserva {r_data.get('codigo_reserva')}: {e}")
        
        print(f"SISTEMA INICIADO: {len(self.__administradores)} Admins, {len(self.__clientes)} Clientes, {len(self.__vuelos)} Vuelos, {len(self.__reservas)} Reservas.")

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
        Requerimientos 6 y 7:
        - Acumular millas (500 por reserva).
        - Calcular costos de equipaje (Reglas de Cabina y Bodega).
        - Finalizar Check-In.
        """
        try:
            id_reserva = payload.get("idReserva")
            pasajeros_config = payload.get("pasajeros") # Lista que viene del Vue

            # 1. Buscar la reserva en memoria
            reserva: Reserva = next((r for r in self.__reservas if r.getId() == id_reserva), None)
            
            if not reserva:
                return {"success": False, "message": "Reserva no encontrada"}
            
            if reserva.getCheckInRealizado():
                return {"success": False, "message": "El Check-In ya fue realizado anteriormente."}

            total_costo_equipaje = 0.0

            # 2. Procesar cada pasajero y sus maletas
            for p_conf in pasajeros_config:
                doc_pasajero = p_conf.get("num_doc")
                
                # Buscar el objeto Pasajero dentro de la Reserva
                # (Accedemos a los atributos protegidos del objeto Pasajero)
                pasajero_obj = next((p for p in reserva.getPasajeros() if p._Pasajero__numDoc == doc_pasajero), None)
                
                if pasajero_obj:
                    # Determinar la clase del vuelo basada en el asiento del pasajero
                    asiento = pasajero_obj._Pasajero__asiento
                    es_preferencial = isinstance(asiento, AsientoPreferencial)
                    clase_str = "PREF" if es_preferencial else "ECO"

                    # --- A. EQUIPAJE CABINA (Req 7) ---
                    if p_conf.get("maleta_cabina"):
                        eq_cabina = EquipajeCabina(10, 0) # Peso estándar 10kg
                        costo_cabina = eq_cabina.calcularCosto(clase_str)
                        total_costo_equipaje += costo_cabina
                        
                        # Guardar en el objeto pasajero
                        pasajero_obj.agregarEquipaje(eq_cabina)

                    # --- B. EQUIPAJE BODEGA (Req 7) ---
                    bodega_data = p_conf.get("maleta_bodega")
                    peso = float(bodega_data.get("peso", 0))
                    vol = float(bodega_data.get("volumen", 0))

                    if peso > 0:
                        eq_bodega = EquipajeBodega(peso, vol)
                        costo_bodega = eq_bodega.calcularCosto(clase_str)
                        
                        # Regla: 1 maleta incluida para Preferencial
                        # Verificamos si ya tiene equipaje de bodega agregado en este proceso
                        # Para simplificar: Asumimos que el input trae 1 maleta de bodega por persona.
                        # Si es PREF, esta primera maleta sale gratis.
                        if es_preferencial:
                            costo_bodega = 0.0 
                            # Si permitieras agregar multiples maletas de bodega por persona, 
                            # aquí deberías usar un contador. Pero el form actual permite 1.
                        
                        total_costo_equipaje += costo_bodega
                        pasajero_obj.agregarEquipaje(eq_bodega)

            # 3. Finalizar Check-In
            reserva.setCheckInRealizado(True)

            # 4. Acumular Millas (Req 6: 500 millas por reserva)
            titular = reserva.getTitular()
            millas_ganadas = 500
            
            if titular and isinstance(titular, Cliente):
                titular.acumularMillas(millas_ganadas)
            
            # (El guardado en TXT se hace automático al cerrar la ventana gracias al init.py)

            return {
                "success": True, 
                "millas_ganadas": millas_ganadas,
                "costo_equipaje": total_costo_equipaje,
                "mensaje": f"Check-In Exitoso. Costo extra equipaje: ${total_costo_equipaje:,.0f}"
            }

        except Exception as e:
            print(f"Error en Check-In: {e}")
            return {"success": False, "message": f"Error interno: {str(e)}"}
                
    def guardar_datos_cierre(self) -> None:
        """
        Guarda todo en los TXT al cerrar el programa.
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

        # 3. Guardar Vuelos
        lista_vuelos = []
        for v in self.__vuelos:
            dt = v.getFechaHoraSalida()
            lista_vuelos.append({
                "id": v.getCodigo(),
                "origen": v.getOrigen(),
                "destino": v.getDestino(),
                "fechaDiaSalida": dt.strftime("%Y-%m-%d"),
                "fechaHoraSalida": dt.strftime("%H:%M"),
                "asientosPref": v.getAsientosPref(),
                "asientosEco": v.getAsientosEco()
            })
        self.__persistencia.guardarDatos("vuelos.txt", lista_vuelos)

        # 4. GUARDAR RESERVAS (NUEVO REQUERIMIENTO)
        lista_reservas_txt = []
        for r in self.__reservas:
            # Formatear pasajeros como string: Nombre;Doc;Tipo|Nombre;Doc;Tipo
            pax_strings = []
            for p in r.getPasajeros():
                # Acceso a atributos privados usando name mangling
                nombre = p._Pasajero__nombre
                doc = p._Pasajero__numDoc
                # Determinar tipo asiento
                asiento = p._Pasajero__asiento
                tipo = "VIP" if isinstance(asiento, AsientoPreferencial) else "ECO"
                pax_strings.append(f"{nombre};{doc};{tipo}")
            
            pax_raw = "|".join(pax_strings)

            lista_reservas_txt.append({
                "codigo_reserva": r.getId(),
                "codigo_vuelo": r.getVuelo().getCodigo(),
                "doc_titular": r.getTitular().getNumDoc(),
                "fecha": r.getFechaReserva(),
                "checkin": str(r.getCheckInRealizado()),
                "pasajeros_raw": pax_raw
            })
        
        self.__persistencia.guardarDatos("reservas.txt", lista_reservas_txt)
        print("Datos guardados correctamente.")

    # --- LÓGICA DE NEGOCIO ---

    def crearReserva(self, payload: Dict) -> Dict:
        """
        Crea una reserva en MEMORIA (Lista self.__reservas).
        NO guarda en TXT inmediatamente.
        """
        try:
            # Usamos .get() para evitar KeyErrors
            vuelo_id = payload.get("vuelo_id")
            pasajeros_data = payload.get("pasajeros") 
            asientos_data = payload.get("asientos")
            titular_doc = payload.get("titular_doc")

            if not vuelo_id:
                return {"success": False, "message": "Falta el ID del vuelo."}

            # 1. Buscar Vuelo
            vuelo = next((v for v in self.__vuelos if v.getCodigo() == vuelo_id), None)
            if not vuelo:
                return {"success": False, "message": "Vuelo no encontrado"}

            # 2. Identificar Titular
            titular = next((c for c in self.__clientes if c.getNumDoc() == titular_doc), None)
            
            # Si no existe, lo creamos temporalmente para que la reserva tenga un objeto Cliente válido
            if not titular:
                # Usamos los datos del primer pasajero
                p1 = pasajeros_data[0]
                titular = Cliente(p1["nombre"], p1["email"], p1["documento"], "temp123", 0, False)
                self.__clientes.append(titular) # Agregamos a memoria para persistencia

            # 3. Generar Código
            codigo_res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            fecha_actual = datetime.now().strftime("%Y-%m-%d")

            # 4. Crear Objeto Reserva
            nueva_reserva = Reserva(codigo_res, titular, vuelo, fecha_actual)

            # 5. Crear y Asignar Pasajeros
            for i, p_data in enumerate(pasajeros_data):
                info_asiento = asientos_data[i]
                es_vip = (info_asiento["tipo"] == "vip")
                
                # Objetos asiento dummy para almacenar el tipo
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
                nueva_reserva.getPasajeros().append(nuevo_pasajero)

            # 6. Guardar SOLO en Memoria
            self.__reservas.append(nueva_reserva)
            print(f"Reserva creada en memoria: {codigo_res}")

            return {
                "success": True, 
                "codigo": codigo_res, 
                "message": "Reserva creada exitosamente"
            }

        except Exception as e:
            print(f"Error creando reserva: {e}")
            return {"success": False, "message": f"Error interno: {str(e)}"}

    # ... (El resto de métodos como login, registro, buscarVuelos, obtener_sillas_ocupadas se mantienen igual que en la versión anterior)
    
    def obtener_sillas_ocupadas(self, id_vuelo: str) -> List[str]:
        sillas_ocupadas = []
        for reserva in self.__reservas:
            if reserva.getVuelo().getCodigo() == id_vuelo:
                for pax in reserva.getPasajeros():
                    # Obtenemos el ID del asiento (está dentro del objeto Asiento privado)
                    asiento = pax._Pasajero__asiento
                    sillas_ocupadas.append(asiento._id)
        return sillas_ocupadas

    def login(self, doc: str, password: str) -> Dict:
        for admin in self.__administradores:
            if admin.getNumDoc() == doc and admin.verificarPassword(password):
                self.__usuarioSesion = admin
                return {"success": True, "user": {"nombre": admin.getNombre(), "correo": admin.getCorreo(), "doc": admin.getNumDoc(), "tipo_usuario": "Admin"}}

        for cliente in self.__clientes:
            if cliente.getNumDoc() == doc and cliente.verificarPassword(password):
                self.__usuarioSesion = cliente
                return {"success": True, "user": {"nombre": cliente.getNombre(), "correo": cliente.getCorreo(), "doc": cliente.getNumDoc(), "tipo_usuario": "Cliente", "millas": cliente.getMillas()}}
        
        return {"success": False, "message": "Credenciales inválidas."}

    def registro(self, datos: Dict) -> Dict:
        for admin in self.__administradores:
            if admin.getNumDoc() == datos["numDoc"]: return {"success": False, "message": "Documento ya registrado."}
        for cli in self.__clientes:
            if cli.getNumDoc() == datos["numDoc"]: return {"success": False, "message": "Documento ya registrado."}

        nuevo_cliente = Cliente(datos["nombre"], datos["correo"], datos["numDoc"], datos["password"], miles=0, es_hash=False)
        self.__clientes.append(nuevo_cliente)
        return {"success": True, "message": "Registro exitoso"}

    def buscarVuelos(self, filtros: Dict) -> List[Dict]:
        resultado = []
        id_b = filtros.get("id", "").strip()
        origen_b = filtros.get("origen", "").lower().strip()
        destino_b = filtros.get("destino", "").lower().strip()
        dia_b = filtros.get("dia", "").upper().strip() 
        hora_inicio_str = filtros.get("horaInicio", "")
        hora_fin_str = filtros.get("horaFin", "")
        dias_semana_map = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]

        for v in self.__vuelos:
            if id_b and v.getCodigo() != id_b: continue
            if origen_b and origen_b not in v.getOrigen().lower(): continue
            if destino_b and destino_b not in v.getDestino().lower(): continue
            dt_vuelo = v.getFechaHoraSalida()
            if dia_b and dia_b != "TODOS":
                dia_vuelo_str = dias_semana_map[dt_vuelo.weekday()]
                if dia_b == "MIERCOLES" and dia_vuelo_str == "MIÉRCOLES": pass
                elif dia_b != dia_vuelo_str: continue
            try:
                if hora_inicio_str or hora_fin_str:
                    hora_vuelo = dt_vuelo.time()
                    if hora_inicio_str:
                        if hora_vuelo < datetime.strptime(hora_inicio_str, "%H:%M").time(): continue
                    if hora_fin_str:
                        if hora_vuelo > datetime.strptime(hora_fin_str, "%H:%M").time(): continue
            except ValueError: continue
            resultado.append(self._vuelo_to_dict(v))
        return resultado

    def obtenerVuelosIniciales(self) -> List[Dict]:
        return [self._vuelo_to_dict(v) for v in self.__vuelos]
    
    def _vuelo_to_dict(self, v: Vuelo) -> Dict:
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
    
    def obtener_dashboard_stats(self) -> Dict:
        return {"vuelos_activos": len(self.__vuelos), "destinos": len(set(v.getDestino() for v in self.__vuelos)), "reservas_count": len(self.__reservas), "millas": self.__usuarioSesion.getMillas() if isinstance(self.__usuarioSesion, Cliente) else 0}

    def obtener_mis_reservas(self) -> List[Dict]:
        return [] # Implementar si se requiere listado
    
    def admin_eliminar_vuelo(self, idVuelo: str) -> Dict:
        # Implementación simplificada
        self.__vuelos = [v for v in self.__vuelos if v.getCodigo() != idVuelo]
        return {"success": True}
    
    def admin_modificar_vuelo(self, idVuelo: str, datos: Dict) -> Dict:
        v = next((v for v in self.__vuelos if v.getCodigo() == idVuelo), None)
        if v:
            # Lógica de actualización (simplificada)
            return {"success": True}
        return {"success": False}