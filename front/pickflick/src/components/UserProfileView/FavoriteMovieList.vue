<template>
  <div class="favorite-movie-list">
    <h3>👍 내가 좋아요 표시한 영화</h3>
    <div class="movie-list" v-if="movies.length > 0">
      <FavoriteMovieListItem
        v-for="movie in movies"
        :key="movie.movie_id"
        :movie="movie"
        class="movie-card"
      />
    </div>
    <p v-else class="no-movies-message">내가 좋아하는 영화로 나만의 리스트를 만들어보세요! 🍿</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import FavoriteMovieListItem from './FavoriteMovieListItem.vue'

const props = defineProps({
  movies: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.favorite-movie-list {
  color: white;
  padding: 20px;
  background-color: #141414; /* 넷플릭스 스타일의 검은 배경 */
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px 0;
}

.no-movies-message {
  color: #aaa; /* 텍스트 색상 */
  font-size: 1.4rem;
  text-align: center;
  margin-top: 60px;
}
</style>
