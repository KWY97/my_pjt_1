<template>
  <div class="weather-movie-list">
    <h1 :class="headerClass">지금 {{ getTranslatedCityName(store.cityName) }} {{ getTranslatedWeatherMain(props.weatherMain) }}</h1>
    <h3 :class="messageClass">{{ weatherMessage }}</h3>
    <div v-if="movies.length > 0">
      <Carousel v-bind="carouselConfig">
        <Slide v-for="movie in movies" :key="movie.movie_id">
          <WeatherMovieListItem :movie="movie" class="movie-card" />
        </Slide>

        <template #addons>
          <Navigation />
        </template>
      </Carousel>
    </div>
    <p v-else>현재 날씨에 맞는 추천 영화를 찾지 못했습니다. 😢 다른 날씨에 맞는 영화를 찾아보세요!</p>
  </div>
</template>

<script setup>
import 'vue3-carousel/dist/carousel.css';
import { Carousel, Slide, Navigation } from 'vue3-carousel';
import { ref, watch, defineProps, computed } from 'vue';
import WeatherMovieListItem from './WeatherMovieListItem.vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();

const props = defineProps({
  movies: {
    type: Array,
    required: true,
  },
  weatherMain: {
    type: String,
    required: true,
  },
});

const headerClass = ref('animated-header');
const messageClass = ref('animated-message');

watch(() => store.cityName, () => {
  headerClass.value = ''; // 기존 클래스 제거
  messageClass.value = ''; // 기존 클래스 제거
  setTimeout(() => {
    headerClass.value = 'animated-header'; // 다시 적용
    messageClass.value = 'animated-message'; // 다시 적용
  }, 0);
});

// 캐로셀 설정
const carouselConfig = {
  itemsToShow: 3.95, // 슬라이드 크기 설정
  wrapAround: true,
  transition: 5000,
  autoplay: {
    interval: 5000, // 슬라이드 전환 시간 (ms)
    pauseOnHover: true, // 마우스 오버 시 자동 재생 일시 정지
  },
};

// 날씨에 따른 메시지 계산
const weatherMessage = computed(() => {
  switch (props.weatherMain) {
    case 'Clear':
      return '☀️ 햇살 가득한 날, 유쾌한 코미디로 웃음을 채워보세요 ! 😊';
    case 'Clouds':
    case 'Mist':
    case 'Haze':
    case 'Fog':
      return '☁︎ 흐린 날씨엔 뭔가 미스터리한 이야기가 끌리죠. 함께 풀어볼까요 ? 🕵️‍♀️';
    case 'Snow':
      return '❄️ 눈 내리는 날엔 마법 같은 이야기가 딱이죠. 애니메이션으로 마음 속 따뜻함을 느껴보세요. ⛄';
    case 'Rain':
    case 'Drizzle':
      return '☔ 빗소리와 함께 감성적인 로맨스 한 편 어때요 ? 🌧️';
    case 'Thunderstorm':
    case 'Ash':
    case 'Squall':
    case 'Tornado':
      return '⚡️ 거친 날씨와 함께 스릴 넘치는 이야기에 빠져볼까요 ? 🌀';
    case 'Dust':
    case 'Smoke':
      return '💨 먼지 바람 속에서 펼쳐지는 치열한 전쟁의 이야기로 몰입해 보세요. ⚔️';
    default:
      return '오늘 날씨에 어울리는 영화를 찾아보세요 !';
  }
});

// 도시 및 날씨 변환 함수
const cityNameMap = {
  Seoul: '서울은',
  Busan: '부산은',
  Daegu: '대구는',
  Daejeon: '대전은',
  Gwangju: '광주는',
  Incheon: '인천은',
  London: '런던은',
  'New York': '뉴욕은',
  Paris: '파리는',
  Tokyo: '도쿄는',
  Beijing: '베이징은',
  Moscow: '모스크바는',
  Canberra: '호주는',
  'Cape Town': '남아공은',
  Brasília: '브라질은', 
};

const weatherMainMap = {
  Clear: '맑음 ☀️',
  Clouds: '흐림 ☁︎',
  Rain: '비 ☔',
  Snow: '눈 ❄️',
  Thunderstorm: '거침 ⚡️',
  Drizzle: '비 🌧️',
  Mist: '흐림 ☁︎',
  Fog: '흐림 ☁︎',
  Haze: '흐림 ☁︎',
  Dust: '먼지 투성 💨',
  Smoke: '먼지 투성 💨',
  Ash: '거침 ⚡️',
  Squall: '거침 ⚡️',
  Tornado: '거침 ⚡️',
};

const getTranslatedCityName = (city) => cityNameMap[city] || city;
const getTranslatedWeatherMain = (weatherMain) => weatherMainMap[weatherMain] || weatherMain;
</script>

<style scoped>
.weather-movie-list {
  padding: 20px;
  background-color: #141414;
  color: white;
  max-width: 85%;
  margin: 0 auto;
}


.animated-header {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #ffffff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  text-align: center;
  animation: zoomIn 2s ease-in-out;
}

@keyframes zoomIn {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }
  50% {
    transform: scale(1.4);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.animated-message {
  font-size: 1.5rem;
  font-weight: 500;
  color: #d1d1d1;
  text-align: center;
  opacity: 0;
  transform: translateY(20px);
  animation: slideUp 2s ease-in-out forwards;
  animation-delay: 1.8s;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}


.carousel__track {
  transform-style: preserve-3d;
}

.carousel__slide {
  opacity: 0.9;
  transform: rotateY(-20deg) scale(0.9);
  transition: transform 0.5s;
}

.carousel__slide--prev {
  opacity: 1;
  transform: rotateY(-10deg) scale(0.95);
}

.carousel__slide--active {
  opacity: 1;
  transform: rotateY(0) scale(1);
}

.carousel__slide--active ~ .carousel__slide {
  transform: rotateY(20deg) scale(0.9);
}

.movie-card {
  padding: 10px;
  background: #141414;
  border-radius: 8px;
  width: 100%;
  text-align: center;
}
</style>
