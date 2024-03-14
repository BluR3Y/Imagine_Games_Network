provider "aws" {
  region = "us-east-1" # Declare preferred AWS region
  profile = "localstack" # Profile name for aws credentials in path C:/Users/<user>/.aws/credentials

  # *** Esential for localstack
  skip_credentials_validation = true
  skip_metadata_api_check = true
  skip_requesting_account_id = true

  endpoints {
    s3 = "http://s3.localhost.localstack.cloud:4566"
  }
  # **************************
}

resource "aws_s3_bucket" "main_bucket" {
  bucket = "imagine-games-network"
}