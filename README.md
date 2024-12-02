# Development Log

## ~ 2024.11.18
### 1. 기획
#### 아이디어
- 당일 날씨 기반 영화 추천 서비스 제공

#### 홈페이지 구상
- 초기 페이지 (로그인, 회원가입)
- 메인 페이지 (Top 10, 날씨 기반 추천 등 ...)
- 상세 페이지 (줄거리, 좋아요, 댓글)

#### 사용할 API
- 영화: TMDB, 영화진흥위원회(KOFIC)
- 날씨: Open Weather Map(OWM)

---

## 2024.11.18
### 1. 기획 세부내용
#### 필요한 데이터 추출
- 영화 (TMDB): 제목, 줄거리, 장르, 포스터, 인기도, 개봉일, 언어, 성인 여부, 영화 번호
- 날씨 (OWM): 날씨 상태 (맑음, 흐림, 비, 눈)

#### JSON 파일 생성
- movies.json
- genres.json

#### 추가 작업
- Mockup 세부화
- ERD 작성

---

## 2024.11.19
### 1. 기획 세부내용
#### 데이터 관리
- `movies.json` 구조 변경: `movie_id`를 `pk`로 설정
- `genres.json`, `weather.json` 필드명 수정 (`id` → `pk`)

#### Front
- 영화 리스트 페이지네이션 구현
- CSS: 넷플릭스 스타일 적용

#### Back
- 로그인, 회원가입 기능 구현 (인증 및 권한 활용)

---

## 2024.11.20
### 1. 기획 세부내용
#### Front
- 로고 제작 및 삽입
- 로그인 여부에 따라 네비게이션 바 상태 변경
- 초기 페이지와 메인 페이지 분리
- 메인 페이지 Top 10 구현

#### Back
- 날씨 연동 개발 완료
- 토큰 인증 구현 완료

---

## 2024.11.21
### 1. 기획 세부내용
#### Front
- 초기 페이지 배경 추가
- 메인 페이지와 상세 페이지 연동
- 댓글 CRUD 기능 추가
- 메인 페이지 CSS 개선

#### Back
- 댓글 CRUD 기능 구현

---

## 2024.11.22
### 1. 기획 세부내용
#### Front
- 인기영화 페이지 CSS 작업 완료
- 디테일 페이지 댓글 CRUD 및 CSS 작업
- 검색 버튼 추가

#### Back
- 검색 기능 구현

#### 추가 기능
- 각 페이지 이동 시 스크롤 최상단으로 이동
- 메인 페이지 캐로셀 구현

---

## 2024.11.23
### 1. 기획 세부내용
#### Front
- 검색 페이지 개발 및 기능 연동
- 상세 페이지 이동 기능 추가

#### Back
- 장르별 영화 구현 진행

---

## 2024.11.24
### 1. 기획 세부내용
#### Front
- 장르 페이지 구현 및 페이지네이션 완료
- 좋아요 버튼 기능 완료
- CSS 수정 작업 완료

#### Back
- 좋아요 기능 및 데이터 연동

---

## 2024.11.25
### 1. 기획 세부내용
#### Front
- 메인 페이지 완성 (캐로셀 완료)
- 프로필 페이지 제작 및 사진 업로드 기능 추가
- 페이지네이션 개선 (10페이지씩 이동)
- 디테일 페이지 수정 (감독, 배우, 런타임 추가)
- 유튜브 API 연동

#### Back
- 영화 데이터 가공 완료
- 영화 모델 최종 수정

### Result
- 발표 자료 준비 완료! 🎉
