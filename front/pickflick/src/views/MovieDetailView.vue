<template>
  <div class="movie-detail-page">
    <div
      class="movie-backdrop"
      :style="{ backgroundImage: `url(${backdropUrl})` }"
    ></div>

    <div class="movie-info-card">
      <img :src="posterUrl" alt="Poster" class="movie-poster" />
      <div class="movie-details">
        <h1 class="movie-title">{{ movie.title }}</h1>
        <p class="movie-overview">{{ movie.overview }}</p>
        <ul>
          <li><strong>평점:</strong> {{ movie.vote_average }}</li>
          <li><strong>상영시간:</strong> {{ movie.runtime }}분</li>
          <li><strong>감독:</strong> 
            {{ movie.director ? JSON.parse(movie.director.replace(/'/g, '"')).name : '정보 없음' }}
          </li>
          <li><strong>출연:</strong>
            {{ getCastNames(movie.cast) }}
          </li>
          <li><strong>개봉일:</strong> {{ movie.release_date }}</li>
        </ul>
        <div class="movie-actions">
          <button class="play-button" @click="playTrailer">▶예고편</button>
          <button 
            class="favorite-button" 
            :class="favoriteStatus ? 'is-like' : 'is-not-like'"
            @click="toggleFavorite"
          >
            ♥ 좋아요
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="comments-container">
    <h3>댓글 작성</h3>
    <!-- 댓글 작성 -->
    <div class="comment-form">
        <textarea 
          v-model="newComment" 
          rows="3" 
          placeholder="댓글을 작성하세요..." 
          class="comment-input">
        </textarea>
        <button @click="postComment" class="comment-submit-button">작성</button>
    </div>
    <!-- 댓글 목록 -->
    <div>
    <h3>댓글 목록</h3>
    <ul class="comment-list">
  <li
    v-for="comment in sortedComments"
    :key="comment.id"
    :id="`comment-${comment.id}`"
    class="comment-item"
  >
    <div class="comment-header">
      <span class="comment-user">{{ comment.user }}</span>
      <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
    </div>
    <div class="comment-actions">
      <p class="comment-content">{{ comment.content }}</p>
      <div v-if="comment.user === store.userName">
        <!-- 수정 버튼 -->
        <button @click="editComment(comment)" class="edit-button">수정</button>
        <textarea
          v-if="editingComment === comment.id"
          v-model="editedCommentContent"
          class="comment-edit-input"
        ></textarea>
        <button
          v-if="editingComment === comment.id"
          @click="saveEdit(comment.id)"
          class="save-button"
        >
          저장
        </button>
        <!-- 삭제 버튼 -->
        <button
          v-if="comment.user === store.userName"
          @click="deleteComment(comment.id)"
          class="delete-button"
        >
          삭제
        </button>
      </div>
    </div>
  </li>
</ul>
</div>
<!-- YouTube 예고편 모달 -->
<div v-if="isTrailerVisible" class="trailer-modal">
  <div class="trailer-content">
    <button class="close-button" @click="isTrailerVisible = false">X</button>
    <iframe
      :src="`https://www.youtube.com/embed/${videoId}`"
      frameborder="0"
      allow="autoplay; encrypted-media"
      allowfullscreen
      class="trailer-iframe"
    ></iframe>
  </div>
</div>

</div>
</template>


<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

const route = useRoute()
const movie = ref({})
const store = useCounterStore()
const favoriteStatus = ref(false)

const sortedComments = computed(() => {
  return [...comments.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
})

const fetchFavoriteStatus = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/users/${store.userId}/movies/${route.params.id}/isliked/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      console.log('서버 데이터', res.data)
      favoriteStatus.value = res.data.is_liked; // 서버에서 좋아요 상태 받아오기
      console.log('가져오기 성공', favoriteStatus.value)
    })
    .catch((err) => {
      console.error('좋아요 상태 가져오기 실패:', err);
    });
};

const toggleFavorite = () => {
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/movies/${route.params.id}/likes/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      console.log('변경성공')
      favoriteStatus.value = res.data.is_liked; // 서버에서 최신 상태 받아오기
      console.log(favoriteStatus.value)
    })
    .catch((err) => {
      console.error('좋아요 상태 업데이트 실패:', err);
    });
};


const comments = ref([]) // 댓글 조회
const newComment = ref("") // 댓글 작성 
const editingComment = ref(null) // 수정중인 댓글 ID
const editedCommentContent = ref("") // 수정된 댓글 내용

const commentUser = ref(null) // 댓글을 작성한 유저 ID

