<template>
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
                <span class="detail-value">{{ vuelo.id }}</span>
              </div>
              <div class="summary-detail">
                <span class="detail-label">Ruta</span>
                <span class="detail-value">{{ vuelo.origen }} → {{ vuelo.destino }}</span>
              </div>
              <div class="summary-detail">
                <span class="detail-label">Fecha</span>
                <span class="detail-value">{{ formatearFecha(vuelo.fechaDiaSalida) }}</span>
              </div>
              <div class="summary-detail">
                <span class="detail-label">Hora</span>
                <span class="detail-value">{{ vuelo.fechaHoraSalida }}</span>
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
                  <span>${{ formatPrice(calcularPrecioNormales()) }}</span>
                </div>
                <div class="price-detail">
                  <span>Asientos VIP ({{ contarVIP() }})</span>
                  <span>${{ formatPrice(calcularPrecioVIP()) }}</span>
                </div>
                <div class="price-divider"></div>
                <div class="price-detail price-total">
                  <span>Total</span>
                  <span>${{ formatPrice(calcularTotal()) }}</span>
                </div>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="summary-actions">
              <button @click="volver" class="btn btn-secondary">Volver</button>
              <button
                @click="confirmarReserva"
                class="btn btn-primary"
                :disabled="!formularioValido || cargando"
              >
                {{ cargando ? 'Procesando...' : 'Confirmar Reserva' }}
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
      vuelo: null,
      asientos: [],
      pasajeros: [],
      usuarioActual: null,
      cargando: false,
    }
  },
  computed: {
    formularioValido() {
      if (!this.pasajeros.length) return false
      return this.pasajeros.every(
        (p) =>
          p.nombre &&
          p.nombre.trim() !== '' &&
          p.email &&
          p.email.trim() !== '' &&
          p.documento &&
          p.documento.trim() !== '',
      )
    },
  },
  mounted() {
    this.cargarDatos()
    this.inicializarPasajeros()
  },
  methods: {
    cargarDatos() {
      const vueloStr = localStorage.getItem('vueloReserva')
      if (vueloStr) this.vuelo = JSON.parse(vueloStr)

      const asientosStr = localStorage.getItem('asientosSeleccionados')
      if (asientosStr) this.asientos = JSON.parse(asientosStr)

      const usuarioStr = localStorage.getItem('usuarioActual')
      if (usuarioStr) this.usuarioActual = JSON.parse(usuarioStr)
    },

    inicializarPasajeros() {
      // Solución Error #2: Autorellenar con datos reales del usuario (doc y correo)
      this.pasajeros = this.asientos.map((asiento, index) => {
        if (index === 0 && this.usuarioActual) {
          return {
            asiento: asiento.id,
            nombre: this.usuarioActual.nombre || '',
            // Nota: API.py ahora retorna 'correo' y 'doc' en el login
            email: this.usuarioActual.correo || '',
            documento: this.usuarioActual.doc || this.usuarioActual.numDoc || '',
          }
        }
        return {
          asiento: asiento.id,
          nombre: '',
          email: '',
          documento: '',
        }
      })
    },

    contarNormales() {
      return this.asientos.filter((a) => a.tipo === 'normal').length
    },
    contarVIP() {
      return this.asientos.filter((a) => a.tipo === 'vip').length
    },

    // Solución Error #3: Aseguramos conversión a Number para evitar NaN
    calcularPrecioNormales() {
      const asientosEco = this.asientos.filter((a) => a.tipo === 'normal')
      return asientosEco.reduce((sum, a) => sum + Number(a.precio), 0)
    },
    calcularPrecioVIP() {
      const asientosVIP = this.asientos.filter((a) => a.tipo === 'vip')
      return asientosVIP.reduce((sum, a) => sum + Number(a.precio), 0)
    },
    calcularTotal() {
      // Suma total segura
      return this.calcularPrecioNormales() + this.calcularPrecioVIP()
    },

    formatPrice(value) {
      return Number(value).toLocaleString('es-CO')
    },

    formatearFecha(fecha) {
      if (!fecha) return ''
      // Detecta si es formato YYYY-MM-DD para convertirlo bien
      const date = new Date(fecha + 'T00:00:00')
      // Si fecha no es valida, usar new Date(fecha)
      const validDate = isNaN(date.getTime()) ? new Date(fecha) : date

      return validDate.toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      })
    },

    volver() {
      this.$router.go(-1)
    },

    // Solución Error #4: Llamar al API para crear la reserva y guardar respuesta
    confirmarReserva() {
      if (!this.formularioValido) {
        alert('Por favor, completa todos los campos obligatorios')
        return
      }

      this.cargando = true

      // Asegurar que enviamos el doc del usuario logueado
      const docTitular = this.usuarioActual
        ? this.usuarioActual.doc || this.usuarioActual.numDoc
        : this.pasajeros[0].documento

      const datosReserva = {
        vuelo_id: this.vuelo.id, // CORREGIDO: vuelo_id para coincidir con Python
        titular_doc: docTitular,
        asientos: this.asientos,
        pasajeros: this.pasajeros,
        total: this.calcularTotal()
      }

      if (window.pywebview) {
        window.pywebview.api
          .crearReserva(datosReserva)
          .then((response) => {
            if (response.success) {
              // Creamos el objeto final con el código real generado por el backend
              const reservaFinal = {
                codigo: response.codigo, // <--- CÓDIGO DEL BACKEND
                vuelo: this.vuelo,
                asientos: this.asientos,
                pasajeros: this.pasajeros,
                total: datosReserva.total,
                fecha: new Date().toISOString(),
              }

              // Guardamos en LocalStorage con la clave que ConfirmationView espera
              localStorage.setItem('reservaActual', JSON.stringify(reservaFinal))

              this.$router.push('/confirmacion')
            } else {
              alert('Error al crear la reserva: ' + response.message)
              this.cargando = false
            }
          })
          .catch((err) => {
            console.error(err)
            alert('Error de comunicación con el servidor.')
            this.cargando = false
          })
      } else {
        // Fallback solo para pruebas sin backend (dev mode)
        alert('Modo desarrollo: Backend no detectado.')
        this.cargando = false
      }
    },

    irAInicio() {
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/PassengerInfo.css';
</style>
