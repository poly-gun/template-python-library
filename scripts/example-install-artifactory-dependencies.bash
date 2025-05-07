#!/bin/bash --posix

# -*-  Coding: UTF-8  -*- #
# -*-  System: Linux  -*- #
# -*-  Usage:   *.*   -*- #

# Author: Jacob Sanders (GitHub - Segmentational)

# See Bash Set-Options Reference Below

set -euo pipefail # (0)
set -o xtrace # (6)

# --------------------------------------------------------------------------------
# Bash Set-Options Reference
#     - https://tldp.org/LDP/abs/html/options.html
# --------------------------------------------------------------------------------

# 0. An Opinionated, Well Agreed Upon Standard for Bash Script Execution
# 1. set -o verbose     ::: Print Shell Input upon Read
# 2. set -o allexport   ::: Export all Variable(s) + Function(s) to Environment
# 3. set -o errexit     ::: Exit Immediately upon Pipeline'd Failure
# 4. set -o monitor     ::: Output Process-Separated Command(s)
# 5. set -o privileged  ::: Ignore Externals - Ensures of Pristine Run Environment
# 6. set -o xtrace      ::: Print a Trace of Simple Commands
# 7. set -o braceexpand ::: Enable Brace Expansion
# 8. set -o no-exec     ::: Bash Syntax Debugging

# Establish a virtual environment.
# python3 -m venv "$(git rev-parse --show-toplevel)/.venv"
# source $(git rev-parse --show-toplevel)/.venv/bin/activate

if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Invalid Runtime - No Python Virtual Environment Found."
    echo " - Creating Virtual Environment"

    python3 -m venv "$(git rev-parse --show-toplevel)/.venv"

    echo "Please run the following command, and try again"
    echo "    source .venv/bin/activate"

    exit 1
fi

# Ensure private CA bundle is added to virtual environment.

if [[ ! $(pip show certifi) ]]; then
    echo "Installing Required Certificate Package(s) ..."

    pip install certifi
fi

cat "$(git rev-parse --show-toplevel)/assets/certificates/ca.crt.example.pem" >> "$(python -c "import certifi; print(certifi.where())")"

# Install common packages through private registry.

pip install --upgrade pip --no-cache-dir --force-reinstall \
    --index-url "https://artifactory.example.com/artifactory/api/pypi/pypi/simple"

# Optionally install common packages through private registry (--extra-index-url).

pip install . --no-cache-dir --force-reinstall \
    --extra-index-url "https://artifactory.example.com/artifactory/api/pypi/pypi/simple"
