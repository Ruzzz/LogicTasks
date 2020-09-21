#!/usr/bin/env bash
docker stop mblog-api && docker rm mblog-api

CUR_DIR=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
pushd $CUR_DIR/..

docker build \
    -t mblog/api \
    -f Dockerfile .

[[ $? -eq 0 ]] && docker container create \
    --name mblog-api \
    --restart unless-stopped \
    --network host \
    -p 8080:8080 \
    -e "MBLOG_HOST=localhost" \
    -e "MBLOG_PORT=8080" \
    -e "MBLOG_DB=mblog" \
    -e "MBLOG_DB_USER=mblog" \
    -e "MBLOG_DB_PASSWORD=mblog" \
    -e "MBLOG_SECRET=mblog" \
    mblog/api

[[ $? -eq 0 ]] && docker start mblog-api
popd
