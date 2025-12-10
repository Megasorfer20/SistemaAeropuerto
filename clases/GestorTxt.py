import os
from typing import List, Dict, Any
from clases.IPersistencia import IPersistencia

class GestorTxtGestorTxt(IPersistencia): 
    def __init__(self, rutaBase: str = "database"):
        self.__rutaBase = rutaBase

    def cargarDatos(self, nombre_archivo: str, keys: List[str]) -> List[Dict[str, Any]]:
        ruta_completa = self._construirRuta(nombre_archivo)
        resultados = []

        if not os.path.exists(ruta_completa):
            return []

        try:
            with open(ruta_completa, "r", encoding="utf-8") as archivo:
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
            ruta_carpeta = os.path.join(os.getcwd(), self.__rutaBase)
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)

            lineas_formateadas = self._formatearDatos(datos)
            
            with open(ruta_completa, "w", encoding="utf-8") as archivo:
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
        return os.path.join(os.getcwd(), self.__rutaBase, nombre_archivo)