const getMovieDetail = function () {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/${route.params.id}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      movie.value = res.data
      console.log('영화 데이터:', res.data)
    })
    .catch((err) => {
      console.error('API 호출 중 오류:', err)
    })
}


// 댓글 작성
const postComment = function () {
  if (!newComment.value.trim()) return;

  console.log("전송할 댓글 내용:", newComment.value);
  console.log("영화 ID:", route.params.id);
  console.log("사용자 토큰:", store.token);

  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/movies/${route.params.id}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: {
      content: newComment.value,
    },
  })
    .then((res) => {
      console.log("댓글 작성 성공:", res.data.user);
      console.log("댓글 작성 성공2:", store.userName);
      commentUser.value = res.data.user;

      // 댓글 추가
      comments.value.unshift(res.data);
      newComment.value = ""; // 입력 필드 초기화

      // DOM 업데이트 후 작성한 댓글로 스크롤
      nextTick(() => {
        const addedCommentElement = document.getElementById(`comment-${res.data.id}`);
        if (addedCommentElement) {
          addedCommentElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    })
    .catch((err) => {
      console.error("댓글 작성 오류:", err);
    });
};


// 댓글 조회
const getComments = function () {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/${route.params.id}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      console.log('댓글 조회 데이터 입니다.', res.data)
      comments.value = res.data
    })
    .catch((err) => {
      console.error('댓글 가져오기 오류:', err)
    })
}

// 댓글 수정
const editComment = function (comment) {
  editingComment.value = comment.id
  editedCommentContent.value = comment.content
}

// 댓글 수정 저장
const saveEdit = function (commentId) {
  if (!editedCommentContent.value.trim()) return
  axios({
    method: 'put',
    url: `${store.API_URL}/api/v1/movies/${route.params.id}/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: {
      content: editedCommentContent.value,
    },
  })
    .then((res) => {
      console.log("댓글 수정 성공:", res.data)
      const index = comments.value.findIndex(comment => comment.id === commentId)
      if (index !== -1) {
        comments.value[index].content = editedCommentContent.value
      }
      editingComment.value = null // 수정 모드 종료
      editedCommentContent.value = "" // 수정 내용 초기화
    })
    .catch((err) => {
      console.error("댓글 수정 오류:", err)
    })
}

// 댓글 삭제
const deleteComment = function (commentId) {
  axios({
    method: 'delete',
    url: `${store.API_URL}/api/v1/movies/${route.params.id}/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      console.log("댓글 삭제 성공:", res.data)
      comments.value = comments.value.filter(comment => comment.id !== commentId)
    })
    .catch((err) => {
      console.error("댓글 삭제 오류:", err)
    })
}


const backdropUrl = computed(() => {
  return movie.value.backdrop_path
    ? `https://image.tmdb.org/t/p/w1280${movie.value.backdrop_path}`
    : 'default-backdrop.png'
})

const posterUrl = computed(() => {
  return movie.value.poster_path
    ? `https://image.tmdb.org/t/p/w500${movie.value.poster_path}`
    : 'default-poster.png'
})

const formatDate = function (dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString() + " " + date.toLocaleTimeString()
}

// 유튜브 예고편 드가자
const videoId = ref(null)
const isTrailerVisible = ref(false)

const YOUTUBE_API_KEY = 'Input Your API KEY' // 본인의 API 키 입력하기

const fetchTrailer = async (movieTitle) => {
  const API_URL = 'https://www.googleapis.com/youtube/v3/search';

  try {
    const response = await axios.get(API_URL, {
      params: {
        part: 'snippet',
        q: `${movieTitle} official trailer`, // 영화 제목 + 예고편 검색어
        key: YOUTUBE_API_KEY,
        maxResults: 1,
        type: 'video',
      },
    });

    const videoId = response.data.items[0]?.id?.videoId;
    if (videoId) {
      return videoId;
    } else {
      throw new Error('예고편을 찾을 수 없습니다.');
    }
  } catch (error) {
    console.error('YouTube API 호출 오류:', error);
    throw error;
  }
};

const playTrailer = async () => {
  try {
    const trailerId = await fetchTrailer(movie.value.title); // 영화 제목으로 예고편 검색
    videoId.value = trailerId;
    isTrailerVisible.value = true; // 모달 표시
  } catch (error) {
    alert('예고편을 불러올 수 없습니다.');
  }
};


