<template>
  <div class="gaming-background-container">
    <!-- Canvas principal pour les effets 3D -->
    <canvas 
      ref="mainCanvas" 
      class="gaming-canvas-main"
      @mousemove="handleMouseMove"
    ></canvas>
    
    <!-- Canvas pour les particules -->
    <canvas 
      ref="particlesCanvas" 
      class="gaming-canvas-particles"
    ></canvas>
    
    <!-- Grille overlay -->
    <div class="gaming-grid-overlay"></div>
    
    <!-- Scan lines effect -->
    <div class="gaming-scan-lines"></div>
    
    <!-- Particules HTML pour les effets légers -->
    <div class="html-particles">
      <div 
        v-for="n in particleCount" 
        :key="n"
        class="html-particle"
        :style="getParticleStyle(n)"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GamingBackground',
  data() {
    return {
      particleCount: 30,
      animationId: null,
      mouse: { x: 0, y: 0 },
      particles: [],
      connections: [],
      time: 0
    }
  },
  mounted() {
    this.initializeCanvas();
    this.createParticles();
    this.animate();
    this.handleResize();
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    initializeCanvas() {
      const mainCanvas = this.$refs.mainCanvas;
      const particlesCanvas = this.$refs.particlesCanvas;
      
      if (!mainCanvas || !particlesCanvas) return;
      
      this.mainCtx = mainCanvas.getContext('2d');
      this.particlesCtx = particlesCanvas.getContext('2d');
      
      this.resizeCanvases();
    },
    
    resizeCanvases() {
      const width = window.innerWidth;
      const height = window.innerHeight;
      
      [this.$refs.mainCanvas, this.$refs.particlesCanvas].forEach(canvas => {
        if (canvas) {
          canvas.width = width;
          canvas.height = height;
        }
      });
    },
    
    handleResize() {
      this.resizeCanvases();
      this.createParticles();
    },
    
    handleMouseMove(event) {
      this.mouse.x = event.clientX;
      this.mouse.y = event.clientY;
    },
    
    createParticles() {
      this.particles = [];
      const canvas = this.$refs.mainCanvas;
      if (!canvas) return;
      
      const particleCount = Math.floor((canvas.width * canvas.height) / 15000);
      
      for (let i = 0; i < particleCount; i++) {
        this.particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          size: Math.random() * 2 + 1,
          opacity: Math.random() * 0.5 + 0.2,
          color: this.getRandomColor(),
          connectionRadius: 100 + Math.random() * 50
        });
      }
    },
    
    getRandomColor() {
      const colors = ['#00ff41', '#00ccff', '#ff0080', '#ffff00'];
      return colors[Math.floor(Math.random() * colors.length)];
    },
    
    updateParticles() {
      const canvas = this.$refs.mainCanvas;
      if (!canvas) return;
      
      this.particles.forEach(particle => {
        // Mouvement basique
        particle.x += particle.vx;
        particle.y += particle.vy;
        
        // Rebond sur les bords
        if (particle.x < 0 || particle.x > canvas.width) {
          particle.vx *= -1;
        }
        if (particle.y < 0 || particle.y > canvas.height) {
          particle.vy *= -1;
        }
        
        // Attraction vers la souris
        const dx = this.mouse.x - particle.x;
        const dy = this.mouse.y - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 150) {
          const force = (150 - distance) / 150;
          particle.vx += (dx / distance) * force * 0.01;
          particle.vy += (dy / distance) * force * 0.01;
        }
        
        // Limite de vitesse
        const speed = Math.sqrt(particle.vx * particle.vx + particle.vy * particle.vy);
        if (speed > 2) {
          particle.vx = (particle.vx / speed) * 2;
          particle.vy = (particle.vy / speed) * 2;
        }
      });
    },
    
    drawParticles() {
      const ctx = this.particlesCtx;
      if (!ctx) return;
      
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      
      // Dessiner les particules
      this.particles.forEach(particle => {
        ctx.save();
        ctx.globalAlpha = particle.opacity;
        ctx.fillStyle = particle.color;
        ctx.shadowColor = particle.color;
        ctx.shadowBlur = 10;
        
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      });
      
      // Dessiner les connexions
      this.drawConnections();
    },
    
    drawConnections() {
      const ctx = this.particlesCtx;
      if (!ctx) return;
      
      for (let i = 0; i < this.particles.length; i++) {
        for (let j = i + 1; j < this.particles.length; j++) {
          const p1 = this.particles[i];
          const p2 = this.particles[j];
          
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < p1.connectionRadius) {
            const opacity = (1 - distance / p1.connectionRadius) * 0.3;
            
            ctx.save();
            ctx.globalAlpha = opacity;
            ctx.strokeStyle = p1.color;
            ctx.lineWidth = 1;
            ctx.shadowColor = p1.color;
            ctx.shadowBlur = 5;
            
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
            ctx.restore();
          }
        }
      }
    },
    
    drawMainEffects() {
      const ctx = this.mainCtx;
      if (!ctx) return;
      
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      
      // Effet de vague énergétique
      this.drawEnergyWaves();
      
      // Effet de grille dynamique
      this.drawDynamicGrid();
    },
    
    drawEnergyWaves() {
      const ctx = this.mainCtx;
      const canvas = ctx.canvas;
      
      ctx.save();
      ctx.globalAlpha = 0.1;
      
      const waveCount = 3;
      const colors = ['#00ff41', '#00ccff', '#ff0080'];
      
      for (let i = 0; i < waveCount; i++) {
        const wave = {
          amplitude: 50 + i * 20,
          frequency: 0.01 + i * 0.005,
          phase: this.time * 0.001 + i * Math.PI / 3,
          color: colors[i]
        };
        
        ctx.strokeStyle = wave.color;
        ctx.lineWidth = 2;
        ctx.shadowColor = wave.color;
        ctx.shadowBlur = 20;
        
        ctx.beginPath();
        for (let x = 0; x <= canvas.width; x += 5) {
          const y = canvas.height / 2 + 
                   Math.sin(x * wave.frequency + wave.phase) * wave.amplitude +
                   Math.sin(x * wave.frequency * 2 + wave.phase * 1.5) * wave.amplitude * 0.5;
          
          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        ctx.stroke();
      }
      
      ctx.restore();
    },
    
    drawDynamicGrid() {
      const ctx = this.mainCtx;
      const canvas = ctx.canvas;
      
      ctx.save();
      ctx.globalAlpha = 0.05;
      ctx.strokeStyle = '#00ff41';
      ctx.lineWidth = 1;
      
      const gridSize = 50;
      const offset = (this.time * 0.02) % gridSize;
      
      // Lignes verticales
      for (let x = -offset; x <= canvas.width + gridSize; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }
      
      // Lignes horizontales
      for (let y = -offset; y <= canvas.height + gridSize; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }
      
      ctx.restore();
    },
    
    animate() {
      this.time++;
      this.updateParticles();
      this.drawParticles();
      this.drawMainEffects();
      
      this.animationId = requestAnimationFrame(this.animate);
    },
    
    getParticleStyle(index) {
      const colors = ['#00ff41', '#00ccff', '#ff0080', '#ffff00'];
      const color = colors[index % colors.length];
      const size = Math.random() * 3 + 1;
      const duration = 10 + Math.random() * 20;
      const delay = Math.random() * 5;
      
      return {
        '--particle-color': color,
        '--particle-size': size + 'px',
        '--animation-duration': duration + 's',
        '--animation-delay': delay + 's',
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%'
      };
    }
  }
}
</script>

