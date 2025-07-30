# Frontend (Next.js)

## Setup

```bash
cd frontend
npm install
npm run dev
```

Set backend URL via `.env.local`:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 주요 페이지
- `/login` : 로그인(JWT 발급)
- `/upload` : 이미지 업로드 (presigned S3 → `/images/complete`)

## 디렉토리
```
pages/      # Next.js routes
context/    # React context (Auth)
utils/      # API helper
styles/     # Tailwind CSS
``` 

GitHub 저장소( sprjihoon/ocr01 )에 현재 작업 코드를 커밋-푸시하려면 다음 순서로 진행하세요.  
(터미널은 프로젝트 루트 폴더에서 실행한다고 가정)

1. Git 초기화 및 원격 저장소 연결
```bash
git init                       # 이미 git repo 면 생략
git remote add origin https://github.com/sprjihoon/ocr01.git
```

2. 사용자 정보 설정(한 번만)
```bash
git config user.name  "Your Name"
git config user.email "you@example.com"
```

3. 변경 파일 스테이지 & 커밋
```bash
git add .
git commit -m "Initial project: FastAPI + Next.js OCR price tracker"
```

4. GitHub Personal Access Token 준비  
   – Settings → Developer settings → Tokens (classic) → repo 권한 체크 → 토큰 복사

5. 최초 푸시 (토큰 인증)
```bash
git branch -M main            # main 브랜치 사용
git push -u origin main       # 프롬프트에 사용자명 / 토큰 입력
```

6. 이후에는
```bash
<code_block_to_apply_changes_from>
```

참고
• 토큰을 깃캐시(mgr-credential) 또는 `gh auth login` 으로 저장하면 매번 입력할 필요가 없습니다.  
• VSCode → Source Control 패널에서도 같은 과정을 GUI 로 수행할 수 있습니다.

문제 생기면 오류 메시지를 알려주세요!