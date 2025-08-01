<template>
  <div class="app-container">
    <h1>Fandom Scraper</h1>

    <div class="form-group">
      <input v-model="fandomUrl" type="text" placeholder="Entrez l'URL Fandom" />
      <button @click="launchScraping">Scraper</button>
    </div>

    <div v-if="loading">Scraping en cours...</div>
    <div v-if="success">{{ message }}</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>


<script setup>
import { ref } from 'vue'

const fandomUrl = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(null)
const message = ref('')

const launchScraping = async () => {
  if (!fandomUrl.value) {
    error.value = "Veuillez entrer une URL."
    return
  }

  loading.value = true
  error.value = null
  success.value = false

  try {
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





<style scoped>
.app-container {
  max-width: 600px;
  margin: 50px auto;
  text-align: center;
  font-family: sans-serif;
}

.form-group {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

input[type="text"] {
  width: 60%;
  padding: 8px;
}

button {
  padding: 8px 16px;
  cursor: pointer;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
