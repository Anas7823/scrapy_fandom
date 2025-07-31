<template>
  <div 
    class="character-card" 
    :class="{ 
      'favorite': isFavorite, 
      'in-comparison': inComparison,
      'legendary': character.rarity === 'Légendaire',
      'epic': character.rarity === 'Épique',
      'rare': character.rarity === 'Rare'
    }"
    @click="openDetails"
  >
    <!-- Badge de rareté -->
    <div class="rarity-badge" :class="rarityClass">
      {{ character.rarity }}
    </div>

    <!-- Image du personnage -->
    <div class="character-image">
      <img 
        :src="character.image" 
        :alt="character.name"
        @error="handleImageError"
        loading="lazy"
      />
      <div class="image-overlay">
        <span class="view-details">👁️ Voir détails</span>
      </div>
    </div>

    <!-- Informations du personnage -->
    <div class="character-info">
      <h3 class="character-name">{{ character.name }}</h3>
      <p class="character-universe">{{ character.universe }}</p>
      <p class="character-role">
        <span class="role-icon">{{ getRoleIcon(character.role) }}</span>
        {{ character.role }}
      </p>

      <!-- Stats du personnage -->
      <div class="character-stats">
        <div class="stat">
          <span class="stat-label">Force</span>
          <div class="stat-bar">
            <div 
              class="stat-fill" 
              :style="{ width: character.stats.strength + '%' }"
            ></div>
          </div>
          <span class="stat-value">{{ character.stats.strength }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Agilité</span>
          <div class="stat-bar">
            <div 
              class="stat-fill" 
              :style="{ width: character.stats.agility + '%' }"
            ></div>
          </div>
          <span class="stat-value">{{ character.stats.agility }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Intelligence</span>
          <div class="stat-bar">
            <div 
              class="stat-fill" 
              :style="{ width: character.stats.intelligence + '%' }"
            ></div>
          </div>
          <span class="stat-value">{{ character.stats.intelligence }}</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="card-actions">
        <button 
          @click.stop="toggleFavorite"
          class="action-btn favorite-btn"
          :class="{ 'active': isFavorite }"
        >
          <span class="btn-icon">{{ isFavorite ? '❤️' : '🤍' }}</span>
          <span class="btn-text">Favori</span>
        </button>

        <button 
          @click.stop="toggleComparison"
          class="action-btn compare-btn"
          :class="{ 'active': inComparison }"
          :disabled="!inComparison && comparisonCount >= 2"
        >
          <span class="btn-icon">⚖️</span>
          <span class="btn-text">{{ inComparison ? 'Retirer' : 'Comparer' }}</span>
        </button>
      </div>
    </div>

    <!-- Effet de particules pour les cartes légendaires -->
    <div v-if="character.rarity === 'Légendaire'" class="legendary-effects">
      <div class="particle" v-for="n in 6" :key="n" :style="getParticleStyle(n)"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CharacterCard',
  emits: ['toggle-favorite', 'toggle-comparison', 'open-details'],
  props: {
    character: {
      type: Object,
      required: true
    },
    isFavorite: {
      type: Boolean,
      default: false
    },
    inComparison: {
      type: Boolean,
      default: false
    },
    comparisonCount: {
      type: Number,
      default: 0
    }
  },
  computed: {
    rarityClass() {
      const rarityMap = {
        'Légendaire': 'legendary',
        'Épique': 'epic',
        'Rare': 'rare',
        'Commun': 'common'
      };
      return rarityMap[this.character.rarity] || 'common';
    }
  },
  methods: {
    toggleFavorite() {
      this.$emit('toggle-favorite', this.character.id);
    },
    toggleComparison() {
      this.$emit('toggle-comparison', this.character.id);
    },
    openDetails() {
      this.$emit('open-details', this.character);
    },
    handleImageError(event) {
      event.target.src = 'https://via.placeholder.com/200x250/6366f1/ffffff?text=' + 
                         encodeURIComponent(this.character.name);
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
    getParticleStyle(index) {
      const angles = [0, 60, 120, 180, 240, 300];
      const angle = angles[index - 1];
      const delay = index * 0.2;
      
      return {
        '--angle': angle + 'deg',
        '--delay': delay + 's'
      };
    }
  }
}
</script>

<style scoped>
.character-card {
  background: var(--surface);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px var(--shadow);
  border: 2px solid var(--border);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  animation: fadeInUp 0.6s ease-out;
  animation-fill-mode: both;
}

.character-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  border-color: var(--primary-color);
}

.character-card.favorite {
  border-color: var(--error);
  box-shadow: 0 4px 20px rgba(239, 68, 68, 0.2);
}

.character-card.in-comparison {
  border-color: var(--warning);
  box-shadow: 0 4px 20px rgba(245, 158, 11, 0.2);
}

.character-card.legendary {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  border-color: #ffd700;
  position: relative;
  overflow: visible;
}

.character-card.epic {
  background: linear-gradient(135deg, #a855f7 0%, #c084fc 100%);
  border-color: #a855f7;
}

.character-card.rare {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-color: #3b82f6;
}

.rarity-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  z-index: 3;
  backdrop-filter: blur(10px);
}

.rarity-badge.legendary {
  background: rgba(255, 215, 0, 0.9);
  color: #92400e;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

.rarity-badge.epic {
  background: rgba(168, 85, 247, 0.9);
  color: white;
}

.rarity-badge.rare {
  background: rgba(59, 130, 246, 0.9);
  color: white;
}

.rarity-badge.common {
  background: rgba(107, 114, 128, 0.9);
  color: white;
}

.character-image {
  position: relative;
  height: 250px;
  overflow: hidden;
}

.character-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.character-card:hover .character-image img {
  transform: scale(1.1);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.8) 0%,
    transparent 50%
  );
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 16px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.character-card:hover .image-overlay {
  opacity: 1;
}

.view-details {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.character-info {
  padding: 20px;
  background: var(--surface);
}

.character-name {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.character-universe {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.character-role {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 16px;
}

.role-icon {
  font-size: 1.1rem;
}

.character-stats {
  margin-bottom: 20px;
}

.stat {
  display: grid;
  grid-template-columns: 80px 1fr 40px;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.stat-bar {
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 3px;
  transition: width 0.6s ease;
  animation: fillBar 1s ease-out;
}

.stat-value {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-primary);
  text-align: right;
}

.card-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border: 2px solid var(--border);
  border-radius: 8px;
  background: var(--background);
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.favorite-btn.active {
  background: var(--error);
  border-color: var(--error);
  color: white;
}

.compare-btn.active {
  background: var(--warning);
  border-color: var(--warning);
  color: white;
}

.btn-icon {
  font-size: 1.1rem;
}

.legendary-effects {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #ffd700;
  border-radius: 50%;
  animation: orbit 3s linear infinite;
  animation-delay: var(--delay);
  box-shadow: 0 0 6px #ffd700;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fillBar {
  from { width: 0; }
}

@keyframes orbit {
  from {
    transform: rotate(0deg) translateX(60px) rotate(0deg);
  }
  to {
    transform: rotate(360deg) translateX(60px) rotate(-360deg);
  }
}

/* Animation delay pour les cartes */
.character-card:nth-child(1) { animation-delay: 0.1s; }
.character-card:nth-child(2) { animation-delay: 0.2s; }
.character-card:nth-child(3) { animation-delay: 0.3s; }
.character-card:nth-child(4) { animation-delay: 0.4s; }
.character-card:nth-child(5) { animation-delay: 0.5s; }
.character-card:nth-child(6) { animation-delay: 0.6s; }

@media (max-width: 768px) {
  .character-card {
    margin-bottom: 16px;
  }
  
  .card-actions {
    grid-template-columns: 1fr;
  }
  
  .stat {
    grid-template-columns: 70px 1fr 35px;
    gap: 8px;
  }
}</style>