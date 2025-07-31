<template>
  <div id="app" :class="appClasses">
    <!-- Loading global si nécessaire -->
    <Transition name="fade">
      <div v-if="isInitialLoading" class="app-loading">
        <div class="loading-content">
          <div class="loading-logo">
            <span class="logo-icon">⚔️</span>
            <h1 class="logo-text">Wiki Characters</h1>
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
        <!-- Router View pour la navigation (si nécessaire) -->
        <router-view v-if="$router" />
        
        <!-- Composant Home par défaut -->
        <Home v-else />
        
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

export default {
  name: 'App',
  components: {
    Home
  },
  data() {
    return {
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
        { text: 'Initialisation...', duration: 500 },
        { text: 'Chargement des personnages...', duration: 800 },
        { text: 'Configuration de l\'interface...', duration: 400 },
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
            await this.loadCharacterData();
            break;
          case 2:
            await this.setupUI();
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
        message: 'L\'application a été chargée avec succès',
        duration: 3000
      });
    },
    
    async initializeTheme() {
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
      }
    },
    
    async loadCharacterData() {
      // Ici, on pourrait charger les vraies données depuis une API
      // Pour l'instant, on simule juste le chargement
      return new Promise(resolve => {
        setTimeout(resolve, 300);
      });
    },
    
    async setupUI() {
      // Configuration de l'interface utilisateur
      return new Promise(resolve => {
        setTimeout(resolve, 200);
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

/* Loading Screen */
.app-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  text-align: center;
  color: white;
  max-width: 400px;
  padding: var(--spacing-xl);
}

.loading-logo {
  margin-bottom: var(--spacing-2xl);
  animation: float 3s ease-in-out infinite;
}

.logo-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: var(--spacing-md);
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
}

.logo-text {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.loading-spinner {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto var(--spacing-xl);
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top: 3px solid rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  animation: spin 1.2s linear infinite;
}

.spinner-ring-delay {
  animation-delay: -0.6s;
  border-top-color: rgba(255, 255, 255, 0.4);
}

.loading-text {
  font-size: 1.1rem;
  margin-bottom: var(--spacing-lg);
  font-weight: 500;
  min-height: 1.5em;
  animation: pulse 1.5s ease-in-out infinite;
}

.loading-progress {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 2px;
  transition: width 0.3s ease;
  position: relative;
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

/* Toast Notifications */
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
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--elevation-4);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
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
  background: var(--primary-color);
}

.toast-success::before {
  background: var(--success);
}

.toast-error::before {
  background: var(--error);
}

.toast-warning::before {
  background: var(--warning);
}

.toast-info::before {
  background: var(--info);
}

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
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--spacing-xs);
  color: var(--text-primary);
}

.toast-message {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.4;
  margin: 0;
}

.toast-close {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: var(--spacing-xs);
  border-radius: var(--radius-sm);
  transition: var(--transition-normal);
  flex-shrink: 0;
}

.toast-close:hover {
  background: var(--error-light);
  color: var(--error);
}

/* Indicateur hors ligne */
.offline-indicator {
  position: fixed;
  bottom: 20px;
  left: 20px;
  background: var(--warning);
  color: white;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  box-shadow: var(--elevation-3);
  z-index: 1500;
  animation: slideInLeft 0.5s ease;
}

.offline-icon {
  font-size: 1rem;
}

/* Bouton retour en haut */
.back-to-top {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--elevation-3);
  transition: var(--transition-normal);
  z-index: 1500;
}

.back-to-top:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--elevation-4);
}

.back-to-top-icon {
  font-size: 1.5rem;
  font-weight: bold;
}

/* Overlay global */
.global-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1900;
  animation: fadeIn 0.3s ease;
}

/* Classes d'état */
.app-loading-state {
  overflow: hidden;
}

.app-offline .toast-container {
  bottom: 80px;
}

.app-has-overlay {
  overflow: hidden;
}

/* Animations de transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active {
  transition: all 0.6s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.toast-enter-active {
  transition: all 0.4s ease;
}

.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.toast-move {
  transition: transform 0.3s ease;
}

/* Animations personnalisées */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .toast-container {
    top: 10px;
    right: 10px;
    left: 10px;
    max-width: none;
  }
  
  .offline-indicator {
    bottom: 10px;
    left: 10px;
  }
  
  .back-to-top {
    bottom: 80px;
    right: 10px;
    width: 45px;
    height: 45px;
  }
  
  .loading-content {
    padding: var(--spacing-lg);
  }
  
  .logo-icon {
    font-size: 3rem;
  }
  
  .logo-text {
    font-size: 2rem;
  }
  
  .loading-spinner {
    width: 60px;
    height: 60px;
  }
}

@media (max-width: 480px) {
  .toast {
    padding: var(--spacing-sm);
    font-size: var(--font-size-xs);
  }
  
  .toast-title {
    font-size: var(--font-size-xs);
  }
  
  .toast-message {
    font-size: var(--font-size-xs);
  }
  
  .offline-indicator {
    font-size: var(--font-size-xs);
    padding: var(--spacing-xs) var(--spacing-sm);
  }
  
  .back-to-top {
    width: 40px;
    height: 40px;
  }
  
  .back-to-top-icon {
    font-size: 1.2rem;
  }
}

/* Optimisations pour les performances */
.loading-spinner,
.progress-bar,
.toast {
  will-change: transform;
}

.app-loading {
  will-change: opacity;
}

/* Support pour le mode sombre */
[data-theme="dark"] .app-loading {
  background: linear-gradient(135deg, #1e293b, #0f172a);
}

[data-theme="dark"] .toast {
  background: var(--surface);
  border-color: var(--border);
  backdrop-filter: blur(20px);
}

/* Mode réduit de mouvement */
@media (prefers-reduced-motion: reduce) {
  .loading-logo,
  .loading-text,
  .spinner-ring,
  .progress-bar::after {
    animation: none;
  }
  
  .back-to-top:hover {
    transform: none;
  }
  
  * {
    transition-duration: 0.01ms !important;
  }
}

/* Support pour les écrans haute résolution */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .toast {
    backdrop-filter: blur(20px);
  }
  
  .app-loading {
    background-attachment: fixed;
  }
}

/* Focus et accessibilité */
.toast-close:focus-visible,
.back-to-top:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* États d'interaction améliorés */
.toast:hover {
  transform: translateY(-1px);
  box-shadow: var(--elevation-5);
}

.back-to-top:active {
  transform: translateY(0) scale(0.95);
}

/* Animations de chargement avancées */
.loading-content {
  animation: fadeInUp 1s ease-out;
}

.loading-spinner {
  animation: scaleIn 0.5s ease-out 0.5s both;
}

.loading-text {
  animation: fadeInUp 0.6s ease-out 0.8s both;
}

.loading-progress {
  animation: fadeInUp 0.6s ease-out 1s both;
}
</style>