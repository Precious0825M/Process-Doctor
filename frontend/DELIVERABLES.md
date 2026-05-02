# ProcessDoctor — UX Deliverables Summary

**Owner:** Adetutu (Tutu) Adenusi, UX Coordinator
**Hackathon:** IBM Bob Dev Day | May 3, 2026
**Architecture:** Single-page dashboard (Carbon Design System)

This is the index of everything in this package. Five deliverables, all UX scope, ready to hand to engineering.

---

## What's in here

### 1. Global stylesheet with IBM-aligned tokens
**File:** `src/styles/global.css`
- Color tokens (IBM Blue, semantic status colors, surfaces)
- Typography tokens (IBM Plex Sans, Carbon type scale)
- Spacing tokens (8px base grid, Carbon spacing scale)
- Custom component classes for stage indicators, metric cards, workflow nodes, reasoning panels
- Accessibility built in: focus rings, skip links, reduced-motion support, sr-only utilities

### 2. Dashboard wireframes (built as React code)
**Files:** `src/App.tsx` + `src/sections/*.tsx`
- `DashboardHeader.tsx` — persistent brand header
- `InputSection.tsx` — Phase 1: workflow description or GitHub URL
- `DiagnoseSection.tsx` — Phase 2: bottlenecks + Bob reasoning (the hero moment)
- `PrescribeSection.tsx` — Phase 3: before/after with impact metrics
- `TreatSection.tsx` — Phase 4: artifact preview, approval gate, success state

Single-page dashboard architecture with progressive phase reveal via Carbon Tabs. Faster to build than five separate screens; keeps the diagnose → prescribe → treat narrative.

### 3. Carbon Design System setup
**Files:** `package.json`, `src/index.tsx`, `tsconfig.json`, `public/index.html`
- React + TypeScript scaffolding
- Carbon Design System wired up with correct stylesheet ordering
- IBM Plex font family loaded
- All Carbon components imported in the section files: Button, TextArea, TextInput, ContentSwitcher, Switch, Tag, Tile, Modal, Tabs, CodeSnippet
- Custom components ready to import: MetricCard, ReasoningPanel, WorkflowGraph, StageIndicator

### 4. Accessibility checklist
**File:** `docs/accessibility-checklist.md`
- Pre-submission WCAG 2.1 AA checklist
- Specific to ProcessDoctor's screens and components
- Pre-demo smoke test sequence
- Why accessibility is a competitive judging advantage, not just compliance

### 5. Demo data
**File:** `src/data/demo-data.ts`
- Pre-canned example prompts for the input section
- Current workflow nodes (with bottlenecks) and metrics
- Optimized workflow nodes and metrics (40 min → 13 min, 67% reduction)
- Bob's multi-step reasoning text
- Identified bottlenecks with severity and fixes
- Generated GitHub Actions YAML
- Pull request details for the success state

Engineers swap `import from '../data/demo-data'` for `import from '../api/bob'` when wiring real Bob calls. Bobcoins stay reserved for real usage.

---

## How engineers run it

```bash
npm install
npm start
```

App runs at `http://localhost:3000`. The full demo flow works end-to-end with simulated data — no backend needed for design review or demo prep.

---

## What engineers still need to build

UX scope is complete. Engineering scope:
- Wire Bob API calls in `DiagnoseSection` (replace demo-data imports with real API)
- Wire Granite API calls in `PrescribeSection`
- Wire watsonx Orchestrate in `TreatSection.handleConfirm()` (currently a setTimeout)
- Backend FastAPI routes per architecture doc
- GitHub repo parsing logic

The UI does not need to change for any of this. Engineers replace data sources, the visual layer stays.

---

## Documentation

- `README.md` — project setup and conventions
- `docs/wireframes.md` — full visual specifications for every section, plus the demo flow choreography (what the presenter says at each timestamp)
- `docs/accessibility-checklist.md` — pre-submission compliance checklist

---

## Design decisions on the record

**Single dashboard, not five screens.** Faster to build, fewer transitions to break, narrative still works through phase tabs.

**IBM Plex Sans + IBM Blue + Carbon.** Free judging-fit signal. We use IBM's actual brand assets, not custom fonts or off-brand colors. This is the competitive advantage other teams will miss.

**Demo data calibrated to land cleanly.** 40 min → 13 min = 67% reduction (within our success metric range). 14 hours saved per week. Zero manual steps. Numbers are believable AND impactful.

**Approval gate is non-negotiable.** Modal confirmation before any "real system change." This is our human-in-the-loop differentiator and answers the agent-value question.

**Accessibility is in scope, not a stretch goal.** WCAG 2.1 AA. Carbon handles most of it for free. We hit the rest via the checklist.

---

If anything is unclear, ping me on Slack. — Tutu
