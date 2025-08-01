<template>
  <div id="app" :class="appClasses">
    <!-- Loading global si nécessaire -->
    <Transition name="fade">
      <div v-if="isInitialLoading" class="app-loading">
        <div class="loading-content">
          <div class="loading-logo">
            <span class="logo-icon">⚔️</span>
            <h1 class="logo-text">Fandom Scraper</h1>
          </div>
          <div class="loading-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-ring spinner-ring-delay"></div>
          </div>
          <p class="loading-text">{{ loadingText }}</p>
          <div class="loading-progress">
            <div class="progress-bar" :style="{ width: loadingProgress + '%' }"></div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Application principale -->
    <Transition name="slide-up" appear>
      <main v-if="!isInitialLoading" class="app-main">
        <!-- Navigation simple -->
        <nav class="simple-nav">
          <div class="nav-container">
            <button 
              @click="currentView = 'home'"
              class="nav-btn"
              :class="{ 'active': currentView === 'home' }"
            >
              🏠 Home Original
            </button>
            <button 
              @click="currentView = 'scraped'"
              class="nav-btn"
              :class="{ 'active': currentView === 'scraped' }"
            >
              🎮 Données Scrappées
            </button>
          </div>
        </nav>

        <!-- Affichage conditionnel des composants -->
        <component :is="currentComponent" />
        
        <!-- Notifications Toast -->
        <div class="toast-container">
          <TransitionGroup name="toast" tag="div">
            <div
              v-for="toast in toasts"
              :key="toast.id"
              class="toast"
              :class="[`toast-${toast.type}`]"
            >
              <div class="toast-icon">
                <span v-if="toast.type === 'success'">✅</span>
                <span v-else-if="toast.type === 'error'">❌</span>
                <span v-else-if="toast.type === 'warning'">⚠️</span>
                <span v-else-if="toast.type === 'info'">ℹ️</span>
                <span v-else>📢</span>
              </div>
              <div class="toast-content">
                <h4 v-if="toast.title" class="toast-title">{{ toast.title }}</h4>
                <p class="toast-message">{{ toast.message }}</p>
              </div>
              <button @click="removeToast(toast.id)" class="toast-close">
                ✕
              </button>
            </div>
          </TransitionGroup>
        </div>

        <!-- Indicateur de connexion -->
        <div v-if="!isOnline" class="offline-indicator">
          <span class="offline-icon">📶</span>
          <span class="offline-text">Mode hors ligne</span>
        </div>

        <!-- Back to top button -->
        <Transition name="scale">
          <button
            v-if="showBackToTop"
            @click="scrollToTop"
            class="back-to-top"
            aria-label="Retour en haut"
          >
            <span class="back-to-top-icon">↑</span>
          </button>
        </Transition>
      </main>
    </Transition>

    <!-- Overlay global pour les modales, etc. -->
    <div v-if="hasGlobalOverlay" class="global-overlay" @click="closeGlobalOverlay"></div>
  </div>
</template>

<script>
import Home from './view/Home.vue'
import RealDataHome from './view/RealDataHome.vue'

