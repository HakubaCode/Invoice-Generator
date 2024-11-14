from database import clear_database, init_db

if __name__ == "__main__":
    print("Clearing database...")
    clear_database()
    print("Reinitializing database...")
    init_db()
    print("Database has been reset!")
