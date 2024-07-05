#!/bin/bash

set -e

docker run --rm -it --name pg-comtrade-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d ${1:-postgres}