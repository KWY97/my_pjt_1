<template>
    <div class="weather-movie-item" @click="navigateToDetail(movie.movie_id)">
      <img :src="posterUrl" alt="Movie Poster" class="movie-poster" />
      <div class="movie-info">
        <h4>{{ movie.title }}</h4>
        <p>{{ movie.overview }}</p>
        <p class="rating">평점: {{ movie.vote_average }}</p>
        <p class="release-date">출시일: {{ movie.release_date }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps, computed } from 'vue'
  import { useCounterStore } from '@/stores/counter'

  const store = useCounterStore()
  const navigateToDetail = store.navigateToDetail
  
  // props 정의하기: 부모 컴포넌트에서 영화 정보를 받아요
  const props = defineProps({
    movie: {
      type: Object,
      required: true
    }
  })
  
  // 영화 포스터 URL 계산하기
  const posterUrl = computed(() => {
    return props.movie.poster_path ? `https://image.tmdb.org/t/p/w500${props.movie.poster_path}` : 'default-poster.png'
  })
  </script>
  
<style scoped>
.weather-movie-item {
  width: 20%;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  transition: transform 0.3s ease;
  background-color: #222; /* 카드 배경 */
  cursor: pointer;
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
  padding: 20px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  opacity: 0;
  transition: opacity 0.3s;
  font-family: 'Noto Sans KR', sans-serif;
}
  
.weather-movie-item:hover .movie-info {
  opacity: 1;
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2);
}

.weather-movie-item:hover {
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

.rating,
.release-date {
  font-size: 12px;
  margin: 0;
}
</style>
  