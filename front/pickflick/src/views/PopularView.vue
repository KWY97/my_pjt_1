<template>
  <div class="movie-page">
    <PopularMovieList :movies="store.movies || []" :totalPage="store.totalPages"/>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import PopularMovieList from '@/components/PopularView/PopularMovieList.vue'

const store = useCounterStore()

onMounted(() => {
  store.getMovies()
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
