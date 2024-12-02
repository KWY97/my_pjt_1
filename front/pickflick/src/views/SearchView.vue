<template>
  <div class="container">
    <div class="search-header">
      <h2 class="search-keyword">"{{ keyword }}" 검색 결과</h2>
      <span class="search-results" v-if="searchList.length">({{ searchList.length }}건)</span>
    </div>
    <div v-if="searchList.length > 0" class="movie-list">
      <div
        v-for="(movie, index) in searchList"
        :key="index"
        class="movie-item"
        @click="navigateToDetail(movie.movie_id)"
      >
        <img
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          alt="포스터"
          class="movie-poster"
        />
        <div class="movie-info">
          <h4>{{ movie.title }}</h4>
          <p class="overview">{{ movie.overview }}</p>
          <p class="rating">평점: {{ movie.vote_average }}</p>
          <p class="release-date">출시일: {{ movie.release_date }}</p>
        </div>
      </div>
    </div>
    <div v-else class="no-results">
      <p>검색 결과가 없습니다.</p>
    </div>
  </div>
</template>

  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import { useRoute } from 'vue-router';
  import { useCounterStore } from '@/stores/counter';
  import axios from 'axios';
  
  const store = useCounterStore();
  const route = useRoute();
  const keyword = ref(route.params.keyword);
  const searchList = ref([]);
  const navigateToDetail = store.navigateToDetail
  
  // 검색 API 호출 함수
  const searchMovies = () => {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/movies/search/${keyword.value}/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    })
      .then((res) => {
        console.log(res.data);
        searchList.value = res.data.serializer || res.data.results || res.data; // 적합한 키 사용
      })
      .catch((err) => {
        console.error(err);
      });
  };
  
  // 검색어 변경 시 반응
  watch(() => route.params.keyword, (newKeyword) => {
    keyword.value = newKeyword;
    searchMovies();
  })
  
  // 컴포넌트가 마운트되면 초기 검색 실행
  onMounted(() => {
    searchMovies();
  });
  </script>
  
  <style scoped>
 /* 전체 컨테이너 스타일 */
.container {
  padding: 20px;
  background-color: #141414;
  color: #fff;
  font-family: 'Noto Sans KR', sans-serif;
}

/* 리스트 컨테이너 */
.movie-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

/* 개별 리스트 아이템 스타일 */
.movie-item {
  display: flex;
  gap: 30px;
  padding: 15px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  margin-bottom: 20px;
}

.movie-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2);
}

/* 포스터 이미지 */
.movie-poster {
  width: 150px; /* 이미지 크기 고정 */
  height: 225px;
  object-fit: cover;
  border-radius: 5px;
}

/* 텍스트 컨테이너 */
.movie-info {
  flex: 1; /* 텍스트 영역이 남은 공간을 차지하도록 설정 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.movie-info h4 {
  font-size: 1.5em;
  margin-bottom: 10px;
  color: fff; /* 제목 강조 */
}

.movie-info p {
  font-size: 0.9em;
  line-height: 1.5;
  color: #ccc; /* 텍스트 가독성 향상 */
}

/* 줄거리 */
.movie-info .overview {
  display: -webkit-box;
  -webkit-line-clamp: 3; /* 최대 3줄로 제한 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 10px;
}

/* 평점, 출시일 */
.movie-info .rating,
.movie-info .release-date {
  font-size: 0.8em;
  color: #aaa;
}

.search-header {
  display: flex;
  justify-content: space-between; /* 제목과 개수를 양쪽 끝으로 배치 */
  align-items: center; /* 세로 정렬 */
  margin-bottom: 20px;
}

/* 검색 키워드 스타일 */
.search-keyword {
  font-size: 2.1em;
  font-weight: bold;
  color: #fff;
}

/* 검색 결과 개수 스타일 */
.search-results {
  margin-top: 40px;
  font-size: 1.0em;
  color: #ccc; /* 부드러운 색상 */
}
</style>
  