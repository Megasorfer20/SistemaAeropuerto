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

    <div class="container flights-section">
      <!-- Sección de filtros (Restaurada completa) -->
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

          <!-- Filtro Día (Restaurado) -->
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

          <!-- Filtro Hora (Restaurado) -->
          <div class="filter-group">
            <label class="form-label">Hora Salida (Desde - Hasta)</label>
            <div style="display: flex; gap: 5px">
              <input type="time" v-model="filtros.horaInicio" class="form-input" />
              <input type="time" v-model="filtros.horaFin" class="form-input" />
            </div>
          </div>

          <!-- Botones de Filtro -->
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

        <!-- PAGINACIÓN SUPERIOR (Restaurada) -->
        <div v-if="totalPages > 1" class="pagination-container">
          <button
            @click="cambiarPagina(currentPage - 1)"
            :disabled="currentPage === 1"
            class="btn-page"
          >
            &lt; Anterior
          </button>
          <span class="page-info">Página {{ currentPage }} de {{ totalPages }}</span>
          <button
            @click="cambiarPagina(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="btn-page"
          >
            Siguiente &gt;
          </button>
        </div>

        <!-- Grid de tarjetas -->
        <div v-if="vuelos.length > 0" class="flights-grid">
          <div
            v-for="(vuelo, index) in vuelosPaginados"
            :key="vuelo.id"
            class="flight-card card fade-in"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <!-- Header -->
            <div class="flight-header">
              <div class="flight-number">
                <span style="color: var(--primary-red)">✈</span>
                <span>{{ vuelo.id }}</span>
              </div>
              <div class="flight-route-simple">{{ vuelo.origen }} ➝ {{ vuelo.destino }}</div>
            </div>

            <!-- Ruta y Hora -->
            <div class="flight-route">
              <div class="route-point">
                <div class="route-label">Día Salida</div>
                <div class="route-value">{{ vuelo.fechaDiaSalida }}</div>
              </div>

              <div class="route-line">
                <span style="color: #ccc">--------</span>
              </div>

              <div class="route-point">
                <div class="route-label">Hora Salida</div>
                <div class="route-value" style="color: var(--primary-red); font-weight: bold">
                  {{ vuelo.fechaHoraSalida }}
                </div>
              </div>
            </div>

            <!-- Información Asientos (Texto corregido) -->
            <div class="flight-info">
              <div class="info-item">
                <span style="font-weight: 600">Económico:</span> {{ vuelo.asientosEco }} sillas
              </div>
              <div class="info-item">
                <span style="font-weight: 600">Preferencial:</span> {{ vuelo.asientosPref }} sillas
              </div>
            </div>

            <!-- BOTONES DE ACCIÓN (Lógica Admin vs Usuario) -->
            <div class="flight-actions">
              <!-- OPCIONES DE ADMIN -->
              <template v-if="esAdmin">
                <button @click="abrirModalEdicion(vuelo)" class="btn btn-outline">Editar</button>
                <button
                  @click="eliminarVuelo(vuelo.id)"
                  class="btn btn-primary"
                  style="background: #dc2626; border-color: #dc2626"
                >
                  Eliminar
                </button>
              </template>

              <!-- OPCIONES DE USUARIO -->
              <template v-else>
                <button @click="verDetalles(vuelo.id)" class="btn btn-outline">Detalles</button>
                <button
                  @click="reservarVuelo(vuelo.id)"
                  class="btn btn-primary"
                  :disabled="!usuarioActual"
                >
                  {{ usuarioActual ? 'Reservar' : 'Login para Reservar' }}
                </button>
              </template>
            </div>
          </div>
        </div>

        <!-- PAGINACIÓN INFERIOR (Restaurada) -->
        <div v-if="totalPages > 1" class="pagination-container" style="margin-top: 30px">
          <button
            @click="cambiarPagina(currentPage - 1)"
            :disabled="currentPage === 1"
            class="btn-page"
          >
            &lt; Anterior
          </button>
          <span class="page-info">Página {{ currentPage }} de {{ totalPages }}</span>
          <button
            @click="cambiarPagina(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="btn-page"
          >
            Siguiente &gt;
          </button>
        </div>

        <!-- Mensaje sin resultados -->
        <div v-else-if="vuelos.length === 0" class="no-flights card">
          <h3>No se encontraron vuelos</h3>
          <p>Intenta ajustar tus filtros de búsqueda</p>
        </div>
      </div>
    </div>

    <!-- MODAL DE EDICIÓN (SOLO ADMIN) -->
    <div v-if="mostrarModalEdicion" class="modal-overlay">
      <div class="modal-card card">
        <h3>Editar Vuelo {{ vueloEnEdicion.codigo }}</h3>
        <form @submit.prevent="guardarEdicion" class="edit-form">
          <div class="form-group">
            <label>Origen</label>
            <input v-model="vueloEnEdicion.origen" class="form-input" required />
          </div>
          <div class="form-group">
            <label>Destino</label>
            <input v-model="vueloEnEdicion.destino" class="form-input" required />
          </div>
          <div class="form-group">
            <label>Fecha (AAAA-MM-DD)</label>
            <input type="text" v-model="vueloEnEdicion.dia" class="form-input" required />
          </div>
          <div class="form-group">
            <label>Hora (HH:MM)</label>
            <input type="time" v-model="vueloEnEdicion.hora" class="form-input" required />
          </div>
          <div class="form-group">
            <label>Sillas Económico</label>
            <input type="number" v-model="vueloEnEdicion.sillas_eco" class="form-input" required />
          </div>
          <div class="form-group">
            <label>Sillas Preferencial</label>
            <input type="number" v-model="vueloEnEdicion.sillas_pref" class="form-input" required />
          </div>

          <div class="modal-actions">
            <button type="button" @click="cerrarModal" class="btn btn-outline">Cancelar</button>
            <button type="submit" class="btn btn-primary">Guardar Cambios</button>
          </div>
        </form>
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
      vuelos: [],
      // Filtros completos
      filtros: {
        origen: '',
        destino: '',
        dia: 'TODOS',
        horaInicio: '',
        horaFin: '',
      },
      usuarioActual: null,
      // Paginación
      currentPage: 1,
      itemsPerPage: 10,
      // Modal Admin
      mostrarModalEdicion: false,
      vueloEnEdicion: {},
    }
  },
  computed: {
    esAdmin() {
      return this.usuarioActual?.tipo_usuario === 'Admin' || this.usuarioActual?.tipo === 'Admin'
    },
    totalPages() {
      return Math.ceil(this.vuelos.length / this.itemsPerPage)
    },
    vuelosPaginados() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.vuelos.slice(start, end)
    },
  },
  mounted() {
    this.cargarUsuario()

    if (window.pywebview) {
      this.cargarVuelosIniciales()
    } else {
      window.addEventListener('pywebviewready', () => {
        this.cargarVuelosIniciales()
      })
    }
  },
  methods: {
    cargarUsuario() {
      const usuario = localStorage.getItem('usuarioActual')
      if (usuario) {
        this.usuarioActual = JSON.parse(usuario)
      }
    },
    cargarVuelosIniciales() {
      window.pywebview.api
        .obtenerVuelosIniciales()
        .then((response) => {
          this.vuelos = response
          this.currentPage = 1
        })
        .catch((error) => console.error('Error python:', error))
    },
    filtrarVuelosEnBackend() {
      window.pywebview.api
        .buscarVuelos(this.filtros)
        .then((response) => {
          this.vuelos = response
          this.currentPage = 1
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
    cambiarPagina(nuevaPagina) {
      if (nuevaPagina >= 1 && nuevaPagina <= this.totalPages) {
        this.currentPage = nuevaPagina
        const listElement = document.querySelector('.flights-list')
        if (listElement) {
          listElement.scrollIntoView({ behavior: 'smooth' })
        }
      }
    },

    // --- ACCIONES DE USUARIO ---
    verDetalles(vueloId) {
      this.$router.push(`/vuelo/${vueloId}`)
    },
    reservarVuelo(vueloId) {
      if (!this.usuarioActual) {
        this.$router.push('/login')
      } else {
        this.$router.push(`/asientos/${vueloId}`)
      }
    },

    // --- ACCIONES DE ADMINISTRADOR ---
    eliminarVuelo(id) {
      if (confirm('¿Estás seguro de eliminar el vuelo ' + id + '?')) {
        window.pywebview.api.admin_eliminar_vuelo(id).then((res) => {
          if (res.success) {
            alert('Vuelo eliminado')
            this.cargarVuelosIniciales() // Recargar lista
          } else {
            alert('Error: ' + res.message)
          }
        })
      }
    },
    abrirModalEdicion(vuelo) {
      this.vueloEnEdicion = {
        codigo: vuelo.id,
        origen: vuelo.origen,
        destino: vuelo.destino,
        dia: vuelo.fechaDiaSalida,
        hora: vuelo.fechaHoraSalida,
        sillas_eco: vuelo.asientosEco,
        sillas_pref: vuelo.asientosPref,
      }
      this.mostrarModalEdicion = true
    },
    cerrarModal() {
      this.mostrarModalEdicion = false
      this.vueloEnEdicion = {}
    },
    guardarEdicion() {
      window.pywebview.api
        .admin_modificar_vuelo(this.vueloEnEdicion.codigo, this.vueloEnEdicion)
        .then((res) => {
          if (res.success) {
            alert('Vuelo modificado correctamente')
            this.cerrarModal()
            this.cargarVuelosIniciales() // Recargar lista
          } else {
            alert('Error: ' + res.message)
          }
        })
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/HomeView.css';
</style>
