<template>
  <div class="main-content">
    <div class="overlay"></div> <!-- 어두운 오버레이 추가 -->
    <div class="center-content">
      <img src="@/assets/pickflick_logo.png" alt="PickFlick Logo" class="main-logo" />
      <h2 class="main-message">오늘의 날씨에 딱 맞는 영화를 추천해드립니다! <br> 기분 좋은 하루를 PickFlick과 함께 해보세요 😊</h2>
      <RouterLink :to="{ name: 'LogInView' }" class="login-button">로그인</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.main-content {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 화면 전체 높이 */
  color: white;
  text-align: center;
  font-family: Arial, sans-serif;
  background-image: url('@/assets/first_background.png'); /* 배경 이미지 추가 */
  background-size: cover; /* 이미지를 화면에 꽉 채우기 */
  background-position: center; /* 이미지 중앙 정렬 */
}

/* 어두운 오버레이 */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* 반투명 검은색 */
  z-index: 1; /* 콘텐츠 아래 배치 */
}

.center-content {
  position: relative;
  max-width: 700px;
  z-index: 2; /* 오버레이 위에 배치 */
}

.main-logo {
  width: 600px;
  margin-bottom: 20px;
}

.main-message {
  font-size: 30px;
  margin-bottom: 50px;
  font-family: 'Noto Sans KR', sans-serif;
}

.login-button {
  background-color: #e50914;
  color: white;
  text-decoration: none;
  padding: 15px 30px;
  font-weight: bold;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #ff0a16;
}
</style>
