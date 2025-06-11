#!/bin/bash
# Run all backend and frontend tests

set -e

# Install backend dependencies
pip install -r requirements.txt || exit 1

# Install frontend dependencies
cd frontend && npm install && npm run build && cd .. || exit 1

# Run backend tests
pytest backend/tests || exit 1

# Run frontend tests
cd frontend && npx vitest run && cd ..
