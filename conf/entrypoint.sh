#!/bin/bash

set -e
trap "kill 0" SIGINT SIGTERM

nginx &
exec keystone-api "$@"
