<template>
  <div class="real-data-container" :data-theme="isDark ? 'dark' : 'light'">
    <!-- Header Gaming Style -->
    <header class="gaming-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-3d">
            <div class="logo-face front">🎮</div>
            <div class="logo-face back">⚔️</div>
          </div>
          <div class="title-glitch">
            <h1 class="main-title">FANDOM SCRAPER</h1>
            <div class="subtitle">REAL DATA VIEWER</div>
          </div>
        </div>
        
        <div class="header-controls">
          <div class="stats-display">
            <div class="stat-item">
              <span class="stat-value">{{ filteredItems.length }}</span>
              <span class="stat-label">ITEMS</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ gameCount }}</span>
              <span class="stat-label">GAMES</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ characterCount }}</span>
              <span class="stat-label">CHARACTERS</span>
            </div>
          </div>

          <!-- Bouton de scraping -->
          <button 
            @click="launchScraping" 
            :disabled="isScrapingInProgress"
            class="scraping-btn"
            :class="{ 'scraping-active': isScrapingInProgress }"
          >
            <div class="scraping-icon">
              <span v-if="!isScrapingInProgress">🕷️</span>
              <span v-else class="spinning">⚡</span>
            </div>
            <div class="scraping-text">
              <span class="scraping-label">{{ isScrapingInProgress ? 'SCRAPING...' : 'LAUNCH SCRAPE' }}</span>
              <span class="scraping-sublabel">{{ isScrapingInProgress ? 'En cours...' : 'Nouveaux jeux' }}</span>
            </div>
          </button>
          
          <button @click="toggleTheme" class="theme-toggle-gaming">
            <div class="toggle-3d">
              <div class="toggle-face front">{{ isDark ? '🌙' : '☀️' }}</div>
              <div class="toggle-face back">{{ isDark ? '☀️' : '🌙' }}</div>
            </div>
          </button>
        </div>
      </div>

      <!-- Barre de progression du scraping -->
      <div v-if="isScrapingInProgress" class="scraping-progress">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: scrapingProgress + '%' }"></div>
        </div>
        <div class="progress-info">
          <span class="progress-text">{{ scrapingStatus }}</span>
          <span class="progress-percentage">{{ scrapingProgress }}%</span>
        </div>
      </div>
    </header>

    <!-- Notification de scraping -->
    <div v-if="scrapingNotification" class="scraping-notification" :class="scrapingNotification.type">
      <div class="notification-content">
        <span class="notification-icon">{{ scrapingNotification.icon }}</span>
        <div class="notification-text">
          <strong>{{ scrapingNotification.title }}</strong>
          <p>{{ scrapingNotification.message }}</p>
        </div>
        <button @click="closeNotification" class="notification-close">✕</button>
      </div>
    </div>

    <!-- Filters Section -->
    <section class="filters-section">
      <div class="filters-container">
        <div class="search-bar-real">
          <div class="search-input-group">
            <button @click="launch_Scrap" class="search-icon">🔍</button>
            <input 
              v-model="fandomUrl"
              type="text" 
              placeholder="Rechercher des liens..."
              class="search-input"
            />
            <button 
              v-if="searchQueryX" 
              @click="clearSearch"
              class="clear-btn"
            >
              ✕
            </button>
          </div>
          <div class="search-input-group">
            <span class="search-icon">🔍</span>
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Rechercher des jeux, personnages..."
              class="search-input"
            />
            <button 
              v-if="searchQuery" 
              @click="clearSearch"
              class="clear-btn"
            >
              ✕
            </button>
          </div>
        </div>

        <div class="filter-buttons">
          <button 
            @click="setFilter('all')"
            class="filter-btn"
            :class="{ 'active': currentFilter === 'all' }"
          >
            <span class="btn-icon">📊</span>
            <span class="btn-text">Tout ({{ scrapedData.length }})</span>
          </button>
          
          <button 
            @click="setFilter('games')"
            class="filter-btn"
            :class="{ 'active': currentFilter === 'games' }"
          >
            <span class="btn-icon">🎮</span>
            <span class="btn-text">Jeux ({{ gameCount }})</span>
          </button>
          
          <button 
            @click="setFilter('characters')"
            class="filter-btn"
            :class="{ 'active': currentFilter === 'characters' }"
          >
            <span class="btn-icon">👤</span>
            <span class="btn-text">Personnages ({{ characterCount }})</span>
          </button>
        </div>
      </div>
    </section>

    <!-- Main Content Grid -->
    <section class="content-section">
      <div class="content-container">
        <!-- No results message -->
        <div v-if="filteredItems.length === 0" class="no-results">
          <div class="no-results-content">
            <span class="no-results-icon">🔍</span>
            <h3>Aucun résultat trouvé</h3>
            <p>Essayez de modifier votre recherche ou vos filtres</p>
            <button @click="clearFilters" class="clear-filters-btn">
              Effacer les filtres
            </button>
          </div>
        </div>

        <!-- Items Grid -->
        <div v-else class="items-grid">
          <div 
            v-for="(item, index) in paginatedItems" 
            :key="item.url || index"
            class="item-card"
            :class="getItemTypeClass(item)"
            @click="openItemDetails(item)"
          >
            <!-- Item Type Badge -->
            <div class="type-badge" :class="getItemTypeClass(item)">
              <span class="badge-icon">{{ getItemIcon(item) }}</span>
              <span class="badge-text">{{ getItemType(item) }}</span>
            </div>

            <!-- Item Image -->
            <div class="item-image">
              <img 
                v-if="item.image" 
                :src="item.image" 
                :alt="item.name"
                @error="handleImageError"
                loading="lazy"
              />
              <div v-else class="placeholder-image">
                <span class="placeholder-icon">{{ getItemIcon(item) }}</span>
                <span class="placeholder-text">{{ item.name }}</span>
              </div>
              <div class="image-overlay">
                <span class="view-details">👁️ Voir détails</span>
              </div>
            </div>

            <!-- Item Info -->
            <div class="item-info">
              <h3 class="item-name">{{ item.name || 'Sans nom' }}</h3>
              
              <!-- Game info for characters -->
              <p v-if="item.game" class="item-game">
                <span class="game-icon">🎮</span>
                {{ item.game }}
              </p>

              <!-- Attributes display -->
              <div v-if="hasMainAttributes(item)" class="item-attributes">
                <div v-for="(value, key) in getMainAttributes(item)" :key="key" class="attribute">
                  <span class="attr-label">{{ formatAttributeKey(key) }}:</span>
                  <span class="attr-value">{{ formatAttributeValue(value) }}</span>
                </div>
              </div>

              <!-- Description preview -->
              <p v-if="item.description" class="item-description">
                {{ truncateDescription(item.description, 100) }}
              </p>

              <!-- URL Display -->
              <div class="item-url">
                <span class="url-icon">🔗</span>
                <span class="url-text">{{ getDomainFromUrl(item.url) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination-real">
          <button 
            @click="currentPage = 1" 
            :disabled="currentPage === 1"
            class="pagination-btn"
          >
            ⏮️
          </button>
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            class="pagination-btn"
          >
            ⏪
          </button>
          
          <div class="pagination-pages">
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="currentPage = page"
              class="pagination-btn page-btn"
              :class="{ 'active': page === currentPage }"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="pagination-btn"
          >
            ⏩
          </button>
          <button 
            @click="currentPage = totalPages" 
            :disabled="currentPage === totalPages"
            class="pagination-btn"
          >
            ⏭️
          </button>
        </div>
      </div>
    </section>

    <!-- Details Modal -->
    <div v-if="selectedItem" class="modal-overlay" @click="closeDetails">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">{{ selectedItem.name || 'Détails' }}</h2>
          <button @click="closeDetails" class="modal-close">✕</button>
        </div>
        
        <div class="modal-body">
          <div class="item-details">
            <!-- Image -->
            <div v-if="selectedItem.image" class="detail-image">
              <img :src="selectedItem.image" :alt="selectedItem.name" @error="handleImageError"/>
            </div>

            <!-- Basic Info -->
            <div class="detail-info">
              <div class="info-section">
                <h3>Informations de base</h3>
                <div class="info-grid">
                  <div class="info-item">
                    <span class="info-label">Type</span>
                    <span class="info-value">{{ getItemType(selectedItem) }}</span>
                  </div>
                  <div v-if="selectedItem.game" class="info-item">
                    <span class="info-label">Jeu</span>
                    <span class="info-value">{{ selectedItem.game }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Source</span>
                    <span class="info-value">{{ getDomainFromUrl(selectedItem.url) }}</span>
                  </div>
                </div>
              </div>

              <!-- Description -->
              <div v-if="selectedItem.description" class="info-section">
                <h3>Description</h3>
                <p class="full-description">{{ selectedItem.description }}</p>
              </div>

              <!-- All Attributes -->
              <div v-if="selectedItem.attributes && Object.keys(selectedItem.attributes).length > 0" class="info-section">
                <h3>Attributs détaillés</h3>
                <div class="attributes-grid">
                  <div 
                    v-for="(value, key) in selectedItem.attributes" 
                    :key="key"
                    class="attribute-item"
                  >
                    <span class="attribute-key">{{ formatAttributeKey(key) }}</span>
                    <span class="attribute-value">{{ formatAttributeValue(value) }}</span>
                  </div>
                </div>
              </div>

              <!-- External Link -->
              <div class="info-section">
                <h3>Lien externe</h3>
                <a :href="selectedItem.url" target="_blank" rel="noopener noreferrer" class="external-link">
                  <span class="link-icon">🔗</span>
                  <span class="link-text">Voir sur {{ getDomainFromUrl(selectedItem.url) }}</span>
                  <span class="external-icon">↗</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const fandomUrl = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(null)
const message = ref('')

const launch_Scrap = async () => {
  if (!fandomUrl.value) {
    error.value = "Veuillez entrer une URL."
    return
  }

  loading.value = true
  error.value = null
  success.value = false

  try {
    console.log("Lancement du scraping...")
    const response = await fetch('http://localhost:8000/scrape', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: fandomUrl.value }),
    })

    if (!response.ok) {
      throw new Error(`Erreur ${response.status}`)
    }

    const data = await response.json()
    message.value = data.detail || "Scraping terminé avec succès."
    success.value = true
  } catch (err) {
    error.value = err.message || "Une erreur est survenue."
  } finally {
    loading.value = false
  }
}
</script>

