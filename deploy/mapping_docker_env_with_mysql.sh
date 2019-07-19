#!/usr/bin/env bash

sed -e "s/\${APP_HTTP_PORT}/${DEV_HTTP_PORT}/g;
            s/\${APP_MONGO_PORT}/${DEV_MONGO_PORT}/g;
            s/\${APP_MONGO_USER}/${DEV_MONGO_USER}/g;
            s/\${APP_MONGO_PASSWORD}/${DEV_MONGO_PASSWORD}/g;
            s/\${APP_MYSQL_DATABASE}/${DEV_MYSQL_DATABASE}/g;
            s/\${APP_MYSQL_PASSWORD}/${DEV_MYSQL_PASSWORD}/g;
            s/\${APP_MYSQL_PORT}/${DEV_MYSQL_PORT}/g;"  ./deploy/docker-compose.dev.tpl.yml > docker-compose.yml

sed -e "s/\${APP_HTTP_PORT}/${DEV_HTTP_PORT}/g;
         s/\${APP_MYSQL_DATABASE}/${DEV_MYSQL_DATABASE}/g;
         s/\${APP_BASE_URL}/${SSH_HOST_VPS}/g;
         s/\${APP_MYSQL_PASSWORD}/${DEV_MYSQL_PASSWORD}/g;"  ./deploy/.env.dist.deploy > ./deploy/env/.env.dist
