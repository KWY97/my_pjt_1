<template>
  <div class="movie-card-content" @click="navigateToDetail(movie.movie_id)">
    <img :src="posterUrl" alt="Movie Poster" class="movie-poster">
    <div class="movie-info">
      <h4>{{ movie.title }}</h4>
      <p>{{ movie.overview }}</p>
      <p class="rating">평점: {{ movie.vote_average }}</p>
      <p class="release-date">출시일: {{ movie.release_date }}</p>
    </div>
    <div>
      <h4 class="movie-card-title">{{ movie.title }}</h4>
    </div>
  </div>
</template>

<script setup>
  import { defineProps, computed } from 'vue'
  import { useCounterStore } from '@/stores/counter'

  const store = useCounterStore()
  const navigateToDetail = store.navigateToDetail

  const props = defineProps({
    movie: {
      type: Object,
      required: true
    }
  })

  const posterUrl = computed(() => {
  return props.movie.poster_path ? `https://image.tmdb.org/t/p/w500${props.movie.poster_path}` : 'default-poster.png'
})
</script>

<style scoped>
.movie-card-content {
  width: 200px;
  height: 300px;
  position: relative;
  border-radius: 10px;
  transition: transform 0.3s ease;
  background-color: #222; /* 카드 배경 */
  cursor: pointer;
  margin-bottom: 30px;
  margin-left: 10px;
  margin-right: 10px;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4%;
}

.movie-info {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 10px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  opacity: 0;
  transition: opacity 0.3s;
  font-family: 'Noto Sans KR', sans-serif;
}

.movie-card-content:hover .movie-info {
  opacity: 1;
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2);
}

.movie-card-content:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2);
}

.movie-info h4 {
  font-size: 16px;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.movie-info p {
  font-size: 12px;
  margin: 5px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.movie-card-title {
  margin-top: 8px;
  font-size: 16px;
  color: white;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rating,
.release-date {
  font-size: 12px;
  margin: 0;
}
</style>