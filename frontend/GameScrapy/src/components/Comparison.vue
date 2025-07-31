<template>
  <div v-if="characters.length > 0" class="comparison-panel" :class="{ 'battle-mode': isBattling }">
    <div class="comparison-header">
      <h3 class="comparison-title">
        <span class="title-icon">⚖️</span>
        Comparateur de Personnages
      </h3>
      <button @click="clearComparison" class="clear-btn">
        <span>🗑️</span>
      </button>
    </div>

    <div class="comparison-content">
      <!-- Zone de comparaison normale -->
      <div v-if="!isBattling" class="comparison-grid">
        <div 
          v-for="(character, index) in displayCharacters" 
          :key="character?.id || `empty-${index}`"
          class="comparison-slot"
          :class="{ 'empty': !character }"
        >
          <div v-if="character" class="character-compare-card">
            <!-- Image et infos de base -->
            <div class="compare-avatar">
              <img :src="character.image" :alt="character.name" @error="handleImageError" />
              <div class="character-name-overlay">{{ character.name }}</div>
            </div>

            <!-- Stats comparées -->
            <div class="compare-stats">
              <div v-for="stat in statsList" :key="stat.key" class="compare-stat">
                <span class="stat-name">{{ stat.label }}</span>
                <div class="stat-comparison">
                  <div class="stat-bar-compare">
                    <div 
                      class="stat-fill-compare" 
                      :style="{ 
                        width: character.stats[stat.key] + '%',
                        background: getStatColor(character.stats[stat.key])
                      }"
                    ></div>
                  </div>
                  <span class="stat-value-compare">{{ character.stats[stat.key] }}</span>
                </div>
              </div>
            </div>

            <!-- Bouton retirer -->
            <button @click="removeFromComparison(character.id)" class="remove-btn">
              ✕
            </button>
          </div>
          
          <!-- Slot vide -->
          <div v-else class="empty-slot">
            <div class="empty-content">
              <span class="empty-icon">➕</span>
              <p class="empty-text">Sélectionnez un personnage</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Zone de bataille -->
      <div v-if="isBattling" class="battle-arena">
        <div class="battle-participants">
          <div 
            v-for="(character, index) in characters" 
            :key="character.id"
            class="battle-character"
            :class="{ 
              'winner': battleResult && battleResult.winner === character.id,
              'loser': battleResult && battleResult.winner !== character.id,
              'attacking': currentAttacker === character.id
            }"
          >
            <!-- Avatar de combat -->
            <div class="battle-avatar">
              <img :src="character.image" :alt="character.name" />
              <div class="battle-effects" v-if="currentAttacker === character.id">
                <div class="attack-effect"></div>
              </div>
            </div>

            <!-- Nom et informations -->
            <h4 class="battle-name">{{ character.name }}</h4>

            <!-- Barre de vie -->
            <div class="health-bar">
              <div class="health-label">
                <span>❤️ PV</span>
                <span>{{ Math.round(character.currentHealth || character.totalHealth) }}/{{ character.totalHealth }}</span>
              </div>
              <div class="health-bar-bg">
                <div 
                  class="health-bar-fill"
                  :style="{ 
                    width: ((character.currentHealth || character.totalHealth) / character.totalHealth * 100) + '%' 
                  }"
                ></div>
              </div>
            </div>

            <!-- Stats de combat -->
            <div class="battle-stats">
              <div class="battle-stat">
                <span>⚔️</span>
                <span>{{ character.stats.strength }}</span>
              </div>
              <div class="battle-stat">
                <span>🏃</span>
                <span>{{ character.stats.agility }}</span>
              </div>
              <div class="battle-stat">
                <span>🧠</span>
                <span>{{ character.stats.intelligence }}</span>
              </div>
            </div>

            <!-- Effets visuels de victoire/défaite -->
            <div v-if="battleResult" class="result-effect">
              <span v-if="battleResult.winner === character.id" class="victory-text">🏆 VICTOIRE!</span>
              <span v-else class="defeat-text">💀 DÉFAITE</span>
            </div>
          </div>

          <!-- Éclair de combat au centre -->
          <div class="battle-center" v-if="isBattling">
            <div class="vs-text" :class="{ 'animated': isAttacking }">⚡ VS ⚡</div>
            <div v-if="currentAttackText" class="attack-text">{{ currentAttackText }}</div>
          </div>
        </div>

        <!-- Log de combat -->
        <div class="battle-log" v-if="battleLog.length > 0">
          <h5>📜 Journal de Combat</h5>
          <div class="log-entries">
            <div 
              v-for="(entry, index) in battleLog" 
              :key="index"
              class="log-entry"
              :class="entry.type"
            >
              {{ entry.message }}
            </div>
          </div>
        </div>
      </div>

      <!-- Boutons d'action -->
      <div class="comparison-actions">
        <button 
          v-if="characters.length === 2 && !isBattling" 
          @click="startBattle"
          class="battle-btn"
        >
          <span class="btn-icon">⚔️</span>
          <span class="btn-text">Simuler un Duel</span>
        </button>

        <button 
          v-if="isBattling && !battleResult" 
          @click="stopBattle"
          class="stop-battle-btn"
        >
          <span class="btn-icon">⏹️</span>
          <span class="btn-text">Arrêter le Combat</span>
        </button>

        <button 
          v-if="battleResult" 
          @click="resetBattle"
          class="reset-battle-btn"
        >
          <span class="btn-icon">🔄</span>
          <span class="btn-text">Nouveau Combat</span>
        </button>

        <button 
          v-if="isBattling" 
          @click="exitBattle"
          class="exit-battle-btn"
        >
          <span class="btn-icon">🚪</span>
          <span class="btn-text">Quitter</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ComparisonPanel',
  emits: ['remove-character', 'clear-comparison'],
  props: {
    characters: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      isBattling: false,
      battleResult: null,
      battleLog: [],
      currentAttacker: null,
      currentAttackText: '',
      isAttacking: false,
      battleInterval: null,
      statsList: [
        { key: 'strength', label: 'Force' },
        { key: 'agility', label: 'Agilité' },
        { key: 'intelligence', label: 'Intelligence' }
      ]
    }
  },
  computed: {
    displayCharacters() {
      const result = [...this.characters];
      while (result.length < 2) {
        result.push(null);
      }
      return result.slice(0, 2);
    }
  },
  watch: {
    characters: {
      handler(newCharacters) {
        if (newCharacters.length < 2 && this.isBattling) {
          this.exitBattle();
        }
      },
      immediate: true
    }
  },
  methods: {
    removeFromComparison(characterId) {
      this.$emit('remove-character', characterId);
    },
    clearComparison() {
      this.$emit('clear-comparison');
      this.exitBattle();
    },
    handleImageError(event) {
      event.target.src = 'https://via.placeholder.com/100x100/6366f1/ffffff?text=?';
    },
    getStatColor(value) {
      if (value >= 80) return 'linear-gradient(90deg, #10b981, #059669)';
      if (value >= 60) return 'linear-gradient(90deg, #f59e0b, #d97706)';
      if (value >= 40) return 'linear-gradient(90deg, #3b82f6, #2563eb)';
      return 'linear-gradient(90deg, #6b7280, #4b5563)';
    },
    startBattle() {
      if (this.characters.length !== 2) return;

      this.isBattling = true;
      this.battleResult = null;
      this.battleLog = [];
      
      // Initialiser les PV
      this.characters.forEach(char => {
        this.$set(char, 'totalHealth', this.calculateTotalHealth(char));
        this.$set(char, 'currentHealth', char.totalHealth);
      });

      this.battleLog.push({
        type: 'start',
        message: `⚔️ Le combat commence entre ${this.characters[0].name} et ${this.characters[1].name}!`
      });

      // Commencer la simulation
      this.simulateBattle();
    },
    stopBattle() {
      if (this.battleInterval) {
        clearInterval(this.battleInterval);
        this.battleInterval = null;
      }
      this.currentAttacker = null;
      this.isAttacking = false;
      this.currentAttackText = '';
    },
    resetBattle() {
      this.battleResult = null;
      this.battleLog = [];
      this.currentAttacker = null;
      this.currentAttackText = '';
      this.isAttacking = false;
      this.startBattle();
    },
    exitBattle() {
      this.stopBattle();
      this.isBattling = false;
      this.battleResult = null;
      this.battleLog = [];
    },
    calculateTotalHealth(character) {
      // Formule basique pour calculer les PV
      return Math.round((character.stats.strength + character.stats.agility + character.stats.intelligence) * 2);
    },
    calculateDamage(attacker, defender) {
      const baseDamage = attacker.stats.strength;
      const criticalChance = attacker.stats.agility / 100 * 0.3; // 30% max de critique
      const isCritical = Math.random() < criticalChance;
      
      let damage = baseDamage + Math.random() * 20; // Variabilité
      
      if (isCritical) {
        damage *= 1.5;
      }
      
      // Réduction de dégâts basée sur l'agilité du défenseur
      const reduction = defender.stats.agility / 100 * 0.2; // 20% max de réduction
      damage *= (1 - reduction);
      
      return {
        damage: Math.round(damage),
        isCritical
      };
    },
    simulateBattle() {
      let round = 1;
      
      this.battleInterval = setInterval(() => {
        if (this.battleResult) {
          clearInterval(this.battleInterval);
          return;
        }

        const attacker = this.characters[round % 2];
        const defender = this.characters[(round + 1) % 2];
        
        this.currentAttacker = attacker.id;
        this.isAttacking = true;
        
        setTimeout(() => {
          const attack = this.calculateDamage(attacker, defender);
          defender.currentHealth = Math.max(0, defender.currentHealth - attack.damage);
          
          let attackMessage = `${attacker.name} attaque ${defender.name} et inflige ${attack.damage} dégâts`;
          if (attack.isCritical) {
            attackMessage += ' (CRITIQUE!)';
          }
          
          this.currentAttackText = `-${attack.damage}${attack.isCritical ? ' ✨' : ''}`;
          
          this.battleLog.push({
            type: attack.isCritical ? 'critical' : 'attack',
            message: attackMessage
          });

          // Vérifier si le combat est terminé
          if (defender.currentHealth <= 0) {
            this.battleResult = {
              winner: attacker.id,
              loser: defender.id
            };
            
            this.battleLog.push({
              type: 'end',
              message: `🏆 ${attacker.name} remporte le combat!`
            });
            
            clearInterval(this.battleInterval);
            this.currentAttacker = null;
            this.isAttacking = false;
            this.currentAttackText = '';
          }
          
          setTimeout(() => {
            this.currentAttackText = '';
            this.isAttacking = false;
            this.currentAttacker = null;
          }, 1000);
          
        }, 500);
        
        round++;
      }, 2000);
    }
  },
  beforeUnmount() {
    if (this.battleInterval) {
      clearInterval(this.battleInterval);
    }
  }
}
</script>

