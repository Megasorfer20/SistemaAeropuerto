<template>
  <nav class="navbar">
    <div class="container navbar-content">
      <!-- Logo -->
      <div class="navbar-brand" @click="irAInicio">
        <svg class="logo-icon" viewBox="0 0 24 24" fill="none">
          <path
            d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z"
            fill="currentColor"
          />
        </svg>
        <span class="brand-name">AeroRed</span>
      </div>

      <!-- Links -->
      <div class="navbar-links">
        <a href="#" class="nav-link" @click.prevent="irAInicio">Inicio</a>
        <a href="#" class="nav-link" v-if="usuarioActual" @click.prevent="irADashboard"
          >Mi Dashboard</a
        >

        <!-- Menú de Usuario Logueado -->
        <div v-if="usuarioActual" class="user-menu">
          <span class="user-name">Hola, {{ usuarioActual.nombre }}</span>
          <button @click="cerrarSesion" class="btn btn-outline btn-sm">Cerrar Sesión</button>
        </div>

        <!-- Botones Login/Registro -->
        <div v-else class="auth-buttons">
          <button @click="irALogin" class="btn btn-outline btn-sm" style="margin-right: 10px">
            Login
          </button>
          <button @click="irARegistro" class="btn btn-primary btn-sm">Registro</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      // Usuario actualmente logueado
      usuarioActual: null,
    }
  },
  mounted() {
    // Cargar usuario desde localStorage al montar el componente
    this.cargarUsuario()
    // Escuchar cambios en localStorage para actualizar navbar dinámicamente
    window.addEventListener('storage', this.cargarUsuario)
    // Evento personalizado para login/logout dentro de la misma pestaña
    window.addEventListener('user-login', this.cargarUsuario)
    window.addEventListener('user-logout', this.cargarUsuario)
  },
  unmounted() {
    window.removeEventListener('storage', this.cargarUsuario)
    window.removeEventListener('user-login', this.cargarUsuario)
    window.removeEventListener('user-logout', this.cargarUsuario)
  },
  methods: {
    // Cargar información del usuario desde localStorage
    cargarUsuario() {
      const usuario = localStorage.getItem('usuarioActual')
      if (usuario) {
        this.usuarioActual = JSON.parse(usuario)
      } else {
        this.usuarioActual = null
      }
    },
    // Navegar a la página de inicio
    irAInicio() {
      this.$router.push('/')
    },
    irADashboard() {
      this.$router.push('/dashboard')
    },
    irALogin() {
      this.$router.push('/login')
    },
    irARegistro() {
      this.$router.push('/registro')
    },
    cerrarSesion() {
      localStorage.removeItem('usuarioActual')
      this.usuarioActual = null
      // Disparar evento para actualizar otros componentes si es necesario
      window.dispatchEvent(new Event('user-logout'))
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
  @import '../assets/styles/Navbar.css';
</style>
