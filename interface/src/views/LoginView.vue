<template>
  <!-- Vista de inicio de sesión -->
  <div class="login-view">
    <NavBar />

    <div class="login-container">
      <div class="login-card card fade-in">
        <!-- Header del formulario -->
        <div class="login-header">
          <svg
            class="login-icon"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z"
              fill="currentColor"
            />
          </svg>
          <h1 class="login-title">Iniciar Sesión</h1>
          <p class="login-subtitle">Accede a tu cuenta de AeroRed</p>
        </div>

        <!-- Mostrar errores si existen -->
        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>

        <!-- Formulario de login -->
        <form @submit.prevent="iniciarSesion" class="login-form">
          <div class="form-group">
            <label for="email" class="form-label">Correo Electrónico</label>
            <input
              type="email"
              id="email"
              v-model="email"
              class="form-input"
              placeholder="usuario@aerored.com"
              required
            />
          </div>

          <div class="form-group">
            <label for="password" class="form-label">Contraseña</label>
            <input
              type="password"
              id="password"
              v-model="password"
              class="form-input"
              placeholder="••••••••"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary btn-large">Iniciar Sesión</button>
        </form>

        <!-- Información de credenciales de prueba -->
        <div class="demo-credentials">
          <p class="demo-title">Credenciales de prueba:</p>
          <div class="demo-items">
            <div class="demo-item">
              <strong>Usuario Normal:</strong> usuario@aerored.com / usuario123
            </div>
            <div class="demo-item">
              <strong>Administrador:</strong> admin@aerored.com / admin123
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import usuariosData from '../data/usuarios.json'

export default {
  name: 'LoginView',
  components: {
    NavBar,
  },
  data() {
    return {
      // Campos del formulario
      email: '',
      password: '',
      error: null,
    }
  },
  methods: {
    // Método para iniciar sesión
    iniciarSesion() {
      this.error = null

      // Buscar usuario en los datos quemados
      const usuario = usuariosData.find(
        (u) => u.email === this.email && u.password === this.password,
      )

      if (usuario) {
        // Guardar usuario en localStorage
        localStorage.setItem('usuarioActual', JSON.stringify(usuario))

        // Redirigir al dashboard (mismo para ambos tipos de usuario por ahora)
        this.$router.push('/dashboard')
      } else {
        // Mostrar error si las credenciales son incorrectas
        this.error = 'Correo o contraseña incorrectos'
      }
    },
  },
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 50%, #fff 100%);
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
}

.login-card {
  width: 100%;
  max-width: 450px;
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-icon {
  width: 64px;
  height: 64px;
  color: var(--primary-red);
  margin-bottom: 16px;
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 8px;
}

.login-subtitle {
  color: var(--text-light);
  font-size: 16px;
}

.login-form {
  margin-bottom: 24px;
}

.btn-large {
  width: 100%;
  padding: 14px 20px;
  font-size: 18px;
  margin-top: 8px;
}

.demo-credentials {
  background-color: var(--light-gray);
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid var(--primary-red);
}

.demo-title {
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 12px;
}

.demo-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.demo-item {
  font-size: 14px;
  color: var(--text-light);
}

.demo-item strong {
  color: var(--text-dark);
}
</style>