<style scoped>
.comparison-panel {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 400px;
  max-height: 80vh;
  background: var(--surface);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 2px solid var(--border);
  z-index: 1000;
  transition: all 0.4s ease;
  animation: slideInRight 0.5s ease-out;
}

.comparison-panel.battle-mode {
  width: 600px;
  max-width: 90vw;
}

.comparison-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 2px solid var(--border);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-radius: 14px 14px 0 0;
}

.comparison-title {
  font-size: 1.1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 1.3rem;
}

.clear-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 8px;
  padding: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.comparison-content {
  padding: 20px;
  max-height: calc(80vh - 80px);
  overflow-y: auto;
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.comparison-slot {
  min-height: 200px;
}

.character-compare-card {
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  position: relative;
  transition: all 0.3s ease;
}

.compare-avatar {
  position: relative;
  margin-bottom: 12px;
}

.compare-avatar img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary-color);
}

.character-name-overlay {
  font-size: 0.9rem;
  font-weight: 600;
  margin-top: 8px;
  text-align: center;
  color: var(--text-primary);
}

.compare-stats {
  margin-bottom: 12px;
}

.compare-stat {
  margin-bottom: 8px;
}

.stat-name {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
  display: block;
  margin-bottom: 4px;
}

.stat-comparison {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-bar-compare {
  flex: 1;
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  overflow: hidden;
}

.stat-fill-compare {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease;
}

.stat-value-compare {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-primary);
  min-width: 30px;
  text-align: right;
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: var(--error);
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  transform: scale(1.2);
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
}

