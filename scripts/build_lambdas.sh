#!/bin/bash 

#build attach hosted zone
cd lambda/attach_hosted_zone/
pip install -r requirements.txt -t .
mkdir -p ../../builds
zip -r ../../builds/attach_hosted_zone.zip ./*
