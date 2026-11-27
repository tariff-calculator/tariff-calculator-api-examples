# Tariff Calculator API — Examples

Code samples for the [Tariff Calculator API](https://tariff.synnaxstudio.com/docs): estimate US import duties by HTS code and country of origin, including Section 301, Section 232 and other Chapter 99 tariffs, plus MPF and HMF.

- **Try it without code:** https://tariff.synnaxstudio.com/calculator
- **Current US tariff measures:** https://tariff.synnaxstudio.com/us-tariffs
- **Full API docs:** https://tariff.synnaxstudio.com/docs

## Setup

API access is a **Business Plan** feature (2,500 calls per monthly billing cycle). Get your key from your Tariff Calculator account and set it as an environment variable — never commit a real key:

```bash
export TARIFF_API_KEY="YOUR_UNIQUE_API_KEY"
```

All requests go to `https://tariff.synnaxstudio.com` with the key in the `X-API-Key` header.

## Examples

| File | What it does |
| --- | --- |
| `examples/calculate.py` | Python (stdlib only): basic calculation + steel (Section 232) example, with the `isIncomplete` check |
| `examples/calculate.js` | Node.js (fetch, Node 18+): same two calculations |
| `examples/calculate.sh` | cURL: basic calculation + steel example |
| `postman/Tariff-Calculator-API.postman_collection.json` | Postman Collection v2.1: calculate + tariff-info requests |

## The two endpoints

**Calculate** — `POST /api/business/calculate`

```json
{
  "hsCode": "6201201120",
  "value": 15000,
  "country": "VN",
  "entryDate": "2025-08-15",
  "transport": "OCEAN",
  "unitOfMeasures": { "KG": 100 },
  "additionalFields": {
    "STEEL_PERCENTAGE": 0,
    "ALUMINUM_PERCENTAGE": 0,
    "COPPER_PERCENTAGE": 0,
    "US_CONTENT_PERCENTAGE": 0
  }
}
```

**Tariff info** — `GET /api/tariff/info?hsCode=7326901000`

Returns tariff metadata for an HS code, including `metalProfiles` (which Section 232 fields a code needs) and `userSelectionCandidates` (provisions only you can confirm — send a confirmed code in `additionalFields.CHOSEN_HTS_CODES` as `true`).

## Always check `isIncomplete`

A successful (200) response can still be understated: when required fields (e.g. metal composition) are missing, the API returns `isIncomplete: true` and lists the skipped tariff codes in `excludedCandidates`. Check it on every response before using `totalDuty`.

Example response (abridged):

```json
{
  "totalDuty": "3986",
  "dutyRate": "0.26573333333333333333",
  "hmf": "18.75",
  "mpf": "51.96",
  "duties": [{ "hscode": "99030125", "value": "1500", "label": "IEEPA Reciprocal All Country 10%" }],
  "isIncomplete": false,
  "excludedCandidates": [],
  "userSelectionCandidates": []
}
```

## Errors

| Status | Meaning |
| --- | --- |
| 400 | Bad request — missing/invalid parameter, missing required unit of measure, or restricted country of origin |
| 401 | Missing or invalid API key |
| 403 | Not a Business Plan subscriber |
| 404 | HS code not found |
| 429 | Monthly API quota exceeded |
| 500 | Server error |

Built by [Synnax Studio Ltd](https://tariff.synnaxstudio.com). Rates come from the official USITC Harmonized Tariff Schedule.