.empty-slot {
  border: 2px dashed var(--border);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  transition: all 0.3s ease;
}

.empty-slot:hover {
  border-color: var(--primary-color);
  background: rgba(99, 102, 241, 0.05);
}

.empty-content {
  text-align: center;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 8px;
  display: block;
}

.empty-text {
  font-size: 0.9rem;
  font-weight: 600;
}

/* Styles de bataille */
.battle-arena {
  margin-bottom: 20px;
}

.battle-participants {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 20px;
  align-items: center;
  margin-bottom: 20px;
}

.battle-character {
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  position: relative;
  transition: all 0.4s ease;
}

.battle-character.attacking {
  transform: scale(1.05);
  border-color: var(--warning);
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
}

.battle-character.winner {
  border-color: var(--success);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
  animation: victoryPulse 2s ease-in-out infinite;
}

.battle-character.loser {
  border-color: var(--error);
  background: rgba(239, 68, 68, 0.1);
  opacity: 0.7;
}

.battle-avatar {
  position: relative;
  margin-bottom: 12px;
}

.battle-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary-color);
}

.battle-effects {
  position: absolute;
  inset: 0;
}

.attack-effect {
  position: absolute;
  inset: -10px;
  border: 3px solid var(--warning);
  border-radius: 50%;
  animation: attackPulse 0.5s ease-in-out;
}

