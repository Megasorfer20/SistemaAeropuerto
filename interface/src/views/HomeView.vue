<template>
  <div class="home-view">
    <NavBar />

    <!-- Hero section -->
    <div class="hero-section">
      <div class="hero-overlay">
        <div class="container hero-content">
          <h1 class="hero-title fade-in">Descubre el Mundo con AeroRed</h1>
          <p class="hero-subtitle fade-in" style="animation-delay: 0.2s">
            Vuelos nacionales e internacionales
          </p>
        </div>
      </div>
    </div>

    <!-- Sección de filtros (MODIFICADA) -->
    <div class="container flights-section">
      <div class="filters-card card fade-in">
        <h2 class="filters-title">Buscar Vuelos</h2>

        <div class="filters-grid">
          <!-- Filtro Origen -->
          <div class="filter-group">
            <label class="form-label">Origen</label>
            <input
              type="text"
              v-model="filtros.origen"
              placeholder="Ej. Medellin"
              class="form-input"
            />
          </div>

          <!-- Filtro Destino -->
          <div class="filter-group">
            <label class="form-label">Destino</label>
            <input
              type="text"
              v-model="filtros.destino"
              placeholder="Ej. Bogota"
              class="form-input"
            />
          </div>

          <!-- Filtro Día de la Semana -->
          <div class="filter-group">
            <label class="form-label">Día</label>
            <select v-model="filtros.dia" class="form-input">
              <option value="TODOS">Cualquier día</option>
              <option value="LUNES">Lunes</option>
              <option value="MARTES">Martes</option>
              <option value="MIERCOLES">Miércoles</option>
              <option value="JUEVES">Jueves</option>
              <option value="VIERNES">Viernes</option>
              <option value="SABADO">Sábado</option>
              <option value="DOMINGO">Domingo</option>
            </select>
          </div>

          <!-- Filtro Rango Hora -->
          <div class="filter-group">
            <label class="form-label">Hora Salida (Desde - Hasta)</label>
            <div style="display: flex; gap: 5px">
              <input type="time" v-model="filtros.horaInicio" class="form-input" />
              <input type="time" v-model="filtros.horaFin" class="form-input" />
            </div>
          </div>

          <!-- Botón Buscar (Llama al Backend) -->
          <div class="filter-group filter-actions">
            <button @click="filtrarVuelosEnBackend" class="btn btn-primary">Buscar</button>
            <button @click="limpiarFiltros" class="btn btn-secondary" style="margin-top: 5px">
              Limpiar
            </button>
          </div>
        </div>
      </div>

      <!-- Lista de vuelos -->
      <div class="flights-list">
        <div class="flights-header">
          <h2 class="section-title">Resultados de búsqueda</h2>
          <p class="flights-count">{{ vuelos.length }} vuelos encontrados</p>
        </div>

        <!-- Grid de tarjetas (MODIFICADA CON TUS KEYS) -->
        <div v-if="vuelos.length > 0" class="flights-grid">
          <div
            v-for="(vuelo, index) in vuelos"
            :key="vuelo.id"
            class="flight-card card fade-in"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <!-- Header: ID y Origen-Destino -->
            <div class="flight-header">
              <div class="flight-number">
                <span style="color: var(--primary-red)">✈</span>
                <span>{{ vuelo.id }}</span>
              </div>
              <!-- Sin precio porque no viene en el CSV/JSON -->
              <div class="flight-route-simple">{{ vuelo.origen }} ➝ {{ vuelo.destino }}</div>
            </div>

            <!-- Información Horaria -->
            <div class="flight-route">
              <div class="route-point">
                <div class="route-label">Día Salida</div>
                <div class="route-value">{{ vuelo.fechaDiaSalida }}</div>
              </div>

              <div class="route-line">
                <!-- Flecha decorativa -->
                <span style="color: #ccc">--------</span>
              </div>

              <div class="route-point">
                <div class="route-label">Hora Salida</div>
                <div class="route-value" style="color: var(--primary-red); font-weight: bold">
                  {{ vuelo.fechaHoraSalida }}
                </div>
              </div>
            </div>

            <!-- Información Asientos -->
            <div class="flight-info">
              <div class="info-item">
                <span>Económicos: {{ vuelo.asientosEco }} sillas</span>
              </div>
              <div class="info-item">
                <span>Preferenciales: {{ vuelo.asientosPref }} sillas</span>
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
                {{ usuarioActual ? 'Reservar' : 'Login para Reservar' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Mensaje cuando no hay vuelos -->
        <div v-else class="no-flights card">
          <h3>No se encontraron vuelos</h3>
          <p>Intenta ajustar tus filtros de búsqueda</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'HomeView',
  components: {
    NavBar,
  },
  data() {
    return {
      vuelos: [], // Aquí guardamos lo que llega de Python
      filtros: {
        origen: '',
        destino: '',
        dia: 'TODOS',
        horaInicio: '',
        horaFin: '',
      },
      usuarioActual: null,
    }
  },
  mounted() {
    this.cargarUsuario()

    // Lógica de espera para PyWebView
    if (window.pywebview) {
      this.cargarVuelosIniciales()
    } else {
      window.addEventListener('pywebviewready', () => {
        this.cargarVuelosIniciales()
      })
    }
  },
  methods: {
    // 1. Carga inicial
    cargarVuelosIniciales() {
      // Llamada al método nuevo en Python
      window.pywebview.api
        .obtenerVuelosIniciales()
        .then((response) => {
          console.log('Vuelos cargados:', response)
          this.vuelos = response
        })
        .catch((error) => console.error('Error python:', error))
    },

    // 2. Búsqueda con filtros en Backend
    filtrarVuelosEnBackend() {
      // Preparamos el objeto para enviar a Python
      const params = {
        origen: this.filtros.origen,
        destino: this.filtros.destino,
        dia: this.filtros.dia,
        horaInicio: this.filtros.horaInicio,
        horaFin: this.filtros.horaFin,
      }

      window.pywebview.api
        .buscarVuelos(params)
        .then((response) => {
          console.log('Resultados búsqueda:', response)
          this.vuelos = response
        })
        .catch((error) => console.error('Error buscando:', error))
    },

    limpiarFiltros() {
      this.filtros = {
        origen: '',
        destino: '',
        dia: 'TODOS',
        horaInicio: '',
        horaFin: '',
      }
      this.cargarVuelosIniciales()
    },

    cargarUsuario() {
      const usuario = localStorage.getItem('usuarioActual')
      if (usuario) {
        this.usuarioActual = JSON.parse(usuario)
      }
    },
    
    // Ver detalles de un vuelo
    verDetalles(vueloId) {
      this.$router.push(`/vuelo/${vueloId}`)
    },
    // Iniciar proceso de reserva
    reservarVuelo(vueloId) {
      if (!this.usuarioActual) {
        this.$router.push('/login')
      } else {
        this.$router.push(`/asientos/${vueloId}`)
      }
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/HomeView.css';
</style>
