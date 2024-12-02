<template>
  <div class="login-container">
    <div class="logo-container">
      <img src="@/assets/pickflick_logo.png" alt="PickFlick Logo" class="logo" />
    </div>
    <form @submit.prevent="logIn" class="login-form">
      <label for="username" class="sr-only">아이디를 입력해주세요</label>
      <input type="text" id="username" v-model.trim="username" placeholder="아이디를 입력해주세요" class="input-field"><br>

      <label for="password" class="sr-only">비밀번호를 입력해주세요</label>
      <input type="password" id="password" v-model.trim="password" placeholder="비밀번호를 입력해주세요" class="input-field"><br>
      <input type="submit" value="로그인" class="login-button">
      <form @submit.pervent="signUp">
        <input type="submit" value="픽플릭 가입하기" class="signup-button">
      </form>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const username = ref(null)
const password = ref(null)

const store = useCounterStore()
const router = useRouter()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}

const signUp = function () {
  router.push({ name: 'SignUpView' })
}

</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; /* 화면 전체 높이 사용 */
  background-color: #141414; /* 넷플릭스 스타일의 검은 배경 */
  color: white;
}

.logo-container {
  margin-bottom: 20px; /* 로고와 로그인 폼 사이 간격 */
}

.logo {
  width: 500px; /* 로고 크기 조정 */
  margin-bottom: 50px;
}

.login-form {
  width: 400px; /* 폼 크기 설정 */
  height: 350px;
  background-color: #222; /* 폼 배경색 */
  padding: 20px; /* 폼 내부 간격 */
  border-radius: 10px; /* 테두리 둥글게 */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); /* 약간의 그림자 */
}

.input-field {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: none;
  border-radius: 5px;
  background-color: #333;
  color: white;
  font-size: 16px;
}

.login-button {
  width: 100%;
  padding: 10px;
  background-color: #e50914;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 40px;
}

.login-button:hover {
  background-color: #f40612; /* 호버 시 밝게 */
}

.signup-button {
  width: 100%;
  padding: 10px;
  background-color: black;
  color: white;
  border-color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
}
</style>
