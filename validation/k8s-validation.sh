#!/bin/bash

set -e

echo "========================================="
echo " Validating Kubernetes Manifests"
echo "========================================="

echo "Checking Backend ConfigMap..."
kubectl apply --dry-run=client -f kubernetes/backend/configmap.yaml

echo "Checking Backend Secret..."
kubectl apply --dry-run=client -f kubernetes/backend/secret.yaml

echo "Checking Backend Deployment..."
kubectl apply --dry-run=client -f kubernetes/backend/deployment.yaml

echo "Checking Backend Service..."
kubectl apply --dry-run=client -f kubernetes/backend/service.yaml

echo "Checking Frontend Deployment..."
kubectl apply --dry-run=client -f kubernetes/frontend/deployment.yaml

echo "Checking Frontend Service..."
kubectl apply --dry-run=client -f kubernetes/frontend/service.yaml

echo ""
echo "✅ All Kubernetes manifests are valid!"