import assert from "node:assert/strict";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { chromium } from "playwright";
import { startGalleryServer } from "./server.mjs";
import { createDemoFixture } from "./test-helpers.mjs";

async function openBrowserFixture(
  t,
  viewport,
  { additionalBatchIds = [] } = {},
) {
  const dataRoot = await mkdtemp(join(tmpdir(), "akari-browser-"));
  await createDemoFixture(dataRoot);
  for (const batchId of additionalBatchIds) {
    await createDemoFixture(dataRoot, { batchId });
  }
  const running = await startGalleryServer({
    dataRoot,
    host: "127.0.0.1",
    port: 0,
    allowLoopback: true,
  });
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  const page = await browser.newPage({ viewport });
  t.after(async () => {
    await browser.close();
    await running.close();
  });
  await page.goto(running.url);
  await page.waitForSelector("[data-image-id]");
  return { dataRoot, page, running };
}

test("desktop grid supports keyboard review and persisted progress", async (t) => {
  const { page } = await openBrowserFixture(t, {
    width: 1440,
    height: 900,
  });

  assert.equal(await page.locator("[data-image-id]").count(), 50);
  assert.equal(
    await page.locator("[data-image-id] img[loading='lazy']").count(),
    50,
  );
  assert.equal(
    await page.locator("[data-detail-image]").getAttribute("src"),
    null,
  );
  await page.locator("[data-image-id]").first().click();
  assert.match(
    await page.locator("[data-detail-image]").getAttribute("src"),
    /\/media\/B001\/B001-001\/image$/,
  );
  await page.keyboard.press("3");
  await page.waitForSelector('[data-review-status="favorite"]');
  assert.match(await page.locator("[data-progress]").textContent(), /1\s*\/\s*50/);

  const persisted = await page.evaluate(() =>
    fetch("/api/batches/B001/reviews").then((response) => response.json())
  );
  assert.equal(persisted.data.reviews["B001-001"].status, "favorite");
  assert.equal(persisted.data.reviews["B001-001"].revision, 1);

  const firstId = await page.locator("[data-detail-dialog]").getAttribute(
    "data-active-image-id",
  );
  await page.keyboard.press("ArrowRight");
  const secondId = await page.locator("[data-detail-dialog]").getAttribute(
    "data-active-image-id",
  );
  assert.notEqual(firstId, secondId);
  await page.keyboard.press("ArrowLeft");
  assert.equal(
    await page.locator("[data-detail-dialog]").getAttribute(
      "data-active-image-id",
    ),
    firstId,
  );
});

test("mobile detail saves reject reason and advances", async (t) => {
  const { page } = await openBrowserFixture(t, {
    width: 390,
    height: 844,
  });
  await page.locator("[data-image-id]").first().click();
  const controlHeights = await page.locator(
    "[data-detail-dialog] button:visible",
  ).evaluateAll((controls) =>
    controls.map((control) => control.getBoundingClientRect().height)
  );
  assert.ok(controlHeights.every((height) => height >= 44));
  await page.locator("[data-review-note]").fill("keep this note while moving");
  await page.locator("[data-next]").click();
  await page.locator("[data-previous]").click();
  assert.equal(
    await page.locator("[data-review-note]").inputValue(),
    "keep this note while moving",
  );
  await page.locator("[data-review-status-button='reject']").click();
  await page.waitForSelector("[data-reason-controls]:not([hidden])");
  await page.locator("[data-reason='skin-flat']").click();
  await page.locator("[data-save-review]").click();
  await page.waitForSelector(
    '[data-review-status="reject"][data-review-reasons~="skin-flat"]',
  );
  const firstId = await page.locator("[data-detail-dialog]").getAttribute(
    "data-active-image-id",
  );
  await page.locator("[data-next]").click();
  const secondId = await page.locator("[data-detail-dialog]").getAttribute(
    "data-active-image-id",
  );
  assert.notEqual(firstId, secondId);
});

