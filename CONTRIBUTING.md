# Contribution Guide

## Template Development

_Only applicable for the template, example project repository._

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ".[all]"

python -m pytest
```

## Local Development

In order to install all local, optional dependencies in [***editable***](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#working-in-development-mode) mode:

```bash
python -m pip install --extra-index-url "https://artifactory.example.com/artifactory/api/pypi/pypi/simple" ".[all]"
```

***Editable***

```bash
python -m pip install --editable ".[all]"
```

### Testing

```bash
python -m pytest --junit-xml unit-testing.xml
```

## Standards

### Versioning

Please see [`pyproject.toml`](./pyproject.toml) for versioning usage and packaging implications.

### Code & Inline Documentation

This project uses various, but official, docstring formats for inline documentation.

Additionally, `pydantic` models are extensively used where properties have `description` assignments; these
types of properties allow for auto-documentation capabilities.

### Unit Testing

The following project makes use of [`pytest`](https://pypi.org/project/pytest-mock/) due to its 
file-level testing simplicity and because of its integration capabilities with the CI system.

Please see Pytest's [official documentation](https://pypi.org/project/pytest-mock/) for additional information.

## Distributions

### Authenticating into Artifactory

Artifactory can and is configured differently across instances and companies; ideally, there should 
be a CI-specific user with read & write permissions, where the credentials for which are automatically rotated and 
published to CICD variables.

- GitLab Example
  - Use the API to scan all projects where a platform team's dedicated CI-user is added to a group/project as an Owner.
  - For every project/group, publish the newly rotated Artifactory credentials into CI-CD environment variables.
  - Project maintainers then modify their `.gitlab-ci.yml` jobs to use the Artifactory credentials either as `pip` CLI arguments or environment variables.

Depending on the environment, ideally, read-only access is granted to everyone on a private network without having to 
specify credentials. In more locked-down approaches, engineers should have their own API personal access tokens.

## Useful Commands and References

### Adding Python Virtual-Environment to `${PATH}`

In the system's rc file (e.g. `~/.zshrc` or `~/.profile`):

```bash
if [[ -d "$(pwd)/venv" ]]; then 
    export PATH="${PATH}:$(pwd)/venv/bin"
elif [[ -d "$(pwd)/.venv" ]]; then
    export PATH="${PATH}:$(pwd)/.venv/bin"
fi
```

- If a `venv` "virtual environment" is available (commonly `venv` or `.venv`), then 
  export the directory's `bin` directory as a part of the user's `${PATH}`.
  - Enables the ability execute the callable, if applicable (i.e. `example-cli` vs `python -m src/example/cli`)

### Debian + Ubuntu Example Layer for TLS/CA Certificates

```Dockerfile
ARG PLATFORM="linux/amd64"

[...]

FROM --platform=${PLATFORM} ubuntu:22.04 AS example-layer

WORKDIR /

# Company specific certificate-authority.
COPY ./assets/certificates/ca.crt.example.pem /usr/local/share/ca-certificates/example-root-ca.crt

RUN chmod 644 /usr/local/share/ca-certificates/example-root-ca.crt

# Update OS package registry and system certificate authorities.
RUN apt update && apt install -y curl ca-certificates && update-ca-certificates

[...]
```

## Useful Commands

**Get `pip` Cache Directory**

```bash
pip cache dir
```

**Install Package Without Cache & With Private Registry**

```bash
pip install . --no-cache-dir --force-reinstall --extra-index-url "https://artifactory.example.com/artifactory/api/pypi/pypi/simple"
````

## General Troubleshooting

### Docker

#### Local Usage with Corporate VPN & Proxy

Due to Docker's corporate restrictions relating to installation of "Docker Desktop", `colima` can be used for local-development 
purposes. Additionally, if the company requires privately-signed TLS certificate(s), a proxy, and/or a VPN, please use 
the following code snippet for system setup.

```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ./assets/certificates/ca.crt.example.pem
mkdir -p "${HOME}/.ca-certificates"
cp -rf ./assets/certificates/ca.crt.example.pem ~/.ca-certificates

function start-colima() {
    local CERTS="${HOME}/.ca-certificates"
    local URL="registry-1.docker.io:443"
    mkdir -p ${CERTS}
    openssl s_client -showcerts -connect ${URL} </dev/null 2>/dev/null|openssl x509 -outform PEM >${CERTS}/docker-com.pem
    openssl s_client -showcerts -verify 5 -connect ${URL} </dev/null 2>/dev/null | sed -ne '/-BEGIN/,/-END/p' >${CERTS}/docker-com-chain.pem
    colima start
  
    for file in ${HOME}/.ca-certificates/*.pem; do 
        cp -f -- "${file}" "${file%.pem}.crt"  
    done
  
    colima ssh -- sudo cp ${HOME}/.ca-certificates/* /usr/local/share/ca-certificates/
    colima ssh -- sudo update-ca-certificates
    colima ssh -- sudo service docker restart
    
    colima restart
}

start-colima
```

##### Noteable Colima Issue(s)

- https://github.com/abiosoft/colima/issues/256

### Python - Multiplexed-Path Support

For errors relating to:

```
NotADirectoryError: MultiplexedPath only supports directories
```

