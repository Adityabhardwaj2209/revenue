import os
import sys
import datetime
import random
from celery import Celery
from celery.schedules import crontab

# Add parent directory to path to import api modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.database import SessionLocal, engine, Base
from api.models import (
    Company, FactProfitLoss, FactBalanceSheet, FactCashFlow, 
    FactMLScore, FactProsCons, FactAnalysis, FactAnomaly
)

# Configure Celery
app = Celery(
    'ml_engine',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

app.conf.beat_schedule = {
    'run_etl_pipeline_daily': {
        'task': 'ml_engine.tasks.run_etl_pipeline',
        'schedule': crontab(hour=1, minute=0),
    },
    'score_all_companies_daily': {
        'task': 'ml_engine.tasks.score_all_companies',
        'schedule': crontab(hour=2, minute=0),
    },
    'generate_pros_cons_daily': {
        'task': 'ml_engine.tasks.generate_pros_cons',
        'schedule': crontab(hour=2, minute=30),
    },
}
app.conf.timezone = 'UTC'

@app.task
def run_etl_pipeline():
    """Run ETL scripts — clean and load warehouse."""
    print("Running ETL pipeline...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if we already have data
        if db.query(Company).count() > 0:
            print("Data already exists, skipping ETL.")
            return

        companies_data = ["TCS", "HDFCBANK", "RELIANCE", "INFY", "ITC", "WIPRO", "ADANIPOWER"]
        for i in range(1, 101):
            name = companies_data[i-1] if i <= len(companies_data) else f"CMP{i}"
            c = Company(
                company_name=name,
                sector=random.choice(["IT", "Banking", "Energy", "FMCG", "Auto"]),
                roe_percentage=random.uniform(5.0, 35.0)
            )
            db.add(c)
        db.commit()
        
        # Add facts for each company
        companies = db.query(Company).all()
        for c in companies:
            for year in range(2019, 2024):
                sales = random.uniform(1000, 50000)
                pl = FactProfitLoss(
                    company_id=c.id, year_date=year,
                    sales=sales,
                    net_profit=sales * random.uniform(0.05, 0.25),
                    operating_profit=sales * random.uniform(0.1, 0.3),
                    opm_pct=random.uniform(10, 30),
                    interest=sales * random.uniform(0.01, 0.05),
                    expenses=sales * random.uniform(0.5, 0.8),
                    dividend_payout_pct=random.uniform(0, 50)
                )
                db.add(pl)
                
                bs = FactBalanceSheet(
                    company_id=c.id, year_date=year,
                    debt_to_equity=random.uniform(0.0, 2.5),
                    borrowings=random.uniform(100, 10000),
                    equity_capital=random.uniform(500, 20000),
                    reserves=random.uniform(1000, 50000),
                    total_assets=random.uniform(5000, 100000)
                )
                db.add(bs)
                
                cf = FactCashFlow(
                    company_id=c.id, year_date=year,
                    operating_activity=random.uniform(-1000, 10000),
                    investing_activity=random.uniform(-5000, 2000),
                    free_cash_flow=random.uniform(-2000, 8000)
                )
                db.add(cf)
        
        db.commit()
        print("ETL pipeline completed.")
    finally:
        db.close()

@app.task
def invalidate_cache(company_id=None):
    """Clear Redis cache for changed company data (Called after score tasks)."""
    print(f"Invalidating cache for {company_id if company_id else 'all companies'}...")

@app.task
def detect_anomalies():
    print("Detecting anomalies...")

@app.task
def detect_trends():
    print("Detecting trends...")

@app.task
def score_all_companies():
    print("Scoring all companies...")
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        for c in companies:
            # Delete old scores
            db.query(FactMLScore).filter(FactMLScore.company_id == c.id).delete()
            
            # Simplified mock logic for dimensions
            p_score = random.uniform(10, 25)
            g_score = random.uniform(5, 20)
            l_score = random.uniform(5, 20)
            c_score = random.uniform(5, 15)
            d_score = random.uniform(0, 10)
            t_score = random.uniform(2, 10)
            
            overall = p_score + g_score + l_score + c_score + d_score + t_score
            
            if overall >= 85: label = "EXCELLENT"
            elif overall >= 70: label = "GOOD"
            elif overall >= 50: label = "AVERAGE"
            elif overall >= 35: label = "WEAK"
            else: label = "POOR"
            
            score = FactMLScore(
                company_id=c.id,
                overall_score=overall,
                health_label=label,
                score_profitability=p_score,
                score_growth=g_score,
                score_leverage=l_score,
                score_cash_flow=c_score,
                score_dividend=d_score,
                score_trend=t_score
            )
            db.add(score)
        db.commit()
    finally:
        db.close()
    invalidate_cache()

@app.task
def generate_pros_cons():
    print("Generating pros and cons...")
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        for c in companies:
            db.query(FactProsCons).filter(FactProsCons.company_id == c.id).delete()
            
            # Adding mock pros and cons
            pros = ["Company is almost debt free.", "Improving operating margins consistently"]
            cons = ["Below-average sales growth", "Low interest coverage ratio"]
            
            for p in pros:
                db.add(FactProsCons(company_id=c.id, point_type="PRO", description=p))
            for con in cons:
                db.add(FactProsCons(company_id=c.id, point_type="CON", description=con))
        db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    app.start()
