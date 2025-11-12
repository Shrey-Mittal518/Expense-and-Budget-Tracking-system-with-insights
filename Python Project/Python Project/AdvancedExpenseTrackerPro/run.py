#!/usr/bin/env python3
"""
Application entry point for AdvancedExpenseTrackerPro
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
