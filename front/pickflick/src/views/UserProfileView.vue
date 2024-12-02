<template>
  <div class="profile-page">
    <div class="profile-header">
      <!-- 기본 프로필 이미지 -->
      <div class="profile-image-container">
        <img
          :src="selectedImage"
          alt="Profile Image"
          class="profile-image"
        />
        <FontAwesomeIcon 
          icon="pen" 
          class="edit-icon" 
          @click="toggleImageSelector" 
        />
      </div>

      <h2>{{ store.userName }}님 안녕하세요 ! 😄</h2>
    </div>

    <!-- 이미지 선택창 (버튼 클릭 시 보임) -->
    <div v-if="imageSelectorVisible" class="image-selector">
      <div
        v-for="(image, index) in profileImages"
        :key="index"
        class="image-option"
        @click="changeProfileImage(image)"
      >
        <img :src="image" alt="Profile Image Option" class="option-image" />
      </div>
    </div>

    <hr />
    <div class="favorite-movies-section">
      <FavoriteMovieList :movies="favoriteMovies"></FavoriteMovieList>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import axios from 'axios';
import FavoriteMovieList from '@/components/UserProfileView/FavoriteMovieList.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPen } from '@fortawesome/free-solid-svg-icons';

library.add(faPen);

// 이미지 경로를 import로 불러오기
import profileImageRed from '@/assets/profile_image_red.png';
import profileImageNavy from '@/assets/profile_image_navy.png';
import profileImageYellow from '@/assets/profile_image_yellow.png';
import profileImagePurple from '@/assets/profile_image_purple.png';
import profileImageGreen from '@/assets/profile_image_green.png';

const store = useCounterStore(); // Pinia 스토어
const favoriteMovies = ref([]);

// 여러 개의 프로필 이미지 배열
const profileImages = ref([profileImageRed, profileImageNavy, profileImageYellow, profileImagePurple, profileImageGreen]);

const selectedImage = ref(store.profileImage); // Pinia에서 초기 이미지 가져옴
const imageSelectorVisible = ref(false); // 이미지 선택창 visible 상태

// 프로필 이미지 변경 함수
const changeProfileImage = (image) => {
  store.updateProfileImage(image); // Pinia 상태 업데이트
  selectedImage.value = image; // 로컬 상태도 업데이트
  imageSelectorVisible.value = false; // 이미지 선택창 닫기
};

// 이미지 선택창 토글 함수
const toggleImageSelector = () => {
  imageSelectorVisible.value = !imageSelectorVisible.value;
};

// 좋아요 상태 가져오기
const getFavoriteStatus = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/users/${store.userId}/liked-movies/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      console.log('서버 데이터', res.data);
      favoriteMovies.value = res.data;
    })
    .catch((err) => {
      console.error('좋아요 상태 가져오기 실패:', err);
    });
};

onMounted(() => {
  getFavoriteStatus();
});
</script>


<style scoped>
.profile-page {
  background-color: #141414;
  color: #fff;
  padding: 20px;
  min-height: 100vh;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-image-container {
  position: relative;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.change-image-btn {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #fff;
  color: #141414;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 14px;
}

.image-selector {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.image-option {
  cursor: pointer;
}

.option-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.favorite-movies-section {
  margin-top: 40px;
}

.edit-icon {
  position: absolute;
  bottom: 0px; /* 프로필 이미지 아래에 위치 */
  right: 0px; /* 오른쪽 하단 */
  font-size: 20px; /* 아이콘 크기 */
  color: black; /* 기본 색상 */
  background-color: white; /* 어두운 배경 */
  border-radius: 50%; /* 동그란 배경 */
  padding: 5px; /* 아이콘과 배경 간격 */
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.edit-icon:hover {
  transform: scale(1.15); /* 아이콘 확대 효과 */
}

</style>
