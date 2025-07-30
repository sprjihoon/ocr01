# OCR 가격표 추적 서비스

코스트코 가격표 이미지를 업로드하여 자동으로 가격 정보를 추출하고 최저가를 추적하는 웹 애플리케이션입니다.

## 🚀 빠른 배포 (서버)

### Option 1: Railway (백엔드) + Vercel (프론트엔드) [추천]

#### 백엔드 배포 (Railway)
1. [Railway](https://railway.app) 회원가입 후 GitHub 연결
2. New Project → Deploy from GitHub repo 선택
3. 이 저장소 선택 → Root Directory를 `backend`로 설정
4. 자동 배포 완료 → 백엔드 URL 확인 (예: `https://yourapp.railway.app`)

#### 프론트엔드 배포 (Vercel)
1. [Vercel](https://vercel.com) 회원가입 후 GitHub 연결
2. New Project → GitHub에서 이 저장소 선택
3. Root Directory를 `frontend`로 설정
4. Environment Variables 추가:
   - `NEXT_PUBLIC_BACKEND_URL`: Railway에서 받은 백엔드 URL
5. Deploy → 프론트엔드 URL 확인 (예: `https://yourapp.vercel.app`)

### Option 2: Docker Compose (VPS 서버)

```bash
# 서버에서 실행
git clone https://github.com/sprjihoon/ocr01.git
cd ocr01
docker-compose -f docker-compose.prod.yml up -d
```

### Option 3: Render (올인원)

1. [Render](https://render.com) 회원가입
2. New Web Service → GitHub 연결
3. Root Directory: `backend`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 🏠 로컬 실행

### 백엔드
```bash
cd backend
pip install -r requirements.txt
python create_admin.py
uvicorn app.main:app --reload
```

### 프론트엔드
```bash
cd frontend
npm install
npm run dev
```

## 🔑 기본 로그인
- **사용자명**: `admin`
- **비밀번호**: `admin123`

## ✨ 주요 기능
- 🖼️ 이미지 업로드 (로컬/S3 저장)
- 🔍 OCR 가격 추출 (Google Vision API/목 데이터)
- 📊 가격 이력 추적 및 최저가 배지
- �� 가격 변동 차트
- 🏪 매장별 가격 비교

## 🛠️ 기술 스택
- **백엔드**: FastAPI, SQLAlchemy, SQLite
- **프론트엔드**: Next.js, React, Tailwind CSS
- **OCR**: Google Cloud Vision API (선택사항)
- **스토리지**: AWS S3 (선택사항, 로컬 폴백)

## 📝 환경변수

### 백엔드 (.env)
```
DATABASE_URL=sqlite:///./costco_ocr.db
SECRET_KEY=your-super-secret-jwt-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### 프론트엔드 (.env.local)
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```