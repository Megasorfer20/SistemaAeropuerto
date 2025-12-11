<template>
  <!-- Página principal con lista de vuelos disponibles -->
  <div class="home-view">
    <NavBar />

    <!-- Hero section con imagen de fondo -->
    <div class="hero-section">
      <div class="hero-overlay">
        <div class="container hero-content">
          <h1 class="hero-title fade-in">Descubre el Mundo con AeroRed</h1>
          <p class="hero-subtitle fade-in" style="animation-delay: 0.2s">
            Los mejores destinos a tu alcance
          </p>
        </div>
      </div>
    </div>

    <!-- Sección de filtros y búsqueda -->
    <div class="container flights-section">
      <div class="filters-card card fade-in">
        <h2 class="filters-title">Buscar Vuelos</h2>

        <div class="filters-grid">
          <!-- Filtro por fecha de salida -->
          <div class="filter-group">
            <label class="form-label">Fecha de Salida</label>
            <input type="date" v-model="filtroFecha" class="form-input" :min="fechaMinima" />
          </div>

          <!-- Filtro por destino -->
          <div class="filter-group">
            <label class="form-label">Destino</label>
            <select v-model="filtroDestino" class="form-input">
              <option value="">Todos los destinos</option>
              <option v-for="destino in destinosUnicos" :key="destino" :value="destino">
                {{ destino }}
              </option>
            </select>
          </div>

          <!-- Botón para limpiar filtros -->
          <div class="filter-group filter-actions">
            <button @click="limpiarFiltros" class="btn btn-secondary">Limpiar Filtros</button>
          </div>
        </div>
      </div>

      <!-- Lista de vuelos -->
      <div class="flights-list">
        <div class="flights-header">
          <h2 class="section-title">Vuelos Disponibles Hoy</h2>
          <p class="flights-count">{{ vuelosFiltrados.length }} vuelos encontrados</p>
        </div>

        <!-- Grid de tarjetas de vuelos -->
        <div v-if="vuelosFiltrados.length > 0" class="flights-grid">
          <div
            v-for="(vuelo, index) in vuelosFiltrados"
            :key="vuelo.id"
            class="flight-card card fade-in"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <!-- Header de la tarjeta -->
            <div class="flight-header">
              <div class="flight-number">
                <svg class="flight-icon" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z"
                    fill="currentColor"
                  />
                </svg>
                <span>{{ vuelo.numeroVuelo }}</span>
              </div>
              <div class="flight-price">${{ vuelo.precio.toFixed(2) }}</div>
            </div>

            <!-- Información de ruta -->
            <div class="flight-route">
              <div class="route-point">
                <div class="route-city">{{ vuelo.origen }}</div>
                <div class="route-time">{{ vuelo.horaSalida }}</div>
                <div class="route-date">{{ formatearFecha(vuelo.fechaSalida) }}</div>
              </div>

              <div class="route-line">
                <div class="route-arrow">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M16.01 11H4V13H16.01V16L20 12L16.01 8V11Z" fill="currentColor" />
                  </svg>
                </div>
              </div>

              <div class="route-point">
                <div class="route-city">{{ vuelo.destino }}</div>
                <div class="route-time">{{ vuelo.horaLlegada }}</div>
                <div class="route-date">{{ formatearFecha(vuelo.fechaLlegada) }}</div>
              </div>
            </div>

            <!-- Información adicional -->
            <div class="flight-info">
              <div class="info-item">
                <svg viewBox="0 0 24 24" fill="none">
                  <path
                    d="M7 11H9V13H7V11ZM21 5V19C21 20.1 20.1 21 19 21H5C3.89 21 3 20.1 3 19V5C3 3.9 3.89 3 5 3H6V1H8V3H16V1H18V3H19C20.1 3 21 3.9 21 5ZM5 7H19V5H5V7ZM19 19V9H5V19H19ZM15 13V11H17V13H15ZM11 13V11H13V13H11Z"
                    fill="currentColor"
                  />
                </svg>
                <span>{{ calcularDuracion(vuelo) }}</span>
              </div>
              <div class="info-item">
                <svg viewBox="0 0 24 24" fill="none">
                  <path
                    d="M4 4H20V6H4V4ZM4 11H12V13H4V11ZM4 18H20V20H4V18ZM16 13H20V17H16V13Z"
                    fill="currentColor"
                  />
                </svg>
                <span>{{ vuelo.asientosNormales + vuelo.asientosVIP }} asientos</span>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="flight-actions">
              <button @click="verDetalles(vuelo.id)" class="btn btn-outline">Ver Detalles</button>
              <button
                @click="reservarVuelo(vuelo.id)"
                class="btn btn-primary"
                :disabled="!usuarioActual"
              >
                {{ usuarioActual ? 'Reservar' : 'Inicia Sesión para Reservar' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Mensaje cuando no hay vuelos -->
        <div v-else class="no-flights card">
          <svg class="no-flights-icon" viewBox="0 0 24 24" fill="none">
            <path
              d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z"
              fill="currentColor"
            />
          </svg>
          <h3>No se encontraron vuelos</h3>
          <p>Intenta ajustar tus filtros de búsqueda</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
// import vuelosData from '../data/vuelos.json'

export default {
  name: 'HomeView',
  components: {
    NavBar,
  },
  data() {
    return {
      // Datos de vuelos cargados desde JSON
      vuelos: [],
      // Filtros aplicados
      filtroFecha: '',
      filtroDestino: '',
      // Usuario actual
      usuarioActual: null,
      // Fecha mínima para el selector de fecha (hoy)
      fechaMinima: new Date().toISOString().split('T')[0],
    }
  },
  computed: {
    // Obtener lista de destinos únicos para el filtro
    destinosUnicos() {
      return [...new Set(this.vuelos.map((v) => v.destino))].sort()
    },
    // Filtrar vuelos según los criterios seleccionados
    vuelosFiltrados() {
      return this.vuelos.filter((vuelo) => {
        // Filtro por fecha
        const cumpleFecha = !this.filtroFecha || vuelo.fechaSalida === this.filtroFecha
        // Filtro por destino
        const cumpleDestino = !this.filtroDestino || vuelo.destino === this.filtroDestino

        return cumpleFecha && cumpleDestino && vuelo.disponible
      })
    },
  },
  mounted() {
    // Cargar datos al montar el componente
    // Verificamos si pywebview ya está inyectado
    if (window.pywebview) {
      this.cargarVuelos()
    } else {
      // Si no, esperamos al evento 'pywebviewready'
      window.addEventListener('pywebviewready', () => {
        this.cargarVuelos()
      });
    }

    console.log("Usuario actual en HomeView:", this.usuarioActual);
    console.log("Vuelos cargados en HomeView:", this.vuelos);

    this.cargarUsuario()
  },
  methods: {
    // Cargar vuelos desde el archivo JSON
    cargarVuelos() {
      // Llamamos al método que creamos en la clase API
      window.pywebview.api
        .obtenerVuelosIniciales()
        .then((response) => {
          console.log('Datos recibidos:', response)
          // Asignamos la respuesta a nuestra variable de Vue
          this.listaVuelos = response
        })
        .catch((error) => {
          console.error('Error comunicando con Python:', error)
        })
    },
    // Cargar usuario desde localStorage
    cargarUsuario() {
      const usuario = localStorage.getItem('usuarioActual')
      if (usuario) {
        this.usuarioActual = JSON.parse(usuario)
      }
    },
    // Limpiar todos los filtros
    limpiarFiltros() {
      this.filtroFecha = ''
      this.filtroDestino = ''
    },
    // Formatear fecha para mostrar de forma legible
    formatearFecha(fecha) {
      const date = new Date(fecha + 'T00:00:00')
      return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: 'short',
      })
    },
    // Calcular duración estimada del vuelo
    calcularDuracion(vuelo) {
      const salida = new Date(`${vuelo.fechaSalida}T${vuelo.horaSalida}`)
      const llegada = new Date(`${vuelo.fechaLlegada}T${vuelo.horaLlegada}`)
      const duracion = (llegada - salida) / (1000 * 60 * 60)
      return `${Math.floor(duracion)}h ${Math.round((duracion % 1) * 60)}m`
    },
    // Ver detalles de un vuelo
    verDetalles(vueloId) {
      this.$router.push(`/vuelo/${vueloId}`)
    },
    // Iniciar proceso de reserva
    reservarVuelo(vueloId) {
      if (!this.usuarioActual) {
        // Redirigir a login si no está autenticado
        this.$router.push('/login')
      } else {
        // Ir a selección de asientos
        this.$router.push(`/asientos/${vueloId}`)
      }
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/HomeView.css';
</style>
