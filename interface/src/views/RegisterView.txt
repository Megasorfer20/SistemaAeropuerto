<template>
  <div class="login-view">
    <!-- Reutilizamos clase de fondo -->
    <NavBar />

    <div class="login-container">
      <div class="login-card card fade-in">
        <div class="login-header">
          <h1 class="login-title">Crear Cuenta</h1>
          <p class="login-subtitle">Únete a AeroRed y empieza a viajar</p>
        </div>

        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>
        <div
          v-if="successMsg"
          class="alert alert-success"
          style="
            background-color: #d1fae5;
            color: #065f46;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
          "
        >
          {{ successMsg }}
        </div>

        <form @submit.prevent="registrarse" class="login-form">
          <div class="form-group">
            <label class="form-label">Nombre Completo</label>
            <input type="text" v-model="form.nombre" class="form-input" required />
          </div>

          <div class="form-group">
            <label class="form-label">Correo Electrónico</label>
            <input type="email" v-model="form.correo" class="form-input" required />
          </div>

          <div class="form-group">
            <label class="form-label">Número de Documento</label>
            <input type="text" v-model="form.numDoc" class="form-input" required />
          </div>

          <div class="form-group">
            <label class="form-label">Contraseña</label>
            <input type="password" v-model="form.password" class="form-input" required />
          </div>

          <button type="submit" class="btn btn-primary btn-large" :disabled="cargando">
            {{ cargando ? 'Registrando...' : 'Registrarse' }}
          </button>
        </form>

        <div style="text-align: center; margin-top: 15px">
          <router-link to="/login" style="color: var(--primary-red); text-decoration: none"
            >¿Ya tienes cuenta? Inicia sesión</router-link
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'RegisterView',
  components: { NavBar },
  data() {
    return {
      form: {
        nombre: '',
        correo: '',
        numDoc: '',
        password: '',
      },
      error: null,
      successMsg: null,
      cargando: false,
    }
  },
  methods: {
    registrarse() {
      this.error = null
      this.successMsg = null
      this.cargando = true

      if (window.pywebview) {
        // Enviamos los datos a Python
        window.pywebview.api
          .registro(this.form)
          .then((response) => {
            this.cargando = false
            if (response.success) {
              this.successMsg = 'Registro exitoso. Redirigiendo al login...'
              setTimeout(() => {
                this.$router.push('/login')
              }, 2000)
            } else {
              this.error = response.message
            }
          })
          .catch((err) => {
            this.cargando = false
            console.error(err)
            this.error = 'Error de conexión.'
          })
      } else {
        this.cargando = false
        this.error = 'PyWebview no detectado.'
      }
    },
  },
}
</script>

<style scoped>
@import '../assets/styles/LoginView.css';
</style>
