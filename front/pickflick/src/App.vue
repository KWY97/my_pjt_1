<template>
  <div class="app-container">
    <nav class="navigation-bar">
      <!-- 로고 -->
      <div class="logo-container">
        <div v-if="!store.isLogin">
          <RouterLink :to="{ name: 'LoginSignupView' }">
            <img src="@/assets/p_logo.png" alt="PickFlick Logo" class="logo" />
          </RouterLink>
        </div>
        <div v-else>
          <RouterLink :to="{ name: 'HomeView' }">
            <img src="@/assets/p_logo.png" alt="PickFlick Logo" class="logo" />
          </RouterLink>
        </div>
      </div>

      <!-- 네비게이션 링크 -->
      <div v-if="store.isLogin">
        <div class="nav-links">
          <RouterLink :to="{ name: 'PopularView' }" class="nav-link">인기영화</RouterLink>
          <div 
            class="nav-item dropdown" 
            @mouseenter="isDropdownOpen = true" 
            @mouseleave="isDropdownOpen = false"
          >
            <span class="nav-link dropdown-toggle" id="genre-nav-bar">카테고리</span>
            <ul v-if="isDropdownOpen" class="dropdown-menu">
              <li
                v-for="genre in genres"
                :key="genre.id"
                @click="navigateToGenre(genre.name)"
              >
                <span class="dropdown-item cursor-pointer">{{ genre.name }}</span>
              </li>
            </ul>
          </div>
          <div 
            class="nav-item dropdown" 
            @mouseenter="isCityDropdownOpen = true" 
            @mouseleave="isCityDropdownOpen = false"
          >
            <span class="nav-link dropdown-toggle" id="city-nav-bar">지역</span>
            <ul v-if="isCityDropdownOpen" class="dropdown-menu">
              <li
                v-for="city in cities"
                :key="city"
                @click="handleCityClick(city)"
              >
                <span class="dropdown-item cursor-pointer">{{ getTranslatedCityName(city) }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 로그인 / 회원가입 및 로그아웃 버튼 -->
      <div class="auth-container">
        <div v-if="!store.isLogin">
          <RouterLink :to="{ name: 'LogInView' }" class="auth-link">로그인</RouterLink> |
          <RouterLink :to="{ name: 'SignUpView' }" class="auth-link">회원가입</RouterLink>
        </div>
        <div v-else class="logged-in-container">
          <div class="logout-container"></div>
            <!-- 검색 창 -->
            <div v-if="showSearch" class="search-box">
              <input 
                type="text" 
                v-model="searchQuery" 
                class="search-input" 
                placeholder="영화 제목을 입력하세요..." 
              />
              <button @click="searchMovies" class="search-button">검색</button>
            </div>
            <!-- 검색 버튼 -->
            <div class="search-container">
              <FontAwesomeIcon 
                icon="magnifying-glass" 
                class="search-icon" 
                @click="toggleSearch"
              />
            </div>
            <!-- 프로필 이미지 -->
            <div>
              <img
                :src="store.profileImage"
                alt="User Profile"
                class="profile-image"
                @click="toggleDropdown"
              />
              <!-- 드롭다운 메뉴 -->
              <ul v-if="profileDropdownOpen" class="profile-dropdown-menu">
                <li @click="goToProfile">프로필</li>
                <li @click="logOut">로그아웃</li>
              </ul>
            </div>
        </div>
      </div>
    </nav>
    <RouterView />
  </div>
</template>

<script setup>
// Font Awesome
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons';

library.add(faMagnifyingGlass);

import { ref, onMounted, watch } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import router from './router';
import axios from 'axios';

const store = useCounterStore(); // Pinia 스토어
const genres = ref([]);
const cities = [
  'Seoul', 'Busan', 'Daegu', 'Daejeon', 'Gwangju', 'Incheon', 
  'New York', 'London', 'Paris', 'Tokyo', 'Beijing', 'Moscow', 
  'Canberra', 'Cape Town', 'Brasilia'
];

const isCityDropdownOpen = ref(false);
const isDropdownOpen = ref(false); // 원래 true
const profileDropdownOpen = ref(false);
const showSearch = ref(false);
const searchQuery = ref('');

// 프로필 관련 함수
const toggleDropdown = () => {
  profileDropdownOpen.value = !profileDropdownOpen.value;
};

const goToProfile = () => {
  router.push({ name: 'UserProfileView', params: { username: store.userName } });
  profileDropdownOpen.value = false;
};

const logOut = () => {
  store.logOut();
  profileDropdownOpen.value = false;
};

// 검색 창 상태 토글
const toggleSearch = () => {
  showSearch.value = !showSearch.value;
};

const searchMovies = () => {
  router.push({ name: 'SearchView', params: { keyword: searchQuery.value } });
  searchQuery.value = '';
  showSearch.value = false;
};

const navigateToGenre = (genreName) => {
  router.push({ name: 'GenreView', params: { genre: genreName } });
  isDropdownOpen.value = false;
};

const getGenres = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/genres/`,
    headers: { Authorization: `Token ${store.token}` },
  })
    .then((res) => {
      genres.value = res.data;
    })
    .catch((err) => {
      console.error(err);
    });
};

onMounted(() => {
  getGenres(); // 컴포넌트 마운트 시 장르 데이터 호출
});

watch(
  () => store.isLogin, // 로그인 상태 감시
  (newVal) => {
    if (newVal) {
      getGenres(); // 로그인 후 장르 데이터 로드
    }
  }
);

// 도시 이름 한글 번역 매핑
const cityNameMap = {
  Seoul: '서울',
  Busan: '부산',
  Daegu: '대구',
  Daejeon: '대전',
  Gwangju: '광주',
  Incheon: '인천'
};

const fetchCityWeatherAndRecommendations = (city) => {
  store.getCityWeather(city)
    .then(() => {
      store.getWeatherBasedRecommendations();
      router.push({ name: 'HomeView'})
  }
    )}

// 도시 이름 한글 변환 함수
const getTranslatedCityName = (city) => {
  return cityNameMap[city] || city; // 매핑이 없으면 원래 이름 반환
};

// 도시 클릭 이벤트
const handleCityClick = (city) => {
  fetchCityWeatherAndRecommendations(city); // API 요청에 영어 이름 사용
  isCityDropdownOpen.value = false; // 드롭다운 닫기
};
</script>


<style scoped>
.app-container {
  background-color: #141414; /* 넷플릭스 스타일의 검은 배경 */
  color: white;
  min-height: 100vh; /* 화면 전체 높이 차지 */
  font-family: Arial, sans-serif; /* 깔끔한 폰트 사용 */
}

.navigation-bar {
  display: flex;
  justify-content: space-between; /* 네비게이션 바 양쪽 정렬 */
  align-items: center;
  padding: 20px;
  background-color: #000; /* 완전 검은색 배경 */
  border-bottom: 1px solid #333; /* 하단 경계선 */
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  height: 40px; /* 로고의 크기 조절 */
  margin-right: 20px; /* 로고와 네비게이션 링크 간의 간격 */
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-link {
  margin: 0 15px;
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #e50914; /* 넷플릭스 빨간색 강조 효과 */
}

.auth-container {
  display: flex;
  align-items: center; /* 내부 요소를 수직 가운데 정렬 */
  margin-left: auto; /* 오른쪽 정렬 */
}

.auth-container {
  display: flex;
  align-items: center;
  margin-left: auto; /* 로그인/회원가입 및 로그아웃 버튼을 네비게이션 바의 끝으로 정렬 */
}

.auth-link {
  margin: 0 10px;
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.auth-link:hover {
  color: #e50914; /* 넷플릭스 빨간색 강조 효과 */
}

.logged-in-container {
  display: flex; /* 검색 버튼과 로그아웃 버튼을 수평 정렬 */
  gap: 15px; /* 검색 버튼과 로그아웃 버튼 사이 간격 */
  align-items: center; /* 수직 가운데 정렬 */
}

.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.search-icon {
  font-size: 20px;
  color: white;
  transition: color 0.3s ease;
}

.search-icon:hover {
  color: #e50914; /* 넷플릭스 빨간 강조 효과 */
}

.search-box {
  text-align: center;
}

.search-input {
  padding: 5px 10px;
  width: 300px;
  font-size: 16px;
  border: 1px solid #444;
  border-radius: 4px;
  margin-right: 10px;
}

.search-button {
  background-color: #e50914;
  color: white;
  border: none;
  padding: 5px 8px;
  cursor: pointer;
  border-radius: 5px;
  width: 73px;
}

.search-button:hover {
  background-color: #ff4d4d;
}

.logout-form {
  margin-left: 20px;
}

.logout-button {
  background-color: #e50914;
  color: white;
  border: none;
  padding: 5px 8px;
  cursor: pointer;
  border-radius: 5px;
}

.logout-button:hover {
  background-color: #ff4d4d; /* 버튼에 호버시 좀 더 밝은 빨간색으로 변경 */
}

.nav-item {
  position: relative;
}

.dropdown-toggle {
  position: relative;
  display: inline-block;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  text-decoration: none;
  padding: 10px 15px;
  cursor: pointer;
  transition: color 0.3s ease;
}

.dropdown-toggle:hover {
  color: #e50914; /* 넷플릭스 빨간색 강조 */
}

.dropdown-menu {
  display: none; /* 기본적으로 숨김 */
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #000; /* 완전 검은색 배경 */
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.7); /* 부드러운 그림자 */
  z-index: 1000;
  border-radius: 8px;
  overflow: hidden;
  padding: 10px 0;
}

.nav-item:hover .dropdown-menu {
  display: block; /* 호버 시 표시 */
}

.dropdown-item {
  display: block;
  padding: 10px 15px;
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.dropdown-item:hover {
  background-color: #e50914; /* 넷플릭스 빨간색 배경 */
  color: white; /* 텍스트 색상 유지 */
}

.cursor-pointer {
  cursor: pointer;
}

.profile-image {
  width: 50px;
  height: 50px;
  margin-left: 20px;
  cursor: pointer;
}

.profile-dropdown-menu {
  position: absolute;
  background-color: black;
  list-style: none;
  padding: 5px;
  width: 100%;
  margin-top: 10px;
  margin-right: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
.profile-dropdown-menu li {
  padding: 5px 10px;
  cursor: pointer;
}
.profile-dropdown-menu li:hover {
  background-color: #e50914; /* 넷플릭스 빨간색 */
  color: #ffffff; /* 흰색 텍스트 유지 */
  border-radius: 2px; /* 강조된 모서리 */
}

</style>