const REJECT_REASONS = [
  "identity-drift",
  "age-drift",
  "not-cute",
  "duplicate",
  "anatomy",
  "hands",
  "composition",
  "garment",
  "artifact",
  "skin-flat",
  "skin-plastic",
  "compression-missing",
  "compression-excessive",
  "sock-painted-on",
  "tissue-anatomy",
  "fabric-texture-weak",
];

const state = {
  batches: [],
  batch: null,
  reviews: null,
  visibleEntries: [],
  activeIndex: -1,
  saving: false,
  activeEntryId: null,
  drafts: new Map(),
  unavailableMedia: new Set(),
  saveError: "",
  loadGeneration: 0,
  filters: {
    lane: "all",
    status: "all",
    texture: "all",
    reason: "all",
  },
};

const elements = {
  batchFilter: document.querySelector("[data-batch-filter]"),
  laneFilter: document.querySelector("[data-lane-filter]"),
  statusFilter: document.querySelector("[data-status-filter]"),
  textureFilter: document.querySelector("[data-texture-filter]"),
  reasonFilter: document.querySelector("[data-reason-filter]"),
  progress: document.querySelector("[data-progress]"),
  readiness: document.querySelector("[data-readiness]"),
  grid: document.querySelector("[data-review-grid]"),
  loadError: document.querySelector("[data-load-error]"),
  dialog: document.querySelector("[data-detail-dialog]"),
  detailImage: document.querySelector("[data-detail-image]"),
  detailCaption: document.querySelector("[data-detail-caption]"),
  reviewControls: document.querySelector("[data-review-controls]"),
  reasonControls: document.querySelector("[data-reason-controls]"),
  note: document.querySelector("[data-review-note]"),
  save: document.querySelector("[data-save-review]"),
  saveError: document.querySelector("[data-save-error]"),
};

function option(value, label, { disabled = false } = {}) {
  const item = document.createElement("option");
  item.value = value;
  item.textContent = label;
  item.disabled = disabled;
  return item;
}

function replaceOptions(select, options, selected = "all") {
  select.replaceChildren(...options);
  select.value = selected;
}

async function requestJson(path, options) {
  const response = await fetch(path, options);
  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error(`Request failed (${response.status})`);
  }
  if (!response.ok) {
    throw new Error(payload.error?.message ?? `Request failed (${response.status})`);
  }
  return payload.data;
}

function reviewFor(entry) {
  return state.reviews.reviews[entry.id];
}

function draftFor(entry) {
  let draft = state.drafts.get(entry.id);
  if (draft === undefined) {
    const review = reviewFor(entry);
    draft = {
      status: review.status,
      reasons: [...review.reasons],
      note: review.note,
    };
    state.drafts.set(entry.id, draft);
  }
  return draft;
}

function activeEntry() {
  return state.visibleEntries[state.activeIndex] ?? null;
}

function syncDraftNote() {
  const entry = activeEntry();
  if (entry === null || !elements.dialog.open) return;
  draftFor(entry).note = elements.note.value;
}

function applyFilters() {
  if (state.batch === null || state.reviews === null) {
    state.visibleEntries = [];
    state.activeIndex = -1;
    return;
  }
  state.visibleEntries = state.batch.entries.filter((entry) => {
    const review = reviewFor(entry);
    return (
      (state.filters.lane === "all" || entry.lane === state.filters.lane) &&
      (state.filters.status === "all" ||
        review.status === state.filters.status) &&
      (state.filters.texture === "all" ||
        (state.filters.texture === "texture") === entry.textureFocus) &&
      (state.filters.reason === "all" ||
        review.reasons.includes(state.filters.reason))
    );
  });
  const activeIndex = state.visibleEntries.findIndex(
    ({ id }) => id === state.activeEntryId,
  );
  state.activeIndex = activeIndex;
}

function markMediaUnavailable(card, entry) {
  state.unavailableMedia.add(entry.id);
  card.disabled = true;
  card.dataset.mediaUnavailable = "true";
  const message = document.createElement("span");
  message.className = "media-unavailable";
  message.textContent = "Media unavailable";
  const copy = card.querySelector(".card-copy");
  card.replaceChildren(message);
  if (copy !== null) card.append(copy);
}

function makeCard(entry) {
  const review = reviewFor(entry);
  const card = document.createElement("button");
  card.type = "button";
  card.className = "review-card";
  card.dataset.imageId = entry.id;
  card.dataset.reviewStatus = review.status;
  card.dataset.reviewReasons = review.reasons.join(" ");
  card.dataset.mediaUnavailable = String(
    state.unavailableMedia.has(entry.id),
  );
  card.setAttribute(
    "aria-label",
    `${entry.id}, ${entry.lane}, ${review.status}`,
  );

  const copy = document.createElement("span");
  copy.className = "card-copy";
  const id = document.createElement("strong");
  id.textContent = entry.id;
  const lane = document.createElement("small");
  lane.textContent = entry.lane;
  copy.append(id, lane);

  if (state.unavailableMedia.has(entry.id)) {
    card.disabled = true;
    const unavailable = document.createElement("span");
    unavailable.className = "media-unavailable";
    unavailable.textContent = "Media unavailable";
    card.append(unavailable, copy);
    return card;
  }

  const image = document.createElement("img");
  image.loading = "lazy";
  image.alt = `${entry.id} review thumbnail`;
  image.src =
    `/media/${encodeURIComponent(state.batch.batchId)}/${encodeURIComponent(entry.id)}/thumb`;
  image.addEventListener("error", () => markMediaUnavailable(card, entry), {
    once: true,
  });
  card.append(image, copy);
  card.addEventListener("click", () => openDetail(entry.id));
  return card;
}

