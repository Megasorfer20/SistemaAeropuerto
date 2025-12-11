<template>
  <!-- Vista de detalles de un vuelo específico -->
  <div class="flight-selection-view">
    <NavBar />

    <div class="container flight-details-container">
      <!-- Botón para volver atrás -->
      <button @click="volver" class="btn-back">
        <svg viewBox="0 0 24 24" fill="none">
          <path
            d="M20 11H7.83L13.42 5.41L12 4L4 12L12 20L13.41 18.59L7.83 13H20V11Z"
            fill="currentColor"
          />
        </svg>
        Volver a la lista
      </button>

      <div v-if="vuelo" class="flight-details-content">
        <!-- Header con información principal -->
        <div class="flight-main-card card fade-in">
          <div class="flight-main-header">
            <div>
              <div class="flight-number-large">
                <svg viewBox="0 0 24 24" fill="none">
                  <path
                    d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z"
                    fill="currentColor"
                  />
                </svg>
                <!-- KEY: id -->
                <span>{{ vuelo.id }}</span>
              </div>
              <!-- KEYS: origen y destino -->
              <p class="flight-subtitle">{{ vuelo.origen }} → {{ vuelo.destino }}</p>
            </div>

            <!-- ELIMINADO: Precio (no existe en el TXT) -->
          </div>

          <!-- Información de horarios (SIMPLIFICADA) -->
          <div class="flight-schedule">
            <div class="schedule-item">
              <div class="schedule-label">Día de Salida</div>
              <!-- KEY: fechaDiaSalida -->
              <div class="schedule-value">{{ vuelo.fechaDiaSalida }}</div>
            </div>

            <div class="schedule-divider">
              <!-- Icono de flecha simple -->
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M5 12H19M19 12L12 5M19 12L12 19"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>

            <div class="schedule-item">
              <div class="schedule-label">Hora de Salida</div>
              <!-- KEY: fechaHoraSalida -->
              <div class="schedule-value">{{ vuelo.fechaHoraSalida }}</div>
            </div>
          </div>
        </div>

        <!-- Grid con información adicional -->
        <div class="info-grid">
          <div class="info-card card fade-in" style="animation-delay: 0.1s">
            <h3 class="info-title">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M4 4H20V6H4V4ZM4 11H12V13H4V11ZM4 18H20V20H4V18ZM16 13H20V17H16V13Z"
                  fill="currentColor"
                />
              </svg>
              Asientos Disponibles
            </h3>
            <div class="seat-types">
              <div class="seat-type">
                <span class="seat-label">Clase Económica</span>
                <!-- KEY: asientosEco -->
                <span class="seat-count">{{ vuelo.asientosEco }} asientos</span>
              </div>
              <div class="seat-type">
                <span class="seat-label">Clase Preferencial</span>
                <!-- KEY: asientosPref -->
                <span class="seat-count">{{ vuelo.asientosPref }} asientos</span>
              </div>
            </div>
          </div>

          <div class="info-card card fade-in" style="animation-delay: 0.2s">
            <h3 class="info-title">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 2C8.13 2 5 5.13 5 9C5 14.25 12 22 12 22C12 22 19 14.25 19 9C19 5.13 15.87 2 12 2ZM12 11.5C10.62 11.5 9.5 10.38 9.5 9C9.5 7.62 10.62 6.5 12 6.5C13.38 6.5 14.5 7.62 14.5 9C14.5 10.38 13.38 11.5 12 11.5Z"
                  fill="currentColor"
                />
              </svg>
              Destino
            </h3>
            <!-- KEY: destino -->
            <p class="destination-name">{{ vuelo.destino }}</p>
            <p class="destination-description">Vuelo directo desde {{ vuelo.origen }}</p>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="action-buttons card fade-in" style="animation-delay: 0.3s">
          <button
                  @click="reservarVuelo(vuelo.id)"
                  class="btn btn-primary"
          >
            {{ usuarioActual ? 'Continuar con la Reserva' : 'Inicia Sesión para Reservar' }}
          </button>
          <p v-if="!usuarioActual" class="auth-notice">
            Necesitas iniciar sesión para poder reservar este vuelo
          </p>
        </div>
      </div>

      <!-- Mensaje de carga o error -->
      <div v-else class="loading-card card">
        <p>{{ mensajeCarga }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'FlightSelectionView',
  components: {
    NavBar,
  },
  data() {
    return {
      vuelo: null,
      usuarioActual: null,
      mensajeCarga: 'Cargando información del vuelo...',
    }
  },
  mounted() {
    this.cargarUsuario()

    if (window.pywebview) {
      this.cargarVueloBackend()
    } else {
      window.addEventListener('pywebviewready', () => {
        this.cargarVueloBackend()
      })
    }
  },
  methods: {
    // 1. Cargar vuelo usando el ID de la ruta
    cargarVueloBackend() {
      // Obtenemos el ID de la URL (ej: /vuelo/VU1234L)
      const vueloId = this.$route.params.id

      // Creamos el filtro solo con el ID
      const filtros = { id: vueloId }

      window.pywebview.api
        .buscarVuelos(filtros)
        .then((response) => {
          if (response && response.length > 0) {
            // Como buscarVuelos devuelve un array, tomamos el primero
            this.vuelo = response[0]
          } else {
            this.mensajeCarga = 'No se encontró el vuelo solicitado.'
          }
        })
        .catch((err) => {
          console.error('Error cargando vuelo:', err)
          this.mensajeCarga = 'Error de conexión.'
        })
    },

    cargarUsuario() {
      const usuario = localStorage.getItem('usuarioActual')
      if (usuario) {
        this.usuarioActual = JSON.parse(usuario)
      }
    },

    volver() {
      this.$router.go(-1) // Vuelve a la página anterior (Home) manteniendo estado si es posible
    },

    reservarVuelo() {
      if (!this.usuarioActual) {
        this.$router.push('/login')
      } else {
        this.$router.push(`/asientos/${this.vuelo.id}`)
      }
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/FlightSelectionView.css';
</style>
