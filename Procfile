web: cd backend && python -c "
import os
import sys
sys.path.insert(0, '.')
from app.main import app
import uvicorn
port = int(os.environ.get('PORT', 8000))
uvicorn.run(app, host='0.0.0.0', port=port)
"