<template>
  <div class="app-container" :data-theme="isDark ? 'dark' : 'light'">
    <!-- Barre de recherche et filtres -->
    <SearchBar 
      :characters="mockCharacters"
      :filtered-count="filteredCharacters.length"
      @search="handleSearch"
      @filter="handleFilter"
      @theme-changed="handleThemeChange"
    />

    <!-- Section favoris (si il y en a) -->
    <div v-if="favorites.length > 0" class="favorites-section">
      <h2 class="section-title">
        <span class="title-icon">❤️</span>
        Mes Favoris ({{ favorites.length }})
      </h2>
      <div class="characters-grid">
        <CharacterCard
          v-for="character in favorites"
          :key="`fav-${character.id}`"
          :character="character"
          :is-favorite="true"
          :in-comparison="comparisonIds.includes(character.id)"
          :comparison-count="comparisonIds.length"
          @toggle-favorite="toggleFavorite"
          @toggle-comparison="toggleComparison"
          @open-details="openCharacterDetails"
        />
      </div>
    </div>

    <!-- Section tous les personnages -->
    <div class="characters-section">
      <h2 class="section-title">
        <span class="title-icon">⚔️</span>
        Tous les Personnages ({{ filteredCharacters.length }})
      </h2>
      
      <!-- Message si aucun résultat -->
      <div v-if="filteredCharacters.length === 0" class="no-results">
        <div class="no-results-content">
          <span class="no-results-icon">🔍</span>
          <h3>Aucun personnage trouvé</h3>
          <p>Essayez de modifier vos critères de recherche ou filtres</p>
          <button @click="clearAllFilters" class="clear-filters-btn">
            Effacer tous les filtres
          </button>
        </div>
      </div>

      <!-- Grille des personnages -->
      <div v-else class="characters-grid">
        <CharacterCard
          v-for="character in paginatedCharacters"
          :key="character.id"
          :character="character"
          :is-favorite="favoriteIds.includes(character.id)"
          :in-comparison="comparisonIds.includes(character.id)"
          :comparison-count="comparisonIds.length"
          @toggle-favorite="toggleFavorite"
          @toggle-comparison="toggleComparison"
          @open-details="openCharacterDetails"
        />
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
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

    <!-- Panel de comparaison -->
    <ComparisonPanel
      v-if="comparisonCharacters.length > 0"
      :characters="comparisonCharacters"
      @remove-character="removeFromComparison"
      @clear-comparison="clearComparison"
    />

    <!-- Modal de détails -->
    <div v-if="selectedCharacter" class="modal-overlay" @click="closeDetails">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">{{ selectedCharacter.name }}</h2>
          <button @click="closeDetails" class="modal-close">✕</button>
        </div>
        
        <div class="modal-body">
          <div class="character-details">
            <!-- Image principale -->
            <div class="detail-image">
              <img 
                :src="selectedCharacter.image" 
                :alt="selectedCharacter.name"
                @error="handleImageError"
              />
              <div class="detail-rarity-badge" :class="getRarityClass(selectedCharacter.rarity)">
                {{ selectedCharacter.rarity }}
              </div>
            </div>

            <!-- Informations détaillées -->
            <div class="detail-info">
              <div class="info-section">
                <h3>Informations Générales</h3>
                <div class="info-grid">
                  <div class="info-item">
                    <span class="info-label">Univers</span>
                    <span class="info-value">{{ selectedCharacter.universe }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Rôle</span>
                    <span class="info-value">
                      {{ getRoleIcon(selectedCharacter.role) }} {{ selectedCharacter.role }}
                    </span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Rareté</span>
                    <span class="info-value">{{ selectedCharacter.rarity }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Niveau</span>
                    <span class="info-value">{{ selectedCharacter.level || 'N/A' }}</span>
                  </div>
                </div>
              </div>

              <!-- Description -->
              <div class="info-section">
                <h3>Description</h3>
                <p class="character-description">{{ selectedCharacter.description }}</p>
              </div>

              <!-- Statistiques détaillées -->
              <div class="info-section">
                <h3>Statistiques</h3>
                <div class="detailed-stats">
                  <div v-for="stat in detailedStats" :key="stat.key" class="detailed-stat">
                    <div class="stat-header">
                      <span class="stat-name">{{ stat.icon }} {{ stat.label }}</span>
                      <span class="stat-value">{{ selectedCharacter.stats[stat.key] }}/100</span>
                    </div>
                    <div class="stat-bar-detailed">
                      <div 
                        class="stat-fill-detailed" 
                        :style="{ 
                          width: selectedCharacter.stats[stat.key] + '%',
                          background: getStatGradient(selectedCharacter.stats[stat.key])
                        }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Compétences -->
              <div class="info-section" v-if="selectedCharacter.abilities">
                <h3>Compétences</h3>
                <div class="abilities-grid">
                  <div 
                    v-for="ability in selectedCharacter.abilities" 
                    :key="ability.name"
                    class="ability-card"
                  >
                    <div class="ability-icon">{{ ability.icon }}</div>
                    <div class="ability-info">
                      <h4 class="ability-name">{{ ability.name }}</h4>
                      <p class="ability-description">{{ ability.description }}</p>
                      <div class="ability-stats">
                        <span class="ability-damage" v-if="ability.damage">
                          ⚔️ {{ ability.damage }}
                        </span>
                        <span class="ability-cooldown" v-if="ability.cooldown">
                          ⏱️ {{ ability.cooldown }}s
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions dans la modal -->
          <div class="modal-actions">
            <button 
              @click="toggleFavoriteModal"
              class="modal-action-btn favorite-modal-btn"
              :class="{ 'active': favoriteIds.includes(selectedCharacter.id) }"
            >
              <span>{{ favoriteIds.includes(selectedCharacter.id) ? '❤️' : '🤍' }}</span>
              {{ favoriteIds.includes(selectedCharacter.id) ? 'Retirer des favoris' : 'Ajouter aux favoris' }}
            </button>
            
            <button 
              @click="toggleComparisonModal"
              class="modal-action-btn compare-modal-btn"
              :class="{ 'active': comparisonIds.includes(selectedCharacter.id) }"
              :disabled="!comparisonIds.includes(selectedCharacter.id) && comparisonIds.length >= 2"
            >
              <span>⚖️</span>
              {{ comparisonIds.includes(selectedCharacter.id) ? 'Retirer de la comparaison' : 'Ajouter à la comparaison' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>Chargement des personnages...</p>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from '../components/SearchBar.vue'
import CharacterCard from '../components/Card.vue'
import ComparisonPanel from '../components/Comparison.vue'

export default {
  name: 'Home',
  components: {
    SearchBar,
    CharacterCard,
    ComparisonPanel
  },
  data() {
    return {
      isDark: false,
      isLoading: false,
      searchQuery: '',
      filters: {
        role: '',
        rarity: '',
        universe: ''
      },
      favoriteIds: [],
      comparisonIds: [],
      selectedCharacter: null,
      currentPage: 1,
      itemsPerPage: 12,
      
      // Données mockées - à remplacer par de vraies données
      mockCharacters: [
        {
          id: 1,
          name: "Aragorn",
          universe: "Le Seigneur des Anneaux",
          role: "Guerrier",
          rarity: "Légendaire",
          level: 85,
          image: "https://images.unsplash.com/photo-1566492031773-4f4e44671d66?w=200&h=250&fit=crop",
          description: "Héritier du trône du Gondor, Aragorn est un rôdeur expérimenté et un leader né. Son courage et sa détermination en font un allié précieux dans la lutte contre les forces du mal.",
          stats: {
            strength: 92,
            agility: 78,
            intelligence: 85
          },
          abilities: [
            {
              name: "Lame du Roi",
              icon: "⚔️",
              description: "Une attaque puissante qui inflige des dégâts massifs",
              damage: "250-300",
              cooldown: 8
            },
            {
              name: "Inspiration Royale",
              icon: "👑",
              description: "Boost les stats de tous les alliés",
              cooldown: 15
            }
          ]
        },
        {
          id: 2,
          name: "Gandalf",
          universe: "Le Seigneur des Anneaux",
          role: "Mage",
          rarity: "Légendaire",
          level: 99,
          image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=250&fit=crop",
          description: "Mage puissant et sage, Gandalf guide les peuples libres dans leur quête. Sa magie et sa sagesse sont légendaires.",
          stats: {
            strength: 65,
            agility: 70,
            intelligence: 98
          },
          abilities: [
            {
              name: "Éclair Divin",
              icon: "⚡",
              description: "Frappe les ennemis avec la puissance de la foudre",
              damage: "300-400",
              cooldown: 10
            },
            {
              name: "Bouclier de Lumière",
              icon: "🛡️",
              description: "Protège les alliés des attaques magiques",
              cooldown: 12
            }
          ]
        },
        {
          id: 3,
          name: "Legolas",
          universe: "Le Seigneur des Anneaux",
          role: "Archer",
          rarity: "Épique",
          level: 75,
          image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=250&fit=crop",
          description: "Elfe archer d'une précision inégalée, Legolas peut toucher sa cible à des distances impossibles.",
          stats: {
            strength: 72,
            agility: 95,
            intelligence: 80
          },
          abilities: [
            {
              name: "Tir de Précision",
              icon: "🏹",
              description: "Un tir qui ne rate jamais sa cible",
              damage: "200-250",
              cooldown: 6
            },
            {
              name: "Pluie de Flèches",
              icon: "🌧️",
              description: "Attaque multiple touchant tous les ennemis",
              damage: "150-180",
              cooldown: 14
            }
          ]
        },
        {
          id: 4,
          name: "Naruto Uzumaki",
          universe: "Naruto",
          role: "Guerrier",
          rarity: "Légendaire",
          level: 90,
          image: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=250&fit=crop",
          description: "Ninja au grand cœur, Naruto possède une détermination sans faille et la puissance du démon renard.",
          stats: {
            strength: 88,
            agility: 92,
            intelligence: 75
          },
          abilities: [
            {
              name: "Rasengan",
              icon: "🌀",
              description: "Technique de chakra concentré",
              damage: "280-320",
              cooldown: 8
            },
            {
              name: "Multi-Clonage",
              icon: "👥",
              description: "Crée plusieurs clones pour attaquer",
              damage: "150-200",
              cooldown: 10
            }
          ]
        },
        {
          id: 5,
          name: "Sasuke Uchiha",
          universe: "Naruto",
          role: "Assassin",
          rarity: "Légendaire",
          level: 88,
          image: "https://images.unsplash.com/photo-1507591064344-4c6ce005b128?w=200&h=250&fit=crop",
          description: "Dernier survivant du clan Uchiha, maître du Sharingan et techniques de foudre.",
          stats: {
            strength: 85,
            agility: 94,
            intelligence: 90
          },
          abilities: [
            {
              name: "Chidori",
              icon: "⚡",
              description: "Attaque de foudre dévastatrice",
              damage: "300-350",
              cooldown: 9
            },
            {
              name: "Sharingan",
              icon: "👁️",
              description: "Copie les techniques ennemies",
              cooldown: 20
            }
          ]
        },
        {
          id: 6,
          name: "Sakura Haruno",
          universe: "Naruto",
          role: "Soigneur",
          rarity: "Épique",
          level: 82,
          image: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&h=250&fit=crop",
          description: "Ninja médical d'exception, élève de Tsunade, capable de soigner et de se battre.",
          stats: {
            strength: 78,
            agility: 75,
            intelligence: 92
          },
          abilities: [
            {
              name: "Soin Mystique",
              icon: "💚",
              description: "Soigne les blessures des alliés",
              cooldown: 8
            },
            {
              name: "Force de Cent Sceaux",
              icon: "💪",
              description: "Décuple temporairement la force physique",
              damage: "250-300",
              cooldown: 25
            }
          ]
        },
        {
          id: 7,
          name: "Goku",
          universe: "Dragon Ball",
          role: "Guerrier",
          rarity: "Légendaire",
          level: 95,
          image: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200&h=250&fit=crop",
          description: "Saiyan au cœur pur, toujours en quête de dépassement et de combats épiques.",
          stats: {
            strength: 98,
            agility: 90,
            intelligence: 70
          },
          abilities: [
            {
              name: "Kamehameha",
              icon: "💥",
              description: "Vague d'énergie dévastatrice",
              damage: "350-450",
              cooldown: 12
            },
            {
              name: "Transformation",
              icon: "⭐",
              description: "Augmente toutes les statistiques",
              cooldown: 30
            }
          ]
        },
        {
          id: 8,
          name: "Vegeta",
          universe: "Dragon Ball",
          role: "Guerrier",
          rarity: "Légendaire",
          level: 93,
          image: "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=200&h=250&fit=crop",
          description: "Prince des Saiyans, orgueilleux et puissant, rival éternel de Goku.",
          stats: {
            strength: 96,
            agility: 88,
            intelligence: 85
          },
          abilities: [
            {
              name: "Final Flash",
              icon: "🔥",
              description: "Attaque énergétique ultime",
              damage: "380-420",
              cooldown: 15
            },
            {
              name: "Orgueil du Prince",
              icon: "👑",
              description: "Résiste aux effets de statut négatifs",
              cooldown: 20
            }
          ]
        },
        {
          id: 9,
          name: "Piccolo",
          universe: "Dragon Ball",
          role: "Tank",
          rarity: "Épique",
          level: 78,
          image: "https://images.unsplash.com/photo-1543610892-0b1f7e6d8ac1?w=200&h=250&fit=crop",
          description: "Namek devenu protecteur de la Terre, mentor et combattant redoutable.",
          stats: {
            strength: 80,
            agility: 70,
            intelligence: 95
          },
          abilities: [
            {
              name: "Makankosappo",
              icon: "🌀",
              description: "Rayon spiral perforant",
              damage: "280-320",
              cooldown: 10
            },
            {
              name: "Régénération",
              icon: "💚",
              description: "Récupère des points de vie",
              cooldown: 18
            }
          ]
        },
        {
          id: 10,
          name: "Luffy",
          universe: "One Piece",
          role: "Guerrier",
          rarity: "Légendaire",
          level: 87,
          image: "https://images.unsplash.com/photo-1552058544-f2b08422138a?w=200&h=250&fit=crop",
          description: "Capitaine pirate au corps de caoutchouc, déterminé à devenir le Roi des Pirates.",
          stats: {
            strength: 90,
            agility: 85,
            intelligence: 65
          },
          abilities: [
            {
              name: "Gear Second",
              icon: "💨",
              description: "Accélère tous les mouvements",
              cooldown: 15
            },
            {
              name: "Gomu Gomu Pistol",
              icon: "👊",
              description: "Étend le bras pour frapper à distance",
              damage: "200-280",
              cooldown: 5
            }
          ]
        },
        {
          id: 11,
          name: "Zoro",
          universe: "One Piece",
          role: "Guerrier",
          rarity: "Épique",
          level: 84,
          image: "https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=200&h=250&fit=crop",
          description: "Épéiste à trois sabres, bras droit de Luffy et futur plus grand épéiste du monde.",
          stats: {
            strength: 92,
            agility: 88,
            intelligence: 60
          },
          abilities: [
            {
              name: "Santoryu",
              icon: "⚔️",
              description: "Technique des trois sabres",
              damage: "270-320",
              cooldown: 8
            },
            {
              name: "Oni Giri",
              icon: "👹",
              description: "Attaque dévastatrice aux trois lames",
              damage: "300-350",
              cooldown: 12
            }
          ]
        },
        {
          id: 12,
          name: "Nami",
          universe: "One Piece",
          role: "Support",
          rarity: "Rare",
          level: 65,
          image: "https://images.unsplash.com/photo-1494790108755-2616b612b754?w=200&h=250&fit=crop",
          description: "Navigatrice exceptionnelle maîtrisant la météorologie et la cartographie.",
          stats: {
            strength: 45,
            agility: 78,
            intelligence: 90
          },
          abilities: [
            {
              name: "Clima-Tact",
              icon: "🌩️",
              description: "Contrôle la météo pour attaquer",
              damage: "180-220",
              cooldown: 10
            },
            {
              name: "Navigation",
              icon: "🗺️",
              description: "Guide l'équipe vers la victoire",
              cooldown: 20
            }
          ]
        }
      ],

      detailedStats: [
        { key: 'strength', label: 'Force', icon: '⚔️' },
        { key: 'agility', label: 'Agilité', icon: '🏃' },
        { key: 'intelligence', label: 'Intelligence', icon: '🧠' }
      ]
    }
  },
  computed: {
    filteredCharacters() {
      let filtered = this.mockCharacters;

      // Filtre par recherche
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(char =>
          char.name.toLowerCase().includes(query) ||
          char.universe.toLowerCase().includes(query) ||
          char.role.toLowerCase().includes(query)
        );
      }

      // Filtres par attributs
      if (this.filters.role) {
        filtered = filtered.filter(char => char.role === this.filters.role);
      }
      if (this.filters.rarity) {
        filtered = filtered.filter(char => char.rarity === this.filters.rarity);
      }
      if (this.filters.universe) {
        filtered = filtered.filter(char => char.universe === this.filters.universe);
      }

      return filtered;
    },
    paginatedCharacters() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredCharacters.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredCharacters.length / this.itemsPerPage);
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
    favorites() {
      return this.mockCharacters.filter(char => this.favoriteIds.includes(char.id));
    },
    comparisonCharacters() {
      return this.mockCharacters.filter(char => this.comparisonIds.includes(char.id));
    }
  },
  watch: {
    filteredCharacters() {
      // Reset à la première page quand les filtres changent
      this.currentPage = 1;
    }
  },
  mounted() {
    this.loadFavorites();
    this.loadTheme();
  },
  methods: {
    handleSearch(query) {
      this.searchQuery = query;
    },
    handleFilter(filters) {
      this.filters = { ...filters };
    },
    handleThemeChange(isDark) {
      this.isDark = isDark;
    },
    toggleFavorite(characterId) {
      const index = this.favoriteIds.indexOf(characterId);
      if (index === -1) {
        this.favoriteIds.push(characterId);
      } else {
        this.favoriteIds.splice(index, 1);
      }
      this.saveFavorites();
    },
    toggleFavoriteModal() {
      if (this.selectedCharacter) {
        this.toggleFavorite(this.selectedCharacter.id);
      }
    },
    toggleComparison(characterId) {
      const index = this.comparisonIds.indexOf(characterId);
      if (index === -1 && this.comparisonIds.length < 2) {
        this.comparisonIds.push(characterId);
      } else if (index !== -1) {
        this.comparisonIds.splice(index, 1);
      }
    },
    toggleComparisonModal() {
      if (this.selectedCharacter) {
        this.toggleComparison(this.selectedCharacter.id);
      }
    },
    removeFromComparison(characterId) {
      const index = this.comparisonIds.indexOf(characterId);
      if (index !== -1) {
        this.comparisonIds.splice(index, 1);
      }
    },
    clearComparison() {
      this.comparisonIds = [];
    },
    openCharacterDetails(character) {
      this.selectedCharacter = character;
      document.body.style.overflow = 'hidden';
    },
    closeDetails() {
      this.selectedCharacter = null;
      document.body.style.overflow = 'auto';
    },
    clearAllFilters() {
      this.searchQuery = '';
      this.filters = {
        role: '',
        rarity: '',
        universe: ''
      };
    },
    loadFavorites() {
      const saved = localStorage.getItem('character-favorites');
      if (saved) {
        this.favoriteIds = JSON.parse(saved);
      }
    },
    saveFavorites() {
      localStorage.setItem('character-favorites', JSON.stringify(this.favoriteIds));
    },
    loadTheme() {
      const saved = localStorage.getItem('theme');
      if (saved) {
        this.isDark = saved === 'dark';
      }
    },
    handleImageError(event) {
      event.target.src = 'https://via.placeholder.com/300x400/6366f1/ffffff?text=' + 
                         encodeURIComponent('Personnage');
    },
    getRoleIcon(role) {
      const roleIcons = {
        'Guerrier': '⚔️',
        'Mage': '🔮',
        'Assassin': '🗡️',
        'Archer': '🏹',
        'Soigneur': '💚',
        'Tank': '🛡️',
        'Support': '🤝'
      };
      return roleIcons[role] || '⭐';
    },
    getRarityClass(rarity) {
      const rarityMap = {
        'Légendaire': 'legendary',
        'Épique': 'epic',
        'Rare': 'rare',
        'Commun': 'common'
      };
      return rarityMap[rarity] || 'common';
    },
    getStatGradient(value) {
      if (value >= 90) return 'linear-gradient(90deg, #10b981, #059669)';
      if (value >= 80) return 'linear-gradient(90deg, #f59e0b, #d97706)';
      if (value >= 70) return 'linear-gradient(90deg, #3b82f6, #2563eb)';
      if (value >= 60) return 'linear-gradient(90deg, #8b5cf6, #7c3aed)';
      return 'linear-gradient(90deg, #6b7280, #4b5563)';
    }
  }
}
</script>

<style scoped>
:root {
  --primary-color: #6366f1;
  --secondary-color: #8b5cf6;
  --background: #ffffff;
  --surface: #f8fafc;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border: #e2e8f0;
  --shadow: rgba(0, 0, 0, 0.1);
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
}

[data-theme="dark"] {
  --background: #0f172a;
  --surface: #1e293b;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --border: #334155;
  --shadow: rgba(0, 0, 0, 0.3);
}

.app-container {
  min-height: 100vh;
  background: var(--background);
  color: var(--text-primary);
  transition: all 0.3s ease;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-primary);
}

