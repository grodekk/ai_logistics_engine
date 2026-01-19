# AI-Powered Logistics Decision Engine (In Progress)

**Overview:**  
Rule-based logistics engine to calculate route rates and based on monthly costs, freight counts, target profit. Includes Clients risk score prediction. Designed for Python, Pandas, and PostgreSQL integration.

**Features:**  
- PostgreSQL DB integration (routes, clients, monthly costs)  
- Pandas-based data preprocessing and calculations  
- Per-route cost & profit distribution  
- Required rate per trip calculation
- Clients risk score prediction
- Modular, testable design with shadow tests

**Project Structure:**  
```
AI-Powered-Logistics-Decision-Engine/
├─ src/                 # Core modules: DB, data processing, engines
│  ├─ db_service.py      
│  ├─ data_processing.py
│  ├─ decision_engine.py
│  └─ predictive_engine.py
│  └─ config.py
├─ data/                # Sample JSON datasets│ 
│  ├─ monthly_costs.json
│  ├─ routes_costs.json
│  └─ clients.json
├─ tests/               # unit tests
├─ playground/          # shadow tests
├─ requirements.txt
└─ README.md
```

**Tech & Skills:**  
Python 3.x | Pandas | PostgreSQL | OOP (SRP) | Rule-based logic | Shadow testing | Testable design

**Next Steps:**  
- FastAPI REST API  
- AI-powered predictive scoring  
- Expanded testing & logging
