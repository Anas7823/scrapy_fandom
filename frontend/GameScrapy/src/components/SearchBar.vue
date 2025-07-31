<template>
  <div class="search-container">
    <!-- Header avec toggle dark mode -->
    <header class="app-header">
      <h1 class="app-title">
        <span class="title-icon">⚔️</span>
        Wiki Characters
      </h1>
      <button 
        @click="toggleTheme" 
        class="theme-toggle"
        :class="{ 'dark': isDark }"
      >
        <span class="theme-icon">{{ isDark ? '☀️' : '🌙' }}</span>
      </button>
    </header>

    <!-- Barre de recherche -->
    <div class="search-bar">
      <div class="search-input-group">
        <span class="search-icon">🔍</span>
        <input 
          v-model="searchQuery"
          @input="handleSearch"
          type="text" 
          placeholder="Rechercher un personnage..."
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

    <!-- Filtres dynamiques -->
    <div class="filters-section">
      <div class="filters-row">
        <div class="filter-group">
          <label>Rôle</label>
          <select v-model="selectedRole" @change="handleFilter" class="filter-select">
            <option value="">Tous</option>
            <option v-for="role in availableRoles" :key="role" :value="role">
              {{ role }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label>Rareté</label>
          <select v-model="selectedRarity" @change="handleFilter" class="filter-select">
            <option value="">Toutes</option>
            <option v-for="rarity in availableRarities" :key="rarity" :value="rarity">
              {{ rarity }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label>Univers</label>
          <select v-model="selectedUniverse" @change="handleFilter" class="filter-select">
            <option value="">Tous</option>
            <option v-for="universe in availableUniverses" :key="universe" :value="universe">
              {{ universe }}
            </option>
          </select>
        </div>

        <button @click="clearAllFilters" class="clear-filters-btn">
          <span>🗑️</span> Effacer les filtres
        </button>
      </div>

      <!-- Compteur de résultats -->
      <div class="results-info" v-if="filteredCount !== null">
        <span class="results-count">{{ filteredCount }} personnage(s) trouvé(s)</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  emits: ['search', 'filter', 'theme-changed'],
  props: {
    characters: {
      type: Array,
      default: () => []
    },
    filteredCount: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      searchQuery: '',
      selectedRole: '',
      selectedRarity: '',
      selectedUniverse: '',
      isDark: false
    }
  },
  computed: {
    availableRoles() {
      return [...new Set(this.characters.map(char => char.role).filter(Boolean))].sort();
    },
    availableRarities() {
      return [...new Set(this.characters.map(char => char.rarity).filter(Boolean))].sort();
    },
    availableUniverses() {
      return [...new Set(this.characters.map(char => char.universe).filter(Boolean))].sort();
    }
  },
  mounted() {
    // Récupérer le thème sauvegardé
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      this.isDark = savedTheme === 'dark';
      this.applyTheme();
    }
  },
  methods: {
    handleSearch() {
      this.$emit('search', this.searchQuery);
    },
    handleFilter() {
      const filters = {
        role: this.selectedRole,
        rarity: this.selectedRarity,
        universe: this.selectedUniverse
      };
      this.$emit('filter', filters);
    },
    clearSearch() {
      this.searchQuery = '';
      this.handleSearch();
    },
    clearAllFilters() {
      this.selectedRole = '';
      this.selectedRarity = '';
      this.selectedUniverse = '';
      this.handleFilter();
    },
    toggleTheme() {
      this.isDark = !this.isDark;
      this.applyTheme();
      localStorage.setItem('theme', this.isDark ? 'dark' : 'light');
      this.$emit('theme-changed', this.isDark);
    },
    applyTheme() {
      document.documentElement.setAttribute('data-theme', this.isDark ? 'dark' : 'light');
    }
  }
}
</script>

<style scoped>
.search-container {
  background: var(--surface);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 4px 20px var(--shadow);
  border: 1px solid var(--border);
  transition: all 0.3s ease;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.app-title {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 2.5rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.theme-toggle {
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.2rem;
}

.theme-toggle:hover {
  background: var(--primary-color);
  border-color: var(--primary-color);
  transform: scale(1.1);
}

.theme-toggle.dark {
  background: var(--warning);
  border-color: var(--warning);
}

.search-bar {
  margin-bottom: 24px;
}

.search-input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  font-size: 1.2rem;
  color: var(--text-secondary);
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: 16px 16px 16px 52px;
  border: 2px solid var(--border);
  border-radius: 12px;
  background: var(--background);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.clear-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: var(--error);
  color: white;
}

.filters-section {
  animation: slideUp 0.5s ease-out;
}

.filters-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  align-items: end;
  margin-bottom: 16px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.filter-select {
  padding: 12px 16px;
  border: 2px solid var(--border);
  border-radius: 8px;
  background: var(--background);
  color: var(--text-primary);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.clear-filters-btn {
  background: var(--error);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  height: fit-content;
}

.clear-filters-btn:hover {
  background: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.results-info {
  text-align: center;
  padding: 12px;
  background: var(--primary-color);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  animation: fadeIn 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .app-header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .filters-row {
    grid-template-columns: 1fr;
  }
  
  .app-title {
    font-size: 1.5rem;
  }
}</style>