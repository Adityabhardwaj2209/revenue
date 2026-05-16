from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import engine, Base, get_db
from .models import Company, FactMLScore, FactAnomaly

app = FastAPI(title="Nifty 100 Financial ML API")

# Enable CORS for Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health-scores")
def get_health_scores(db: Session = Depends(get_db)):
    results = db.query(Company, FactMLScore).join(FactMLScore, Company.id == FactMLScore.company_id).all()
    
    data = []
    for comp, score in results:
        # Determine color
        if score.health_label == "EXCELLENT": color = "#2ECC71"
        elif score.health_label == "GOOD": color = "#82E0AA"
        elif score.health_label == "AVERAGE": color = "#F7DC6F"
        elif score.health_label == "WEAK": color = "#F0A500"
        else: color = "#E74C3C"
        
        data.append({
            "company": comp.company_name,
            "score": round(score.overall_score, 1),
            "label": score.health_label,
            "color": color,
            "debt_to_equity": 0, # You can join FactBalanceSheet to get this
            "roe": round(comp.roe_percentage, 1) if comp.roe_percentage else 0
        })
    return sorted(data, key=lambda x: x["score"], reverse=True)

@app.get("/api/anomalies")
def get_anomalies(db: Session = Depends(get_db)):
    return [
        {"id": 1, "company": "ADANIPOWER", "year": 2022, "metric": "Sales", "severity": "High"},
        {"id": 2, "company": "WIPRO", "year": 2023, "metric": "OPM%", "severity": "Medium"},
    ]

@app.get("/api/summary")
def get_summary(db: Session = Depends(get_db)):
    total = db.query(Company).count()
    excellent = db.query(FactMLScore).filter(FactMLScore.health_label == "EXCELLENT").count()
    needs_attn = db.query(FactMLScore).filter(FactMLScore.health_label.in_(["WEAK", "POOR"])).count()
    
    avg_roe_result = db.query(func.avg(Company.roe_percentage)).scalar()
    avg_roe = round(avg_roe_result, 1) if avg_roe_result else 0
    
    return {
        "total_companies": total,
        "excellent_health": excellent,
        "needs_attention": needs_attn,
        "avg_market_roe": avg_roe
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
