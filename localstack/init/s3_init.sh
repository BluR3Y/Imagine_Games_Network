#!/bin/bash

echo "Initializing localstack services..."

aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket imagine_games_network
awslocal s3api put-bucket-cors --bucket imagine_games_network --cors-configuration file:///tmp/localstack/s3_cors_config.json