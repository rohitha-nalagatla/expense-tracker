"""
Production entry point for Expense Tracker
Uses Waitress WSGI server for production deployment
Auto-initializes database on first run
"""
from waitress import serve
from app import app
import os
from init_database import init_database

if __name__ == '__main__':
    # Auto-initialize database on first run
    print("Checking database...")
    init_database()
    
    port = int(os.getenv('PORT', 8080))
    print(f"\n{'='*60}")
    print(f"  Expense Tracker Starting")
    print(f"{'='*60}")
    print(f"  URL: http://localhost:{port}")
    print(f"  Database: SQLite (expense_tracker.db)")
    print(f"  Press Ctrl+C to stop")
    print(f"{'='*60}\n")
    
    # Open browser automatically
    try:
        import webbrowser
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass
    
    serve(app, host='0.0.0.0', port=port, threads=4)