<script>
import scrapedData from '../../../../data/fandom_data.json'

export default {
  name: 'RealDataHome',
  data() {
    return {
      isDark: true,
      searchQuery: '',
      currentFilter: 'all',
      selectedItem: null,
      currentPage: 1,
      itemsPerPage: 12,
      scrapedData: scrapedData,
      // Données pour le scraping
      isScrapingInProgress: false,
      scrapingProgress: 0,
      scrapingStatus: 'Initialisation...',
      scrapingNotification: null
    }
  },
  computed: {
    filteredItems() {
      let filtered = this.scrapedData;

      // Filtre par recherche
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(item =>
          (item.name && item.name.toLowerCase().includes(query)) ||
          (item.game && item.game.toLowerCase().includes(query)) ||
          (item.description && item.description.toLowerCase().includes(query)) ||
          (item.url && item.url.toLowerCase().includes(query))
        );
      }

      // Filtre par type
      if (this.currentFilter === 'games') {
        filtered = filtered.filter(item => this.isGame(item));
      } else if (this.currentFilter === 'characters') {
        filtered = filtered.filter(item => this.isCharacter(item));
      }

      return filtered;
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredItems.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    visiblePages() {
      const pages = [];
      const start = Math.max(1, this.currentPage - 2);
      const end = Math.min(this.totalPages, start + 4);
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },
    gameCount() {
      return this.scrapedData.filter(item => this.isGame(item)).length;
    },
    characterCount() {
      return this.scrapedData.filter(item => this.isCharacter(item)).length;
    }
  },
  watch: {
    filteredItems() {
      this.currentPage = 1;
    }
  },
  methods: {
    // Méthode pour lancer le scraping
    async launchScraping() {
      if (this.isScrapingInProgress) return;

      this.isScrapingInProgress = true;
      this.scrapingProgress = 0;
      this.scrapingStatus = 'Démarrage du scraping...';

      try {
        // Simulation du processus de scraping avec WebSocket ou polling
        // Remplacez par votre logique réelle
        await this.startScrapingProcess();
        
      } catch (error) {
        console.error('Erreur lors du scraping:', error);
        this.showNotification({
          type: 'error',
          icon: '❌',
          title: 'Erreur de scraping',
          message: 'Une erreur est survenue lors du lancement du scraping.'
        });
      } finally {
        this.isScrapingInProgress = false;
        this.scrapingProgress = 0;
      }
    },

    async startScrapingProcess() {
      try {
        // Appel à votre API backend pour lancer le scraping
        const response = await fetch('/api/start-scraping', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            command: 'scrapy crawl fandom',
            path: 'C:\\Users\\willi\\Documents\\Ecole_ipssi_MIA4\\juillet_aout_2025\\fandom_scrape_tp\\scrapy_fandom\\fandom_scraper_anas'
          })
        });

        if (!response.ok) {
          throw new Error('Erreur réseau');
        }

        // Simulation du suivi de progression
        this.simulateScrapingProgress();

        const result = await response.json();
        
        if (result.success) {
          this.showNotification({
            type: 'success',
            icon: '✅',
            title: 'Scraping terminé',
            message: `${result.itemsScraped || 0} nouveaux éléments ajoutés !`
          });
          
          // Recharger les données
          await this.reloadScrapedData();
        } else {
          throw new Error(result.error || 'Erreur inconnue');
        }

      } catch (error) {
        console.error('Erreur:', error);
        this.showNotification({
          type: 'error',
          icon: '❌',
          title: 'Erreur',
          message: error.message || 'Erreur lors du scraping'
        });
      }
    },

    simulateScrapingProgress() {
      const stages = [
        { progress: 10, status: 'Connexion au site Fandom...' },
        { progress: 25, status: 'Exploration des pages de jeux...' },
        { progress: 40, status: 'Extraction des données...' },
        { progress: 60, status: 'Traitement des personnages...' },
        { progress: 80, status: 'Sauvegarde des données...' },
        { progress: 95, status: 'Finalisation...' },
        { progress: 100, status: 'Scraping terminé !' }
      ];

      let currentStage = 0;
      const updateProgress = () => {
        if (currentStage < stages.length && this.isScrapingInProgress) {
          const stage = stages[currentStage];
          this.scrapingProgress = stage.progress;
          this.scrapingStatus = stage.status;
          currentStage++;
          
          setTimeout(updateProgress, 2000 + Math.random() * 3000);
        }
      };

      setTimeout(updateProgress, 1000);
    },

    async reloadScrapedData() {
      try {
        // Recharger les données depuis le fichier JSON
        const response = await fetch('/data/scrapedData.json?' + Date.now());
        if (response.ok) {
          const newData = await response.json();
          this.scrapedData = newData;
        }
      } catch (error) {
        console.error('Erreur lors du rechargement des données:', error);
      }
    },

    showNotification(notification) {
      this.scrapingNotification = notification;
      setTimeout(() => {
        this.scrapingNotification = null;
      }, 5000);
    },

    closeNotification() {
      this.scrapingNotification = null;
    },

    isGame(item) {
      if (item.attributes) {
        if (item.attributes.Type === 'GAME') return true;
        if (item.attributes.Developer || item.attributes['Developer(s)']) return true;
        if (item.attributes.Publisher || item.attributes['Publisher(s)']) return true;
        if (item.attributes.Genre) return true;
        if (item.attributes['Release date'] || item.attributes['Release Date']) return true;
      }
      
      const gameKeywords = ['Red_Dead_Redemption', 'Grand_Theft_Auto_V', 'Need_for_Speed', 'Detroit:_Become_Human'];
      return gameKeywords.some(keyword => item.url.includes(keyword));
    },
    isCharacter(item) {
      if (item.game) return true;
      if (item.attributes && item.attributes.Type === 'CHARACTER') return true;
      if (item.attributes && (item.attributes.Gender || item.attributes['Voiced by'])) return true;
      
      const characterKeywords = ['Protagonist', 'character', 'Traci'];
      return characterKeywords.some(keyword => item.url.includes(keyword));
    },
    getItemType(item) {
      if (this.isGame(item)) return 'Jeu';
      if (this.isCharacter(item)) return 'Personnage';
      return 'Élément';
    },
    getItemIcon(item) {
      if (this.isGame(item)) return '🎮';
      if (this.isCharacter(item)) return '👤';
      return '📄';
    },
    getItemTypeClass(item) {
      if (this.isGame(item)) return 'item-game';
      if (this.isCharacter(item)) return 'item-character';
      return 'item-other';
    },
    hasMainAttributes(item) {
      if (!item.attributes) return false;
      const mainKeys = ['Developer', 'Publisher', 'Genre', 'Gender', 'Status', 'Type'];
      return mainKeys.some(key => item.attributes[key]);
    },
    getMainAttributes(item) {
      if (!item.attributes) return {};
      
      const mainKeys = ['Developer', 'Publisher', 'Genre', 'Gender', 'Status', 'Type', 'Release date'];
      const result = {};
      
      mainKeys.forEach(key => {
        if (item.attributes[key]) {
          result[key] = item.attributes[key];
        }
      });
      
      const entries = Object.entries(result).slice(0, 3);
      return Object.fromEntries(entries);
    },
    formatAttributeKey(key) {
      const keyMap = {
        'Developer': 'Développeur',
        'Publisher': 'Éditeur',
        'Genre': 'Genre',
        'Gender': 'Sexe',
        'Status': 'Statut',
        'Type': 'Type',
        'Release date': 'Date de sortie',
        'Voiced by': 'Voix',
        'Appears in': 'Apparaît dans'
      };
      return keyMap[key] || key;
    },
    formatAttributeValue(value) {
      if (typeof value === 'string' && value.length > 50) {
        return value.substring(0, 50) + '...';
      }
      return value;
    },
    truncateDescription(description, maxLength) {
      if (!description) return '';
      if (description.length <= maxLength) return description;
      return description.substring(0, maxLength) + '...';
    },
    getDomainFromUrl(url) {
      try {
        const domain = new URL(url).hostname;
        return domain.replace('www.', '');
      } catch {
        return url;
      }
    },
    setFilter(filter) {
      this.currentFilter = filter;
    },
    clearSearch() {
      this.searchQuery = '';
    },
    clearFilters() {
      this.searchQuery = '';
      this.currentFilter = 'all';
    },
    openItemDetails(item) {
      this.selectedItem = item;
      document.body.style.overflow = 'hidden';
    },
    closeDetails() {
      this.selectedItem = null;
      document.body.style.overflow = 'auto';
    },
    handleImageError(event) {
      event.target.src = 'https://via.placeholder.com/268x268/1a1f2e/00ff41?text=' + 
                         encodeURIComponent('Image non disponible');
    },
    toggleTheme() {
      this.isDark = !this.isDark;
      const theme = this.isDark ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
    }
  }
}
</script>

<style>
@import '../assets/realDataStyles.css';
</style>