<template>
  <!-- Componente raíz de la aplicación -->
  <div id="app">
    <!-- El RouterView renderiza el componente de la ruta actual -->
    <RouterView />
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style scoped>
@import './assets/styles/main.css';
</style>