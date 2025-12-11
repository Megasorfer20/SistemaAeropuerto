<template>
  <div class="login-view">
    <NavBar />

    <div class="login-container">
      <div class="login-card card fade-in">
        <div class="login-header">
          <svg class="login-icon" viewBox="0 0 24 24" fill="none">
            <path d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z" fill="currentColor"/>
          </svg>
          <h1 class="login-title">Iniciar Sesión</h1>
          <p class="login-subtitle">Accede a tu cuenta de AeroRed</p>
        </div>

        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>

        <form @submit.prevent="iniciarSesion" class="login-form">
          <div class="form-group">
            <label for="doc" class="form-label">Número de Documento</label>
            <input
              type="text"
              id="doc"
              v-model="doc"
              class="form-input"
              placeholder="Ej. 1001"
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

          <button type="submit" class="btn btn-primary btn-large" :disabled="cargando">
            {{ cargando ? 'Verificando...' : 'Iniciar Sesión' }}
          </button>
        </form>

        <!-- Información de credenciales de prueba -->
        <div class="demo-credentials">
          <p class="demo-title">Credenciales de prueba:</p>
          <div class="demo-items">
            <div class="demo-item"><strong>Cliente:</strong> Doc: 2002 / Clave: 12345</div>
            <div class="demo-item"><strong>Admin:</strong> Doc: 1001 / Clave: 12345</div>
          </div>
        </div>
        
        <div style="text-align: center; margin-top: 15px;">
            <router-link to="/registro" style="color: var(--primary-red); text-decoration: none;">¿No tienes cuenta? Regístrate</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'LoginView',
  components: { NavBar },
  data() {
    return {
      doc: '',
      password: '',
      error: null,
      cargando: false
    }
  },
  methods: {
    // Método para iniciar sesión
    iniciarSesion() {
      this.error = null
      this.cargando = true

      if (window.pywebview) {
        window.pywebview.api.login(this.doc, this.password)
          .then(response => {
            this.cargando = false
            if (response.success) {
              // Guardar usuario en localStorage
              const usuarioData = { ...response.user, doc: this.doc } // Agregamos el doc por si acaso
              localStorage.setItem('usuarioActual', JSON.stringify(usuarioData))
              
              // Disparar evento para que NavBar se actualice
              window.dispatchEvent(new Event('user-login'))

              this.$router.push('/dashboard')
            } else {
              this.error = response.message
            }
          })
          .catch(err => {
            this.cargando = false
            console.error(err)
            this.error = "Error de conexión con el servidor."
          })
      } else {
        // Fallback solo para pruebas visuales si no está corriendo python
        this.cargando = false
        this.error = "PyWebview no detectado. Ejecuta desde Python."
      }
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/LoginView.css';
</style>
