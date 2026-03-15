# 🤖 AI Agent Team - Business Execution Platform

Multi-team AI agent system for real business task execution across Engineering, Marketing, Design, Product, Operations, and more.

**Leadership:** CEO/Orchestrator, CISO, CTO  
**Teams:** 8 teams (5 core + 3 optional) with 23+ agents  
**Status:** ✅ Production Ready

---

## 🚀 빠른 시작 (Quick Start)

### 1️⃣ 설치 (Installation)

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

### 2️⃣ API 키 설정 (API Key Setup)

```bash
# 환경변수로 설정 (권장)
export ANTHROPIC_API_KEY="sk-ant-..."

# 또는 .env 파일 생성
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### 3️⃣ 대시보드 실행 (Run Dashboard)

```bash
python simple_dashboard.py
```

그 다음 브라우저에서:
```
http://localhost:8000
```

---

## 📊 팀 구조 (Team Structure)

### 리더십 (Leadership)
- 👑 **CEO/Orchestrator** - 조직 관리, 요청 분류
- 🔐 **CISO** - 보안 검토
- 🏗️ **CTO** - 아키텍처/성능 검토

### 핵심 팀 (Core Teams)
- 🛠️ **Engineering** - 기술 아키텍처, 시스템 설계
- 📢 **Marketing** - 전략, 캠페인, 콘텐츠
- 🎨 **Design** - UX/UI, 디자인 시스템
- 📊 **Product** - 로드맵, 기능, 전략
- ⚙️ **Operations** - 프로세스, HR, 재정

### 선택적 팀 (Optional)
- 📈 **Data & Analytics**
- 💼 **Business Development**
- 😊 **Customer Success**

---

## 💻 사용 방법 (Usage)

### 웹 대시보드

```bash
python simple_dashboard.py
# http://localhost:8000 에서 접속
```

### CLI 명령어

```bash
agent-team team-status
agent-team execute "Engineering: 마이크로서비스 아키텍처 설계"
```

---

## 🔧 문제 해결 (Troubleshooting)

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

**Status:** ✅ Production Ready  
**Last Updated:** 2026-03-15
