#!/bin/bash

export WATERMARK_OUTPUT_BUCKET_NAME=watermarkoutput
gcloud functions deploy watermark_file \
--runtime python39 --trigger-bucket=watermarkinput \
--set-env-vars WATERMARK_OUTPUT_BUCKET_NAME=watermarkoutput