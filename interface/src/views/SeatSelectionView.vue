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
            <span class="info-value">{{ vuelo.numeroVuelo }}</span>
          </div>
          <div class="flight-info-item">
            <span class="info-label">Ruta</span>
            <span class="info-value">{{ vuelo.origen }} → {{ vuelo.destino }}</span>
          </div>
          <div class="flight-info-item">
            <span class="info-label">Fecha</span>
            <span class="info-value">{{ formatearFecha(vuelo.fechaSalida) }}</span>
          </div>
          <div class="flight-info-item">
            <span class="info-label">Asientos Seleccionados</span>
            <span class="info-value info-highlight">{{ asientosSeleccionados.length }}</span>
          </div>
        </div>

        <div class="seat-layout-container">
          <!-- Panel de selección de asientos -->
          <div class="seat-map-section card fade-in" style="animation-delay: 0.1s">
            <div class="seat-map-header">
              <h2 class="section-title">Selecciona tus Asientos</h2>

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
                <h3>Clase VIP</h3>
                <span class="cabin-price">+${{ configAsientos.vip.precio }}</span>
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
                  :disabled="asiento.ocupado"
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
                <h3>Clase Normal</h3>
                <span class="cabin-price">Incluido</span>
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
                  :disabled="asiento.ocupado"
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
                      {{ asiento.tipo === 'vip' ? 'VIP' : 'Normal' }}
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
                  <span>Precio base</span>
                  <span>${{ vuelo.precio.toFixed(2) }}</span>
                </div>
                <div class="price-item">
                  <span>Asientos VIP ({{ contarAsientosVIP() }})</span>
                  <span>${{ calcularPrecioVIP().toFixed(2) }}</span>
                </div>
                <div class="price-item">
                  <span>Asientos Normales ({{ contarAsientosNormales() }})</span>
                  <span>${{ calcularPrecioNormales().toFixed(2) }}</span>
                </div>
                <div class="price-divider"></div>
                <div class="price-item price-total">
                  <span>Total</span>
                  <span>${{ calcularTotal().toFixed(2) }}</span>
                </div>
              </div>

              <!-- Botón de continuar -->
              <button
                @click="continuarReserva"
                class="btn btn-primary btn-large"
                :disabled="asientosSeleccionados.length === 0"
              >
                Continuar con la Reserva
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="loading-card card">
        <p>Cargando información del vuelo...</p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import vuelosData from '../data/vuelos.json'
import configAsientosData from '../data/asientos.json'

export default {
  name: 'SeatSelectionView',
  components: {
    NavBar,
  },
  data() {
    return {
      // Vuelo actual
      vuelo: null,
      // Configuración de asientos desde JSON
      configAsientos: configAsientosData,
      // Asientos generados dinámicamente
      asientosVIP: [],
      asientosNormales: [],
      // Asientos seleccionados por el usuario
      asientosSeleccionados: [],
    }
  },
  mounted() {
    // Cargar datos al montar
    this.cargarVuelo()
    this.generarAsientos()
  },
  methods: {
    // Cargar información del vuelo
    cargarVuelo() {
      const vueloId = parseInt(this.$route.params.id)
      this.vuelo = vuelosData.find((v) => v.id === vueloId)
    },
    // Generar asientos dinámicamente según configuración
    generarAsientos() {
      const letras = ['A', 'B', 'C', 'D', 'E', 'F']

      // Generar asientos VIP
      const filasVIP = this.configAsientos.vip.filas
      const asientosPorFilaVIP = this.configAsientos.vip.asientosPorFila

      for (let fila = 1; fila <= filasVIP; fila++) {
        for (let i = 0; i < asientosPorFilaVIP; i++) {
          this.asientosVIP.push({
            id: `VIP-${fila}${letras[i]}`,
            numero: `${fila}${letras[i]}`,
            fila: fila,
            letra: letras[i],
            tipo: 'vip',
            precio: this.configAsientos.vip.precio,
            // Simular algunos asientos ocupados aleatoriamente
            ocupado: Math.random() < 0.3,
          })
        }
      }

      // Generar asientos normales
      const filasNormales = this.configAsientos.normal.filas
      const asientosPorFilaNormal = this.configAsientos.normal.asientosPorFila
      const filaInicio = filasVIP + 1

      for (let fila = filaInicio; fila < filaInicio + filasNormales; fila++) {
        for (let i = 0; i < asientosPorFilaNormal; i++) {
          this.asientosNormales.push({
            id: `NORMAL-${fila}${letras[i]}`,
            numero: `${fila}${letras[i]}`,
            fila: fila,
            letra: letras[i],
            tipo: 'normal',
            precio: this.configAsientos.normal.precio,
            // Simular algunos asientos ocupados aleatoriamente
            ocupado: Math.random() < 0.4,
          })
        }
      }
    },
    // Verificar si un asiento está seleccionado
    estaSeleccionado(asientoId) {
      return this.asientosSeleccionados.some((a) => a.id === asientoId)
    },
    // Alternar selección de asiento
    toggleAsiento(asiento) {
      if (asiento.ocupado) return

      const index = this.asientosSeleccionados.findIndex((a) => a.id === asiento.id)

      if (index !== -1) {
        // Remover asiento si ya está seleccionado
        this.asientosSeleccionados.splice(index, 1)
      } else {
        // Agregar asiento a la selección
        this.asientosSeleccionados.push(asiento)
      }
    },
    // Remover un asiento específico
    removerAsiento(asiento) {
      const index = this.asientosSeleccionados.findIndex((a) => a.id === asiento.id)
      if (index !== -1) {
        this.asientosSeleccionados.splice(index, 1)
      }
    },
    // Contar asientos VIP seleccionados
    contarAsientosVIP() {
      return this.asientosSeleccionados.filter((a) => a.tipo === 'vip').length
    },
    // Contar asientos normales seleccionados
    contarAsientosNormales() {
      return this.asientosSeleccionados.filter((a) => a.tipo === 'normal').length
    },
    // Calcular precio de asientos VIP
    calcularPrecioVIP() {
      return this.contarAsientosVIP() * this.configAsientos.vip.precio
    },
    // Calcular precio de asientos normales
    calcularPrecioNormales() {
      return this.contarAsientosNormales() * this.vuelo.precio
    },
    // Calcular precio total
    calcularTotal() {
      return this.calcularPrecioVIP() + this.calcularPrecioNormales()
    },
    // Formatear fecha
    formatearFecha(fecha) {
      const date = new Date(fecha + 'T00:00:00')
      return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      })
    },
    // Volver atrás
    volver() {
      this.$router.go(-1)
    },
    // Continuar con la reserva
    continuarReserva() {
      if (this.asientosSeleccionados.length === 0) return

      // Guardar asientos seleccionados en localStorage para la siguiente vista
      localStorage.setItem('asientosSeleccionados', JSON.stringify(this.asientosSeleccionados))
      localStorage.setItem('vueloReserva', JSON.stringify(this.vuelo))

      // Navegar a la página de información de pasajeros
      this.$router.push(`/pasajeros/${this.vuelo.id}`)
    },
  },
}
</script>

