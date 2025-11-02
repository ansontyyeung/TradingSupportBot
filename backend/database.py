from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class StockTrade(Base):
    __tablename__ = "stock_trades"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_code = Column(String(20), index=True)
    trade_date = Column(DateTime, default=datetime.utcnow)
    notional_amount = Column(Float)
    volume = Column(Integer)
    price = Column(Float)

class Database:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost/stock_db")
        self.engine = create_engine(self.db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def get_session(self):
        return self.SessionLocal()
    
    def get_today_notional(self, stock_code: str):
        session = self.get_session()
        try:
            today = date.today()
            result = session.query(StockTrade).filter(
                StockTrade.stock_code == stock_code,
                StockTrade.trade_date >= today
            ).all()
            
            total_notional = sum(trade.notional_amount for trade in result)
            return total_notional
        finally:
            session.close()

# Sample data initialization
def init_sample_data():
    db = Database()
    Base.metadata.create_all(bind=db.engine)
    
    session = db.get_session()
    try:
        # Check if sample data already exists
        existing = session.query(StockTrade).first()
        if not existing:
            # Add sample data for 0148.HK
            sample_trades = [
                StockTrade(
                    stock_code="0148.HK",
                    notional_amount=1500000.0,
                    volume=10000,
                    price=150.0,
                    trade_date=datetime.now()
                ),
                StockTrade(
                    stock_code="0148.HK",
                    notional_amount=2500000.0,
                    volume=15000,
                    price=166.67,
                    trade_date=datetime.now()
                ),
                StockTrade(
                    stock_code="0700.HK",
                    notional_amount=5000000.0,
                    volume=10000,
                    price=500.0,
                    trade_date=datetime.now()
                )
            ]
            session.add_all(sample_trades)
            session.commit()
    finally:
        session.close()