<style scoped>
.gaming-background-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -10;
  overflow: hidden;
}

.gaming-canvas-main,
.gaming-canvas-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.gaming-canvas-main {
  z-index: -9;
}

.gaming-canvas-particles {
  z-index: -8;
}

.gaming-grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px),
    linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridPulse 4s ease-in-out infinite;
  z-index: -7;
}

.gaming-scan-lines {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 255, 65, 0.01) 2px,
    rgba(0, 255, 65, 0.01) 4px
  );
  animation: scanMove 8s linear infinite;
  z-index: -6;
}

.html-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -5;
}

.html-particle {
  position: absolute;
  width: var(--particle-size);
  height: var(--particle-size);
  background: var(--particle-color);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--particle-color);
  animation: 
    particleFloat var(--animation-duration) linear infinite var(--animation-delay),
    particleGlow 2s ease-in-out infinite alternate;
}

@keyframes gridPulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

@keyframes scanMove {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}

@keyframes particleFloat {
  0% {
    transform: translateY(100vh) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-10vh) translateX(50px) rotate(360deg);
    opacity: 0;
  }
}

@keyframes particleGlow {
  0% { 
    box-shadow: 0 0 5px var(--particle-color);
    transform: scale(1);
  }
  100% { 
    box-shadow: 0 0 15px var(--particle-color), 0 0 25px var(--particle-color);
    transform: scale(1.2);
  }
}

/* Performance optimizations */
.gaming-canvas-main,
.gaming-canvas-particles {
  will-change: transform;
}

.html-particle {
  will-change: transform, opacity;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .gaming-grid-overlay {
    background-size: 30px 30px;
  }
  
  .html-particles .html-particle:nth-child(n+16) {
    display: none;
  }
}

@media (max-width: 480px) {
  .gaming-grid-overlay {
    background-size: 25px 25px;
    opacity: 0.5;
  }
  
  .gaming-scan-lines {
    opacity: 0.3;
  }
  
  .html-particles .html-particle:nth-child(n+11) {
    display: none;
  }
}

/* Reduce motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  .gaming-grid-overlay,
  .gaming-scan-lines,
  .html-particle {
    animation: none;
  }
  
  .gaming-canvas-main,
  .gaming-canvas-particles {
    opacity: 0.3;
  }
}</style>