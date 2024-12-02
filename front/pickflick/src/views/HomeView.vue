<template>
  <div class="movie-page">
    <WeatherMovieList :movies="store.weatherMovies || []" :weatherMain="store.weatherMain || ''" />
    <br><br>
    <TopMovieList :movies="store.topMovies || []" />
    <br><br>
    <LatestAnimeList :movies="store.latestAnime || []" />
    <br><br>
    <AdultMovieList :movies="store.adultMovies || []" />
  </div>
</template>

<script setup>
import TopMovieList from '@/components/HomeView/TopMovieList.vue'
import WeatherMovieList from '@/components/HomeView/WeatherMovieList.vue'
import LatestAnimeList from '@/components/HomeView/LatestAnimeList.vue'
import AdultMovieList from '@/components/HomeView/AdultMovieList.vue'
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

onMounted(() => {
  store.getTopMovies()
  store.getWeatherBasedRecommendations()
  store.getLatestAnime()
  store.getAdultMovies()
  store.getCityWeather('Seoul')
})


</script>

<style scoped>
.movie-page {
  padding: 20px;
  color: white;
  background-color: #141414; /* 넷플릭스 스타일의 검은 배경 */
  min-height: 100vh; /* 화면 전체 높이 차지 */
}
</style>
