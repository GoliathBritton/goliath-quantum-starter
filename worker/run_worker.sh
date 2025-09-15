#!/usr/bin/env bash
export PYTHONUNBUFFERED=1
rq worker dialer --url $REDIS_URL