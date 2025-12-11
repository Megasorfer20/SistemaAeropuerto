<template>
  <!-- Vista de confirmación de reserva -->
  <div class="confirmation-view">
    <NavBar />

    <div class="container confirmation-container">
      <div v-if="reserva" class="confirmation-content">
        <!-- Success Animation -->
        <div class="success-animation fade-in">
          <div class="success-circle">
            <svg class="checkmark" viewBox="0 0 52 52">
              <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none" />
              <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" />
            </svg>
          </div>
          <h1 class="success-title">¡Reserva Confirmada!</h1>
          <p class="success-subtitle">Tu vuelo ha sido reservado exitosamente</p>
        </div>

        <!-- Reservation Details -->
        <div class="reservation-details card fade-in" style="animation-delay: 0.3s">
          <div class="detail-header">
            <h2 class="detail-title">Detalles de la Reserva</h2>
            <div class="reservation-code">
              <span class="code-label">Código de Reserva</span>
              <span class="code-value">{{ codigoReserva }}</span>
            </div>
          </div>

          <!-- Flight Information -->
          <div class="detail-section">
            <h3 class="section-header">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z"
                  fill="currentColor"
                />
              </svg>
              Información del Vuelo
            </h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="item-label">Número de Vuelo</span>
                <span class="item-value">{{ reserva.vuelo.numeroVuelo }}</span>
              </div>
              <div class="info-item">
                <span class="item-label">Origen</span>
                <span class="item-value">{{ reserva.vuelo.origen }}</span>
              </div>
              <div class="info-item">
                <span class="item-label">Destino</span>
                <span class="item-value">{{ reserva.vuelo.destino }}</span>
              </div>
              <div class="info-item">
                <span class="item-label">Fecha de Salida</span>
                <span class="item-value">{{ formatearFecha(reserva.vuelo.fechaSalida) }}</span>
              </div>
              <div class="info-item">
                <span class="item-label">Hora de Salida</span>
                <span class="item-value">{{ reserva.vuelo.horaSalida }}</span>
              </div>
              <div class="info-item">
                <span class="item-label">Hora de Llegada</span>
                <span class="item-value">{{ reserva.vuelo.horaLlegada }}</span>
              </div>
            </div>
          </div>

          <!-- Seats Information -->
          <div class="detail-section">
            <h3 class="section-header">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M4 4H20V6H4V4ZM4 11H12V13H4V11ZM4 18H20V20H4V18ZM16 13H20V17H16V13Z"
                  fill="currentColor"
                />
              </svg>
              Asientos Asignados
            </h3>
            <div class="seats-grid">
              <div v-for="asiento in reserva.asientos" :key="asiento.id" class="seat-card">
                <div class="seat-number-display">{{ asiento.numero }}</div>
                <div :class="['seat-class', asiento.tipo === 'vip' ? 'class-vip' : 'class-normal']">
                  {{ asiento.tipo === 'vip' ? 'VIP' : 'Normal' }}
                </div>
              </div>
            </div>
          </div>

          <!-- Passengers Information -->
          <div class="detail-section">
            <h3 class="section-header">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M16 11C17.66 11 18.99 9.66 18.99 8C18.99 6.34 17.66 5 16 5C14.34 5 13 6.34 13 8C13 9.66 14.34 11 16 11ZM8 11C9.66 11 10.99 9.66 10.99 8C10.99 6.34 9.66 5 8 5C6.34 5 5 6.34 5 8C5 9.66 6.34 11 8 11ZM8 13C5.67 13 1 14.17 1 16.5V19H15V16.5C15 14.17 10.33 13 8 13ZM16 13C15.71 13 15.38 13.02 15.03 13.05C16.19 13.89 17 15.02 17 16.5V19H23V16.5C23 14.17 18.33 13 16 13Z"
                  fill="currentColor"
                />
              </svg>
              Información de Pasajeros
            </h3>
            <div class="passengers-list">
              <div
                v-for="(pasajero, index) in reserva.pasajeros"
                :key="index"
                class="passenger-card"
              >
                <div class="passenger-header">
                  <span class="passenger-index">Pasajero {{ index + 1 }}</span>
                  <span class="passenger-seat">Asiento {{ reserva.asientos[index].numero }}</span>
                </div>
                <div class="passenger-info">
                  <div class="passenger-detail">
                    <span class="detail-icon">👤</span>
                    <span>{{ pasajero.nombre }}</span>
                  </div>
                  <div class="passenger-detail">
                    <span class="detail-icon">📧</span>
                    <span>{{ pasajero.email }}</span>
                  </div>
                  <div class="passenger-detail">
                    <span class="detail-icon">🆔</span>
                    <span>{{ pasajero.documento }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Payment Summary -->
          <div class="detail-section payment-section">
            <h3 class="section-header">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M20 4H4C2.89 4 2.01 4.89 2.01 6L2 18C2 19.11 2.89 20 4 20H20C21.11 20 22 19.11 22 18V6C22 4.89 21.11 4 20 4ZM20 18H4V12H20V18ZM20 8H4V6H20V8Z"
                  fill="currentColor"
                />
              </svg>
              Resumen de Pago
            </h3>
            <div class="payment-summary">
              <div class="payment-item">
                <span>Subtotal</span>
                <span>${{ reserva.total.toFixed(2) }}</span>
              </div>
              <div class="payment-divider"></div>
              <div class="payment-item payment-total">
                <span>Total Pagado</span>
                <span>${{ reserva.total.toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Important Information -->
        <div class="important-info card fade-in" style="animation-delay: 0.5s">
          <h3 class="info-title">
            <svg viewBox="0 0 24 24" fill="none">
              <path
                d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V11H13V17ZM13 9H11V7H13V9Z"
                fill="currentColor"
              />
            </svg>
            Información Importante
          </h3>
          <ul class="info-list">
            <li>Llega al aeropuerto al menos 2 horas antes de tu vuelo</li>
            <li>Lleva tu documento de identidad original</li>
            <li>Revisa las restricciones de equipaje antes de viajar</li>
            <li>Guarda tu código de reserva para el check-in</li>
          </ul>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons fade-in" style="animation-delay: 0.7s">
          <button @click="irAInicio" class="btn btn-primary btn-large">Volver al Inicio</button>
          <button @click="irADashboard" class="btn btn-secondary btn-large">Ir al Dashboard</button>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="error-state card">
        <svg viewBox="0 0 24 24" fill="none">
          <path
            d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z"
            fill="currentColor"
          />
        </svg>
        <h2>No se encontró información de reserva</h2>
        <p>Por favor, realiza una nueva reserva</p>
        <button @click="irAInicio" class="btn btn-primary">Buscar Vuelos</button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'ConfirmationView',
  components: {
    NavBar,
  },
  data() {
    return {
      // Datos de la reserva
      reserva: null,
      // Código de reserva generado
      codigoReserva: '',
    }
  },
  mounted() {
    // Cargar reserva y generar código
    this.cargarReserva()
    this.generarCodigoReserva()
  },
  methods: {
    // Cargar reserva desde localStorage
    cargarReserva() {
      const reservaStr = localStorage.getItem('reservaActual')
      if (reservaStr) {
        this.reserva = JSON.parse(reservaStr)
      }
    },
    // Generar código de reserva único
    generarCodigoReserva() {
      const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      let codigo = ''
      for (let i = 0; i < 6; i++) {
        codigo += caracteres.charAt(Math.floor(Math.random() * caracteres.length))
      }
      this.codigoReserva = codigo
    },
    // Formatear fecha
    formatearFecha(fecha) {
      const date = new Date(fecha + 'T00:00:00')
      return date.toLocaleDateString('es-ES', {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      })
    },
    // Navegar al inicio
    irAInicio() {
      // Limpiar datos de reserva
      localStorage.removeItem('reservaActual')
      localStorage.removeItem('vueloReserva')
      localStorage.removeItem('asientosSeleccionados')
      this.$router.push('/')
    },
    // Navegar al dashboard
    irADashboard() {
      // Limpiar datos de reserva
      localStorage.removeItem('reservaActual')
      localStorage.removeItem('vueloReserva')
      localStorage.removeItem('asientosSeleccionados')
      this.$router.push('/dashboard')
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/ConfirmationView.css';
</style>
