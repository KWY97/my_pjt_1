
<template>
  <div class="popular-movie-list">
    <h2>🎬 지금 가장 인기 있는 영화들을 만나보세요 !</h2>
      <div class="movie-list">
        <PopularMovieListItem
          v-for="movie in movies"
          :key="movie.movie_id"
          :movie="movie"
          class="movie-card"
        />
      </div>

    <!-- Pagination Controls -->
    <div class="pagination-controls">
        <div class="pagination-controls">
          <button @click="jumpBackward" :disabled="currentPage <= 1" class="pagination-button"><<</button>
          <button @click="previousPage" :disabled="currentPage === 1" class="pagination-button"><</button>
          <!-- 페이지 입력 -->
          <input 
            type="text" 
            v-model="currentPage" 
            @change="goToPage($event)"
            @input="currentPage = currentPage.replace(/[^0-9]/g, '')"
            class="page-input" 
            :max="props.totalPage" 
            :min="1" 
          />
            <span>/ {{ props.totalPage }}</span>
          <button @click="nextPage" :disabled="currentPage === props.totalPage" class="pagination-button">></button>
          <button @click="jumpForward" :disabled="currentPage === props.totalPage" class="pagination-button">>></button>
        </div>
      </div>
  </div>
</template>

<script setup>
  import PopularMovieListItem from '@/components/PopularView/PopularMovieListItem.vue'
  import { defineProps, ref, watch } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  const store = useCounterStore()

  const props = defineProps({
    movies: {
      type: Array,
      required: true
    },
    totalPage: {
      type: Number,
      required: true
    }
  })

  const currentPage = ref(1);
  const inputPage = ref(currentPage.value);

  watch(currentPage, (newPage) => {
    inputPage.value = newPage;
  });


  // Functions to change pages
  const previousPage = () => {
    if (store.currentPage > 1) {
      currentPage.value -= 1
      store.getMovies(store.currentPage - 1)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  const nextPage = () => {
    if (store.currentPage < props.totalPage) {
      currentPage.value += 1
      store.getMovies(store.currentPage + 1)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  // 10페이지 앞으로 이동
  const jumpForward = () => {
    const targetPage = Math.min(currentPage.value + 10, props.totalPage);
    store.getMovies(targetPage);
    currentPage.value = targetPage;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // 10페이지 뒤로 이동
  const jumpBackward = () => {
    const targetPage = Math.max(currentPage.value - 10, 1);
    store.getMovies(targetPage);
    currentPage.value = targetPage;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // 입력된 페이지로 이동
  const goToPage = (event) => {
    const targetPage = parseInt(inputPage.value, 10);
    if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= props.totalPage) {
      store.getMovies(targetPage);
      currentPage.value = targetPage;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      alert(`1부터 ${props.totalPage} 사이의 숫자를 입력하세요.`);
      inputPage.value = currentPage.value; // 잘못된 입력 시 원래 페이지로 복구
    }
    event.target.blur();
    };
</script>

<style scoped>
.popular-movie-list {
  color: white;
  padding: 20px;
  background-color: #141414; /* 넷플릭스 스타일의 검은 배경 */
}

.movie-list {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px 0;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination-button {
  background-color: #e50914;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 0 10px;
  cursor: pointer;
  border-radius: 4px;
}

.pagination-button:disabled {
  background-color: #555;
  cursor: not-allowed;
}

.page-input {
  width: 50px;
  text-align: center;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 5px;
  margin: 0 10px;
  background-color: #222;
  color: white;
}

.page-input:focus {
  outline: none;
  border-color: #e50914; /* 포커스 시 넷플릭스 레드 */
}
</style>
