import { createApp } from 'vue'
import App from './App.vue'

// Import des styles dans l'ordre
import './assets/style.css'           // Styles de base
import './assets/gaming-styles.css'   // Styles gaming
import './assets/realDataStyles.css'  // Styles pour les données scrappées

// Créer et monter l'application
const app = createApp(App)
app.mount('#app')

// Configuration pour le développement
if (process.env.NODE_ENV === 'development') {
  console.log('🎮 Fandom Scraper - Mode Développement')
  console.log('🚀 Gaming interface activée')
  console.log('📊 Données scrappées chargées')
}