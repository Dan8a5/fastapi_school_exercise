# Import necessary modules from SQLModel
from sqlmodel import create_engine, SQLModel, Session

# Database configuration
# This is the connection string for the Supabase PostgreSQL database
# In a production environment, this should be stored as an environment variable for security
DATABASE_URL = "postgresql://postgres.shlpxirwffgjdudmxkuo:week6codeschool@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

# Create a SQLAlchemy engine instance
# The engine is the starting point for any SQLAlchemy application
# echo=True means that all SQL statements will be printed to the console (useful for debugging)
engine = create_engine(DATABASE_URL, echo=True)

# Function to initialize the database
def init_db():
    # Create all tables in the database based on the SQLModel classes
    # This is typically called once when the application starts
    SQLModel.metadata.create_all(engine)

# Function to get a database session
def get_session():
    # Create a new SQLAlchemy session
    # This session is used to interact with the database
    # The 'with' statement ensures that the session is properly closed after use
    with Session(engine) as session:
        # yield the session, allowing it to be used as a dependency in FastAPI
        yield session