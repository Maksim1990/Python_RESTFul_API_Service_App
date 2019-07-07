#!/usr/bin/env bash

sed -e "s/\${APP_HTTP_PORT}/${DEV_HTTP_PORT}/g;"  ./deploy/docker-compose_with_mysql_as_shared_service.dev.tpl.yml > docker-compose.yml

sed -e "s/\${APP_HTTP_PORT}/${DEV_HTTP_PORT}/g;
         s/\${APP_MYSQL_DATABASE}/${DEV_MYSQL_DATABASE}/g;
         s/\${APP_MYSQL_PASSWORD}/${DEV_SHARED_MYSQL_PASSWORD}/g;"  ./deploy/.env.dist.deploy > ./deploy/env/.env.dist
