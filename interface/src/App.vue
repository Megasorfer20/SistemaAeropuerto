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
#app {
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>