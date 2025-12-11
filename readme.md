
---

# Sistema de Gestión de Reservas de Aerolínea (Backend API)

## 1. Descripción del Proyecto

Este sistema es una solución de backend en Python diseñada bajo los principios de **Programación Orientada a Objetos (POO)**. Su función principal es gestionar la lógica de negocio de una aerolínea (usuarios, vuelos, reservas, check-in, equipaje y fidelización) y exponer estos servicios a través de una **Clase Fachada (Facade)** llamada `API_Sistema`.

El sistema está diseñado para funcionar con una interfaz gráfica desacoplada (HTML/JS vía `pywebview`). El backend **no genera HTML**; recibe datos, procesa lógica compleja y retorna estructuras de datos (JSON/Diccionarios) listas para ser renderizadas por el Frontend.

---

## 2. Arquitectura del Software

El sistema sigue una arquitectura por capas simplificada para aplicaciones de escritorio:

1.  **Capa de Presentación (Frontend):** HTML/Vue.js (Fuera del alcance de este documento, solo consume la API).
2.  **Capa de Control (Facade):** Clase `API_Sistema`. Es el único punto de entrada.
3.  **Capa de Dominio (Modelos):** Clases que contienen la lógica de negocio (`Vuelo`, `Reserva`, `Usuario`, etc.).
4.  **Capa de Persistencia:** Manejo de archivos `.txt` a través de interfaces.

### Principios POO Aplicados

- **Encapsulamiento:** Uso de atributos protegidos (`#`) y privados (`-`) con métodos públicos (`+`) para el acceso.
- **Abstracción:** Clases base como `Usuario`, `Asiento` y `Equipaje` definen comportamientos genéricos.
- **Herencia:** Especialización de clases (ej. `Cliente` hereda de `Usuario`).
- **Polimorfismo:** Métodos como `calcularPrecio()` o `calcularCosto()` se comportan diferente según la clase hija.
- **Interfaces:** `IPersistencia` para desacoplar el almacenamiento.

---

## 3. Diccionario de Clases y Guía de Implementación

A continuación se detalla cómo debe programarse cada clase según el diagrama UML.

### 3.1. Persistencia (Data Layer)

#### `<<Interface>> IPersistencia`

Define el contrato obligatorio para cualquier mecanismo de guardado.

- **Métodos:**
  - `cargarDatos(ruta)`: Debe retornar una lista de objetos.
  - `guardarDatos(ruta, datos)`: Recibe una lista y sobrescribe el archivo.

#### `GestorTxt` (Implementa IPersistencia)

Clase concreta que maneja la lectura/escritura en archivos planos (`.txt` o `.csv`).

- **Detalle Técnico:** Usar la librería `csv` de Python.
- **Formatos de Archivo:**
  - _usuarios.txt:_ `tipo,nombre,doc,correo,password_hash,millas`
  - _vuelos.txt:_ `CODIGO,ORIGEN,DESTINO,DIA,HORA,CANT_PREF,CANT_ECO`
  - _reservas.txt:_ `id_reserva,doc_titular,cod_vuelo,estado,total,json_pasajeros`
  - _Nota:_ Para guardar listas complejas (como pasajeros dentro de una reserva), serializar esa parte a JSON string antes de guardar en el TXT.

---

### 3.2. Usuarios

#### `<<Abstract>> Usuario`

Clase padre. No se puede instanciar directamente.

- **Atributos Protegidos (`#`):** Accesibles por las clases hijas (`Cliente`, `Admin`).
- **Seguridad:** `passwordHash` nunca guarda la contraseña en texto plano. Usar `hashlib.sha256`.
- **Métodos:**
  - `verificarPassword(pass)`: Compara el hash del input con el atributo.
  - `getTipo()`: Método abstracto que debe retornar "ADMIN" o "CLIENTE".

#### `Cliente` (Extends Usuario)

- **Lógica de Millas:**
  - `acumularMillas(500)`: Se llama al confirmar Check-In.
  - `puedeMejorarClase()`: Retorna `True` si `millas >= 2000`. Si se usa, debe restar las millas.

#### `Administrador` (Extends Usuario)

- **Reportes:**
  - `verSillasVendidas()`: Filtra los vuelos y retorna estadísticas para que el Admin vea ocupación.

---

### 3.3. Asientos y Tarifas (Polimorfismo)

#### `<<Abstract>> Asiento`

Representa una silla física en el avión.

- **Atributos:**
  - `ocupado`: Booleano.
  - `seleccionManual`: Si el usuario eligió este asiento específicamente (implica costo extra).
- **Método Polimórfico `calcularPrecio(esPasajeroFrecuente)`:**
  - Es la base del cálculo. Las hijas definen el precio base.

#### `AsientoEconomico`

- **Precio Base:** $235.000.
- **Cálculo:** `Base + (15% si seleccionManual es True)`.

#### `AsientoPreferencial`

- **Precio Base:** $850.000.
- **Cálculo:**
  - Si `esPasajeroFrecuente` es `True` (usa millas): El precio base se convierte temporalmente a precio económico ($235.000).
  - Si no: $850.000.
  - Al final, sumar el 15% si hubo `seleccionManual`.

---

### 3.4. Equipaje (Polimorfismo)

#### `<<Abstract>> Equipaje`

Define la estructura de una maleta.

