#!/bin/bash

export UID=$(id -u)
export GID=$(id -g)

docker compose --env-file <(env | grep -E '^(UID|GID|DISPLAY)=') up --build