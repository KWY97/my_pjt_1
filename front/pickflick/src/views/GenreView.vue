<template>
    <div class="movie-page">
      <h2>🎥 {{ genre }} 장르의 인기 영화들을 만나보세요!</h2>
      <div class="movie-list">
        <div 
          class="movie-card-content"
          v-for="movie in movies"
          :key="movie.movie_id"
          @click="navigateToDetail(movie.movie_id)"
        >
          <img :src="getPosterUrl(movie.poster_path)" alt="Movie Poster" class="movie-poster" />
          <div class="movie-info">
            <h4>{{ movie.title }}</h4>
            <p>{{ movie.overview }}</p>
            <p class="rating">평점: {{ movie.vote_average }}</p>
            <p class="release-date">출시일: {{ movie.release_date }}</p>
          </div>
          <h4 class="movie-card-title">{{ movie.title }}</h4>
        </div>
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
            :max="totalPages" 
            :min="1" 
          />
            <span>/ {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages" class="pagination-button">></button>
          <button @click="jumpForward" :disabled="currentPage === totalPages" class="pagination-button">>></button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import { useRoute } from 'vue-router';
  import axios from 'axios';
  import { useCounterStore } from '@/stores/counter';
  
  const route = useRoute();
  const store = useCounterStore();
  const genre = ref(route.params.genre);
  const movies = ref([]);
  const currentPage = ref(1);
  const totalPages = ref(0);
  const navigateToDetail = store.navigateToDetail

  // 10페이지씩 앞으로 이동
  const jumpForward = () => {
    if (currentPage.value + 10 < totalPages.value) {
      currentPage.value += 10;
    } else {
      currentPage.value = totalPages.value; // 마지막 페이지로 이동
    }
    fetchMoviesByGenre();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // 10페이지씩 뒤로 이동
  const jumpBackward = () => {
    if (currentPage.value === 10) {
      currentPage.value = 1; // 현재 페이지가 10일 때 1페이지로 이동
    } else if (currentPage.value - 10 >= 1) {
      currentPage.value -= 10;
    } else {
      currentPage.value = 1; // 첫 페이지로 이동
    }
    fetchMoviesByGenre();
    window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const goToPage = (event) => {
      const targetPage = parseInt(currentPage.value); // 입력된 페이지 번호
      if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= totalPages.value) {
        currentPage.value = targetPage; // 입력된 페이지로 이동
        fetchMoviesByGenre(); // 새로운 데이터를 로드
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        alert(`1부터 ${totalPages.value} 사이의 숫자를 입력하세요.`); // 유효하지 않은 경우 알림
      }
        event.target.blur(); // 입력 필드에서 포커스 해제
      };


  
  const fetchMoviesByGenre = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/genre/${genre.value}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    params: {
      page: currentPage.value,
    },
  })
    .then((res) => {
      movies.value = res.data.results || []
      totalPages.value = Math.ceil(res.data.count / 35)
    })
    .catch((error) => {
      console.error('영화 데이터를 가져오는 데 실패했습니다:', error)
    })
  }

  
  // 한 페이지 앞으로 이동
  const previousPage = () => {
    if (currentPage.value > 1) {
      currentPage.value -= 1
      fetchMoviesByGenre()
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
  
  // 한 페이지 뒤로 이동
  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value += 1
      fetchMoviesByGenre()
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
  
  
  // URL 변경 감지
  watch(
    () => route.params.genre,
    (newGenre) => {
      genre.value = newGenre;
      currentPage.value = 1; // 페이지를 초기화
      fetchMoviesByGenre(); // 새로운 데이터를 로드
    }
  );
  
  onMounted(() => {
    fetchMoviesByGenre()
  })
  
  // 포스터 URL 생성
  const getPosterUrl = (posterPath) => {
    return posterPath ? `https://image.tmdb.org/t/p/w500${posterPath}` : 'default-poster.png';
  };
  </script>
  
  <style scoped>
  .movie-page {
    padding: 20px;
    color: white;
    background-color: #141414; /* 넷플릭스 스타일의 검은 배경 */
    min-height: 100vh; /* 화면 전체 높이 차지 */
  }
  
  .movie-list {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px 0;
  }
  
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
    font-weight: bold;
  }
  
  .pagination-button:disabled {
    background-color: #555;
    cursor: not-allowed;
  }
  
  .page-info {
    font-size: 16px;
    margin-left: 15px;
    margin-right: 15px;
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
  font-size: 16px;
}

.page-input:focus {
  outline: none;
  border-color: #e50914; /* 포커스 시 넷플릭스 레드 */
}

</style>
  