- **Método `calcularCosto(claseVuelo)`**: Recibe si el pasajero viaja en "ECO" o "PREF".

#### `EquipajeMano`

- **Regla:** Gratis siempre. Retorna 0.

#### `EquipajeCabina`

- **Regla:**
  - Si `claseVuelo == PREF`: Gratis (0).
  - Si `claseVuelo == ECO`: Costo $40.000.

#### `EquipajeBodega`

- **Regla:**
  - Si `claseVuelo == PREF` Y es la **primera** maleta de bodega del pasajero: Gratis (0).
  - Caso contrario (adicionales o Eco): Costo proporcional.
  - _Fórmula sugerida:_ `(peso * 10.000) + (volumen * 5.000)`.

---

### 3.5. Núcleo del Negocio

#### `Vuelo`

Es la clase más compleja en lógica.

- **`generarMapaAsientos()`:** Se ejecuta al cargar el vuelo. Crea una lista/matriz de objetos `Asiento`.
  - Total: 180 sillas (ejemplo).
  - Filas 1-5: Instancias de `AsientoPreferencial`.
  - Filas 6-30: Instancias de `AsientoEconomico`.
- **`calcularSobreventaPermitida()`:**
  - Obtener `dias_restantes = fecha_vuelo - hoy`.
  - Si `dias_restantes < 2`: Retorna 0% (No se puede sobrevender).
  - Si `dias_restantes > 30`: Retorna 20%.
  - Entre 2 y 30 días: Interpolar valor.
- **`obtenerAsientoAleatorio(tipo)`:**
  - Algoritmo: Recorrer el mapa de asientos. Buscar libre en orden: Ventana -> Pasillo -> Medio. De adelante hacia atrás.
- **`verificarDisponibilidad(cantidad)`:**
  - Valida si `(asientos_ocupados + cantidad) <= (capacidad_total * (1 + porcentaje_sobreventa))`.

#### `Pasajero`

Clase compuesta usada dentro de una Reserva.

- Vincula una persona (datos básicos) con un objeto `Asiento` asignado y una lista de objetos `Equipaje`.
- **Importante:** Si es el Pasajero #1, sus datos suelen ser copia del Usuario titular, pero es un objeto independiente.

#### `Reserva`

- **Estado:** Puede ser "PENDIENTE", "CONFIRMADA", "CANCELADA", "CHECKIN_OK".
- **Flujo:**
  1.  Crear reserva.
  2.  `agregarPasajero()` x veces.
  3.  `confirmarReserva()`: Guarda en archivo y marca asientos como ocupados en memoria.
  4.  `realizarCheckIn()`: Calcula equipaje, suma millas al titular y cambia estado.

---

## 4. Fachada (API_Sistema) - Guía de Integración

Esta clase es la única que debe instanciarse en el `main.py`.

### Métodos Expuestos (Públicos)

1.  **`iniciar()`**

    - Inicializa el `GestorTxt`.
    - Carga usuarios y vuelos a memoria RAM desde los TXT.
    - Ejecuta `generarMapaAsientos()` para cada vuelo cargado.

2.  **`login(doc, pass)`** -> `dict`

    - Retorna: `{'auth': True, 'rol': 'ADMIN', 'usuario': {...}}` o `{'auth': False}`.

3.  **`buscarVuelos(filtros)`** -> `List[dict]`

    - `filtros`: `{'origen': 'MEDELLIN', 'destino': 'BOGOTA'}`.
    - Retorna lista limpia para mostrar en tabla HTML.

4.  **`obtenerDetalleVuelo(idVuelo)`** -> `dict`

    - Retorna la estructura completa para pintar el avión en HTML.
    - Formato de salida vital para el Frontend:
      ```json
      {
        "codigo": "VU123",
        "asientos": [
          { "id": "1A", "tipo": "PREF", "estado": "LIBRE" },
          { "id": "1B", "tipo": "PREF", "estado": "OCUPADO" }
        ]
      }
      ```

5.  **`crearReserva(idVuelo, pasajerosData)`** -> `dict`

    - Recibe datos crudos del formulario.
    - Orquesta: Creación de objetos `Pasajero`, asignación de asientos (aleatoria o manual), cálculo de precios.
    - Guarda y retorna el código de reserva.

6.  **`realizarCheckIn(idReserva, configEquipaje)`** -> `dict`
    - Recibe qué maletas lleva cada pasajero.
    - Calcula costos extra.
    - Acumula millas.
    - Genera pase de abordar (simulado en el retorno).

---

## 5. Notas para el Desarrollador

- **Manejo de Errores:** Usar bloques `try-except` dentro de la API y retornar diccionarios con llave `{'error': 'Mensaje'}` para que el frontend pueda mostrar alertas (SweetAlert, etc.).
- **Fechas:** Usar siempre librería `datetime` estándar. El formato en TXT debe ser ISO o consistente (ej: `YYYY-MM-DD HH:MM`).
- **Idempotencia:** Asegurarse de que cargar los datos dos veces no duplique registros en memoria. Limpiar listas antes de cargar (`self.vuelos = []`).


### Datos extras que toca integrar en una futura version del readme

 Edward pon los usuarios Cliente y Admin aca

**Clientes:**
 ```
 Cliente: Usuario 2002 / Clave 12345
 ```

**Admin:**
 ```
 Admin: Usuario 1001 / Clave 12345
 ```