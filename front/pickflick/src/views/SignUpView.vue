<template>
  <div>
    <div class="signup-container">
      <div class="logo-container">
        <img src="@/assets/pickflick_logo.png" alt="PickFlick Logo" class="logo" />
      </div>
      <form @submit.prevent="signUp" class="signup-form">
        <div class="signup-message-container">
          <h2 class="signup-message">지금 가입하고 날씨에 맞는 <br> 영화 추천을 받아보세요!</h2>
        </div>
        <label for="username" class="sr-only">아이디</label>
        <input type="text" id="username" v-model.trim="username" placeholder="사용할 아이디를 입력해주세요" class="input-field"><br>

        <label for="password1" class="sr-only">비밀번호</label>
        <input type="password" id="password1" v-model.trim="password1" placeholder="사용할 비밀번호를 입력해주세요" class="input-field"><br>

        <label for="password2" class="sr-only">비밀번호 확인</label>
        <input type="password" id="password2" v-model.trim="password2" placeholder="비밀번호를 다시 입력해주세요" class="input-field"><br>

        <input type="submit" value="회원가입" class="signup-button">
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const store = useCounterStore()

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }
  store.signUp(payload)
}
</script>

<style scoped>
.signup-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 110vh; /* 화면 전체 높이 사용 */
  background-color: #141414; /* 넷플릭스 스타일의 검은 배경 */
  color: white;
}

.logo-container {
  margin-bottom: 20px; /* 로고와 회원가입 폼 사이 간격 */
}

.logo {
  width: 500px; /* 로고 크기 조정 */
  margin-bottom: 50px;
}

.signup-form {
  width: 450px; /* 폼 크기 설정 */
  height: 500px;
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

.signup-button {
  width: 100%;
  padding: 10px;
  background-color: #e50914;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 50px;
}

.signup-button:hover {
  background-color: #f40612; /* 호버 시 밝게 */
}

.signup-message {
  margin-bottom: 30px;
}

.signup-message-container {
  text-align: center;
}
</style>
