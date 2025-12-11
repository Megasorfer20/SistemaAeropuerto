<template>
  <!-- Vista de selección de asientos -->
  <div class="seat-selection-view">
    <NavBar />

    <div class="container seat-container">
      <!-- Botón para volver -->
      <button @click="volver" class="btn-back">
        <svg viewBox="0 0 24 24" fill="none">
          <path
            d="M20 11H7.83L13.42 5.41L12 4L4 12L12 20L13.41 18.59L7.83 13H20V11Z"
            fill="currentColor"
          />
        </svg>
        Volver
      </button>

      <div v-if="vuelo" class="seat-content">
        <!-- Header con información del vuelo -->
        <div class="flight-info-bar card fade-in">
          <div class="flight-info-item">
            <span class="info-label">Vuelo</span>
            <span class="info-value">{{ vuelo.id }}</span>
          </div>
          <div class="flight-info-item">
            <span class="info-label">Ruta</span>
            <span class="info-value">{{ vuelo.origen }} → {{ vuelo.destino }}</span>
          </div>
          <div class="flight-info-item">
            <span class="info-label">Salida</span>
            <span class="info-value">{{ vuelo.fechaDiaSalida }} - {{ vuelo.fechaHoraSalida }}</span>
          </div>
          <div class="flight-info-item">
            <span class="info-label">Seleccionados</span>
            <span class="info-value info-highlight">{{ asientosSeleccionados.length }} / 3</span>
          </div>
        </div>

        <div class="seat-layout-container">
          <!-- Panel de selección de asientos -->
          <div class="seat-map-section card fade-in" style="animation-delay: 0.1s">
            <div class="seat-map-header">
              <h2 class="section-title">Selecciona tus Asientos</h2>
              <p style="font-size: 0.9em; color: #666; margin-top: -10px; margin-bottom: 20px">
                Puedes seleccionar máximo 3 asientos.
              </p>

              <!-- Leyenda de colores -->
              <div class="seat-legend">
                <div class="legend-item">
                  <div class="legend-box seat-available"></div>
                  <span>Disponible</span>
                </div>
                <div class="legend-item">
                  <div class="legend-box seat-occupied"></div>
                  <span>Ocupado</span>
                </div>
                <div class="legend-item">
                  <div class="legend-box seat-selected"></div>
                  <span>Seleccionado</span>
                </div>
              </div>
            </div>

            <!-- Mapa de asientos - Sección VIP -->
            <div class="cabin-section">
              <div class="cabin-header">
                <svg viewBox="0 0 24 24" fill="none">
                  <path
                    d="M12 2L2 7V9H5V20H9V14H15V20H19V9H22V7L12 2ZM12 9.5C11.17 9.5 10.5 8.83 10.5 8C10.5 7.17 11.17 6.5 12 6.5C12.83 6.5 13.5 7.17 13.5 8C13.5 8.83 12.83 9.5 12 9.5Z"
                    fill="currentColor"
                  />
                </svg>
                <h3>Clase Preferencial</h3>
                <span class="cabin-price">${{ formatPrice(PRECIO_VIP) }}</span>
              </div>

              <div class="seats-grid">
                <div
                  v-for="asiento in asientosVIP"
                  :key="asiento.id"
                  :class="[
                    'seat-button',
                    { 'seat-available': !asiento.ocupado && !estaSeleccionado(asiento.id) },
                    { 'seat-occupied': asiento.ocupado },
                    { 'seat-selected': estaSeleccionado(asiento.id) },
                  ]"
                  @click="toggleAsiento(asiento)"
                  :title="asiento.ocupado ? 'Ocupado' : asiento.numero"
                >
                  {{ asiento.numero }}
                </div>
              </div>
            </div>

            <!-- Divisor visual -->
            <div class="cabin-divider"></div>

            <!-- Mapa de asientos - Sección Normal -->
            <div class="cabin-section">
              <div class="cabin-header">
                <svg viewBox="0 0 24 24" fill="none">
                  <path
                    d="M4 4H20V6H4V4ZM4 11H12V13H4V11ZM4 18H20V20H4V18ZM16 13H20V17H16V13Z"
                    fill="currentColor"
                  />
                </svg>
                <h3>Clase Económica</h3>
                <span class="cabin-price">${{ formatPrice(PRECIO_ECO) }}</span>
              </div>

              <div class="seats-grid">
                <div
                  v-for="asiento in asientosNormales"
                  :key="asiento.id"
                  :class="[
                    'seat-button',
                    { 'seat-available': !asiento.ocupado && !estaSeleccionado(asiento.id) },
                    { 'seat-occupied': asiento.ocupado },
                    { 'seat-selected': estaSeleccionado(asiento.id) },
                  ]"
                  @click="toggleAsiento(asiento)"
                  :title="asiento.ocupado ? 'Ocupado' : asiento.numero"
                >
                  {{ asiento.numero }}
                </div>
              </div>
            </div>
          </div>

          <!-- Panel de resumen -->
          <div class="summary-section">
            <div class="summary-card card fade-in" style="animation-delay: 0.2s">
              <h3 class="summary-title">Resumen de Reserva</h3>

              <!-- Lista de asientos seleccionados -->
              <div v-if="asientosSeleccionados.length > 0" class="selected-seats-list">
                <div
                  v-for="asiento in asientosSeleccionados"
                  :key="asiento.id"
                  class="selected-seat-item"
                >
                  <div class="seat-info">
                    <span class="seat-number">{{ asiento.numero }}</span>
                    <span
                      :class="[
                        'seat-type',
                        asiento.tipo === 'vip' ? 'seat-type-vip' : 'seat-type-normal',
                      ]"
                    >
                      {{ asiento.tipo === 'vip' ? 'Pref' : 'Eco' }}
                    </span>
                  </div>
                  <button @click="removerAsiento(asiento)" class="remove-btn">
                    <svg viewBox="0 0 24 24" fill="none">
                      <path
                        d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z"
                        fill="currentColor"
                      />
                    </svg>
                  </button>
                </div>
              </div>

              <div v-else class="no-seats-selected">
                <svg viewBox="0 0 24 24" fill="none">
                  <path
                    d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z"
                    fill="currentColor"
                  />
                </svg>
                <p>No has seleccionado ningún asiento</p>
              </div>

              <!-- Desglose de precios -->
              <div class="price-breakdown">
                <div class="price-item">
                  <span>Asientos Preferenciales ({{ contarAsientosVIP() }})</span>
                  <span>${{ formatPrice(calcularPrecioVIP()) }}</span>
                </div>
                <div class="price-item">
                  <span>Asientos Económicos ({{ contarAsientosNormales() }})</span>
                  <span>${{ formatPrice(calcularPrecioNormales()) }}</span>
                </div>
                <div class="price-divider"></div>
                <div class="price-item price-total">
                  <span>Total</span>
                  <span>${{ formatPrice(calcularTotal()) }}</span>
                </div>
              </div>

              <!-- Botón de continuar -->
              <button
                @click="continuarReserva"
                class="btn btn-primary btn-large"
                :disabled="asientosSeleccionados.length === 0"
              >
                Continuar
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="loading-card card">
        <p>{{ mensajeCarga }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'SeatSelectionView',
  components: {
    NavBar,
  },
  data() {
    return {
      vuelo: null,
      asientosVIP: [],
      asientosNormales: [],
      asientosSeleccionados: [],
      mensajeCarga: 'Cargando mapa de asientos...',

      // PRECIOS FIJOS SEGÚN REQUERIMIENTOS
      PRECIO_VIP: 850000,
      PRECIO_ECO: 235000,
      MAX_SILLAS: 3, // Requerimiento #4
    }
  },
  mounted() {
    if (window.pywebview) {
      this.cargarVueloBackend()
    } else {
      window.addEventListener('pywebviewready', () => {
        this.cargarVueloBackend()
      })
    }
  },
  methods: {
    cargarVueloBackend() {
      const vueloId = this.$route.params.id

      // Usamos buscarVuelos con el filtro ID para obtener la info
      window.pywebview.api
        .buscarVuelos({ id: vueloId })
        .then((response) => {
          if (response && response.length > 0) {
            this.vuelo = response[0]
            this.generarAsientos()
          } else {
            this.mensajeCarga = 'Vuelo no encontrado.'
          }
        })
        .catch((err) => {
          console.error(err)
          this.mensajeCarga = 'Error de conexión.'
        })
    },

    generarAsientos() {
      // Obtenemos capacidades desde el TXT (convertir a int)
      const capVip = parseInt(this.vuelo.asientosPref)
      const capEco = parseInt(this.vuelo.asientosEco)

      const asientosPorFila = 6 // Estándar tipo A320
      const letras = ['A', 'B', 'C', 'D', 'E', 'F']

      // --- GENERAR VIP ---
      // Calculamos filas necesarias basado en capacidad total
      const filasVIP = Math.ceil(capVip / asientosPorFila)

      for (let fila = 1; fila <= filasVIP; fila++) {
        for (let i = 0; i < asientosPorFila; i++) {
          // No crear más asientos que la capacidad real
          if (this.asientosVIP.length >= capVip) break

          this.asientosVIP.push({
            id: `VIP-${fila}${letras[i]}`,
            numero: `${fila}${letras[i]}`,
            tipo: 'vip',
            precio: this.PRECIO_VIP,
            // Simulamos ocupación aleatoria (esto debería venir del backend de reservas en una fase avanzada)
            ocupado: Math.random() < 0.2,
          })
        }
      }

      // --- GENERAR ECO ---
      const filasEco = Math.ceil(capEco / asientosPorFila)
      const filaInicioEco = filasVIP + 1

      for (let fila = filaInicioEco; fila < filaInicioEco + filasEco; fila++) {
        for (let i = 0; i < asientosPorFila; i++) {
          if (this.asientosNormales.length >= capEco) break

          this.asientosNormales.push({
            id: `ECO-${fila}${letras[i]}`,
            numero: `${fila}${letras[i]}`,
            tipo: 'normal', // Equivale a economica
            precio: this.PRECIO_ECO,
            ocupado: Math.random() < 0.3,
          })
        }
      }
    },

    estaSeleccionado(asientoId) {
      return this.asientosSeleccionados.some((a) => a.id === asientoId)
    },

    toggleAsiento(asiento) {
      if (asiento.ocupado) return

      const index = this.asientosSeleccionados.findIndex((a) => a.id === asiento.id)

      if (index !== -1) {
        // Deseleccionar
        this.asientosSeleccionados.splice(index, 1)
      } else {
        // Seleccionar (Validar máximo 3)
        if (this.asientosSeleccionados.length >= this.MAX_SILLAS) {
          alert(`Solo puedes seleccionar un máximo de ${this.MAX_SILLAS} sillas.`)
          return
        }
        this.asientosSeleccionados.push(asiento)
      }
    },

    removerAsiento(asiento) {
      const index = this.asientosSeleccionados.findIndex((a) => a.id === asiento.id)
      if (index !== -1) {
        this.asientosSeleccionados.splice(index, 1)
      }
    },

    contarAsientosVIP() {
      return this.asientosSeleccionados.filter((a) => a.tipo === 'vip').length
    },

    contarAsientosNormales() {
      return this.asientosSeleccionados.filter((a) => a.tipo === 'normal').length
    },

    calcularPrecioVIP() {
      return this.contarAsientosVIP() * this.PRECIO_VIP
    },

    calcularPrecioNormales() {
      return this.contarAsientosNormales() * this.PRECIO_ECO
    },

    calcularTotal() {
      return this.calcularPrecioVIP() + this.calcularPrecioNormales()
    },

    // Helper para formato moneda
    formatPrice(value) {
      return value.toLocaleString('es-CO')
    },

    volver() {
      this.$router.go(-1)
    },

    continuarReserva() {
      if (this.asientosSeleccionados.length === 0) return

      // Guardamos en localStorage para persistir entre vistas
      localStorage.setItem('asientosSeleccionados', JSON.stringify(this.asientosSeleccionados))
      localStorage.setItem('vueloReserva', JSON.stringify(this.vuelo))

      this.$router.push(`/pasajeros/${this.vuelo.id}`)
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/SeatSelection.css';
</style>
