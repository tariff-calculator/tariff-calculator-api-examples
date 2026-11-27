#!/usr/bin/env bash
# Tariff Calculator API examples (cURL).
# Docs: https://tariff.synnaxstudio.com/docs
# Auth: Business Plan API key in the X-API-Key header.
# Usage: TARIFF_API_KEY="YOUR_UNIQUE_API_KEY" bash calculate.sh
# Never hard-code a real key.

set -euo pipefail

BASE_URL="https://tariff.synnaxstudio.com"
API_KEY="${TARIFF_API_KEY:-YOUR_UNIQUE_API_KEY}"

# 1. Basic calculation (from the docs): boys' wool overcoat from Vietnam.
echo "== Basic calculation =="
curl -s -X POST "${BASE_URL}/api/business/calculate" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${API_KEY}" \
  -d '{
    "hsCode": "6201201120",
    "value": 15000,
    "country": "VN",
    "entryDate": "2025-08-15",
    "transport": "OCEAN",
    "unitOfMeasures": {
      "KG": 100
    },
    "additionalFields": {
      "STEEL_PERCENTAGE": 0,
      "ALUMINUM_PERCENTAGE": 0,
      "COPPER_PERCENTAGE": 0,
      "US_CONTENT_PERCENTAGE": 0
    }
  }'
echo

# 2. Tariff info (from the docs): what a steel HS code needs.
echo "== Tariff info =="
curl -s "${BASE_URL}/api/tariff/info?hsCode=7326901000" \
  -H "X-API-Key: ${API_KEY}"
echo

# 3. Section 232 steel example (from the docs): steel article from Ukraine, 50% steel.
echo "== Steel example (Section 232) =="
curl -s -X POST "${BASE_URL}/api/business/calculate" \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: ${API_KEY}" \
  -d '{
    "hsCode": "7326901000",
    "value": 10000,
    "country": "UA",
    "transport": "OCEAN",
    "additionalFields": {
      "STEEL_PERCENTAGE": 50,
      "STEEL_COUNTRY_OF_POUR": "UA"
    }
  }'
echo
