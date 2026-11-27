"""Tariff Calculator API examples (Python, standard library only).

Docs: https://tariff.synnaxstudio.com/docs
Auth: Business Plan API key in the X-API-Key header.
Set TARIFF_API_KEY before running; never hard-code a real key.
"""

import json
import os
import urllib.error
import urllib.request

BASE_URL = "https://tariff.synnaxstudio.com"
API_KEY = os.environ.get("TARIFF_API_KEY", "YOUR_UNIQUE_API_KEY")


def calculate(payload):
    """POST /api/business/calculate and return the parsed response dict."""
    req = urllib.request.Request(
        f"{BASE_URL}/api/business/calculate",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8')}")
        raise


def tariff_info(hs_code):
    """GET /api/tariff/info — metal profiles and user-selection candidates."""
    url = f"{BASE_URL}/api/tariff/info?hsCode={hs_code}"
    req = urllib.request.Request(url, headers={"X-API-Key": API_KEY})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def show(result):
    if result.get("isIncomplete"):
        print("WARNING: result is incomplete — some duties were skipped:")
        for c in result.get("excludedCandidates", []):
            print(f"  - {c.get('code')}: missing {c.get('missingField')}")
    print(f"Total duty: ${result.get('totalDuty')} "
          f"(rate {result.get('dutyRate')}, MPF ${result.get('mpf')}, "
          f"HMF ${result.get('hmf')})")
    for d in result.get("duties", []):
        print(f"  - {d.get('hscode')}: ${d.get('value')} — {d.get('label')}")


if __name__ == "__main__":
    # 1. Basic calculation (from the docs): boys' wool overcoat from Vietnam.
    print("== Basic calculation ==")
    show(calculate({
        "hsCode": "6201201120",
        "value": 15000,
        "country": "VN",
        "entryDate": "2025-08-15",
        "transport": "OCEAN",
        "unitOfMeasures": {"KG": 100},
        "additionalFields": {
            "STEEL_PERCENTAGE": 0,
            "ALUMINUM_PERCENTAGE": 0,
            "COPPER_PERCENTAGE": 0,
            "US_CONTENT_PERCENTAGE": 0,
        },
    }))

    # 2. Section 232 steel example (from the docs): steel article from Ukraine.
    print("\n== Steel example (Section 232) ==")
    print(json.dumps(
        tariff_info("7326901000").get("metalProfiles", {}), indent=2))
    show(calculate({
        "hsCode": "7326901000",
        "value": 10000,
        "country": "UA",
        "transport": "OCEAN",
        "additionalFields": {
            "STEEL_PERCENTAGE": 50,
            "STEEL_COUNTRY_OF_POUR": "UA",
        },
    }))
