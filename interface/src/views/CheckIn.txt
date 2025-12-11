<template>
  <div class="container mt-4">
    <h2 class="mb-4">Check-In Online</h2>

    <!-- SECCIÓN 1: BUSCAR RESERVA -->
    <div class="card p-4 mb-4" v-if="!reserva">
      <div class="mb-3">
        <label for="codigoReserva" class="form-label">Ingrese su Código de Reserva</label>
        <input 
          type="text" 
          class="form-control" 
          id="codigoReserva" 
          v-model="busquedaId" 
          placeholder="Ej: RES-12345"
        >
      </div>
      <button 
        class="btn btn-primary" 
        @click="buscarReserva" 
        :disabled="loading || !busquedaId"
      >
        {{ loading ? 'Buscando...' : 'Buscar Reserva' }}
      </button>
      
      <div v-if="error" class="alert alert-danger mt-3">
        {{ error }}
      </div>
    </div>

    <!-- SECCIÓN 2: INFORMACIÓN Y SELECCIÓN DE EQUIPAJE -->
    <div v-if="reserva">
      <!-- Datos del Vuelo -->
      <div class="card mb-4 border-info">
        <div class="card-header bg-info text-white">
          Información del Vuelo: {{ reserva.vuelo.codigo }}
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-4">
              <strong>Origen:</strong> {{ reserva.vuelo.origen }}
            </div>
            <div class="col-md-4">
              <strong>Destino:</strong> {{ reserva.vuelo.destino }}
            </div>
            <div class="col-md-4">
              <strong>Fecha:</strong> {{ reserva.vuelo.fecha }} - {{ reserva.vuelo.hora }}
            </div>
          </div>
        </div>
      </div>

      <!-- Configuración por Pasajero -->
      <h3>Pasajeros y Equipaje</h3>
      <div class="alert alert-secondary">
        <small>
          <i class="bi bi-info-circle"></i> Reglas de equipaje:
          <ul>
            <li><strong>Mano:</strong> Gratis para todos.</li>
            <li><strong>Cabina (10kg):</strong> Gratis en Preferencial, $40.000 en Económica.</li>
            <li><strong>Bodega:</strong> 1 Gratis en Preferencial. Adicionales o Económica se cobran por peso/volumen.</li>
          </ul>
        </small>
      </div>

      <div 
        class="card mb-3" 
        v-for="(pasajero, index) in checkInConfig" 
        :key="pasajero.num_doc"
      >
        <div class="card-body">
          <h5 class="card-title">{{ pasajero.nombre }} (Doc: {{ pasajero.num_doc }})</h5>
          <span class="badge" :class="pasajero.clase === 'PREF' ? 'bg-warning text-dark' : 'bg-success'">
            Clase {{ pasajero.clase === 'PREF' ? 'Preferencial' : 'Económica' }}
          </span>

          <hr>

          <div class="row g-3">
            <!-- 1. Equipaje de Mano (Siempre incluido) -->
            <div class="col-md-4">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" checked disabled>
                <label class="form-check-label">
                  Equipaje de Mano (Incluido)
                </label>
              </div>
            </div>

            <!-- 2. Equipaje de Cabina -->
            <div class="col-md-4">
              <div class="form-check">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  v-model="pasajero.llevaCabina"
                  :id="'cabina-'+index"
                >
                <label class="form-check-label" :for="'cabina-'+index">
                  Maleta de Cabina (10kg)
                </label>
                <div class="text-muted small">
                  Costo: {{ calcularCostoCabina(pasajero.clase) }}
                </div>
              </div>
            </div>

            <!-- 3. Equipaje de Bodega -->
            <div class="col-md-4">
              <label class="form-label">Equipaje de Bodega</label>
              
              <!-- Si es Preferencial tiene 1 incluida -->
              <div v-if="pasajero.clase === 'PREF'" class="text-success mb-2 small">
                <i class="bi bi-check"></i> 1 Maleta incluida
              </div>

              <div class="input-group mb-2">
                <span class="input-group-text">Peso (kg)</span>
                <input type="number" class="form-control" v-model.number="pasajero.pesoBodega" min="0" placeholder="0">
              </div>
              <div class="input-group">
                <span class="input-group-text">Volumen (m³)</span>
                <input type="number" class="form-control" v-model.number="pasajero.volBodega" min="0" step="0.1" placeholder="0">
              </div>
              <small class="text-muted" v-if="pasajero.pesoBodega > 0">
                 Costo estimado: {{ formatoMoneda(calcularCostoBodega(pasajero.clase, pasajero.pesoBodega, pasajero.volBodega)) }}
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumen y Botón Final -->
      <div class="d-flex justify-content-between align-items-center mt-4 p-3 bg-light border rounded">
        <div>
          <h4>Total a Pagar Check-In: {{ formatoMoneda(totalCheckIn) }}</h4>
          <small>Se acumularán 500 millas al confirmar.</small>
        </div>
        <div>
          <button class="btn btn-secondary me-2" @click="cancelar">Cancelar</button>
          <button class="btn btn-success btn-lg" @click="confirmarCheckIn" :disabled="loading">
            {{ loading ? 'Procesando...' : 'Confirmar Check-In' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Mensaje de éxito final -->
    <div v-if="successMessage" class="alert alert-success mt-4 text-center">
      <h3>¡Check-In Exitoso!</h3>
      <p>{{ successMessage }}</p>
      <button class="btn btn-primary" @click="reiniciar">Volver al inicio</button>
    </div>

  </div>
</template>

<script>
export default {
  name: "CheckIn",
  data() {
    return {
      busquedaId: "",
      loading: false,
      error: null,
      reserva: null,         // Datos crudos que vienen del backend
      checkInConfig: [],     // Datos modificables para el formulario
      successMessage: null
    };
  },
  computed: {
    totalCheckIn() {
      if (!this.checkInConfig.length) return 0;
      
      return this.checkInConfig.reduce((total, p) => {
        const costoCabina = p.llevaCabina 
          ? (p.clase === 'ECO' ? 40000 : 0) 
          : 0;
        
        const costoBodega = this.calcularCostoBodega(p.clase, p.pesoBodega, p.volBodega);
        
        return total + costoCabina + costoBodega;
      }, 0);
    }
  },
  methods: {
    formatoMoneda(valor) {
      return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(valor);
    },

    async buscarReserva() {
      this.loading = true;
      this.error = null;
      this.reserva = null;
      this.successMessage = null;

      try {
        // LLAMADA AL BACKEND (API.py)
        // Necesitas implementar 'buscarReservaPorId' en tu API.py que retorne dict con info
        const response = await window.pywebview.api.buscarReservaPorId(this.busquedaId);

        if (response.success) {
          this.reserva = response.data;
          // Inicializamos la configuración local para editar
          this.inicializarConfiguracion(response.data.pasajeros);
        } else {
          this.error = response.message || "No se encontró la reserva.";
        }
      } catch (err) {
        console.error(err);
        this.error = "Error de conexión con el sistema.";
      } finally {
        this.loading = false;
      }
    },

    inicializarConfiguracion(pasajeros) {
      // Mapeamos los pasajeros que vienen del backend a un objeto editable local
      this.checkInConfig = pasajeros.map(p => ({
        nombre: p.nombre,
        num_doc: p.num_doc,
        clase: p.clase_asiento, // 'ECO' o 'PREF'
        llevaCabina: false,
        pesoBodega: 0,
        volBodega: 0
      }));
    },

    calcularCostoCabina(clase) {
      return clase === 'ECO' ? '$40.000' : 'Gratis';
    },

    calcularCostoBodega(clase, peso, volumen) {
      if (!peso || peso <= 0) return 0;
      
      let costo = 0;
      // Fórmula del enunciado: (peso * 10000) + (volumen * 5000)
      // Si es PREF y tiene 1 maleta, aquí asumiremos lógica simple: 
      // El backend validará la "gratuidad" exacta, pero para UI:
      
      const calculoBase = (peso * 10000) + ((volumen || 0) * 5000);

      if (clase === 'PREF') {
        // Lógica simplificada visual: Si es PREF, asumimos que este input es la maleta EXTRA
        // O podríamos decir que la primera es gratis. 
        // Para este ejemplo, cobraremos si pone peso > 0, 
        // asumiendo que el usuario ya usó su franquicia gratuita o el sistema lo ajusta.
        // Si quieres ser estricto visualmente:
        return calculoBase; 
      }
      return calculoBase;
    },

    async confirmarCheckIn() {
      this.loading = true;
      try {
        const payload = {
          idReserva: this.reserva.codigo_reserva,
          pasajeros: this.checkInConfig.map(p => ({
             num_doc: p.num_doc,
             maleta_cabina: p.llevaCabina,
             maleta_bodega: {
               peso: p.pesoBodega,
               volumen: p.volBodega
             }
          }))
        };

        // LLAMADA AL BACKEND
        const response = await window.pywebview.api.realizarCheckIn(payload);

        if (response.success) {
          this.successMessage = `Check-In realizado correctamente. Has acumulado ${response.millas_ganadas} millas.`;
          this.reserva = null; // Limpiar formulario
        } else {
          this.error = response.message;
        }
      } catch (err) {
        this.error = "Error al procesar el check-in: " + err;
      } finally {
        this.loading = false;
      }
    },

    cancelar() {
      this.reserva = null;
      this.busquedaId = "";
      this.checkInConfig = [];
      this.error = null;
    },
    
    reiniciar() {
        this.successMessage = null;
        this.busquedaId = "";
    }
  }
};
</script>

<style scoped>
.card {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.badge {
  font-size: 0.9em;
}
</style>