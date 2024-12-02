<template>
  <div class="latest-anime-list">
    <h2>최신 애니메이션 Top 10 ✨</h2>
    <div class="carousel-wrapper">
      <button @click="prevSlide" class="carousel-control prev">&#8249;</button>
      <div class="carousel">
        <div class="carousel-track" :style="trackStyle">
          <LatestAnimeListItem
            v-for="(movie, index) in movies"
            :key="movie.movie_id"
            :movie="movie"
            class="anime-item"
          />
        </div>
      </div>
      <button @click="nextSlide" class="carousel-control next">&#8250;</button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, computed } from 'vue'
import LatestAnimeListItem from './LatestAnimeListItem.vue'

const props = defineProps({
  movies: {
    type: Array,
    required: true
  }
})

const currentIndex = ref(0)
const itemsToShow = 5  // 한 번에 보여줄 애니메이션 개수

const prevSlide = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const nextSlide = () => {
  if (currentIndex.value < props.movies.length - itemsToShow) {
    currentIndex.value++
  }
}

const trackStyle = computed(() => {
  return {
    transform: `translateX(-${currentIndex.value * (100 / itemsToShow)}%)`,
    transition: 'transform 0.5s ease'
  }
})
</script>

<style scoped>
.latest-anime-list {
  padding: 20px;
  background-color: #141414;
  color: white;
  max-width: 85%; /* 가로 폭을 줄이기 위해 최대 너비 설정 */
  margin: 0 auto; /* 가운데 정렬 */
}

.carousel-wrapper {
  position: relative;
  overflow: hidden;
}

.carousel {
  display: flex;
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease;
}

.anime-item {
  flex: 0 0 calc(100% / 5);
  max-width: calc(100% / 5);
  box-sizing: border-box;
  padding: 0 10px;
  background-color: #141414;
}

.carousel-control {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  font-size: 2em;
  cursor: pointer;
  z-index: 10;
}

.prev {
  left: 0;
}

.next {
  right: 0;
}
</style>
