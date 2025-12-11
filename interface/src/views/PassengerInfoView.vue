<template>
  <!-- Vista de información de pasajeros -->
  <div class="passenger-info-view">
    <NavBar />

    <div class="container passenger-container">
      <!-- Progress indicator -->
      <div class="progress-bar card fade-in">
        <div class="progress-step completed">
          <div class="step-circle">
            <svg viewBox="0 0 24 24" fill="none">
              <path
                d="M9 16.17L4.83 12L3.41 13.41L9 19L21 7L19.59 5.59L9 16.17Z"
                fill="currentColor"
              />
            </svg>
          </div>
          <span>Vuelo</span>
        </div>
        <div class="progress-line completed"></div>
        <div class="progress-step completed">
          <div class="step-circle">
            <svg viewBox="0 0 24 24" fill="none">
              <path
                d="M9 16.17L4.83 12L3.41 13.41L9 19L21 7L19.59 5.59L9 16.17Z"
                fill="currentColor"
              />
            </svg>
          </div>
          <span>Asientos</span>
        </div>
        <div class="progress-line"></div>
        <div class="progress-step active">
          <div class="step-circle">3</div>
          <span>Pasajeros</span>
        </div>
        <div class="progress-line"></div>
        <div class="progress-step">
          <div class="step-circle">4</div>
          <span>Confirmación</span>
        </div>
      </div>

      <div v-if="vuelo && asientos.length > 0" class="passenger-content">
        <div class="forms-section">
          <!-- Header -->
          <div class="forms-header fade-in">
            <h1 class="page-title">Información de Pasajeros</h1>
            <p class="page-subtitle">
              Completa la información para los {{ asientos.length }} pasajeros
            </p>
          </div>

          <!-- Formularios de pasajeros -->
          <div class="passengers-forms">
            <div
              v-for="(asiento, index) in asientos"
              :key="asiento.id"
              class="passenger-form-card card fade-in"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <!-- Header del formulario -->
              <div class="form-card-header">
                <div class="passenger-number">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path
                      d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"
                      fill="currentColor"
                    />
                  </svg>
                  <span>Pasajero {{ index + 1 }}</span>
                </div>
                <div class="seat-badge">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path
                      d="M4 4H20V6H4V4ZM4 11H12V13H4V11ZM4 18H20V20H4V18ZM16 13H20V17H16V13Z"
                      fill="currentColor"
                    />
                  </svg>
                  Asiento {{ asiento.numero }}
                  <span
                    :class="[
                      'seat-type-badge',
                      asiento.tipo === 'vip' ? 'badge-vip' : 'badge-normal',
                    ]"
                  >
                    {{ asiento.tipo === 'vip' ? 'VIP' : 'Normal' }}
                  </span>
                </div>
              </div>

              <!-- Campos del formulario -->
              <form @submit.prevent class="passenger-form">
                <div class="form-row">
                  <div class="form-group">
                    <label :for="`nombre-${index}`" class="form-label">
                      Nombre Completo <span class="required">*</span>
                    </label>
                    <input
                      :id="`nombre-${index}`"
                      type="text"
                      v-model="pasajeros[index].nombre"
                      class="form-input"
                      placeholder="Juan Pérez"
                      required
                    />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label :for="`email-${index}`" class="form-label">
                      Correo Electrónico <span class="required">*</span>
                    </label>
                    <input
                      :id="`email-${index}`"
                      type="email"
                      v-model="pasajeros[index].email"
                      class="form-input"
                      placeholder="correo@ejemplo.com"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label :for="`documento-${index}`" class="form-label">
                      Número de Documento <span class="required">*</span>
                    </label>
                    <input
                      :id="`documento-${index}`"
                      type="text"
                      v-model="pasajeros[index].documento"
                      class="form-input"
                      placeholder="12345678"
                      required
                    />
                  </div>
                </div>

                <!-- Nota para el primer pasajero -->
                <div v-if="index === 0" class="info-note">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path
                      d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V11H13V17ZM13 9H11V7H13V9Z"
                      fill="currentColor"
                    />
                  </svg>
                  <span>Se ha completado automáticamente con tu información de usuario</span>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Resumen lateral -->
        <div class="summary-sidebar">
          <div class="summary-card card fade-in" style="animation-delay: 0.3s">
            <h3 class="summary-title">Resumen de Reserva</h3>

            <!-- Información del vuelo -->
            <div class="summary-section">
              <h4 class="summary-section-title">Vuelo</h4>
              <div class="summary-detail">
                <span class="detail-label">Número</span>
                <span class="detail-value">{{ vuelo.numeroVuelo }}</span>
              </div>
              <div class="summary-detail">
                <span class="detail-label">Ruta</span>
                <span class="detail-value">{{ vuelo.origen }} → {{ vuelo.destino }}</span>
              </div>
              <div class="summary-detail">
                <span class="detail-label">Fecha</span>
                <span class="detail-value">{{ formatearFecha(vuelo.fechaSalida) }}</span>
              </div>
              <div class="summary-detail">
                <span class="detail-label">Hora</span>
                <span class="detail-value">{{ vuelo.horaSalida }}</span>
              </div>
            </div>

            <!-- Asientos seleccionados -->
            <div class="summary-section">
              <h4 class="summary-section-title">Asientos</h4>
              <div class="seats-list">
                <div v-for="asiento in asientos" :key="asiento.id" class="seat-item">
                  <span class="seat-number">{{ asiento.numero }}</span>
                  <span
                    :class="[
                      'seat-type-label',
                      asiento.tipo === 'vip' ? 'label-vip' : 'label-normal',
                    ]"
                  >
                    {{ asiento.tipo === 'vip' ? 'VIP' : 'Normal' }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Desglose de precio -->
            <div class="summary-section">
              <h4 class="summary-section-title">Desglose de Precio</h4>
              <div class="price-items">
                <div class="price-detail">
                  <span>Asientos Normales ({{ contarNormales() }})</span>
                  <span>${{ calcularPrecioNormales().toFixed(2) }}</span>
                </div>
                <div class="price-detail">
                  <span>Asientos VIP ({{ contarVIP() }})</span>
                  <span>${{ calcularPrecioVIP().toFixed(2) }}</span>
                </div>
                <div class="price-divider"></div>
                <div class="price-detail price-total">
                  <span>Total</span>
                  <span>${{ calcularTotal().toLocaleString('es-CO', { maximumFractionDigits: 0 })}}</span>
                </div>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="summary-actions">
              <button @click="volver" class="btn btn-secondary">Volver</button>
              <button
                @click="confirmarReserva"
                class="btn btn-primary"
                :disabled="!formularioValido"
              >
                Confirmar Reserva
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Mensaje de error si no hay datos -->
      <div v-else class="error-card card">
        <svg viewBox="0 0 24 24" fill="none">
          <path
            d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z"
            fill="currentColor"
          />
        </svg>
        <h3>Error al cargar la información</h3>
        <p>No se encontró información de la reserva. Por favor, inicia el proceso nuevamente.</p>
        <button @click="irAInicio" class="btn btn-primary">Volver al Inicio</button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'PassengerInfoView',
  components: {
    NavBar,
  },
  data() {
    return {
      // Datos del vuelo y asientos desde localStorage
      vuelo: null,
      asientos: [],
      // Array de información de pasajeros
      pasajeros: [],
      // Usuario actual
      usuarioActual: null,
    }
  },
  computed: {
    // Verificar si el formulario está completo
    formularioValido() {
      return this.pasajeros.every(
        (p) => p.nombre.trim() !== '' && p.email.trim() !== '' && p.documento.trim() !== '',
      )
    },
  },
  mounted() {
    // Cargar datos al montar
    this.cargarDatos()
    this.inicializarPasajeros()
  },
  methods: {
    // Cargar datos desde localStorage
    cargarDatos() {
      // Cargar vuelo
      const vueloStr = localStorage.getItem('vueloReserva')
      if (vueloStr) {
        this.vuelo = JSON.parse(vueloStr)
      }

      // Cargar asientos
      const asientosStr = localStorage.getItem('asientosSeleccionados')
      if (asientosStr) {
        this.asientos = JSON.parse(asientosStr)
      }

      // Cargar usuario
      const usuarioStr = localStorage.getItem('usuarioActual')
      if (usuarioStr) {
        this.usuarioActual = JSON.parse(usuarioStr)
      }
    },
    // Inicializar array de pasajeros con datos del usuario en el primero
    inicializarPasajeros() {
      this.pasajeros = this.asientos.map((asiento, index) => {
        // El primer pasajero tiene los datos del usuario por defecto
        if (index === 0 && this.usuarioActual) {
          return {
            asiento: asiento.id,
            nombre: this.usuarioActual.nombre || '',
            email: this.usuarioActual.email || '',
            documento: this.usuarioActual.documento || '',
          }
        }

        // Los demás pasajeros tienen campos vacíos
        return {
          asiento: asiento.id,
          nombre: '',
          email: '',
          documento: '',
        }
      })
    },
    // Contar asientos normales
    contarNormales() {
      return this.asientos.filter((a) => a.tipo === 'normal').length
    },
    // Contar asientos VIP
    contarVIP() {
      return this.asientos.filter((a) => a.tipo === 'vip').length
    },
    // Calcular precio de asientos normales
    calcularPrecioNormales() {
      return this.contarNormales() * this.vuelo.precio
    },
    // Calcular precio de asientos VIP
    calcularPrecioVIP() {
      const asientosVIP = this.asientos.filter((a) => a.tipo === 'vip')
      return (
        asientosVIP.reduce((total, asiento) => total + asiento.precio, 0) +
        this.contarVIP() * this.vuelo.precio
      )
    },
    // Calcular total
    calcularTotal() {
      return this.calcularPrecioNormales() + this.calcularPrecioVIP()
    },
    // Formatear fecha
    formatearFecha(fecha) {
      const date = new Date(fecha + 'T00:00:00')
      return date.toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      })
    },
    // Volver a la selección de asientos
    volver() {
      this.$router.go(-1)
    },
    // Confirmar reserva
    confirmarReserva() {
      if (!this.formularioValido) {
        alert('Por favor, completa todos los campos obligatorios')
        return
      }

      // Guardar información de pasajeros en localStorage
      const reserva = {
        vuelo: this.vuelo,
        asientos: this.asientos,
        pasajeros: this.pasajeros,
        total: this.calcularTotal(),
        fecha: new Date().toISOString(),
      }

      localStorage.setItem('reservaActual', JSON.stringify(reserva))

      // Navegar a la página de confirmación
      this.$router.push('/confirmacion')
    },
    // Ir al inicio
    irAInicio() {
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/PassengerInfo.css';
</style>