test("all filters narrow cards independently and compose with status", async (t) => {
  const { page } = await openBrowserFixture(t, {
    width: 1280,
    height: 800,
  }, {
    additionalBatchIds: ["B002"],
  });

  assert.equal(await page.locator("[data-batch-filter] option").count(), 2);
  await page.locator("[data-batch-filter]").selectOption("B002");
  await page.waitForSelector("[data-image-id='B002-001']");
  assert.equal(await page.locator("[data-image-id]").count(), 50);
  await page.locator("[data-batch-filter]").selectOption("B001");
  await page.waitForSelector("[data-image-id='B001-001']");
  await page.locator("[data-lane-filter]").selectOption("everyday-girly");
  assert.deepEqual(
    await page.locator("[data-image-id]:visible").evaluateAll(
      (cards) => cards.map((card) => card.dataset.imageId),
    ),
    ["B001-016", "B001-017", "B001-018", "B001-019", "B001-020"],
  );

  await page.locator("[data-lane-filter]").selectOption("all");
  await page.locator("[data-texture-filter]").selectOption("texture");
  assert.deepEqual(
    await page.locator("[data-image-id]:visible").evaluateAll(
      (cards) => cards.map((card) => card.dataset.imageId),
    ),
    Array.from(
      { length: 10 },
      (_, index) => `B001-${String(index + 1).padStart(3, "0")}`,
    ),
  );

  await page.locator("[data-status-filter]").selectOption("unreviewed");
  assert.equal(await page.locator("[data-image-id]:visible").count(), 10);
  await page.locator("[data-texture-filter]").selectOption("all");
  await page.locator("[data-status-filter]").selectOption("all");

  await page.locator("[data-image-id='B001-002']").click();
  await page.locator("[data-review-status-button='reject']").click();
  await page.locator("[data-reason='skin-flat']").click();
  await page.locator("[data-save-review]").click();
  await page.waitForSelector(
    '[data-image-id="B001-002"][data-review-status="reject"]',
  );
  await page.locator("[data-status-filter]").selectOption("all");
  await page.locator("[data-reason-filter]").selectOption("skin-flat");
  assert.deepEqual(
    await page.locator("[data-image-id]:visible").evaluateAll(
      (cards) => cards.map((card) => card.dataset.imageId),
    ),
    ["B001-002"],
  );
});

test("save failures and missing media remain local and visible", async (t) => {
  const { page } = await openBrowserFixture(t, {
    width: 1280,
    height: 800,
  });

  await page.locator("[data-image-id='B001-003']").click();
  await page.route("**/reviews/**", (route) => route.abort());
  await page.keyboard.press("2");
  await page.waitForSelector("[data-save-error]:not(:empty)");
  assert.match(
    await page.locator("[data-save-error]").textContent(),
    /save|network|failed/i,
  );
  assert.equal(
    await page.locator("[data-image-id='B001-003']").getAttribute(
      "data-review-status",
    ),
    "unreviewed",
  );
  const unchanged = await page.evaluate(() =>
    fetch("/api/batches/B001/reviews").then((response) => response.json())
  );
  assert.equal(unchanged.data.reviews["B001-003"].revision, 0);
  await page.unroute("**/reviews/**");
  await page.locator("[data-close]").click();
  await page.locator("[data-image-id='B001-003']").click();
  await page.waitForSelector("[data-save-error]:not(:empty)");

  await page.route("**/media/B001/B001-001/thumb", (route) =>
    route.fulfill({ status: 404, body: "missing" })
  );
  await page.reload();
  await page.waitForSelector(
    '[data-image-id="B001-001"][data-media-unavailable="true"]',
  );
  assert.match(
    await page.locator("[data-image-id='B001-001']").textContent(),
    /Media unavailable/,
  );
  assert.equal(
    await page.locator(
      "[data-image-id='B001-002'][data-media-unavailable='true']",
    ).count(),
    0,
  );
  assert.equal(await page.locator("[data-image-id]").count(), 50);
});

test("readiness appears only after fifty successful review saves", async (t) => {
  const { page } = await openBrowserFixture(t, {
    width: 1280,
    height: 800,
  });

  await page.evaluate(async () => {
    const batch = await fetch("/api/batches/B001").then((response) =>
      response.json()
    );
    const reviews = await fetch("/api/batches/B001/reviews").then((response) =>
      response.json()
    );
    for (const entry of batch.data.entries.slice(0, 49)) {
      let response;
      try {
        response = await fetch(
          `/api/batches/B001/reviews/${entry.id}`,
          {
            method: "PUT",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({
              expectedRevision: reviews.data.reviews[entry.id].revision,
              status: "keep",
              reasons: [],
              note: "",
            }),
          },
        );
      } catch (error) {
        throw new Error(`failed to fetch ${entry.id}: ${error.message}`);
      }
      if (!response.ok) throw new Error(`failed to save ${entry.id}`);
      await response.json();
    }
  });
  await page.reload();
  await page.waitForSelector("[data-image-id]");
  assert.match(await page.locator("[data-progress]").textContent(), /49\s*\/\s*50/);
  assert.equal(await page.getByText("Ready for next batch").count(), 0);

  await page.locator("[data-image-id='B001-050']").click();
  await page.locator("[data-review-status-button='keep']").click();
  await page.locator("[data-save-review]").click();
  await page.waitForSelector("text=Ready for next batch");
  assert.match(await page.locator("[data-progress]").textContent(), /50\s*\/\s*50/);
});