.battle-name {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.health-bar {
  margin-bottom: 12px;
}

.health-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--text-secondary);
}

.health-bar-bg {
  height: 8px;
  background: var(--border);
  border-radius: 4px;
  overflow: hidden;
}

.health-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--success), #059669);
  border-radius: 4px;
  transition: width 0.6s ease;
}

.battle-stats {
  display: flex;
  justify-content: space-around;
  gap: 8px;
}

.battle-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.battle-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.vs-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: all 0.3s ease;
}

.vs-text.animated {
  animation: battleShake 0.5s ease-in-out;
}

.attack-text {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--error);
  animation: damageFloat 1s ease-out;
}

.result-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-weight: 700;
  font-size: 1.1rem;
  text-align: center;
  z-index: 10;
}

.victory-text {
  color: var(--success);
  animation: victoryBounce 1s ease-out;
}

.defeat-text {
  color: var(--error);
  opacity: 0.8;
}

.battle-log {
  background: var(--background);
  border: 2px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  max-height: 150px;
  overflow-y: auto;
}

.battle-log h5 {
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.log-entries {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.log-entry {
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 4px;
  animation: fadeInLeft 0.3s ease-out;
}

.log-entry.start {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary-color);
  font-weight: 600;
}

.log-entry.attack {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.log-entry.critical {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
  font-weight: 600;
}

.log-entry.end {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
  font-weight: 700;
}

.comparison-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.comparison-actions button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 140px;
}

.battle-btn {
  background: var(--success);
  color: white;
}

.battle-btn:hover {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.stop-battle-btn, .exit-battle-btn {
  background: var(--error);
  color: white;
}

.stop-battle-btn:hover, .exit-battle-btn:hover {
  background: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.reset-battle-btn {
  background: var(--primary-color);
  color: white;
}

.reset-battle-btn:hover {
  background: #4f46e5;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

/* Animations */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes attackPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
}

@keyframes battleShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

@keyframes damageFloat {
  0% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-30px); }
}

@keyframes victoryPulse {
  0%, 100% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.3); }
  50% { box-shadow: 0 0 30px rgba(16, 185, 129, 0.6); }
}

@keyframes victoryBounce {
  0%, 20%, 50%, 80%, 100% { transform: translate(-50%, -50%) translateY(0); }
  40% { transform: translate(-50%, -50%) translateY(-10px); }
  60% { transform: translate(-50%, -50%) translateY(-5px); }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media (max-width: 768px) {
  .comparison-panel {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    max-height: 70vh;
    border-radius: 16px 16px 0 0;
  }
  
  .comparison-panel.battle-mode {
    width: 100%;
  }
  
  .comparison-grid {
    grid-template-columns: 1fr;
  }
  
  .battle-participants {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .battle-center {
    order: -1;
  }
}</style>