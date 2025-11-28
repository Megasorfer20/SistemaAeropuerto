<template>
  <!-- Barra de navegación principal con branding de aerolínea -->
  <nav class="navbar">
    <div class="container navbar-content">
      <!-- Logo y nombre de la aerolínea -->
      <div class="navbar-brand" @click="irAInicio">
        <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z"
            fill="currentColor"
          />
        </svg>
        <span class="brand-name">AeroRed</span>
      </div>

      <!-- Enlaces de navegación -->
      <div class="navbar-links">
        <a href="#" class="nav-link" @click.prevent="irAInicio">Inicio</a>
        <a href="#" class="nav-link">Mis Vuelos</a>

        <!-- Mostrar nombre de usuario o botón de login -->
        <div v-if="usuarioActual" class="user-menu">
          <span class="user-name">{{ usuarioActual.nombre }}</span>
          <button @click="cerrarSesion" class="btn btn-outline btn-sm">Cerrar Sesión</button>
        </div>
        <button v-else @click="irALogin" class="btn btn-primary">Iniciar Sesión</button>
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
  },
  methods: {
    // Cargar información del usuario desde localStorage
    cargarUsuario() {
      const usuario = localStorage.getItem('usuarioActual')
      if (usuario) {
        this.usuarioActual = JSON.parse(usuario)
      }
    },
    // Navegar a la página de inicio
    irAInicio() {
      this.$router.push('/')
    },
    // Navegar a la página de login
    irALogin() {
      this.$router.push('/login')
    },
    // Cerrar sesión del usuario
    cerrarSesion() {
      localStorage.removeItem('usuarioActual')
      this.usuarioActual = null
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
.navbar {
  background-color: var(--white);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.navbar-brand:hover {
  transform: scale(1.05);
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: var(--primary-red);
}

.brand-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-red);
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-link {
  color: var(--text-dark);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: var(--primary-red);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  font-weight: 600;
  color: var(--text-dark);
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}
</style>