function renderCards() {
  elements.grid.replaceChildren(...state.visibleEntries.map(makeCard));
}

function renderProgress() {
  if (state.batch === null || state.reviews === null) {
    elements.progress.textContent = "0 / 0";
    elements.readiness.textContent = "";
    elements.readiness.hidden = true;
    return;
  }
  const records = Object.values(state.reviews.reviews);
  const reviewed = records.filter(
    ({ status }) => status !== "unreviewed",
  ).length;
  elements.progress.textContent = `${reviewed} / ${records.length}`;
  const ready =
    records.length === state.batch.entries.length &&
    records.every(({ status }) => status !== "unreviewed");
  elements.readiness.textContent = ready ? "Ready for next batch" : "";
  elements.readiness.hidden = !ready;
}

function statusButton(status, label, draft) {
  const button = document.createElement("button");
  button.type = "button";
  button.dataset.reviewStatusButton = status;
  button.textContent = label;
  button.setAttribute("aria-pressed", String(draft.status === status));
  button.addEventListener("click", () => {
    draft.status = status;
    if (status !== "reject") draft.reasons = [];
    renderDetail();
  });
  return button;
}

function reasonButton(reason, draft) {
  const button = document.createElement("button");
  button.type = "button";
  button.dataset.reason = reason;
  button.textContent = reason;
  button.setAttribute(
    "aria-pressed",
    String(draft.reasons.includes(reason)),
  );
  button.addEventListener("click", () => {
    const selected = new Set(draft.reasons);
    if (selected.has(reason)) selected.delete(reason);
    else selected.add(reason);
    draft.reasons = [...selected];
    renderDetail();
  });
  return button;
}

function renderDetail() {
  const entry = activeEntry();
  if (entry === null || !elements.dialog.open) return;
  const draft = draftFor(entry);
  elements.dialog.dataset.activeImageId = entry.id;
  elements.detailCaption.textContent =
    `${entry.id} · ${entry.lane} · ${entry.prompt}`;
  elements.detailImage.alt = `${entry.id} full review image`;
  elements.detailImage.src =
    `/media/${encodeURIComponent(state.batch.batchId)}/${encodeURIComponent(entry.id)}/image`;
  elements.reviewControls.replaceChildren(
    statusButton("reject", "1 · Reject", draft),
    statusButton("keep", "2 · Keep", draft),
    statusButton("favorite", "3 · Favorite", draft),
  );
  elements.reasonControls.replaceChildren(
    ...REJECT_REASONS.map((reason) => reasonButton(reason, draft)),
  );
  elements.reasonControls.hidden = draft.status !== "reject";
  elements.note.value = draft.note;
  elements.save.disabled = state.saving || draft.status === "unreviewed";
  elements.save.textContent = state.saving ? "Saving…" : "Save review";
  elements.saveError.textContent = state.saveError;
}

function closeDetail() {
  if (elements.dialog.open) elements.dialog.close();
  elements.detailImage.removeAttribute("src");
  state.activeIndex = -1;
  state.activeEntryId = null;
}

function render() {
  applyFilters();
  if (elements.dialog.open && state.activeIndex === -1) closeDetail();
  renderCards();
  renderProgress();
  renderDetail();
}

function openDetail(imageId) {
  state.activeEntryId = imageId;
  state.activeIndex = state.visibleEntries.findIndex(({ id }) => id === imageId);
  if (!elements.dialog.open) elements.dialog.showModal();
  renderDetail();
  elements.dialog.focus();
}

function navigateDetail(offset) {
  if (state.visibleEntries.length === 0) return;
  syncDraftNote();
  const nextIndex =
    (state.activeIndex + offset + state.visibleEntries.length) %
    state.visibleEntries.length;
  state.activeIndex = nextIndex;
  state.activeEntryId = state.visibleEntries[nextIndex].id;
  renderDetail();
  elements.dialog.focus();
}

async function saveActiveReview() {
  if (state.saving) return;
  const entry = activeEntry();
  if (entry === null) return;
  syncDraftNote();
  const draft = draftFor(entry);
  const current = reviewFor(entry);
  const batch = state.batch;
  const reviews = state.reviews;
  const drafts = state.drafts;
  const ownsActiveState = () =>
    state.batch === batch && state.reviews === reviews;
  state.saving = true;
  renderDetail();
  try {
    const updated = await requestJson(
      `/api/batches/${encodeURIComponent(batch.batchId)}/reviews/${encodeURIComponent(entry.id)}`,
      {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          expectedRevision: current.revision,
          status: draft.status,
          reasons: draft.status === "reject" ? draft.reasons : [],
          note: draft.note.trim(),
        }),
      },
    );
    if (!ownsActiveState()) return;
    reviews.reviews[entry.id] = updated;
    drafts.set(entry.id, {
      status: updated.status,
      reasons: [...updated.reasons],
      note: updated.note,
    });
    state.saveError = "";
  } catch (error) {
    if (ownsActiveState()) {
      state.saveError = `Save failed: ${error.message}`;
    }
  } finally {
    if (ownsActiveState()) {
      state.saving = false;
      render();
    }
  }
}

