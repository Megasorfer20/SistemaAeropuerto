<template>
  <!-- Dashboard para usuarios autenticados (normal y admin) -->
  <div class="dashboard-view">
    <NavBar />

    <div class="dashboard-container container">
      <!-- Header del dashboard con saludo personalizado -->
      <div class="dashboard-header fade-in">
        <div>
          <h1 class="dashboard-title">Bienvenido, {{ usuarioActual?.nombre }}</h1>
          <p class="dashboard-subtitle">
            <span v-if="usuarioActual?.tipo === 'admin'" class="badge-admin">Administrador</span>
            <span v-else class="badge-user">Usuario</span>
            Panel de Control
          </p>
        </div>
      </div>

      <!-- Grid de tarjetas con información -->
      <div class="dashboard-grid">
        <!-- Card de reservas -->
        <div class="stat-card card fade-in" style="animation-delay: 0.1s">
          <div class="stat-icon stat-icon-red">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M9 2C7.89543 2 7 2.89543 7 4V20C7 21.1046 7.89543 22 9 22H18C19.1046 22 20 21.1046 20 20V7.41421C20 7.01639 19.842 6.63486 19.5607 6.35355L16.6464 3.43934C16.3651 3.15804 15.9836 3 15.5858 3H9ZM9 4H15L18 7V20H9V4Z"
                fill="currentColor"
              />
            </svg>
          </div>
          <div class="stat-content">
            <h3 class="stat-value">0</h3>
            <p class="stat-label">Reservas Activas</p>
          </div>
        </div>

        <!-- Card de vuelos disponibles -->
        <div class="stat-card card fade-in" style="animation-delay: 0.2s">
          <div class="stat-icon stat-icon-blue">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z"
                fill="currentColor"
              />
            </svg>
          </div>
          <div class="stat-content">
            <h3 class="stat-value">6</h3>
            <p class="stat-label">Vuelos Disponibles</p>
          </div>
        </div>

        <!-- Card de destinos (solo admin puede ver más detalles) -->
        <div class="stat-card card fade-in" style="animation-delay: 0.3s">
          <div class="stat-icon stat-icon-green">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M12 2C8.13 2 5 5.13 5 9C5 14.25 12 22 12 22C12 22 19 14.25 19 9C19 5.13 15.87 2 12 2ZM12 11.5C10.62 11.5 9.5 10.38 9.5 9C9.5 7.62 10.62 6.5 12 6.5C13.38 6.5 14.5 7.62 14.5 9C14.5 10.38 13.38 11.5 12 11.5Z"
                fill="currentColor"
              />
            </svg>
          </div>
          <div class="stat-content">
            <h3 class="stat-value">6</h3>
            <p class="stat-label">Destinos</p>
          </div>
        </div>
      </div>

      <!-- Acciones rápidas -->
      <div class="quick-actions card fade-in" style="animation-delay: 0.4s">
        <h2 class="section-title">Acciones Rápidas</h2>
        <div class="actions-grid">
          <button @click="irAVuelos" class="action-btn">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M15.5 14H14.71L14.43 13.73C15.41 12.59 16 11.11 16 9.5C16 5.91 13.09 3 9.5 3C5.91 3 3 5.91 3 9.5C3 13.09 5.91 16 9.5 16C11.11 16 12.59 15.41 13.73 14.43L14 14.71V15.5L19 20.49L20.49 19L15.5 14ZM9.5 14C7.01 14 5 11.99 5 9.5C5 7.01 7.01 5 9.5 5C11.99 5 14 7.01 14 9.5C14 11.99 11.99 14 9.5 14Z"
                fill="currentColor"
              />
            </svg>
            <div>
              <h3>Buscar Vuelos</h3>
              <p>Encuentra tu próximo destino</p>
            </div>
          </button>

          <button class="action-btn" disabled>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M19 3H5C3.89 3 3 3.9 3 5V19C3 20.1 3.89 21 5 21H19C20.11 21 21 20.1 21 19V5C21 3.9 20.11 3 19 3ZM19 19H5V5H19V19ZM17 12H12V17H10V12H7L12 7L17 12Z"
                fill="currentColor"
              />
            </svg>
            <div>
              <h3>Mis Reservas</h3>
              <p>Gestiona tus vuelos</p>
            </div>
          </button>
        </div>
      </div>

      <!-- Mensaje especial para administrador -->
      <div
        v-if="usuarioActual?.tipo === 'admin'"
        class="admin-notice card fade-in"
        style="animation-delay: 0.5s"
      >
        <div class="admin-notice-content">
          <svg
            class="admin-icon"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M12 1L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 1ZM12 11.99H19C18.47 16.11 15.72 19.78 12 20.93V12H5V6.3L12 3.19V11.99Z"
              fill="currentColor"
            />
          </svg>
          <div>
            <h3>Panel de Administrador</h3>
            <p>
              Tienes acceso a funciones administrativas. Las características avanzadas se agregarán
              próximamente.
            </p>
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
  components: {
    NavBar,
  },
  data() {
    return {
      // Usuario actual obtenido desde localStorage
      usuarioActual: null,
    }
  },
  mounted() {
    // Cargar información del usuario al montar
    this.cargarUsuario()
  },
  methods: {
    // Cargar usuario desde localStorage
    cargarUsuario() {
      const usuario = localStorage.getItem('usuarioActual')
      if (usuario) {
        this.usuarioActual = JSON.parse(usuario)
      }
    },
    // Navegar a la página de búsqueda de vuelos
    irAVuelos() {
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/DashboardView.css';
</style>
