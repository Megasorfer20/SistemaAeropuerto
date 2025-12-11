import os
from typing import List, Dict, Any
from clases.IPersistencia import IPersistencia

class GestorTxt(IPersistencia): # Corregido el nombre duplicado de la clase
    def __init__(self, rutaBase: str = "database"):
        self.__rutaBase = rutaBase

    def cargarDatos(self, nombre_archivo: str, keys: List[str]) -> List[Dict[str, Any]]:
        # Ahora _construirRuta se encarga de ponerle el .txt si falta
        ruta_completa = self._construirRuta(nombre_archivo)
        resultados = []

        if not os.path.exists(ruta_completa):
            return []

        try:
            with open(ruta_completa, "r", encoding="utf-8-sig") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea:
                        diccionario = self._parsearLinea(linea, keys)
                        if diccionario:
                            resultados.append(diccionario)
            return resultados
        except Exception as e:
            print(f"Error al cargar datos de {ruta_completa}: {e}")
            return []

    def guardarDatos(self, nombre_archivo: str, datos: List[Dict[str, Any]]) -> bool:
        try:
            # Usamos el mismo helper para obtener la ruta con .txt
            ruta_completa = self._construirRuta(nombre_archivo)
            
            # Obtenemos la carpeta a partir de la ruta completa para crearla si no existe
            ruta_carpeta = os.path.dirname(ruta_completa)

            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)

            lineas_formateadas = self._formatearDatos(datos)
            
            with open(ruta_completa, "w", encoding="utf-8-sig") as archivo:
                contenido = "\n".join(lineas_formateadas)
                archivo.write(contenido)
                archivo.write("\n") 

            print(f"Guardado exitosamente en: {ruta_completa}")
            return True
        except Exception as e:
            print(f"Error al guardar datos en {ruta_completa}: {e}")
            return False

    def _parsearLinea(self, linea: str, keys: List[str]) -> Dict[str, Any]:
        valores = linea.split(",")
        
        # Validación para evitar errores si hay desajuste
        if len(valores) != len(keys):
            # Podrías lanzar error o intentar arreglarlo. 
            # Aquí simplemente retornamos lo que se pueda o un dict vacío.
            print(f"Advertencia: La línea '{linea}' no coincide con las keys proporcionadas.")
            # Opcional: Rellenar con None si faltan datos, o recortar si sobran
            # return dict(zip(keys, valores)) 
        
        return dict(zip(keys, valores))

    def _formatearDatos(self, datos: List[Dict[str, Any]]) -> List[str]:
        formatted_data = []
        for dato in datos:
            valores = [str(value) for value in dato.values()]
            linea_csv = ",".join(valores)
            formatted_data.append(linea_csv)
        return formatted_data

    def _construirRuta(self, nombre_archivo: str) -> str:
        if not nombre_archivo.endswith(".txt"):
            nombre_archivo += ".txt"
            
        return os.path.join(os.getcwd(), self.__rutaBase, nombre_archivo)