from datetime import date
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, Date, Boolean, Text, select, text as sql_text

# Database setup
engine = create_engine("sqlite:///finance.db", echo=True, future=True)
metadata = MetaData()

# Advisors table
advisors = Table(
    "advisors", metadata,
    Column("advisor_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("email", String(120), unique=True, nullable=False),
    Column("phone", String(30), nullable=False),
    Column("active", Boolean, nullable=False, default=True),
)

# Investments table
investments = Table(
    "investments", metadata,
    Column("investment_id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(200), nullable=False),  # e.g. "Mutual Fund SIP"
    Column("instrument_type", String(80), nullable=False),  # e.g. "Equity", "Bond"
    Column("risk_level", String(50), nullable=False),  # Low/Medium/High
    Column("units", Float, nullable=True),
    Column("price_per_unit", Float, nullable=False),
    Column("total_value_lakhs", Float, nullable=False),
    Column("description", Text, nullable=True),
    Column("investment_date", Date, nullable=False, default=date.today),
    Column("advisor_id", Integer, ForeignKey("advisors.advisor_id"), nullable=False),
)

# Transactions table
transactions = Table(
    "transactions", metadata,
    Column("transaction_id", Integer, primary_key=True, autoincrement=True),
    Column("investment_id", Integer, ForeignKey("investments.investment_id"), nullable=False),
    Column("transaction_type", String(20), nullable=False),  # 'Buy' or 'Sell'
    Column("status", String(20), nullable=False),  # Pending/Completed
    Column("transaction_date", Date, nullable=True),
    Column("handled_by", Integer, ForeignKey("advisors.advisor_id"), nullable=False),
)

# Create tables
metadata.create_all(engine)

# Insert sample data
with engine.begin() as conn:
    conn.execute(sql_text("DELETE FROM transactions"))
    conn.execute(sql_text("DELETE FROM investments"))
    conn.execute(sql_text("DELETE FROM advisors"))

    conn.execute(advisors.insert(), [
        {"name": "Amit Shah", "email": "amit@finadvisors.in", "phone": "+91-98450-11111", "active": True},
        {"name": "Neha Gupta", "email": "neha@wealthcare.in", "phone": "+91-90080-22222", "active": True},
        {"name": "Rahul Verma", "email": "rahul@investsmart.in", "phone": "+91-99000-33333", "active": True},
    ])

    conn.execute(investments.insert(), [
        {
            "title": "HDFC Equity Fund",
            "instrument_type": "Mutual Fund",
            "risk_level": "High",
            "units": 120.5,
            "price_per_unit": 450.75,
            "total_value_lakhs": 54.3,
            "description": "Long-term equity fund investment.",
            "investment_date": date.today(),
            "advisor_id": 1,
        },
        {
            "title": "Government Bonds 2030",
            "instrument_type": "Bond",
            "risk_level": "Low",
            "units": 200,
            "price_per_unit": 1000,
            "total_value_lakhs": 200.0,
            "description": "Safe government bond with fixed returns.",
            "investment_date": date.today(),
            "advisor_id": 2,
        },
        {
            "title": "Reliance Shares",
            "instrument_type": "Equity",
            "risk_level": "Medium",
            "units": 50,
            "price_per_unit": 2450,
            "total_value_lakhs": 122.5,
            "description": "Blue-chip stock for steady growth.",
            "investment_date": date.today(),
            "advisor_id": 3,
        },
    ])

    conn.execute(transactions.insert(), [
        {"investment_id": 1, "transaction_type": "Buy", "status": "Completed", "transaction_date": date.today(), "handled_by": 1},
        {"investment_id": 2, "transaction_type": "Buy", "status": "Pending", "transaction_date": date.today(), "handled_by": 2},
        {"investment_id": 3, "transaction_type": "Sell", "status": "Completed", "transaction_date": date.today(), "handled_by": 3},
    ])

# Query: Top Investments by Value
stmt = select(
    investments.c.title,
    investments.c.instrument_type,
    investments.c.risk_level,
    investments.c.units,
    investments.c.price_per_unit,
    investments.c.total_value_lakhs
).select_from(
    investments.join(transactions, investments.c.investment_id == transactions.c.investment_id)
).where(
    transactions.c.transaction_type == "Buy"
).order_by(investments.c.total_value_lakhs.desc())

with engine.connect() as conn:
    rows = conn.execute(stmt).all()
    print("\nTop 'Buy' investments by value:")
    for r in rows:
        print(r)
