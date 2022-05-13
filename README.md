# url-status-check-python-prometheus

This repository is to check an external URL status and output the response in Prometheus format

## Table of contents

-   [url-status-check-python-prometheus](#url-status-check-python-prometheus)
    -   [Table of contents:](#table-of-contents)
    -   [Overview](#overview)
    -   [Functionality](#functionality)
    -   [Requirements](#requirements)
    -   [Docker Image Creation](#docker-image-creation)
    -   [Deploying into Kubernetes using Helm](#deploying-into-kubernetes-using-helm)
    -   [Output](#output)

## Overview

When the endpoint is accessed, this service checks the following two external URLs and returns metrics in [Prometheus format]

-   <https://httpstat.us/200> 
-   <https://httpstat.us/503>

There are 2 return metrics:

-   Check whether the URL is up and running
-   The response time in milliseconds

## Functionality

We check for the repsonse code and if it 200 --> that means the service is up and running
If the response is NOT 200 and something else like a 503 --> the we consider that the service is down

## Requirements

Python 3.7 or greater version. Also the following modules are required:

-   prometheus_client (0.0.9)
-   requests (2.27.1)

## Docker Image Creation

Execute the following script to build the image

    ./build-image.sh

You can also use the following command to build the image:

    docker build -t kartheek/url-status-check .

## Deploying into Kubernetes using Helm

### Pre-requisites

-   You have a K8 cluster up and running
-   kubectl and helm installed locally on your machine

### Steps

To run on local you will need to set the context of your K8 cluster

    kubectl config use-context <your cluster>
    kubectl config view --minify
    kubectl cluster-info
    kubectl config current-context

Once that is done run the following commands:

    helm install url-status-check charts/url-status-check/

The output will look something like below once deployed:

    NAME: url-status-check
    NAMESPACE: default
    STATUS: deployed
    REVISION: 1

Once deployed you can get the application URL by using the following commands:

    Get the application URL by running these commands:
      export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services url-status-check)
      export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
      echo http://$NODE_IP:$NODE_PORT

On your chosen node (NODE_IP), create a firewall rule that allows TCP traffic on your node port.
For example, if your Service has a NodePort value of 31568, create a firewall rule that allows TCP traffic on port 31568.

    curl http://$NODE_IP:$NODE_PORT

## Output

Your output should look something like the below

    # HELP sample_external_url_response_ms Response Time
    # TYPE sample_external_url_response_ms gauge
    sample_external_url_response_ms{url="https://httpstat.us/503"} 194.43273544311523
    sample_external_url_response_ms{url="https://httpstat.us/200"} 113.79003524780273
    # HELP sample_external_url_up URL Up
    # TYPE sample_external_url_up gauge
    sample_external_url_up{url="https://httpstat.us/503"} 0.0
    sample_external_url_up{url="https://httpstat.us/200"} 1.0
