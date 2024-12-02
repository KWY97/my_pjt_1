import { createRouter, createWebHistory } from 'vue-router'
import PopularView from '@/views/PopularView.vue'
import LoginSignupView from '@/views/LoginSignupView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import GenreView from '@/views/GenreView.vue'
import { useCounterStore } from '@/stores/counter'
import HomeView from '@/views/HomeView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue' // 상세 페이지 컴포넌트 추가
import SearchView from '@/views/SearchView.vue'
import UserProfileView from '@/views/UserProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/popular',
      name: 'PopularView',
      component: PopularView,
    },
    {
      path: '/',
      name: 'LoginSignupView',
      component: LoginSignupView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView,
    },
    {
      path: '/pickflick',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/movie/:id', // 동적 라우팅 설정
      name: 'MovieDetailView',
      component: MovieDetailView,
      props: true, // 동적 파라미터를 컴포넌트에 props로 전달
    },
    {
      path: '/search/:keyword',
      name: 'SearchView',
      component: SearchView,
      props: true,
    },
    {
      path: '/:genre',
      name: 'GenreView',
      component: GenreView,
      props: true,
    },
    {
      path: '/profile/:username',
      name: 'UserProfileView',
      component: UserProfileView,
      props: true,
    },
  ],

  // 스크롤 동작 설정
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition; // 뒤로가기/앞으로가기에 이전 위치 복원
    } else {
      return { top: 0 }; // 기본적으로 맨 위로 스크롤
    }
  },
})

router.beforeEach((to, from) => {
  const store = useCounterStore()
  // 만약 이동하는 목적지가 메인 페이지이면서
  // 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  if (to.name === 'PopularView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면
  // 메인 페이지로 보냄
  if ((to.name === 'SignUpView' || to.name === 'LogInView' || to.name === 'LoginSignupView') && store.isLogin) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'PopularView' }
  }
})

export default router