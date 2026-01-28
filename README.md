# AI-Powered Logistics Decision Engine (In Progress)

**Overview:**  

Rule-based logistics engine to calculate route rates based on monthly costs, freight counts, and target profit. Includes client risk score prediction. Designed for Python, Pandas, and PostgreSQL integration, with a React + Vite frontend dashboard.

**Features:**  
- PostgreSQL DB integration (routes, clients, monthly costs)  
- Pandas-based data preprocessing and calculations  
- Per-route cost & profit distribution  
- Required rate per trip calculation
- Clients risk score prediction
- Modular, testable design with shadow tests
- Interactive React dashboard with Tailwind CSS  

**Project Structure:**  
```
AI-Powered-Logistics-Decision-Engine/
├─ src/                     # Core modules: DB, data processing, engines
│ ├─ db_service.py
│ ├─ data_processing.py
│ ├─ decision_engine.py
│ ├─ predictive_engine.py
│ └─ config.py
├─ frontend/                # React + Vite frontend
│ ├─ src/
│ │ ├─ App.jsx
│ │ ├─ index.css
│ │ ├─ logisticsdashboard.jsx
│ │ └─ main.jsx
│ └─ package.json
├─ data/                    # Sample JSON datasets
│ ├─ monthly_costs.json
│ ├─ routes_costs.json
│ └─ clients.json
├─ tests/                   # Unit tests
├─ playground/              # Shadow tests
├─ requirements.txt         # Python dependencies
└─ README.md
```

**Tech & Skills:**  

**Backend:**  
Python 3.x | Pandas | PostgreSQL | FastAPI | OOP (SRP) | Rule-based logic | Shadow testing | Testable design  

**Frontend:**  
React 18 | Vite | Tailwind CSS | Lucide React icons | Interactive dashboard | REST API integration

**Next Steps:**  
- AI-powered predictive scoring  
- Expanded testing & logging

**Setup**
- python -m venv venv
- venv\Scripts\activate           # Windows
- source venv/bin/activate        # Linux/Mac
- pip install -r requirements.txt
- uvicorn src.api:app --reload

**Frontend**
- cd frontend
- npm install
- npm run dev

**Access**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173