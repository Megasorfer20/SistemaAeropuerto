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
                <span>{{ vuelo.numeroVuelo }}</span>
              </div>
              <p class="flight-subtitle">{{ vuelo.origen }} → {{ vuelo.destino }}</p>
            </div>
            <div class="flight-price-large">
              <span class="price-label">Desde</span>
              <span class="price-value">${{ vuelo.precio.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Información de horarios -->
          <div class="flight-schedule">
            <div class="schedule-item">
              <div class="schedule-label">Salida</div>
              <div class="schedule-value">{{ vuelo.horaSalida }}</div>
              <div class="schedule-date">{{ formatearFecha(vuelo.fechaSalida) }}</div>
            </div>

            <div class="schedule-divider">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M16.01 11H4V13H16.01V16L20 12L16.01 8V11Z" fill="currentColor" />
              </svg>
              <span>{{ calcularDuracion(vuelo) }}</span>
            </div>

            <div class="schedule-item">
              <div class="schedule-label">Llegada</div>
              <div class="schedule-value">{{ vuelo.horaLlegada }}</div>
              <div class="schedule-date">{{ formatearFecha(vuelo.fechaLlegada) }}</div>
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
                <span class="seat-label">Clase Normal</span>
                <span class="seat-count">{{ vuelo.asientosNormales }} asientos</span>
              </div>
              <div class="seat-type">
                <span class="seat-label">Clase VIP</span>
                <span class="seat-count">{{ vuelo.asientosVIP }} asientos</span>
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
            <p class="destination-name">{{ vuelo.destino }}</p>
            <p class="destination-description">Un lugar increíble para visitar</p>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="action-buttons card fade-in" style="animation-delay: 0.3s">
          <button
            @click="reservarVuelo"
            class="btn btn-primary btn-large"
            :disabled="!usuarioActual"
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
        <p>Cargando información del vuelo...</p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import vuelosData from '../data/vuelos.json'

export default {
  name: 'FlightSelectionView',
  components: {
    NavBar,
  },
  data() {
    return {
      // Vuelo actual
      vuelo: null,
      // Usuario actual
      usuarioActual: null,
    }
  },
  mounted() {
    // Cargar datos al montar
    this.cargarVuelo()
    this.cargarUsuario()
  },
  methods: {
    // Cargar información del vuelo desde el ID en la ruta
    cargarVuelo() {
      const vueloId = parseInt(this.$route.params.id)
      this.vuelo = vuelosData.find((v) => v.id === vueloId)
    },
    // Cargar usuario desde localStorage
    cargarUsuario() {
      const usuario = localStorage.getItem('usuarioActual')
      if (usuario) {
        this.usuarioActual = JSON.parse(usuario)
      }
    },
    // Volver a la lista de vuelos
    volver() {
      this.$router.push('/')
    },
    // Formatear fecha
    formatearFecha(fecha) {
      const date = new Date(fecha + 'T00:00:00')
      return date.toLocaleDateString('es-ES', {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
      })
    },
    // Calcular duración del vuelo
    calcularDuracion(vuelo) {
      const salida = new Date(`${vuelo.fechaSalida}T${vuelo.horaSalida}`)
      const llegada = new Date(`${vuelo.fechaLlegada}T${vuelo.horaLlegada}`)
      const duracion = (llegada - salida) / (1000 * 60 * 60)
      return `${Math.floor(duracion)}h ${Math.round((duracion % 1) * 60)}m`
    },
    // Iniciar proceso de reserva
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
.flight-selection-view {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.flight-details-container {
  padding: 40px 20px;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: var(--text-dark);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: 24px;
  transition: color 0.3s ease;
}

.btn-back:hover {
  color: var(--primary-red);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

.flight-details-content {
  max-width: 900px;
  margin: 0 auto;
}

.flight-main-card {
  padding: 32px;
  margin-bottom: 24px;
}

.flight-main-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 32px;
}

.flight-number-large {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 32px;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 8px;
}

.flight-number-large svg {
  width: 36px;
  height: 36px;
  color: var(--primary-red);
}

.flight-subtitle {
  font-size: 18px;
  color: var(--text-light);
}

.flight-price-large {
  text-align: right;
}

.price-label {
  display: block;
  font-size: 14px;
  color: var(--text-light);
  margin-bottom: 4px;
}

.price-value {
  font-size: 40px;
  font-weight: 700;
  color: var(--primary-red);
}

.flight-schedule {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 32px;
  padding: 24px;
  background-color: var(--light-gray);
  border-radius: 12px;
}

.schedule-item {
  text-align: center;
}

.schedule-label {
  font-size: 14px;
  color: var(--text-light);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.schedule-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-red);
  margin-bottom: 4px;
}

.schedule-date {
  font-size: 14px;
  color: var(--text-dark);
  text-transform: capitalize;
}

.schedule-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.schedule-divider svg {
  width: 32px;
  height: 32px;
  color: var(--primary-red);
}

.schedule-divider span {
  font-size: 14px;
  color: var(--text-light);
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.info-card {
  padding: 24px;
}

.info-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 20px;
}

.info-title svg {
  width: 24px;
  height: 24px;
  color: var(--primary-red);
}

.seat-types {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.seat-type {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background-color: var(--light-gray);
  border-radius: 8px;
}

.seat-label {
  font-weight: 500;
  color: var(--text-dark);
}

.seat-count {
  font-weight: 700;
  color: var(--primary-red);
}

.destination-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 8px;
}

.destination-description {
  color: var(--text-light);
}

.action-buttons {
  padding: 32px;
  text-align: center;
}

.btn-large {
  width: 100%;
  max-width: 400px;
  padding: 16px 32px;
  font-size: 18px;
  margin-bottom: 16px;
}

.auth-notice {
  color: var(--text-light);
  font-size: 14px;
}

.loading-card {
  padding: 60px;
  text-align: center;
  color: var(--text-light);
}

@media (max-width: 768px) {
  .flight-main-header {
    flex-direction: column;
    gap: 20px;
  }

  .flight-price-large {
    text-align: left;
  }

  .flight-schedule {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .schedule-divider {
    transform: rotate(90deg);
  }
}
</style>
