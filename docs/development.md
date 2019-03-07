
# Development

## Setting up the environment

1. Docker

***Note that the port mapping will conflict with running `make test`***

2. Redis

    ```sh
    $ docker run --name dev-redis -d -p 6379:6379 redis
    ```

3. Install go 1.11 

4. Install the golang packages via [dep](https://github.com/golang/dep/releases)

    ```sh
    $ dep ensure
    ```

5.  Protobuf generator tools (Optional)

    - `https://github.com/golang/protobuf`

    - `https://grpc.io/docs/tutorials/basic/python.html`

    To generate proto files, clone [presidio-genproto](https://github.com/Microsoft/presidio-genproto) and run the following commands in `$GOPATH/src/github.com/Microsoft/presidio-genproto/src` folder

    ```sh
    $ python -m grpc_tools.protoc -I . --python_out=../python --grpc_python_out=../python ./*.proto
    ```

    ```sh
    $ protoc -I . --go_out=plugins=grpc:../golang ./*.proto
    ```

6. `presidio-analyzer` development
    *   Install Python 3.7 
    *   Build and install [re2](https://github.com/google/re2)

        ```sh
        $ re2_version="2018-12-01"
        $ wget -O re2.tar.gz https://github.com/google/re2/archive/${re2_version}.tar.gz
        $ mkdir re2 
        $ tar --extract --file "re2.tar.gz" --directory "re2" --strip-components 1
        $ cd re2 && make install
        ```
    *   Install the Python packages for the analyzer in the `presidio-analyzer` folder

        ```sh
        $ pip3 install -r requirements.txt
        $ pip3 install -r requirements-dev.txt
        ```

        **Note:** If you encounter errors with `pyre2` than install `cython` first

        ```sh
        $ pip3 install cython
        ```

    *   Install [tesseract](https://github.com/tesseract-ocr/tesseract/wiki) OCR framework.
    *   Enable Pylint, Flake8 and Pydocstyle linting following the [Code-with Engineering Playbook](https://github.com/Microsoft/code-with-engineering-playbook/blob/master/Engineering/CodeReviews/Python.md) guidelines.

        If you are using VS Code, Pylint is enabled by default and you should add the following workspace settings, as explained in [VS Code Python linting](https://code.visualstudio.com/docs/python/linting).
        This way your workspace settings are aligned with your build settings specifided in the analyzer/Dockerfile.
        ```
        "python.linting.enabled": true,
        "python.linting.pylintArgs": [
        "--rcfile",
            "${workspaceFolder}/presidio-analyzer/pylintrc"
        ],
        "python.linting.flake8Enabled": true,
        "python.linting.flake8Args": [
            "--config",
            "${workspaceFolder}/presidio-analyzer/setup.cfg"
        ],
        "python.linting.pydocstyleEnabled": true,
        "python.linting.pydocstyleArgs": [
            "--config",
            "${workspaceFolder}/presidio-analyzer/setup.cfg"
        ]
        ```

## Development notes

- Build the bins with `make build`
- Build the the Docker image with `make docker-build`
- Push the Docker images with `make docker-push`
- Run the tests with `make test`
- Adding a file in go requires the `make go-format` command before running and building the service.
- Run functional tests with `make test-functional`

### Set the following environnement variables

#### presidio-analyzer

- `GRPC_PORT`: `3001` GRPC listen port

#### presidio-anonymizer

- `GRPC_PORT`: `3002` GRPC listen port

#### presidio-api

- `WEB_PORT`: `8080` HTTP listen port
- `REDIS_URL`: `localhost:6379`, Optional: Redis address
- `ANALYZER_SVC_ADDRESS`: `localhost:3001`, Analyzer address
- `ANONYMIZER_SVC_ADDRESS`: `localhost:3002`, Anonymizer address

## Load test

1. Edit  `post.lua`. Change the template name
2. Run [wrk](https://github.com/wg/wrk)

    ```sh
    wrk -t2 -c2 -d30s -s post.lua http://<api-service-address>/api/v1/projects/<my-project>/analyze
    ```
