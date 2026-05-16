from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Company(Base):
    __tablename__ = "dim_company"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True, index=True)
    sector = Column(String)
    roe_percentage = Column(Float)
    
class FactProfitLoss(Base):
    __tablename__ = "fact_profit_loss"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_company.id"))
    year_date = Column(Integer)
    sales = Column(Float)
    net_profit = Column(Float)
    operating_profit = Column(Float)
    opm_pct = Column(Float)
    interest = Column(Float)
    expenses = Column(Float)
    dividend_payout_pct = Column(Float)

class FactBalanceSheet(Base):
    __tablename__ = "fact_balance_sheet"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_company.id"))
    year_date = Column(Integer)
    debt_to_equity = Column(Float)
    borrowings = Column(Float)
    equity_capital = Column(Float)
    reserves = Column(Float)
    total_assets = Column(Float)

class FactCashFlow(Base):
    __tablename__ = "fact_cash_flow"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_company.id"))
    year_date = Column(Integer)
    operating_activity = Column(Float)
    investing_activity = Column(Float)
    free_cash_flow = Column(Float)

class FactMLScore(Base):
    __tablename__ = "fact_ml_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_company.id"))
    overall_score = Column(Float)
    health_label = Column(String)
    computed_at = Column(DateTime, default=datetime.utcnow)
    # Dimensional Scores
    score_profitability = Column(Float)
    score_growth = Column(Float)
    score_leverage = Column(Float)
    score_cash_flow = Column(Float)
    score_dividend = Column(Float)
    score_trend = Column(Float)

class FactProsCons(Base):
    __tablename__ = "fact_pros_cons"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_company.id"))
    point_type = Column(String) # "PRO" or "CON"
    description = Column(String)
    
class FactAnalysis(Base):
    __tablename__ = "fact_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_company.id"))
    metric = Column(String)
    period_label = Column(String) # e.g. "3Y", "5Y", "10Y"
    value_pct = Column(Float)

class FactAnomaly(Base):
    __tablename__ = "fact_anomalies"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_company.id"))
    year = Column(Integer)
    metric = Column(String)
    severity = Column(String)
    description = Column(String)
