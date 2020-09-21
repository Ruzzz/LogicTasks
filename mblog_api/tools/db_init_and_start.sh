#!/usr/bin/env bash
docker stop mblog-db && docker rm mblog-db

CUR_DIR=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
pushd $CUR_DIR/../db

docker build \
    -t mblog/db \
    -f Dockerfile .

[[ $? -eq 0 ]] && docker container create \
    --name mblog-db \
    --restart unless-stopped \
    -p 5432:5432 \
    -e "POSTGRES_USER=mblog" \
    -e "POSTGRES_PASSWORD=mblog" \
    -e "POSTGRES_DB=mblog" \
    mblog/db

[[ $? -eq 0 ]] && docker start mblog-db
popd
