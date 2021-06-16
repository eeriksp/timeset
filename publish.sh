set -eu

# Run the tests
./test.sh

# Remove old builds
rm dist -r || true

# Build
python3.8 -m build

# Upload to PyPi (will prompt for username and password)
python3.8 -m twine upload dist/*
