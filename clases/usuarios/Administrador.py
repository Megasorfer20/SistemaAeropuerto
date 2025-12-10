from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from clases.usuarios.Usuario import Usuario
from clases.vuelos.Vuelo import Vuelo

class Administrador(Usuario):
    def __init__(self, nombre: str, correo: str, numDoc: str, passwordHash: str):
        super().__init__(nombre, correo, numDoc, passwordHash)
        self.__gestor = GestorTxt("database")
        self.__keys_vuelos = ["codigo", "origen", "destino", "dia", "hora", "sillas_pref", "sillas_eco"]
        

    def modificarVuelo(self, idVuelo: str, data: Dict) -> bool:
        vuelos = self.__gestor.cargarDatos("vuelos.txt", self.__keys_vuelos)

        vuelo_encontrado = False
        for vuelo in vuelos:
            if vuelo["codigo"] == idVuelo:
                vuelo.update(data)
                vuelo_encontrado = True
                break
        
        if vuelo_encontrado:
            return self.__gestor.guardarDatos("vuelos.txt", vuelos, vuelos)
        return False

    def agregarVuelo(self, vuelo: 'Vuelo') -> bool:
        vuelos = self.__gestor.cargarDatos("vuelos.txt", self.__keys_vuelos)

        for v in vuelos:
            if v["codigo"] == vuelo.getCodigo():
                print(f"El vuelo con código {vuelo.getCodigo()} ya existe.")
                return False  
        
        nuevo_vuelo = {
            "codigo": vuelo.getCodigo(),
            "origen": vuelo.getOrigen(),
            "destino": vuelo.getDestino(),
            "dia": vuelo.getDia().strftime("%Y-%m-%d"),
            "hora": vuelo.getHora().strftime("%H:%M"),
            "sillas_pref": vuelo.getSillasPreferencial(),
            "sillas_eco": vuelo.getSillasEconomica()
        }

        vuelos.append(nuevo_vuelo)
        return self.__gestor.guardarDatos("vuelos.txt", vuelos, vuelos)
    

    def verSillasVendidas(self, filtro: Dict) -> Dict:
            keys_reservas = ["codigo_reserva", "codigo_vuelo", "documento_cliente", "tipo_asiento", "asientos_seleccionados", "fecha_reserva"]
            reservas = self.__gestor.cargarDatos("reservas.txt", keys_reservas)

            conteo_ventas = {}

            for reserva in reservas:
                id_vuelo = reserva["codigo_vuelo"]

                if filtro and "codigo_vuelo" in filtro and filtro["codigo_vuelo"] != id_vuelo:
                        continue
                
                if id_vuelo in conteo_ventas:
                     conteo_ventas[id_vuelo] += 1
                else:
                     conteo_ventas[id_vuelo] = 1
            return conteo_ventas

    def verDatosPasajeros(self, idVuelo: str) -> List[Any]:
        pass

    def getTipo(self) -> str:
        return "Admin"