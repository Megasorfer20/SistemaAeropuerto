<template>
  <div class="dashboard-view">
    <NavBar />

    <div class="dashboard-container container">
      <div class="dashboard-header fade-in">
        <div>
          <h1 class="dashboard-title">Bienvenido, {{ usuarioActual?.nombre }}</h1>
          <p class="dashboard-subtitle">
            <span v-if="esAdmin" class="badge-admin">Administrador</span>
            <span v-else class="badge-user">Viajero Frecuente</span>
            Panel de Control
          </p>
        </div>
        <!-- Solo Cliente ve Millas -->
        <div v-if="!esAdmin" class="miles-display">
          <span class="miles-label">Mis Millas:</span>
          <span class="miles-value">{{ stats.millas }}</span>
        </div>
      </div>

      <!-- ESTADÍSTICAS GENERALES -->
      <div class="dashboard-grid">
        <div class="stat-card card fade-in" style="animation-delay: 0.1s">
          <div class="stat-icon stat-icon-blue">✈</div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.vuelos_activos }}</h3>
            <p class="stat-label">Vuelos Activos</p>
          </div>
        </div>
        <div class="stat-card card fade-in" style="animation-delay: 0.2s">
          <div class="stat-icon stat-icon-green">🌍</div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.destinos }}</h3>
            <p class="stat-label">Destinos</p>
          </div>
        </div>
      </div>

      <!-- ================= SECCIÓN ADMINISTRADOR ================= -->
      <div v-if="esAdmin" class="admin-section fade-in">
        
        <!-- Novedad: Panel de Acciones y Reportes -->
        <div class="admin-grid">
          <!-- Tarjeta 1: Agregar Vuelo (La que ya tenías, ligeramente ajustada) -->
          <div class="card form-card">
            <h2 class="section-title">Agregar Nuevo Vuelo</h2>
            <form @submit.prevent="crearVuelo" class="flight-form">
              <!-- ... (MANTÉN TUS INPUTS DE AGREGAR VUELO AQUÍ IGUAL QUE ANTES) ... -->
               <div class="form-grid">
                  <div class="form-group">
                    <label>Código Vuelo</label>
                    <input type="text" v-model="nuevoVuelo.codigo" class="form-input" required placeholder="Ej. AV999" />
                  </div>
                  <div class="form-group">
                    <label>Origen</label>
                    <input type="text" v-model="nuevoVuelo.origen" class="form-input" required />
                  </div>
                  <div class="form-group">
                    <label>Destino</label>
                    <input type="text" v-model="nuevoVuelo.destino" class="form-input" required />
                  </div>
                  <div class="form-group">
                    <label>Fecha</label>
                    <input type="date" v-model="nuevoVuelo.dia" class="form-input" required />
                  </div>
                  <div class="form-group">
                    <label>Hora</label>
                    <input type="time" v-model="nuevoVuelo.hora" class="form-input" required />
                  </div>
                  <div class="form-group">
                    <label>Sillas Eco</label>
                    <input type="number" v-model="nuevoVuelo.sillas_eco" class="form-input" required min="10" />
                  </div>
                  <div class="form-group">
                    <label>Sillas Pref</label>
                    <input type="number" v-model="nuevoVuelo.sillas_pref" class="form-input" required min="0" />
                  </div>
               </div>
              <button type="submit" class="btn btn-primary" style="margin-top: 20px">Publicar Vuelo</button>
            </form>
            <div v-if="mensajeAdmin" :class="['alert', mensajeError ? 'alert-error' : 'alert-success']" style="margin-top: 15px">
              {{ mensajeAdmin }}
            </div>
          </div>

          <!-- Tarjeta 2: Panel de Reportes (NUEVO) -->
          <div class="card report-card">
            <h2 class="section-title">Gestión de Reservas</h2>
            <p style="color: #666; margin-bottom: 20px;">
              Consulta la ocupación de los vuelos, sillas vendidas y ganancias estimadas.
            </p>
            <button @click="abrirReporte" class="btn btn-secondary full-width-btn">
              📊 Ver Reporte de Ocupación
            </button>
          </div>
        </div>
      </div>

      <!-- MODAL DE REPORTES (NUEVO - Pegar esto antes del cierre del div .dashboard-container) -->
      <div v-if="mostrarModalReporte" class="modal-overlay">
        <div class="modal-card card fade-in">
          <div class="modal-header">
            <h2>Reporte de Vuelos y Reservas</h2>
            <button @click="cerrarReporte" class="btn-close">✖</button>
          </div>

          <div class="table-container">
            <table class="report-table">
              <thead>
                <tr>
                  <th>Vuelo</th>
                  <th>Ruta</th>
                  <th>Fecha</th>
                  <th>Ocupación Eco</th>
                  <th>Ocupación VIP</th>
                  <th>Total Ingresos</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="vuelo in reporteData" :key="vuelo.codigo">
                  <td><strong>{{ vuelo.codigo }}</strong></td>
                  <td>{{ vuelo.origen }} ➝ {{ vuelo.destino }}</td>
                  <td>{{ vuelo.fecha }}</td>
                  
                  <!-- Mostrar ocupadas vs totales -->
                  <td>
                    <span :class="{'full-seat': vuelo.vendidas_eco === vuelo.total_eco}">
                      {{ vuelo.vendidas_eco }} / {{ vuelo.total_eco }}
                    </span>
                  </td>
                  <td>
                    <span :class="{'full-seat': vuelo.vendidas_pref === vuelo.total_pref}">
                      {{ vuelo.vendidas_pref }} / {{ vuelo.total_pref }}
                    </span>
                  </td>
                  
                  <td style="color: var(--primary-green); font-weight: bold;">
                    $ {{ formatearDinero(vuelo.ingresos) }}
                  </td>
                </tr>
                <tr v-if="reporteData.length === 0">
                  <td colspan="6" style="text-align: center; padding: 20px;">No hay vuelos registrados.</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="modal-footer">
             <button @click="cerrarReporte" class="btn btn-primary">Cerrar</button>
          </div>
        </div>
      </div>

      <!-- ================= SECCIÓN USUARIO ================= -->
      <div v-else class="user-section fade-in">
        <h2 class="section-title">Mis Reservas</h2>

        <div v-if="reservas.length > 0" class="reservations-list">
          <!-- Aquí iterarías las reservas -->
          <p>Lista de reservas...</p>
        </div>
        <div v-else class="no-data card">
          <p>No tienes reservas activas en este momento.</p>
          <button @click="$router.push('/')" class="btn btn-outline" style="margin-top: 10px">
            Buscar Vuelos
          </button>
        </div>

        <!-- Acciones de Usuario -->
        <div class="quick-actions card" style="margin-top: 20px">
          <h3>Acciones</h3>
          <div class="actions-grid">
            <button class="action-btn" @click="$router.push('/checkin-list')">
              <!-- Ruta futura -->
              <div>
                <h3>Realizar Check-in</h3>
                <p>Disponible 24h antes del vuelo</p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'DashboardView',
  components: { NavBar },
  data() {
    return {
      mostrarModalReporte: false,
      reporteData: [],
      usuarioActual: null,
      stats: { vuelos_activos: 0, destinos: 0, millas: 0 },
      reservas: [],

      // Admin Form Data
      nuevoVuelo: {
        codigo: '',
        origen: '',
        destino: '',
        dia: '',
        hora: '',
        sillas_eco: 50,
        sillas_pref: 10,
      },
      mensajeAdmin: '',
      mensajeError: false,
    }
  },
  computed: {
    esAdmin() {
      return this.usuarioActual?.tipo_usuario === 'Admin' || this.usuarioActual?.tipo === 'Admin'
    },
  },
  mounted() {
    this.cargarUsuario()
    if (window.pywebview) {
      this.cargarDatosBackend()
    }
  },
  methods: {
      abrirReporte() {
      // Llamamos al backend (API.py -> adminGetReporte)
      // Enviamos un diccionario vacío {} para traer todos los vuelos
      window.pywebview.api.adminGetReporte({}).then((response) => {
        if (response && response.ventas_por_vuelo) {
          this.reporteData = response.ventas_por_vuelo
          this.mostrarModalReporte = true
        } else {
          alert("No se pudo cargar el reporte.")
        }
      }).catch(err => {
         console.error(err)
         alert("Error conectando con el sistema.")
      })
    },

    cerrarReporte() {
      this.mostrarModalReporte = false
    },

    formatearDinero(valor) {
       return Number(valor).toLocaleString('es-CO');
    },
    cargarUsuario() {
      const u = localStorage.getItem('usuarioActual')
      if (u) this.usuarioActual = JSON.parse(u)
    },
    cargarDatosBackend() {
      // 1. Stats
      window.pywebview.api.obtener_dashboard_stats().then((res) => (this.stats = res))
      // 2. Reservas (si existen implementadas)
      window.pywebview.api.obtener_mis_reservas().then((res) => (this.reservas = res))
    },
    crearVuelo() {
      this.mensajeAdmin = ''
      this.mensajeError = false

      window.pywebview.api.admin_agregar_vuelo(this.nuevoVuelo).then((res) => {
        if (res.success) {
          this.mensajeAdmin = 'Vuelo creado correctamente.'
          // Limpiar form
          this.nuevoVuelo = {
            codigo: '',
            origen: '',
            destino: '',
            dia: '',
            hora: '',
            sillas_eco: 50,
            sillas_pref: 10,
          }
          this.cargarDatosBackend() // Refrescar stats
        } else {
          this.mensajeAdmin = res.message
          this.mensajeError = true
        }
      })
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/DashboardView.css';


</style>
