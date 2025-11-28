# .

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

# Sistema de Reserva de Vuelos - AeroRed

Sistema completo de reserva de vuelos desarrollado en Vue 3 con Options API, simulando la estética de una aerolínea moderna con color rojo como identidad principal.

## Características Principales

- **Autenticación de Usuarios**: Sistema de login que detecta usuarios normales y administradores
- **Búsqueda y Filtrado de Vuelos**: Lista de vuelos con filtros por fecha y destino
- **Selección Dinámica de Asientos**: Sistema interactivo con asientos VIP y normales generados dinámicamente
- **Formulario de Pasajeros**: Información completa con datos pre-llenados para el usuario logueado
- **Confirmación de Reserva**: Página de confirmación con detalles completos de la reserva

## Tecnologías Utilizadas

- **Vue 3** (Options API)
- **Vue Router** para navegación
- **JSON** para datos simulados (vuelos, usuarios, configuración de asientos)
- **CSS3** con variables personalizadas

## Estructura del Proyecto

\`\`\`
src/
├── assets/
│ └── main.css # Estilos globales y variables CSS
├── components/
│ └── NavBar.vue # Barra de navegación principal
├── data/
│ ├── vuelos.json # Datos de vuelos disponibles
│ ├── usuarios.json # Usuarios de prueba
│ └── asientos.json # Configuración de asientos
├── router/
│ └── index.js # Configuración de rutas
├── views/
│ ├── HomeView.vue # Página principal con lista de vuelos
│ ├── LoginView.vue # Página de inicio de sesión
│ ├── DashboardView.vue # Dashboard de usuario/admin
│ ├── FlightSelectionView.vue # Detalles de vuelo
│ ├── SeatSelectionView.vue # Selección de asientos
│ ├── PassengerInfoView.vue # Información de pasajeros
│ └── ConfirmationView.vue # Confirmación de reserva
├── App.vue # Componente raíz
└── main.js # Punto de entrada
\`\`\`

## Instalación

### Requisitos Previos

- Node.js (versión 16 o superior)
- npm (viene con Node.js)

### Dependencias a Instalar

Todas las dependencias ya están configuradas en el `package.json`. Ejecuta:

\`\`\`bash
npm install
\`\`\`

Esto instalará:

- `vue` (^3.5.22)
- `vue-router` (^4.6.3)
- Y todas las dependencias de desarrollo necesarias

### Ejecutar en Desarrollo

\`\`\`bash
npm run dev
\`\`\`

El proyecto estará disponible en `http://localhost:5173` (o el puerto que Vite asigne).

### Compilar para Producción

\`\`\`bash
npm run build
\`\`\`

Los archivos compilados estarán en la carpeta `dist/`.

## Credenciales de Prueba

### Usuario Normal

- **Email**: usuario@aerored.com
- **Contraseña**: usuario123
- **Documento**: 12345678

### Usuario Administrador

- **Email**: admin@aerored.com
- **Contraseña**: admin123
- **Documento**: 87654321

## Funcionamiento de los Componentes

### 1. Autenticación (LoginView.vue)

- Valida credenciales contra el archivo `usuarios.json`
- Guarda el usuario en `localStorage` al iniciar sesión
- Detecta automáticamente si es usuario normal o administrador
- Redirecciona al dashboard después del login exitoso

### 2. Dashboard (DashboardView.vue)

- Muestra información personalizada según el tipo de usuario
- Badge distintivo para administradores
- Estadísticas de reservas y vuelos disponibles
- Acceso rápido a búsqueda de vuelos

### 3. Lista de Vuelos (HomeView.vue)

- Carga vuelos desde `vuelos.json`
- Filtrado por fecha de salida y destino
- Muestra información completa de cada vuelo
- Restricción de reserva solo para usuarios autenticados

### 4. Detalles de Vuelo (FlightSelectionView.vue)

- Información detallada del vuelo seleccionado
- Muestra horarios, duración y precio
- Información de asientos disponibles (VIP y Normal)
- Botón para continuar con la reserva

### 5. Selección de Asientos (SeatSelectionView.vue)

- **Generación Dinámica**: Los asientos se generan en base a `asientos.json`
- **Configuración por Defecto**:
  - VIP: 5 filas × 6 asientos = 30 asientos (precio adicional: $200)
  - Normal: 25 filas × 6 asientos = 150 asientos
- **Estados de Asientos**:
  - Disponible (blanco)
  - Ocupado (gris, simulado aleatoriamente)
  - Seleccionado (rojo)
- Panel de resumen con cálculo automático de precios
- Múltiples asientos pueden ser seleccionados

### 6. Información de Pasajeros (PassengerInfoView.vue)

- Formulario dinámico según cantidad de asientos seleccionados
- **Datos Pre-llenados**: El primer pasajero tiene los datos del usuario logueado
- Campos requeridos:
  - Nombre completo
  - Correo electrónico
  - Número de documento
- Resumen lateral con toda la información de la reserva
- Validación antes de confirmar

### 7. Confirmación (ConfirmationView.vue)

- Animación de éxito con checkmark
- Código de reserva único generado automáticamente
- Resumen completo de:
  - Información del vuelo
  - Asientos asignados
  - Datos de todos los pasajeros
  - Desglose de precio total
- Información importante para el viaje
- Limpia los datos de localStorage al finalizar

## Rutas de la Aplicación

| Ruta             | Componente          | Requiere Auth | Descripción                          |
| ---------------- | ------------------- | ------------- | ------------------------------------ |
| `/`              | HomeView            | No            | Página principal con lista de vuelos |
| `/login`         | LoginView           | No            | Inicio de sesión                     |
| `/dashboard`     | DashboardView       | Sí            | Panel de control del usuario         |
| `/vuelo/:id`     | FlightSelectionView | No            | Detalles de un vuelo                 |
| `/asientos/:id`  | SeatSelectionView   | Sí            | Selección de asientos                |
| `/pasajeros/:id` | PassengerInfoView   | Sí            | Formulario de pasajeros              |
| `/confirmacion`  | ConfirmationView    | Sí            | Confirmación de reserva              |

## Guards de Navegación

El router incluye un guard global que:

- Verifica si hay un usuario logueado en `localStorage`
- Redirige a `/login` si se intenta acceder a rutas protegidas sin autenticación
- Permite navegación libre en rutas públicas

## Datos JSON

### vuelos.json

Contiene 6 vuelos de ejemplo con:

- Número de vuelo
- Origen y destino
- Fechas y horas de salida/llegada
- Precio base
- Cantidad de asientos (normales y VIP)

### usuarios.json

Contiene 2 usuarios de prueba:

- 1 usuario normal
- 1 administrador

### asientos.json

Configuración de asientos:

- **VIP**: filas, asientos por fila, precio adicional
- **Normal**: filas, asientos por fila, precio adicional (0)

## Estilos y Tema

### Paleta de Colores

- **Rojo Principal**: `#dc2626` (primary-red)
- **Rojo Oscuro**: `#b91c1c` (primary-red-dark)
- **Rojo Claro**: `#ef4444` (primary-red-light)
- **Gris Secundario**: `#374151`
- **Gris Claro**: `#f3f4f6`
- **Blanco**: `#ffffff`

