import { ref, computed, reactive } from 'vue'
import mockData from '../data/mock.json'

// État global partagé
const globalState = reactive({
  characters: [],
  favorites: JSON.parse(localStorage.getItem('fandom-favorites') || '[]'),
  comparison: JSON.parse(localStorage.getItem('fandom-comparison') || '[]'),
  theme: localStorage.getItem('fandom-theme') || 'dark',
  isLoading: false,
  searchHistory: JSON.parse(localStorage.getItem('fandom-search-history') || '[]')
})

export function useCharacters() {
  // Refs reactives
  const characters = ref(globalState.characters.length ? globalState.characters : mockData.characters)
  const favorites = ref(globalState.favorites)
  const comparison = ref(globalState.comparison)
  const isLoading = ref(globalState.isLoading)
  const searchHistory = ref(globalState.searchHistory)

  // Computed properties
  const favoriteCharacters = computed(() => {
    return characters.value.filter(char => favorites.value.includes(char.id))
  })

  const comparisonCharacters = computed(() => {
    return characters.value.filter(char => comparison.value.includes(char.id))
  })

  const universes = computed(() => {
    return [...new Set(characters.value.map(char => char.universe))].sort()
  })

  const roles = computed(() => {
    return [...new Set(characters.value.map(char => char.role))].sort()
  })

  const rarities = computed(() => {
    return [...new Set(characters.value.map(char => char.rarity))].sort()
  })

  const stats = computed(() => ({
    totalCharacters: characters.value.length,
    totalUniverses: universes.value.length,
    totalRoles: roles.value.length,
    totalFavorites: favorites.value.length,
    totalInComparison: comparison.value.length
  }))

  // Methods
  const loadCharacters = async (source = 'local') => {
    isLoading.value = true
    globalState.isLoading = true

    try {
      if (source === 'local') {
        // Charger les données mockées
        characters.value = mockData.characters
        globalState.characters = mockData.characters
      } else if (source === 'api') {
        // Ici vous pourrez ajouter votre logique d'API
        const response = await fetch('/api/characters')
        const data = await response.json()
        characters.value = data
        globalState.characters = data
      }
      
      return characters.value
    } catch (error) {
      console.error('Error loading characters:', error)
      throw error
    } finally {
      isLoading.value = false
      globalState.isLoading = false
    }
  }

  const scrapeFandomWiki = async (url) => {
    isLoading.value = true
    globalState.isLoading = true

    try {
      // Simulation de scraping - à remplacer par votre vraie logique
      const response = await simulateScrapingProcess(url)
      
      // Ajouter les nouveaux personnages
      const newCharacters = response.characters
      characters.value = [...characters.value, ...newCharacters]
      globalState.characters = characters.value
      
      return newCharacters
    } catch (error) {
      console.error('Error scraping Fandom wiki:', error)
      throw error
    } finally {
      isLoading.value = false
      globalState.isLoading = false
    }
  }

  const addToFavorites = (characterId) => {
    if (!favorites.value.includes(characterId)) {
      favorites.value.push(characterId)
      globalState.favorites = favorites.value
      saveFavorites()
    }
  }

  const removeFromFavorites = (characterId) => {
    const index = favorites.value.indexOf(characterId)
    if (index > -1) {
      favorites.value.splice(index, 1)
      globalState.favorites = favorites.value
      saveFavorites()
    }
  }

  const toggleFavorite = (characterId) => {
    if (favorites.value.includes(characterId)) {
      removeFromFavorites(characterId)
    } else {
      addToFavorites(characterId)
    }
  }

  const addToComparison = (characterId) => {
    if (!comparison.value.includes(characterId) && comparison.value.length < 2) {
      comparison.value.push(characterId)
      globalState.comparison = comparison.value
      saveComparison()
    }
  }

  const removeFromComparison = (characterId) => {
    const index = comparison.value.indexOf(characterId)
    if (index > -1) {
      comparison.value.splice(index, 1)
      globalState.comparison = comparison.value
      saveComparison()
    }
  }

  const toggleComparison = (characterId) => {
    if (comparison.value.includes(characterId)) {
      removeFromComparison(characterId)
    } else {
      addToComparison(characterId)
    }
  }

  const clearComparison = () => {
    comparison.value = []
    globalState.comparison = []
    saveComparison()
  }

  const searchCharacters = (query, filters = {}) => {
    let filtered = characters.value

    // Recherche textuelle
    if (query) {
      const lowerQuery = query.toLowerCase()
      filtered = filtered.filter(char =>
        char.name.toLowerCase().includes(lowerQuery) ||
        char.universe.toLowerCase().includes(lowerQuery) ||
        char.role.toLowerCase().includes(lowerQuery) ||
        char.description?.toLowerCase().includes(lowerQuery)
      )
      
      // Ajouter à l'historique de recherche
      addToSearchHistory(query)
    }

    // Filtres
    if (filters.universe) {
      filtered = filtered.filter(char => char.universe === filters.universe)
    }
    if (filters.role) {
      filtered = filtered.filter(char => char.role === filters.role)
    }
    if (filters.rarity) {
      filtered = filtered.filter(char => char.rarity === filters.rarity)
    }
    if (filters.minLevel) {
      filtered = filtered.filter(char => char.level >= filters.minLevel)
    }
    if (filters.maxLevel) {
      filtered = filtered.filter(char => char.level <= filters.maxLevel)
    }

    return filtered
  }

  const getCharacterById = (id) => {
    return characters.value.find(char => char.id === id)
  }

  const addToSearchHistory = (query) => {
    if (!searchHistory.value.includes(query)) {
      searchHistory.value.unshift(query)
      // Garder seulement les 10 dernières recherches
      if (searchHistory.value.length > 10) {
        searchHistory.value = searchHistory.value.slice(0, 10)
      }
      globalState.searchHistory = searchHistory.value
      saveSearchHistory()
    }
  }

  const clearSearchHistory = () => {
    searchHistory.value = []
    globalState.searchHistory = []
    saveSearchHistory()
  }

  // Storage functions
  const saveFavorites = () => {
    localStorage.setItem('fandom-favorites', JSON.stringify(favorites.value))
  }

  const saveComparison = () => {
    localStorage.setItem('fandom-comparison', JSON.stringify(comparison.value))
  }

  const saveSearchHistory = () => {
    localStorage.setItem('fandom-search-history', JSON.stringify(searchHistory.value))
  }

  const saveTheme = (theme) => {
    globalState.theme = theme
    localStorage.setItem('fandom-theme', theme)
  }

  // Simulation de scraping (à remplacer par votre vraie logique)
  const simulateScrapingProcess = async (url) => {
    // Simuler un délai de traitement
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    // Retourner des données simulées basées sur l'URL
    const wikiName = extractWikiName(url)
    const simulatedCharacters = generateSimulatedCharacters(wikiName)
    
    return {
      success: true,
      url: url,
      characters: simulatedCharacters,
      scrapedAt: new Date().toISOString()
    }
  }

  const extractWikiName = (url) => {
    const match = url.match(/https:\/\/([^.]+)\.fandom\.com/)
    return match ? match[1] : 'unknown'
  }

  const generateSimulatedCharacters = (wikiName) => {
    // Générer quelques personnages simulés pour la démonstration
    const baseId = Math.max(...characters.value.map(c => c.id), 0) + 1
    
    return [
      {
        id: baseId,
        name: `${wikiName} Hero 1`,
        universe: wikiName.charAt(0).toUpperCase() + wikiName.slice(1),
        role: 'Guerrier',
        rarity: 'Épique',
        level: Math.floor(Math.random() * 100) + 1,
        image: `https://via.placeholder.com/300x400/1a1f2e/00ff41?text=${encodeURIComponent(wikiName + ' Hero 1')}`,
        description: `Un héros puissant du monde de ${wikiName}, découvert via le scraping automatique.`,
        stats: {
          strength: Math.floor(Math.random() * 100),
          agility: Math.floor(Math.random() * 100),
          intelligence: Math.floor(Math.random() * 100)
        },
        abilities: [
          {
            name: 'Compétence Scrappée',
            icon: '🔍',
            description: 'Une compétence découverte automatiquement',
            damage: '100-150',
            cooldown: 8
          }
        ]
      },
      {
        id: baseId + 1,
        name: `${wikiName} Hero 2`,
        universe: wikiName.charAt(0).toUpperCase() + wikiName.slice(1),
        role: 'Mage',
        rarity: 'Rare',
        level: Math.floor(Math.random() * 100) + 1,
        image: `https://via.placeholder.com/300x400/1a1f2e/00ff41?text=${encodeURIComponent(wikiName + ' Hero 2')}`,
        description: `Un autre héros du monde de ${wikiName}, extrait de la wiki.`,
        stats: {
          strength: Math.floor(Math.random() * 100),
          agility: Math.floor(Math.random() * 100),
          intelligence: Math.floor(Math.random() * 100)
        },
        abilities: [
          {
            name: 'Magie Scrappée',
            icon: '✨',
            description: 'Un sort découvert automatiquement',
            damage: '150-200',
            cooldown: 12
          }
        ]
      }
    ]
  }

  // Retourner toutes les propriétés et méthodes
  return {
    // État
    characters: computed(() => characters.value),
    favorites: computed(() => favorites.value),
    comparison: computed(() => comparison.value),
    favoriteCharacters,
    comparisonCharacters,
    isLoading: computed(() => isLoading.value),
    searchHistory: computed(() => searchHistory.value),
    
    // Computed
    universes,
    roles,
    rarities,
    stats,
    
    // Methods
    loadCharacters,
    scrapeFandomWiki,
    searchCharacters,
    getCharacterById,
    
    // Favorites
    addToFavorites,
    removeFromFavorites,
    toggleFavorite,
    
    // Comparison
    addToComparison,
    removeFromComparison,
    toggleComparison,
    clearComparison,
    
    // Search history
    addToSearchHistory,
    clearSearchHistory,
    
    // Storage
    saveTheme
  }
}

// Fonction utilitaire pour valider les URLs Fandom
export function validateFandomUrl(url) {
  const fandomRegex = /^https:\/\/[a-zA-Z0-9-]+\.fandom\.com\/?.*$/
  return fandomRegex.test(url)
}

// Fonction pour générer des suggestions de recherche
export function generateSearchSuggestions(query, characters, limit = 5) {
  if (!query || query.length < 2) return []
  
  const lowerQuery = query.toLowerCase()
  const suggestions = new Set()
  
  characters.forEach(char => {
    if (char.name.toLowerCase().includes(lowerQuery)) {
      suggestions.add(char.name)
    }
    if (char.universe.toLowerCase().includes(lowerQuery)) {
      suggestions.add(char.universe)
    }
    if (char.role.toLowerCase().includes(lowerQuery)) {
      suggestions.add(char.role)
    }
  })
  
  return Array.from(suggestions).slice(0, limit)
}