.title-icon {
  font-size: 1.8rem;
}

.favorites-section {
  margin-bottom: 48px;
}

.characters-section {
  margin-bottom: 48px;
}

.characters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.no-results {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  margin: 40px 0;
}

.no-results-content {
  text-align: center;
  max-width: 400px;
}

.no-results-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  display: block;
}

.no-results-content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.no-results-content p {
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.clear-filters-btn {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-filters-btn:hover {
  background: #4f46e5;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 32px;
}

.pagination-btn {
  background: var(--surface);
  border: 2px solid var(--border);
  color: var(--text-primary);
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  min-width: 40px;
}

.pagination-btn:hover:not(:disabled) {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
  transform: translateY(-2px);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-pages {
  display: flex;
  gap: 4px;
}

.page-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: var(--surface);
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.4s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 2px solid var(--border);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
}

.modal-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.modal-body {
  max-height: calc(90vh - 140px);
  overflow-y: auto;
  padding: 24px;
}

.character-details {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 32px;
  margin-bottom: 24px;
}

.detail-image {
  position: relative;
}

.detail-image img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 12px;
  border: 3px solid var(--border);
}

.detail-rarity-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  backdrop-filter: blur(10px);
}

.detail-rarity-badge.legendary {
  background: rgba(255, 215, 0, 0.9);
  color: #92400e;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

.detail-rarity-badge.epic {
  background: rgba(168, 85, 247, 0.9);
  color: white;
}

.detail-rarity-badge.rare {
  background: rgba(59, 130, 246, 0.9);
  color: white;
}

.detail-rarity-badge.common {
  background: rgba(107, 114, 128, 0.9);
  color: white;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-section h3 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--primary-color);
  border-bottom: 2px solid var(--border);
  padding-bottom: 8px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.info-value {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.character-description {
  line-height: 1.6;
  color: var(--text-secondary);
  font-size: 1rem;
}

.detailed-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detailed-stat {
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 8px;
  padding: 16px;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.stat-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.stat-value {
  font-size: 1rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-bar-detailed {
  height: 12px;
  background: var(--border);
  border-radius: 6px;
  overflow: hidden;
}

.stat-fill-detailed {
  height: 100%;
  border-radius: 6px;
  transition: width 0.8s ease;
  animation: fillBarDetailed 1.2s ease-out;
}

.abilities-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.ability-card {
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  gap: 16px;
  transition: all 0.3s ease;
}

.ability-card:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadow);
}

.ability-icon {
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 12px;
  color: white;
  flex-shrink: 0;
}

.ability-info {
  flex: 1;
}

.ability-name {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.ability-description {
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 8px;
}

.ability-stats {
  display: flex;
  gap: 16px;
  font-size: 0.875rem;
  font-weight: 600;
}

.ability-damage {
  color: var(--error);
}

.ability-cooldown {
  color: var(--warning);
}

.modal-actions {
  display: flex;
  gap: 16px;
  padding-top: 24px;
  border-top: 2px solid var(--border);
}

.modal-action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  border: 2px solid var(--border);
  border-radius: 12px;
  background: var(--background);
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadow);
}

.modal-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.favorite-modal-btn.active {
  background: var(--error);
  border-color: var(--error);
  color: white;
}

.compare-modal-btn.active {
  background: var(--warning);
  border-color: var(--warning);
  color: white;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.loading-spinner {
  text-align: center;
  color: white;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

.loading-spinner p {
  font-size: 1.1rem;
  font-weight: 600;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes fillBarDetailed {
  from { width: 0; }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .characters-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
  
  .character-details {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .detail-image {
    max-width: 300px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .app-container {
    padding: 16px;
  }
  
  .characters-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .modal-content {
    margin: 10px;
    max-height: calc(100vh - 20px);
  }
  
  .modal-body {
    padding: 16px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .pagination {
    flex-wrap: wrap;
    gap: 4px;
  }
  
  .pagination-pages {
    order: -1;
    width: 100%;
    justify-content: center;
    margin-bottom: 8px;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.25rem;
  }
  
  .detail-image img {
    height: 300px;
  }
  
  .ability-card {
    flex-direction: column;
    text-align: center;
  }
  
  .ability-icon {
    align-self: center;
  }
}
</style>