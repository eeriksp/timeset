set -eu

# Run the tests
python3 src/timeset/tests.py

# Remove old builds
rm dist -r

# Build
python -m build

# Upload to PyPi (will prompt for username and password)
twine upload  dist/*