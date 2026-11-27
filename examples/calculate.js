// Tariff Calculator API examples (Node.js 18+, fetch is built in).
//
// Docs: https://tariff.synnaxstudio.com/docs
// Auth: Business Plan API key in the X-API-Key header.
// Set TARIFF_API_KEY before running; never hard-code a real key.

const BASE_URL = "https://tariff.synnaxstudio.com";
const API_KEY = process.env.TARIFF_API_KEY || "YOUR_UNIQUE_API_KEY";

async function calculate(payload) {
  const res = await fetch(`${BASE_URL}/api/business/calculate`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-API-Key": API_KEY },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

async function tariffInfo(hsCode) {
  const res = await fetch(
    `${BASE_URL}/api/tariff/info?hsCode=${hsCode}`,
    { headers: { "X-API-Key": API_KEY } },
  );
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

function show(result) {
  if (result.isIncomplete) {
    console.log("WARNING: result is incomplete — some duties were skipped:");
    for (const c of result.excludedCandidates || []) {
      console.log(`  - ${c.code}: missing ${c.missingField}`);
    }
  }
  console.log(
    `Total duty: $${result.totalDuty} (rate ${result.dutyRate}, ` +
      `MPF $${result.mpf}, HMF $${result.hmf})`,
  );
  for (const d of result.duties || []) {
    console.log(`  - ${d.hscode}: $${d.value} — ${d.label}`);
  }
}

async function main() {
  // 1. Basic calculation (from the docs): boys' wool overcoat from Vietnam.
  console.log("== Basic calculation ==");
  show(
    await calculate({
      hsCode: "6201201120",
      value: 15000,
      country: "VN",
      entryDate: "2025-08-15",
      transport: "OCEAN",
      unitOfMeasures: { KG: 100 },
      additionalFields: {
        STEEL_PERCENTAGE: 0,
        ALUMINUM_PERCENTAGE: 0,
        COPPER_PERCENTAGE: 0,
        US_CONTENT_PERCENTAGE: 0,
      },
    }),
  );

  // 2. Section 232 steel example (from the docs): steel article from Ukraine.
  console.log("\n== Steel example (Section 232) ==");
  console.log(JSON.stringify((await tariffInfo("7326901000")).metalProfiles, null, 2));
  show(
    await calculate({
      hsCode: "7326901000",
      value: 10000,
      country: "UA",
      transport: "OCEAN",
      additionalFields: {
        STEEL_PERCENTAGE: 50,
        STEEL_COUNTRY_OF_POUR: "UA",
      },
    }),
  );
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
