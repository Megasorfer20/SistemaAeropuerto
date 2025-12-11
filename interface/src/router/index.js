// Configuración del router de Vue para la aplicación de aeropuerto
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue' // Nueva vista
import DashboardView from '../views/DashboardView.vue'
import FlightSelectionView from '../views/FlightSelectionView.vue'
import SeatSelectionView from '../views/SeatSelectionView.vue'
import PassengerInfoView from '../views/PassengerInfoView.vue'
import ConfirmationView from '../views/ConfirmationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/registro', // Nueva Ruta
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      // Requiere autenticación
      meta: { requiresAuth: true },
    },
    {
      path: '/vuelo/:id',
      name: 'flight-details',
      component: FlightSelectionView,
    },
    {
      path: '/asientos/:id',
      name: 'seat-selection',
      component: SeatSelectionView,
      // Requiere autenticación para reservar
      meta: { requiresAuth: true },
    },
    {
      path: '/pasajeros/:id',
      name: 'passenger-info',
      component: PassengerInfoView,
      // Requiere autenticación
      meta: { requiresAuth: true },
    },
    {
      path: '/confirmacion',
      name: 'confirmation',
      component: ConfirmationView,
      // Requiere autenticación
      meta: { requiresAuth: true },
    },
  ],
})

// Guard de navegación para rutas que requieren autenticación
router.beforeEach((to, from, next) => {
  const usuarioActual = JSON.parse(localStorage.getItem('usuarioActual'))

  // Si la ruta requiere autenticación y no hay usuario logueado
  if (to.meta.requiresAuth && !usuarioActual) {
    next('/login')
  } else {
    next()
  }
})

export default router
