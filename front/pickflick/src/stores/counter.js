import { ref, computed, onMounted } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import profileImageRed from '@/assets/profile_image_red.png'

export const useCounterStore = defineStore('counter', () => {
  const router = useRouter()
  const movies = ref([])
  const weatherMovies = ref([])
  const topMovies = ref([])
  const weatherMain = ref('')  // 날씨 메인 상태 초기값을 빈 문자열로 설정
  const cityName = ref('Seoul')
  const API_URL = 'http://127.0.0.1:8000'
  const currentPage = ref(1)
  const totalPages = ref(null)
  const token = ref(null)
  const latestAnime = ref([])  // 최신 애니메이션 상태 추가
  const adultMovies = ref([])
  const userName = ref('') // 로그인한 유저의 아이디
  const userId = ref(null)

  // 프로필 이미지 상태 추가
  const profileImage = ref(profileImageRed); // 초기값 설정
  // 프로필 이미지 업데이트 액션
  const updateProfileImage = (newImage) => {
    profileImage.value = newImage;
  }


  const isLogin = computed(() => token.value !== null)
   // 영화 상세 페이지로 이동
   const navigateToDetail = (movieId) => {
    router.push({ name: 'MovieDetailView', params: { id: movieId } })
  }

  // 영화 데이터 가져오기
  const getMovies = function (page = 1) {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/`,
      params: {
        page: page,
      },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        movies.value = res.data.results
        totalPages.value = Math.ceil(res.data.count / 35)
        currentPage.value = page
      })
      .catch((err) => {
        console.error(err)
      })
  }

  const getTopMovies = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/top/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        topMovies.value = res.data  // 인기 영화 목록 저장
        console.log('인기 영화:', res.data)
      })
      .catch((err) => {
        console.error(err)
      })
  }

  const getAdultMovies = () => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/top_adult/`,
      headers: { 
        Authorization: `Token ${token.value}` 
      },
    })
      .then((res) => {
        adultMovies.value = res.data
        console.log('성인용 영화:', res.data)
      })
      .catch((err) => console.error(err))
  }
  
  const getGenres = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/genres/`,
      headers: {
          Authorization: `Token ${token.value}`
        }
    })
      .then((res) => {
        console.log(res.data)
        genres.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }


  // 이전 페이지로 이동
  const prevPage = () => {
    if (currentPage.value > 1) {
      getMovies(currentPage.value - 1)
    }
  }

  // 다음 페이지로 이동
  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      getMovies(currentPage.value + 1)
    }
  }

  // 회원가입 요청 액션
  const signUp = function (payload) {
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        console.log(res.data)
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 로그인 요청 액션
  const logIn = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        token.value = res.data.key
        console.log('로그인 성공')
        console.log(token.value)
        userName.value = username

        axios({
          method: 'get',
          url: `${API_URL}/accounts/user/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        })
          .then((userRes) => {
            userName.value = userRes.data.username // User 데이터를 저장
            userId.value = userRes.data.pk
            router.push({ name: 'HomeView' })
          })
          .catch((err) => {
            console.error('사용자 정보 요청 오류:', err);
          })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        userName.value = null 
        router.push({ name: 'LoginSignupView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }


const getLatestAnime = function () {
  axios({
    method: 'get',
    url: `${API_URL}/api/v1/movies/latest_anime/`,
    headers: {
      Authorization: `Token ${token.value}`
    }
  })
    .then((res) => {
      latestAnime.value = res.data  // 최신 애니메이션 목록 저장
      console.log('최신 애니메이션:', res.data)
    })
    .catch((err) => {
      console.error(err)
    })
  }

  const getWeatherBasedRecommendations = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/recommend/${cityName.value}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        weatherMovies.value = res.data.movies  // 영화 목록을 movies에 저장
        weatherMain.value = res.data.weather_main || ''  // 날씨 정보를 weatherMain에 저장
        cityName.value = res.data.city_name
        console.log('추천 영화:', res.data)
      })
      .catch((err) => {
        console.error(err)
        console.log('시티네임', cityName)
      })
  }

  const getCityWeather = function (city) {
    return new Promise((resolve, reject) => {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/recommend/${city}`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          console.log('날씨 데이터 확인:', res.data);
          cityName.value = res.data.city_name;
          resolve(res.data); // 작업 완료 시 resolve 호출
        })
        .catch((err) => {
          console.error('날씨 정보 요청 실패:', err);
          reject(err); // 작업 실패 시 reject 호출
        });
    });

    
  };


  return { 
    movies, weatherMain, API_URL, currentPage, totalPages,
    getMovies, prevPage, nextPage, // 수정된 부분: prevPage와 nextPage 추가
    signUp, logIn, logOut, getTopMovies, topMovies,
    token, isLogin, getWeatherBasedRecommendations, weatherMovies, latestAnime, getLatestAnime, navigateToDetail,
    adultMovies, getAdultMovies, userName, userId, cityName, getCityWeather, getGenres,
    profileImage, updateProfileImage,
  }
}, { persist: true })