<style scoped>
.seat-selection-view {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.seat-container {
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

.seat-content {
  max-width: 1400px;
  margin: 0 auto;
}

/* Flight Info Bar */
.flight-info-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  padding: 24px;
  margin-bottom: 24px;
}

.flight-info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: var(--text-light);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-dark);
}

.info-highlight {
  color: var(--primary-red);
}

/* Seat Layout */
.seat-layout-container {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 24px;
}

.seat-map-section {
  padding: 32px;
}

.seat-map-header {
  margin-bottom: 32px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 16px;
}

/* Legend */
.seat-legend {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-dark);
}

.legend-box {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 2px solid var(--border-gray);
}

/* Cabin Sections */
.cabin-section {
  margin-bottom: 32px;
}

.cabin-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--border-gray);
}

.cabin-header svg {
  width: 24px;
  height: 24px;
  color: var(--primary-red);
}

.cabin-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-dark);
  flex: 1;
}

.cabin-price {
  font-size: 16px;
  font-weight: 700;
  color: var(--primary-red);
}

.cabin-divider {
  height: 2px;
  background: linear-gradient(
    to right,
    transparent,
    var(--border-gray) 20%,
    var(--border-gray) 80%,
    transparent
  );
  margin: 32px 0;
}

/* Seats Grid */
.seats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
  max-width: 600px;
}

.seat-button {
  aspect-ratio: 1;
  border: 2px solid var(--border-gray);
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.seat-available {
  background-color: var(--white);
  color: var(--text-dark);
  border-color: var(--border-gray);
}

.seat-available:hover {
  background-color: var(--light-gray);
  border-color: var(--primary-red);
  transform: scale(1.05);
}

.seat-occupied {
  background-color: #f3f4f6;
  color: #9ca3af;
  border-color: #d1d5db;
  cursor: not-allowed;
}

.seat-selected {
  background-color: var(--primary-red);
  color: var(--white);
  border-color: var(--primary-red);
  transform: scale(1.05);
}

/* Summary Section */
.summary-section {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.summary-card {
  padding: 24px;
}

.summary-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 20px;
}

.selected-seats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
  max-height: 300px;
  overflow-y: auto;
}

.selected-seat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background-color: var(--light-gray);
  border-radius: 8px;
}

.seat-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.seat-number {
  font-weight: 700;
  color: var(--text-dark);
  font-size: 16px;
}

.seat-type {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.seat-type-vip {
  background-color: #fee2e2;
  color: var(--primary-red);
}

.seat-type-normal {
  background-color: #dbeafe;
  color: #1e40af;
}

.remove-btn {
  width: 28px;
  height: 28px;
  padding: 0;
  background: none;
  border: none;
  color: var(--text-light);
  cursor: pointer;
  transition: color 0.3s ease;
}

.remove-btn:hover {
  color: var(--primary-red);
}

.remove-btn svg {
  width: 20px;
  height: 20px;
}

.no-seats-selected {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-light);
}

.no-seats-selected svg {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.no-seats-selected p {
  font-size: 14px;
}

/* Price Breakdown */
.price-breakdown {
  margin-bottom: 20px;
}

.price-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  font-size: 14px;
  color: var(--text-dark);
}

.price-divider {
  height: 1px;
  background-color: var(--border-gray);
  margin: 8px 0;
}

.price-total {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-red);
}

.btn-large {
  width: 100%;
  padding: 14px 24px;
  font-size: 16px;
}

.loading-card {
  padding: 60px;
  text-align: center;
  color: var(--text-light);
}

/* Responsive */
@media (max-width: 1024px) {
  .seat-layout-container {
    grid-template-columns: 1fr;
  }

  .summary-section {
    position: static;
  }
}

@media (max-width: 640px) {
  .seats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }

  .seat-button {
    font-size: 12px;
  }

  .flight-info-bar {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