test("fully rated reviews never make a pending batch ready", async (t) => {
  const { dataRoot, page } = await openBrowserFixture(t, {
    width: 1280,
    height: 800,
  });
  const batchDir = join(dataRoot, "batches/B001");
  const manifest = JSON.parse(
    await readFile(join(batchDir, "manifest.json"), "utf8"),
  );
  manifest.entries[0].generation.technicalStatus = "pending";
  manifest.entries[0].artifact.sha256 = null;
  manifest.entries[0].artifact.width = null;
  manifest.entries[0].artifact.height = null;
  await writeFile(
    join(batchDir, "manifest.json"),
    JSON.stringify(manifest),
    "utf8",
  );
  const reviews = await page.evaluate(() =>
    fetch("/api/batches/B001/reviews").then((response) => response.json())
  );
  for (const record of Object.values(reviews.data.reviews)) {
    record.status = "keep";
    record.revision = 1;
    record.updatedAt = "2026-07-30T00:00:00.000Z";
  }
  await writeFile(
    join(batchDir, "reviews.json"),
    JSON.stringify(reviews.data),
    "utf8",
  );

  await page.reload();
  await page.waitForSelector("[data-image-id]");
  assert.match(
    await page.locator("[data-progress]").textContent(),
    /50\s*\/\s*50/,
  );
  assert.equal(await page.getByText("Ready for next batch").count(), 0);
});

test("a completed save cannot mutate a newly selected batch", async (t) => {
  const { page } = await openBrowserFixture(t, {
    width: 1280,
    height: 800,
  }, {
    additionalBatchIds: ["B002"],
  });
  let releaseSave;
  const saveGate = new Promise((resolve) => {
    releaseSave = resolve;
  });
  let markSaveStarted;
  const saveStarted = new Promise((resolve) => {
    markSaveStarted = resolve;
  });
  let markSaveCompleted;
  const saveCompleted = new Promise((resolve) => {
    markSaveCompleted = resolve;
  });
  await page.route(
    "**/api/batches/B001/reviews/B001-001",
    async (route) => {
      markSaveStarted();
      await saveGate;
      const response = await route.fetch();
      await route.fulfill({ response });
      markSaveCompleted();
    },
  );

  await page.locator("[data-image-id='B001-001']").click();
  await page.locator("[data-review-status-button='keep']").click();
  await page.locator("[data-save-review]").click();
  await saveStarted;
  await page.locator("[data-close]").click();
  await page.locator("[data-batch-filter]").selectOption("B002");
  await page.waitForSelector("[data-image-id='B002-001']");

  releaseSave();
  await saveCompleted;
  await page.evaluate(() =>
    new Promise((resolve) =>
      requestAnimationFrame(() => requestAnimationFrame(resolve))
    )
  );
  assert.equal(await page.locator("[data-batch-filter]").inputValue(), "B002");
  assert.equal(await page.locator("[data-image-id]").count(), 50);
  assert.equal(await page.locator("[data-image-id^='B001-']").count(), 0);
  assert.match(await page.locator("[data-progress]").textContent(), /0\s*\/\s*50/);
  assert.equal(await page.locator("[data-save-error]").textContent(), "");

  const saved = await page.evaluate(() =>
    fetch("/api/batches/B001/reviews").then((response) => response.json())
  );
  assert.equal(saved.data.reviews["B001-001"].status, "keep");
});