const getCastNames = (castData) => {
  try {
    // 문자열을 JSON으로 변환
    const castArray = JSON.parse(castData.replace(/'/g, '"'));
    // 이름만 추출 후 콤마로 연결
    return castArray.map(cast => cast.name).join(', ');
  } catch (error) {
    console.error('캐스트 데이터 파싱 중 오류:', error);
    return '정보 없음';
  }
};



onMounted(() => {
  getMovieDetail()
  getComments()
  fetchFavoriteStatus()
})
</script>

<style scoped>
/* 배경 */
.movie-detail-page {
  color: white;
  font-family: Arial, sans-serif;
  background-color: #141414;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative; /* 부모로 위치 기준 설정 */
}

.movie-backdrop {
  width: 100%;
  height: 90vh;
  background-size: cover;
  background-position: center;
  top: 0;
  left: 0;
  z-index: 1; /* 백드롭 레이어 순서 */
}

.movie-backdrop::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6); /* 어두운 오버레이 */
  z-index: 2; /* 오버레이 레이어 */
}

/* 영화 정보 카드 */
.movie-info-card {
  width: 100%;
  display: flex;  
  gap: 20px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  margin-top: -325px; /* 백드롭과 겹치게 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
  animation: fadeIn 1s ease-in-out;
  position: relative; /* 카드가 독립적으로 위치를 가지도록 설정 */
  z-index: 10; /* 백드롭 위에 표시 */
}

/* 포스터 */
.movie-poster {
  width: 200px;
  border-radius: 8px;
}

/* 영화 정보 */
.movie-details {
  flex: 1;
}

.movie-title {
  font-size: 2rem;
  margin-bottom: 10px;
}

.movie-overview {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 20px;
}

.movie-actions {
  display: flex;
  gap: 10px;
}


/* 버튼 */
.play-button {
  background: #e50914;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.play-button:hover {
  background: #f61c27;
}

.favorite-button:hover {
  background: #666; /* Hover 배경색 */
}

.favorite-button.is-like {
  background: #f61c27; /* 좋아요 상태 배경색 */
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.favorite-button.is-not-like {
  background: #444; /* 좋아요 해제 상태 배경색 */
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}


.comments-container {
  margin-top: 40px;
  padding: 20px;
  background-color: #1c1c1c; /* 넷플릭스 스타일의 어두운 배경 */
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.7); /* 부드러운 그림자 */
  color: white;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-input {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #333;
  color: white;
  font-size: 16px;
  resize: none;
}

.comment-input::placeholder {
  color: #777; /* 플레이스홀더 색상 */
}

.comment-submit-button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #e50914; /* 넷플릭스 레드 */
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

.comment-submit-button:hover {
  background-color: #f61c27; /* Hover 효과 */
}

.comment-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.comment-item {
  padding: 15px;
  margin-bottom: 15px;
  background-color: #2a2a2a; /* 댓글 항목 배경 */
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5); /* 부드러운 그림자 */
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: #bbb;
}

.comment-user {
  font-weight: bold;
}

.comment-date {
  font-style: italic;
}

.comment-actions {
  display: flex;
  flex-direction: column;
  gap: 10px; /* 버튼 간격 */
}

.comment-content {
  font-size: 16px;
  color: #eee;
  line-height: 1.5;
  margin-bottom: 10px;
}

.comment-edit-input {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #444;
  color: white;
  font-size: 16px;
  resize: none;
  margin-top: 6px;
}

.edit-button, .save-button, .delete-button {
  padding: 8px 12px;
  font-size: 14px;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease, color 0.3s ease;
}

/* 수정 버튼 */
.edit-button {
  background-color: #333; /* 어두운 배경 */
  color: white
}

.edit-button:hover {
  background-color: #444; /* 약간 더 밝은 배경 */
}

/* 저장 버튼 */
.save-button {
  background-color: #333; /* 어두운 배경 */
  color: white
}

.save-button:hover {
  background-color: #444; /* 약간 더 밝은 배경 */
  color: #42c765; /* 더 밝은 초록색 텍스트 */
}

/* 삭제 버튼 */
.delete-button {
  background-color: #333; /* 어두운 배경 */
  color: #d9534f; /* 빨간색 텍스트 */
}

.delete-button:hover {
  background-color: #444; /* 약간 더 밝은 배경 */
  color: #ff5f5f; /* 더 밝은 빨간색 텍스트 */
}


/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.trailer-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.trailer-content {
  position: relative;
  width: 80%;
  max-width: 800px;
  aspect-ratio: 16 / 9;
}

.trailer-iframe {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.close-button {
  height: 25px;
  width: auto;
  position: absolute;
  top: 0px;
  right: 0px;
  background-color: red;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
}

.close-button:hover {
  background-color: #f61c27; /* 더 밝은 빨간색 */
  color: #fff; /* 텍스트는 선명한 흰색 유지 */
  transform: scale(1.1); /* 살짝 확대 효과 */
}
</style>