This is due to a relatively [complex issue](https://github.com/python/importlib_resources/issues/311); in summary,
when installing from source using `pip install --editable [...] .`, namespaced packages are currently broken for certain
data look-ups. Please see the issue for additional details.

As a workaround, ***when installing from source, do not include the `--editable` flag***.

### Python & PIP TLS Issue(s)

#### Virtual Environment Certificate Configuration

When locally developing, it's always advised to do so under a python *virtual environment*. However,
when creating a new virtual environment, company-specific certificates will not be automatically included.

This will result in various APIs or SDKs (such as `botocore` or `boto3`) to fail when making external HTTPs calls.

See the following script as an example of when to add a `certificates/ca.crt.example.pem` CA PEM bundle to the python virtual environment.

```bash
#!/bin/bash --posix

# -*-  Coding: UTF-8  -*- #
# -*-  System: Linux  -*- #
# -*-  Usage:   *.*   -*- #

# Author: Jacob Sanders (GitHub - Segmentational)

# --------------------------------------------------------------------------------
# Overview
# --------------------------------------------------------------------------------
# The following script assumes a relative directory structure:
#
# .
# ├── venv
# ├── scripts
# │    └── fix-virtual-environment-ca-bundle.bash
# └── assets
#      └── certificates/ca.crt.example.pem
#
# Example Usage
# -------------
#
#   $ python -m venv venv
#   $ source venv/bin/activate
#   $ bash ./scripts/fix-virtual-environment-ca-bundle.bash
#

# See Bash Set-Options Reference Below

set -euo pipefail # (0)
set -o xtrace # (6)

function cwd() {
    printf "%s" "$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
}

function assets() {
    printf "%s" "$(cwd)/../assets"
}

function main() {
    if [[ -z "${VIRTUAL_ENV}" ]]; then
        echo "Invalid Runtime - No Python Virtual Environment Found"

        exit 1
    fi

    if [[ ! $(pip show certifi) ]]; then
        echo "Installing Required Certificate Package(s) ..."

        pip install certifi
    fi

    cat "$(assets)/certificates/ca.crt.example.pem" >> "$(python -c "import certifi; print(certifi.where())")"
}

main

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
```

#### `urllib3` Warnings

`urllib3` warnings will be logged during different types of usage:

- TLS verification is disabled during a request.
- The API endpoint's TLS certificate is invalid.
- An endpoint is using a custom TLS certificate.

The following three sections include instructions for how to disable `urllib3` TLS warnings; please note that none of the these workarounds are officially recommended:

##### Simple

```python
import urllib3

urllib3.disable_warnings()
```

##### Intermediate

```python
import typing
import requests
import contextlib

@contextlib.contextmanager
def disable_ssl_warnings():
    import warnings
    import urllib3
    import urllib3.exceptions

    with warnings.catch_warnings():
        # warnings.filterwarnings("ignore", message="Unverified HTTPS request")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        yield None

...

def example_api_callable(url: str = "https://example-endpoint.com/api/v1/example") -> typing.Any:
    response: requests.Response
    
    with disable_ssl_warnings():
        response = requests.get(url)
        
    if response.status_code == 200:
        return response.json()

    raise RuntimeError("Unexpected Response Status-Code: {}\n{}".format(response.status_code, response.content.decode("utf-8")))
```

##### Advanced

In a more elaborate, targeted approach for endpoints with internal or invalid TLS certificates:

```python
import typing
import contextlib
import pathlib

import ssl

import urllib3
import urllib3.poolmanager

import requests
import requests.adapters
import requests.certs

@contextlib.contextmanager
def disable_ssl_warnings():
    import warnings
    import urllib3

    with warnings.catch_warnings():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        yield None

...

class SSL(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = ssl.create_default_context()

        ctx.set_ciphers("DEFAULT")
        ctx.verify_mode = ssl.CERT_OPTIONAL
        ctx.check_hostname = False

        # ctx = ssl.create_default_context()
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE

        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize, block=block, ssl_context=ctx
        )

...

def example_api_callable(timeout: int = 600, url: str = "https://example-invalid-tls-certificate-endpoint.com/api/v1/example") -> typing.Any:
    response: requests.Response
    
    with disable_ssl_warnings():
        with requests.session() as session:
            session.verify = False

            session.mount("https://", SSL())

            response = session.get(url, timeout=timeout, stream=False, allow_redirects=True)
            
            try:
                response.raise_for_status()
            except ...:
                ...
            
    if response.status_code == 200:
        return response.json()

    raise RuntimeError("Unexpected Response Status-Code: {}\n{}".format(response.status_code, response.content.decode("utf-8")))
```

- https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings

### Botocore S3 SSL Validation Failure

<details>
<summary>Example Log Output</summary>
  
```
botocore.exceptions.SSLError: SSL validation failed for https://example.s3.amazonaws.com/ [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1006)
```
</details>

###### Solution 1

*Add company certificate to the system or virtual environment's ca-bundle.*

For virtual environments, please see [`fix-virtual-environment-ca-bundle.bash`](./scripts/fix-virtual-environment-ca-bundle.bash).

If the runtime is not in a virtual environment, for example, running an interactive Docker container,
please see [`fix-system-ca-bundle.bash`](./scripts/fix-system-ca-bundle.bash).