### Variables CSS

Todas las variables de color están definidas en `src/assets/main.css` para fácil personalización.

## Características Técnicas

### Options API

Todo el código utiliza Vue 3 Options API con:

- `data()` para estado reactivo
- `computed` para propiedades calculadas
- `methods` para funciones
- `mounted()` para inicialización
- `components` para registro de componentes

### LocalStorage

Se utiliza para:

- Almacenar usuario autenticado
- Guardar vuelo seleccionado
- Guardar asientos seleccionados
- Guardar reserva actual

### Responsive Design

- Mobile-first approach
- Breakpoints: 640px, 768px, 1024px
- Grids adaptables con CSS Grid y Flexbox

## Próximas Características (Futuro)

Las siguientes funcionalidades están preparadas para ser implementadas cuando se conecte una API real:

- Conexión con backend real
- Base de datos para persistencia
- Sistema de pago integrado
- Gestión de reservas (cancelaciones, modificaciones)
- Notificaciones por email
- Panel administrativo completo
- Historial de vuelos
- Gestión de flotas
- Reportes y estadísticas

## Comentarios en el Código

Todo el código incluye comentarios explicativos en español para facilitar la comprensión:

- Propósito de cada componente
- Funcionalidad de métodos importantes
- Lógica de negocio
- Flujo de datos

## Notas Importantes

1. **Datos Simulados**: Todos los datos son ficticios y están en archivos JSON. Al conectar una API, estos archivos serán reemplazados por llamadas HTTP.

2. **Asientos Ocupados**: Los asientos ocupados se simulan de forma aleatoria con `Math.random()`. En producción, esto vendrá de la base de datos.

3. **Sin Persistencia**: Las reservas no se guardan permanentemente. Al recargar la página, se pierden. Esto es intencional para desarrollo.

4. **Tipo de Usuario**: El sistema detecta si un usuario es administrador pero ambos dashboards son idénticos por ahora. Las características admin se agregarán en futuras iteraciones.

## Soporte y Problemas

Para cualquier problema o pregunta sobre el proyecto:

1. Verifica que todas las dependencias estén instaladas correctamente
2. Asegúrate de usar Node.js versión 16 o superior
3. Limpia el caché de npm si hay problemas: `npm cache clean --force`
4. Reinstala las dependencias: `rm -rf node_modules && npm install`

---

Desarrollado con Vue 3 + Options API
\`\`\`

Implementé el sistema completo de formulario de pasajeros con información pre-llenada del usuario logueado en el primer boleto, junto con la página de confirmación que muestra todos los detalles de la reserva con animación de éxito, además del README completo con toda la documentación del proyecto.
