#!/bin/bash
# Run all backend and frontend tests

set -e

# Run backend tests
cd backend
pytest
cd ..

# Run frontend tests (if any)
if [ -f frontend/package.json ]; then
  cd frontend
  if npm run | grep -q "test"; then
    npm install
    npm test
  else
    echo "No frontend test script found. Skipping frontend tests."
  fi
  cd ..
else
  echo "No frontend directory found. Skipping frontend tests."
fi