function configureFilters() {
  const lanes = [...new Set(state.batch.entries.map(({ lane }) => lane))];
  replaceOptions(elements.laneFilter, [
    option("all", "All lanes"),
    ...lanes.map((lane) => option(lane, lane)),
  ]);
  replaceOptions(elements.statusFilter, [
    option("all", "All statuses"),
    option("unreviewed", "Unreviewed"),
    option("reject", "Reject"),
    option("keep", "Keep"),
    option("favorite", "Favorite"),
  ]);
  replaceOptions(elements.textureFilter, [
    option("all", "All texture states"),
    option("texture", "Texture focus"),
    option("standard", "Not texture focus"),
  ]);
  replaceOptions(elements.reasonFilter, [
    option("all", "All reject reasons"),
    ...REJECT_REASONS.map((reason) => option(reason, reason)),
  ]);
  state.filters = {
    lane: "all",
    status: "all",
    texture: "all",
    reason: "all",
  };
}

async function loadBatch(batchId) {
  const generation = state.loadGeneration + 1;
  state.loadGeneration = generation;
  elements.loadError.textContent = "";
  state.batch = null;
  state.reviews = null;
  state.visibleEntries = [];
  state.activeIndex = -1;
  state.activeEntryId = null;
  state.drafts = new Map();
  state.unavailableMedia = new Set();
  state.saveError = "";
  state.saving = false;
  render();
  try {
    const [batch, reviews] = await Promise.all([
      requestJson(`/api/batches/${encodeURIComponent(batchId)}`),
      requestJson(`/api/batches/${encodeURIComponent(batchId)}/reviews`),
    ]);
    if (generation !== state.loadGeneration) return;
    state.batch = batch;
    state.reviews = reviews;
    configureFilters();
    render();
  } catch (error) {
    if (generation !== state.loadGeneration) return;
    elements.loadError.textContent = `Unable to load batch: ${error.message}`;
  }
}

async function initialize() {
  try {
    const listing = await requestJson("/api/batches");
    state.batches = listing.batches;
    replaceOptions(
      elements.batchFilter,
      state.batches.map((batch) =>
        option(
          batch.batchId,
          batch.disabled
            ? `${batch.batchId} · unavailable`
            : `${batch.batchId} · ${batch.reviewed}/${batch.total}`,
          { disabled: batch.disabled },
        )
      ),
      state.batches.find((batch) => !batch.disabled)?.batchId,
    );
    const firstBatch = state.batches.find((batch) => !batch.disabled);
    if (firstBatch === undefined) {
      elements.loadError.textContent = "No review batches are available.";
      return;
    }
    await loadBatch(firstBatch.batchId);
  } catch (error) {
    elements.loadError.textContent = `Unable to load batches: ${error.message}`;
  }
}

elements.batchFilter.addEventListener("change", () =>
  loadBatch(elements.batchFilter.value)
);

for (const [select, filter] of [
  [elements.laneFilter, "lane"],
  [elements.statusFilter, "status"],
  [elements.textureFilter, "texture"],
  [elements.reasonFilter, "reason"],
]) {
  select.addEventListener("change", () => {
    syncDraftNote();
    state.filters[filter] = select.value;
    render();
  });
}

document.querySelector("[data-close]").addEventListener("click", () => {
  syncDraftNote();
  closeDetail();
});
document.querySelector("[data-previous]").addEventListener(
  "click",
  () => navigateDetail(-1),
);
document.querySelector("[data-next]").addEventListener(
  "click",
  () => navigateDetail(1),
);
elements.note.addEventListener("input", syncDraftNote);
elements.save.addEventListener("click", saveActiveReview);

document.addEventListener("keydown", async (event) => {
  if (!elements.dialog.open) return;
  const target = event.target;
  if (
    target instanceof HTMLElement &&
    (target.matches("button, input, select, textarea") ||
      target.isContentEditable)
  ) {
    return;
  }
  if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    navigateDetail(event.key === "ArrowLeft" ? -1 : 1);
    return;
  }
  const status = {
    "1": "reject",
    "2": "keep",
    "3": "favorite",
  }[event.key];
  if (status === undefined) return;
  event.preventDefault();
  const entry = activeEntry();
  if (entry === null) return;
  const draft = draftFor(entry);
  draft.status = status;
  if (status !== "reject") draft.reasons = [];
  await saveActiveReview();
});

elements.dialog.addEventListener("cancel", (event) => {
  event.preventDefault();
  syncDraftNote();
  closeDetail();
});

initialize();
