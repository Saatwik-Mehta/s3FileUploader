<!--
title: 'AWS REST API to Upload a simple file S3 bucket using Python'
description: 'This Template will be used to create an REST API to upload a file in S3 bucket. It will be backed by a Lambda function which will upload the data in S3 Bucket. This S3 bucket will have the access policy for the Lambda function to PutObjects in it'
layout: Doc
framework: v4
platform: AWS
language: python
authorLink: 'https://github.com/Saatwik-Mehta'
authorName: 'Saatwik-Mehta'
authorAvatar: 'https://avatars.githubusercontent.com/u/80687021?v=4'
-->

# Serverless Framework Python REST API on AWS

Building A full AWS serverless based Backend for **Simple File Uploader**. Services used are `APIGateway` to manage the actual API, `Lambda Function` to support the REST api and `S3` to store the File in an S3 Bucket.

This app serves as a Simple File Uploader where we learn about serverless functionality of AWS. This app further can be extended for more apps, one such example is a simple resume uploader, PDF editor or infact Legal Document uploader.