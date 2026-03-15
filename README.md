# 🤖 AI 에이전트 팀 - 비즈니스 실행 플랫폼

엔지니어링, 마케팅, 디자인, 제품, 운영 등 다양한 분야의
실제 비즈니스 업무를 처리하는 다중 팀 AI 에이전트 시스템입니다.

**리더십:** CEO/오케스트레이터, CISO, CTO
**팀:** 8개 팀 (핵심 5개 + 선택적 3개), 23명 이상의 에이전트
**상태:** ✅ 프로덕션 준비 완료

---

## 🚀 빠른 시작

### 1️⃣ 설치

```bash
# 저장소 Clone
git clone https://github.com/felix675lt/ai-agent-team.git
cd ai-agent-team

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# 또는
venv\Scripts\activate  # Windows

# 패키지 설치 (자동으로 Flask 포함)
pip install -e .
```

### 2️⃣ API 키 설정

```bash
# 환경변수로 설정 (권장)
export ANTHROPIC_API_KEY="sk-ant-..."

# 또는 .env 파일 생성
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### 3️⃣ 대시보드 실행

```bash
python simple_dashboard.py
```

그 다음 브라우저에서:
```
http://localhost:8000
```

---

## 📊 팀 구조

### 리더십
- 👑 **CEO/오케스트레이터** - 조직 관리, 요청 분류
- 🔐 **CISO** - 보안 검토
- 🏗️ **CTO** - 아키텍처/성능 검토

### 핵심 팀
- 🛠️ **엔지니어링** - 기술 아키텍처, 시스템 설계
- 📢 **마케팅** - 전략, 캠페인, 콘텐츠
- 🎨 **디자인** - UX/UI, 디자인 시스템
- 📊 **제품** - 로드맵, 기능, 전략
- ⚙️ **운영** - 프로세스, HR, 재정

### 선택적 팀
- 📈 **데이터 분석**
- 💼 **사업 개발**
- 😊 **고객 성공**

---

## 💻 사용 방법

### 웹 대시보드

```bash
python simple_dashboard.py
# http://localhost:8000 에서 접속
```

### CLI 명령어

```bash
agent-team team-status
agent-team execute "엔지니어링: 마이크로서비스 아키텍처 설계"
```

---

## 🔧 문제 해결

### Flask가 설치되지 않음

```bash
pip install flask
```

### 대시보드 접속 안 됨

```bash
# 포트 사용 확인
lsof -i :8000
# 프로세스 종료
pkill -f simple_dashboard
# 재실행
python simple_dashboard.py
```

### API 키 오류

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## 📁 프로젝트 구조

```
agent_team/
├── agents/
│   ├── leadership/
│   ├── engineering/
│   ├── marketing/
│   ├── design/
│   ├── product/
│   ├── operations/
│   ├── data_analytics/
│   ├── business_development/
│   └── customer_success/
├── core/
│   ├── models.py
│   ├── dispatcher.py
│   └── config.py
├── cli.py
├── simple_dashboard.py
└── web_dashboard.py
```

---

**상태:** ✅ 프로덕션 준비 완료
**마지막 업데이트:** 2026-03-15