test("a pending save locks every draft and navigation control", async (t) => {
  const { page } = await openBrowserFixture(t, {
    width: 1280,
    height: 800,
  });
  let releaseSave;
  const saveGate = new Promise((resolve) => {
    releaseSave = resolve;
  });
  let markSaveStarted;
  const saveStarted = new Promise((resolve) => {
    markSaveStarted = resolve;
  });
  await page.route(
    "**/api/batches/B001/reviews/B001-001",
    async (route) => {
      markSaveStarted();
      await saveGate;
      const response = await route.fetch();
      await route.fulfill({ response });
    },
  );

  await page.locator("[data-image-id='B001-001']").click();
  await page.locator("[data-review-note]").fill("submitted draft");
  await page.locator("[data-review-status-button='keep']").click();
  await page.locator("[data-save-review]").click();
  await saveStarted;

  assert.equal(
    await page.locator("[data-review-status-button]").evaluateAll(
      (controls) => controls.every((control) => control.disabled),
    ),
    true,
  );
  assert.equal(
    await page.locator("[data-reason]").evaluateAll(
      (controls) => controls.every((control) => control.disabled),
    ),
    true,
  );
  for (const selector of [
    "[data-review-note]",
    "[data-save-review]",
    "[data-previous]",
    "[data-next]",
  ]) {
    assert.equal(await page.locator(selector).isDisabled(), true, selector);
  }

  await page.locator("[data-detail-dialog]").focus();
  await page.keyboard.press("3");
  await page.keyboard.press("ArrowRight");
  assert.equal(
    await page.locator("[data-detail-dialog]").getAttribute(
      "data-active-image-id",
    ),
    "B001-001",
  );
  assert.equal(
    await page.locator(
      "[data-review-status-button='keep']",
    ).getAttribute("aria-pressed"),
    "true",
  );
  assert.equal(
    await page.locator("[data-review-note]").inputValue(),
    "submitted draft",
  );

  releaseSave();
  await page.waitForSelector(
    '[data-image-id="B001-001"][data-review-status="keep"]',
  );
  const saved = await page.evaluate(() =>
    fetch("/api/batches/B001/reviews").then((response) => response.json())
  );
  assert.equal(saved.data.reviews["B001-001"].note, "submitted draft");
});

test("the latest batch selection wins over an earlier slow load", async (t) => {
  const { page } = await openBrowserFixture(t, {
    width: 1280,
    height: 800,
  }, {
    additionalBatchIds: ["B002"],
  });
  let releaseB002;
  const b002Gate = new Promise((resolve) => {
    releaseB002 = resolve;
  });
  let startedCount = 0;
  let markBothStarted;
  const bothStarted = new Promise((resolve) => {
    markBothStarted = resolve;
  });
  let completedCount = 0;
  let markBothCompleted;
  const bothCompleted = new Promise((resolve) => {
    markBothCompleted = resolve;
  });
  const delayB002 = async (route) => {
    startedCount += 1;
    if (startedCount === 2) markBothStarted();
    await b002Gate;
    const response = await route.fetch();
    await route.fulfill({ response });
    completedCount += 1;
    if (completedCount === 2) markBothCompleted();
  };
  await page.route("**/api/batches/B002", delayB002);
  await page.route("**/api/batches/B002/reviews", delayB002);

  await page.locator("[data-batch-filter]").selectOption("B002");
  await bothStarted;
  await page.locator("[data-batch-filter]").selectOption("B001");
  await page.waitForSelector("[data-image-id='B001-001']");

  releaseB002();
  await bothCompleted;
  await page.evaluate(() =>
    new Promise((resolve) =>
      requestAnimationFrame(() => requestAnimationFrame(resolve))
    )
  );
  assert.equal(await page.locator("[data-batch-filter]").inputValue(), "B001");
  assert.equal(await page.locator("[data-image-id]").count(), 50);
  assert.equal(await page.locator("[data-image-id^='B002-']").count(), 0);
  assert.equal(await page.locator("[data-image-id='B001-001']").count(), 1);
});

test("a successful save closes detail when the active status filter removes it", async (t) => {
  const { page } = await openBrowserFixture(t, {
    width: 1280,
    height: 800,
  });
  await page.locator("[data-status-filter]").selectOption("unreviewed");
  await page.locator("[data-image-id='B001-001']").click();
  await page.locator("[data-review-note]").fill("saved before filter removal");
  await page.locator("[data-review-status-button='keep']").click();
  await page.locator("[data-save-review]").click();
  await page.waitForFunction(
    () => document.querySelector("[data-progress]").textContent === "1 / 50",
  );

  assert.equal(
    await page.locator("[data-detail-dialog]").evaluate((dialog) => dialog.open),
    false,
  );
  assert.equal(await page.locator("[data-image-id]").count(), 49);
  assert.equal(await page.locator("[data-image-id='B001-001']").count(), 0);

  const saved = await page.evaluate(() =>
    fetch("/api/batches/B001/reviews").then((response) => response.json())
  );
  assert.equal(
    saved.data.reviews["B001-001"].note,
    "saved before filter removal",
  );
  await page.locator("[data-image-id='B001-002']").click();
  assert.equal(
    await page.locator("[data-save-review]").textContent(),
    "Save review",
  );
});