export default {
  name: 'App',
  components: {
    Home,
    RealDataHome
  },
  data() {
    return {
      currentView: 'scraped', // Démarrer sur les données scrappées
      isInitialLoading: true,
      loadingProgress: 0,
      loadingText: 'Initialisation...',
      isOnline: navigator.onLine,
      showBackToTop: false,
      hasGlobalOverlay: false,
      toasts: [],
      toastIdCounter: 0,
      
      // Étapes de chargement
      loadingSteps: [
        { text: 'Initialisation...', duration: 300 },
        { text: 'Chargement des données scrappées...', duration: 500 },
        { text: 'Configuration de l\'interface gaming...', duration: 400 },
        { text: 'Préparation des animations...', duration: 300 },
        { text: 'Finalisation...', duration: 200 }
      ]
    }
  },
  computed: {
    appClasses() {
      return {
        'app-loading-state': this.isInitialLoading,
        'app-offline': !this.isOnline,
        'app-has-overlay': this.hasGlobalOverlay
      }
    },
    currentComponent() {
      return this.currentView === 'home' ? 'Home' : 'RealDataHome';
    }
  },
  async mounted() {
    await this.initializeApp();
    this.setupEventListeners();
  },
  beforeUnmount() {
    this.removeEventListeners();
  },
  methods: {
    async initializeApp() {
      let totalProgress = 0;
      const stepIncrement = 100 / this.loadingSteps.length;
      
      for (const [index, step] of this.loadingSteps.entries()) {
        this.loadingText = step.text;
        
        // Simule le chargement
        await this.delay(step.duration);
        
        totalProgress = (index + 1) * stepIncrement;
        this.animateProgress(totalProgress);
        
        // Actions spécifiques par étape
        switch (index) {
          case 0:
            await this.initializeTheme();
            break;
          case 1:
            await this.loadScrapedData();
            break;
          case 2:
            await this.setupGamingUI();
            break;
          case 3:
            await this.prepareAnimations();
            break;
          case 4:
            await this.finalizeSetup();
            break;
        }
      }
      
      await this.delay(300);
      this.isInitialLoading = false;
      
      // Toast de bienvenue
      this.showToast({
        type: 'success',
        title: 'Bienvenue !',
        message: 'Fandom Scraper chargé avec succès',
        duration: 3000
      });
    },
    
    async initializeTheme() {
      const savedTheme = localStorage.getItem('theme') || 'dark';
      document.documentElement.setAttribute('data-theme', savedTheme);
    },
    
    async loadScrapedData() {
      // Simuler le chargement des données
      return new Promise(resolve => {
        setTimeout(resolve, 200);
      });
    },
    
    async setupGamingUI() {
      // Configuration de l'interface gaming
      document.body.classList.add('gaming-ready');
      return new Promise(resolve => {
        setTimeout(resolve, 150);
      });
    },
    
    async prepareAnimations() {
      // Préparation des animations CSS
      document.body.classList.add('animations-ready');
      return new Promise(resolve => {
        setTimeout(resolve, 100);
      });
    },
    
    async finalizeSetup() {
      // Finalisation de la configuration
      return new Promise(resolve => {
        setTimeout(resolve, 100);
      });
    },
    
    animateProgress(targetProgress) {
      const currentProgress = this.loadingProgress;
      const increment = (targetProgress - currentProgress) / 20;
      
      const animate = () => {
        if (this.loadingProgress < targetProgress - 1) {
          this.loadingProgress += increment;
          requestAnimationFrame(animate);
        } else {
          this.loadingProgress = targetProgress;
        }
      };
      
      animate();
    },
    
    setupEventListeners() {
      // Détection de la connexion
      window.addEventListener('online', this.handleOnline);
      window.addEventListener('offline', this.handleOffline);
      
      // Scroll pour le bouton "retour en haut"
      window.addEventListener('scroll', this.handleScroll, { passive: true });
      
      // Raccourcis clavier
      window.addEventListener('keydown', this.handleKeydown);
      
      // Gestionnaire d'erreurs global
      window.addEventListener('error', this.handleGlobalError);
      window.addEventListener('unhandledrejection', this.handleUnhandledRejection);
    },
    
    removeEventListeners() {
      window.removeEventListener('online', this.handleOnline);
      window.removeEventListener('offline', this.handleOffline);
      window.removeEventListener('scroll', this.handleScroll);
      window.removeEventListener('keydown', this.handleKeydown);
      window.removeEventListener('error', this.handleGlobalError);
      window.removeEventListener('unhandledrejection', this.handleUnhandledRejection);
    },
    
    handleOnline() {
      this.isOnline = true;
      this.showToast({
        type: 'success',
        title: 'Connexion rétablie',
        message: 'Vous êtes de nouveau en ligne',
        duration: 3000
      });
    },
    
    handleOffline() {
      this.isOnline = false;
      this.showToast({
        type: 'warning',
        title: 'Connexion perdue',
        message: 'Vous êtes maintenant hors ligne',
        duration: 5000
      });
    },
    
    handleScroll() {
      this.showBackToTop = window.scrollY > 300;
    },
    
    handleKeydown(event) {
      // Raccourci pour retourner en haut (Ctrl + Début)
      if (event.ctrlKey && event.key === 'Home') {
        event.preventDefault();
        this.scrollToTop();
      }
      
      // Raccourci pour basculer entre les vues (Ctrl + Tab)
      if (event.ctrlKey && event.key === 'Tab') {
        event.preventDefault();
        this.currentView = this.currentView === 'home' ? 'scraped' : 'home';
        this.showToast({
          type: 'info',
          message: `Basculé vers ${this.currentView === 'home' ? 'Home Original' : 'Données Scrappées'}`,
          duration: 2000
        });
      }
      
      // Raccourci pour basculer le thème (Ctrl + Shift + T)
      if (event.ctrlKey && event.shiftKey && event.key === 'T') {
        event.preventDefault();
        this.toggleTheme();
      }
    },
    
    handleGlobalError(event) {
      console.error('Erreur globale:', event.error);
      this.showToast({
        type: 'error',
        title: 'Erreur inattendue',
        message: 'Une erreur s\'est produite. Veuillez rafraîchir la page.',
        duration: 8000
      });
    },
    
    handleUnhandledRejection(event) {
      console.error('Promise rejetée:', event.reason);
      this.showToast({
        type: 'error',
        title: 'Erreur de chargement',
        message: 'Impossible de charger certaines données.',
        duration: 5000
      });
    },
    
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    },
    
    toggleTheme() {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      
      this.showToast({
        type: 'info',
        message: `Thème ${newTheme === 'dark' ? 'sombre' : 'clair'} activé`,
        duration: 2000
      });
    },
    
    showToast({ type = 'info', title = '', message, duration = 4000 }) {
      const toast = {
        id: ++this.toastIdCounter,
        type,
        title,
        message,
        duration
      };
      
      this.toasts.push(toast);
      
      // Auto-suppression après la durée spécifiée
      setTimeout(() => {
        this.removeToast(toast.id);
      }, duration);
    },
    
    removeToast(toastId) {
      const index = this.toasts.findIndex(toast => toast.id === toastId);
      if (index !== -1) {
        this.toasts.splice(index, 1);
      }
    },
    
    closeGlobalOverlay() {
      this.hasGlobalOverlay = false;
      this.$emit('close-overlay');
    },
    
    delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
  }
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* Navigation simple */
.simple-nav {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(0, 8, 20, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 2px solid var(--gaming-primary, #00ff41);
  box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.nav-btn {
  background: rgba(0, 29, 61, 0.5);
  border: 2px solid var(--gaming-border, #003566);
  color: var(--gaming-text, #ffffff);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Press Start 2P', monospace;
  font-size: 0.7rem;
  text-transform: uppercase;
  position: relative;
  overflow: hidden;
}

.nav-btn:hover {
  border-color: var(--gaming-primary, #00ff41);
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
}

.nav-btn.active {
  background: var(--gaming-primary, #00ff41);
  border-color: var(--gaming-primary, #00ff41);
  color: var(--gaming-bg, #000814);
  box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.nav-btn:hover::before {
  left: 100%;
}

/* Loading Screen */
.app-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #000814, #001d3d);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  text-align: center;
  color: white;
  max-width: 400px;
  padding: 2rem;
}

.loading-logo {
  margin-bottom: 3rem;
  animation: float 3s ease-in-out infinite;
}

.logo-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
  filter: drop-shadow(0 4px 8px rgba(0,255,65,0.3));
  color: var(--gaming-primary, #00ff41);
}

.logo-text {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 0 20px rgba(0,255,65,0.5);
  font-family: 'Orbitron', sans-serif;
  color: var(--gaming-primary, #00ff41);
}

.loading-spinner {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top: 3px solid rgba(0, 255, 65, 0.8);
  border-radius: 50%;
  animation: spin 1.2s linear infinite;
}

.spinner-ring-delay {
  animation-delay: -0.6s;
  border-top-color: rgba(0, 255, 65, 0.4);
}

.loading-text {
  font-size: 1rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
  min-height: 1.5em;
  animation: pulse 1.5s ease-in-out infinite;
  font-family: 'Press Start 2P', monospace;
  font-size: 0.8rem;
}

.loading-progress {
  width: 100%;
  height: 6px;
  background: rgba(0, 255, 65, 0.2);
  border-radius: 3px;
  overflow: hidden;
  border: 1px solid var(--gaming-primary, #00ff41);
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--gaming-primary, #00ff41), var(--gaming-accent, #00ccff));
  border-radius: 3px;
  transition: width 0.3s ease;
  position: relative;
  box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
}

.progress-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: shimmer 1.5s infinite;
}

/* Application principale */
.app-main {
  min-height: 100vh;
  position: relative;
}

/* Toast Notifications - styles identiques */
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 2000;
  max-width: 400px;
  width: 100%;
  pointer-events: none;
}

.toast {
  background: var(--gaming-surface, #001d3d);
  border: 1px solid var(--gaming-border, #003566);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  pointer-events: auto;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.toast::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--gaming-primary, #00ff41);
}

.toast-success::before { background: var(--gaming-success, #00ff88); }
.toast-error::before { background: var(--gaming-error, #ff0040); }
.toast-warning::before { background: var(--gaming-warning, #ffff00); }
.toast-info::before { background: var(--gaming-accent, #00ccff); }

.toast-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: var(--gaming-text, #ffffff);
}

.toast-message {
  font-size: 0.8rem;
  color: var(--gaming-text-dim, #8ecae6);
  line-height: 1.4;
  margin: 0;
}

.toast-close {
  background: none;
  border: none;
  color: var(--gaming-text-dim, #8ecae6);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.toast-close:hover {
  background: var(--gaming-error, #ff0040);
  color: white;
}

/* Autres styles identiques au fichier original */
.offline-indicator {
  position: fixed;
  bottom: 20px;
  left: 20px;
  background: var(--gaming-warning, #ffff00);
  color: var(--gaming-bg, #000814);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  z-index: 1500;
  animation: slideInLeft 0.5s ease;
}

.back-to-top {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  background: var(--gaming-primary, #00ff41);
  color: var(--gaming-bg, #000814);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 255, 65, 0.3);
  transition: all 0.3s ease;
  z-index: 1500;
}

.back-to-top:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 255, 65, 0.4);
}

.back-to-top-icon {
  font-size: 1.5rem;
  font-weight: bold;
}

/* Animations */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-100%); }
  to { opacity: 1; transform: translateX(0); }
}

/* Transitions */
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active { transition: all 0.6s ease; }
.slide-up-enter-from { opacity: 0; transform: translateY(30px); }

.scale-enter-active, .scale-leave-active { transition: all 0.3s ease; }
.scale-enter-from, .scale-leave-to { opacity: 0; transform: scale(0.8); }

.toast-enter-active { transition: all 0.4s ease; }
.toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateX(100%); }
.toast-leave-to { opacity: 0; transform: translateX(100%) scale(0.9); }
.toast-move { transition: transform 0.3s ease; }

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 0.75rem 1rem;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .nav-btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.6rem;
  }
  
  .loading-content { padding: 1.5rem; }
  .logo-icon { font-size: 3rem; }
  .logo-text { font-size: 1.5rem; }
  .loading-spinner { width: 60px; height: 60px; }
  
  .toast-container {
    top: 10px;
    right: 10px;
    left: 10px;
    max-width: none;
  }
}
</style>