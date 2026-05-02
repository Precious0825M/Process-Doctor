# ProcessDoctor — Wireframe Documentation

**Owner:** Adetutu (Tutu) Adenusi, UX Coordinator
**Date:** May 2, 2026
**Architecture:** Single-page dashboard with progressive phase reveal

This document specifies the visual structure of every section in ProcessDoctor. Engineers should reference this alongside the working React code in `/src` to understand intent. Visual decisions (spacing, hierarchy, where things sit) are documented here so engineers don't have to make UX calls while debugging.

---

## Architecture Overview

ProcessDoctor is a **single-page dashboard** — not a multi-page application. Users move through four phases via tabs, but it is one continuous interface, not five separate routes.

```
┌──────────────────────────────────────────────────────────────┐
│  Header: Brand + tagline + IBM tech credit                   │
├──────────────────────────────────────────────────────────────┤
│  Phase tabs: [1. Input] [2. Diagnose] [3. Prescribe] [4. Treat] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│              ACTIVE PHASE CONTENT (changes)                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

Tabs 2-4 are disabled until the user hits "Diagnose workflow" in tab 1. This keeps the demo flow predictable and prevents users from clicking ahead before analysis runs.

---

## Phase 1: Input

**Goal:** capture the user's workflow description with minimal friction.

**Layout:**

```
┌──────────────────────────────────────────────────────────────┐
│  H2: Tell us about your workflow                             │
│  Subhead: Plain English or GitHub repo                       │
│                                                              │
│  [ Workflow description | GitHub repository ]   ← Carbon     │
│                                                ContentSwitcher│
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ TextArea (6 rows)                                    │    │
│  │ Placeholder example                                  │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  Or try one of these examples:                               │
│  [ Tag 1 ]  [ Tag 2 ]  [ Tag 3 ]  [ Tag 4 ]                  │
│                                                              │
│                                  [ Diagnose workflow → ]     │
└──────────────────────────────────────────────────────────────┘
```

**Components used:**
- Carbon `ContentSwitcher` for text vs. GitHub mode toggle
- Carbon `TextArea` (text mode) or `TextInput` (GitHub mode)
- Carbon `Tag` (clickable) for example prompts
- Carbon `Button kind="primary"` for the submit action

**Demo behavior:** clicking an example tag pre-fills the text area. The Diagnose button enables when text is at least 20 characters or the URL starts with `https://github.com/`.

**Accessibility notes:**
- ContentSwitcher provides keyboard navigation between modes (arrow keys).
- TextArea has visible label and helper text via Carbon's `labelText` and `helperText` props.
- Example tags are wrapped in real `<button>` elements with `aria-label` describing the prompt.

---

## Phase 2: Diagnose

**Goal:** the hero moment. Show users that something intelligent just analyzed their workflow.

**Layout:**

```
┌──────────────────────────────────────────────────────────────┐
│  [ red Tag: 3 bottlenecks identified ]                       │
│  H2: Diagnosis: your CI/CD pipeline                          │
│  Subhead: 3 significant inefficiencies                       │
│                                                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐               │
│  │ Cycle  │ │ Manual │ │ Bottle │ │ Runs / │   ← MetricCards │
│  │ time   │ │ steps  │ │ necks  │ │ week   │               │
│  │ 40 min │ │ 5      │ │ 3      │ │ 32     │               │
│  └────────┘ └────────┘ └────────┘ └────────┘               │
│                                                              │
│  H3: Current workflow                                        │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ [Checkout]→[Install*]→[Lint]→[Test*]→[Approval*]→...│    │
│  │  *bottleneck nodes shown in red with warning icon    │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────┐ ┌──────────────────────┐          │
│  │ Bob's analysis       │ │ Identified bottle-   │          │
│  │ (reasoning panel)    │ │ necks (severity list)│          │
│  │                      │ │                      │          │
│  │ → Step 1...          │ │ ● Critical: Install  │          │
│  │ → Step 2...          │ │ ● Critical: Tests    │          │
│  │ → Step 3...          │ │ ● Medium: Approval   │          │
│  └──────────────────────┘ └──────────────────────┘          │
│                                                              │
│                                  [ See prescription → ]      │
└──────────────────────────────────────────────────────────────┘
```

**Components used:**
- Carbon `Tag type="red"` for the bottleneck count chip
- Custom `MetricCard` (4-column grid, responsive)
- Custom `WorkflowGraph` (linear horizontal node display)
- Custom `ReasoningPanel` (left-bordered mono-font readout)
- Carbon `Tile` wrapping the bottleneck list

**Why this is the hero moment:**
- Big numbers (display font size) draw the eye to severity.
- The visual workflow graph is what makes "diagnosis" feel real, not just textual.
- Bob's reasoning panel addresses the "is this really an agent?" question — judges see multi-step reasoning explicitly.
- The bottleneck list pairs each issue with its fix, telegraphing the prescription before the user clicks through.

---

## Phase 3: Prescribe

**Goal:** show before/after with numbers that tell the impact story.

**Layout:**

```
┌──────────────────────────────────────────────────────────────┐
│  [ green Tag: Estimated 67% time reduction ]                 │
│  H2: Prescription: an optimized pipeline                     │
│  Subhead: Granite restructured your workflow                 │
│                                                              │
│  ┌──────────────────────┐ ┌──────────────────────┐          │
│  │ BEFORE (red tint)    │ │ AFTER (green tint)   │          │
│  │                      │ │                      │          │
│  │ 40 min               │ │ 13 min               │          │
│  │ 5 manual · 3 issues  │ │ 0 manual · 0 issues  │          │
│  │                      │ │                      │          │
│  │ [Workflow graph]     │ │ [Workflow graph]     │          │
│  │ (current)            │ │ (optimized)          │          │
│  └──────────────────────┘ └──────────────────────┘          │
│                                                              │
│  H3: Estimated impact                                        │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐               │
│  │ Time   │ │ Hours  │ │ Time   │ │ Manual │               │
│  │ saved  │ │ saved/ │ │ reduce │ │ steps  │               │
│  │ /run   │ │ week   │ │        │ │ removed│               │
│  │ 27 min │ │ 14 hrs │ │ 67%    │ │ 5      │               │
│  └────────┘ └────────┘ └────────┘ └────────┘               │
│                                                              │
│                          [ Review and approve treatment → ]  │
└──────────────────────────────────────────────────────────────┘
```

**Components used:**
- Carbon `Tag type="green"` for the time reduction chip
- Two side-by-side `<section>` cards with semantic color coding
- Display-size numbers (3.375rem) for cycle time on each side
- Custom `WorkflowGraph` rendered in both before and after states
- 4-column `MetricCard` grid for impact metrics

**Why side-by-side and not animated transition:**
- Side-by-side is faster to build than an animation transition.
- Side-by-side stays comparable when users reference back.
- For the demo, the visual contrast between red-tinted "before" and green-tinted "after" reads instantly.

**Demo data:** 40 min → 13 min = 67% reduction. We chose 67% to land within our success metric range (50-70%) while feeling believable. Manual steps go from 5 to 0 — full elimination — for narrative impact.

---

## Phase 4: Treat

**Goal:** show the actual generated artifact, get explicit approval, deliver a polished success state.

**Layout (review state):**

```
┌──────────────────────────────────────────────────────────────┐
│  [ blue Tag: Ready for approval ]                            │
│  H2: Treatment: generated CI/CD pipeline                     │
│  Subhead: Bob has generated the workflow                     │
│                                                              │
│  H3: Generated file: .github/workflows/ci.yml                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ name: CI                                  [Copy]     │    │
│  │ on:                                                  │    │
│  │   push: ...                                          │    │
│  │ jobs:                                                │    │
│  │   validate:                                          │    │
│  │     ...                                              │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  H3: Pull request preview                                    │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ team-just-ship-it/demo-app                           │    │
│  │ Optimize CI pipeline: parallel tests, deps cache...  │    │
│  │ ProcessDoctor diagnosed 3 bottlenecks...             │    │
│  │ [branch tag] [+42 −18] [Generated by ProcessDoctor]  │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│                          [ Cancel ] [ Approve and deploy ]   │
└──────────────────────────────────────────────────────────────┘
```

**Modal on approve:**

```
┌─────────────────────────────────────────┐
│  Approve treatment?                  [×]│
│                                         │
│  This will open a pull request in       │
│  team-just-ship-it/demo-app on branch   │
│  processdoctor/optimize-ci-pipeline.    │
│  The pipeline change does not deploy    │
│  automatically — your team must merge   │
│  the PR before the new workflow takes   │
│  effect.                                │
│                                         │
│  [ Cancel ]  [ Yes, open pull request ] │
└─────────────────────────────────────────┘
```

**Success state:**

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                          ✓                                   │
│              Pull request created                            │
│   Your team will be notified. Bob will monitor execution.    │
│                                                              │
│   ┌──────────────────────────────────────────────────────┐  │
│   │ team-just-ship-it/demo-app                           │  │
│   │ Optimize CI pipeline: parallel tests...              │  │
│   │ [PR #247 opened] [branch]                            │  │
│   └──────────────────────────────────────────────────────┘  │
│                                                              │
│              [ ↻ Diagnose another workflow ]                 │
└──────────────────────────────────────────────────────────────┘
```

**Components used:**
- Carbon `CodeSnippet type="multi"` for the YAML preview (built-in copy button, keyboard accessible)
- Carbon `Modal` for the approval gate
- Carbon `Tag` for status indicators
- Carbon icons: `CheckmarkFilled` (success), `Restart` (restart action)

**Why the approval gate is non-negotiable:**
- It's our human-in-the-loop differentiator. Judges asked "does it just suggest or does it implement?" Our answer is: "it implements, with explicit user consent."
- The modal explicitly says "does not deploy automatically." This signals enterprise trust.
- Without this gate, the product feels reckless. With it, it feels enterprise-grade.

**Simulated execution:** the approval triggers a 1.2s delay before showing the success state. In production this is the watsonx Orchestrate API call. For the demo it's a deterministic timeout so the success state lands predictably.

---

## Component Inventory

Quick reference of every component built and where it lives.

### Custom components (`/src/components`)

| Component | Purpose | Used in |
|-----------|---------|---------|
| `MetricCard` | KPI display with optional delta indicator | Diagnose, Prescribe |
| `ReasoningPanel` | Bob's multi-step reasoning readout | Diagnose |
| `WorkflowGraph` | Horizontal node-and-arrow workflow viz | Diagnose, Prescribe |
| `StageIndicator` | (Reserved — phase tabs replace this in dashboard arch) | — |

### Section components (`/src/sections`)

| Section | Phase | Purpose |
|---------|-------|---------|
| `DashboardHeader` | All | Persistent brand header |
| `InputSection` | 1 | Workflow input capture |
| `DiagnoseSection` | 2 | Workflow analysis + bottlenecks |
| `PrescribeSection` | 3 | Before/after comparison |
| `TreatSection` | 4 | Artifact preview, approval, success |

### Carbon components in use

Buttons (primary, tertiary, ghost), TextArea, TextInput, ContentSwitcher, Tag, Tile, Modal, Tabs/TabList/Tab/TabPanels/TabPanel, CodeSnippet. All from `@carbon/react`.

### Carbon icons in use

ArrowRight, ArrowLeft, Code, LogoGithub, Warning, WarningAlt, CheckmarkFilled, Restart. All from `@carbon/icons-react`.

---

## Demo Flow Choreography

For the 3-minute demo presentation. This is what the presenter narrates while clicking through.

| Time | Phase | What presenter says | What user sees |
|------|-------|---------------------|----------------|
| 0:00 | Input | "Every engineering team has broken workflows." | Landing-style header, input area |
| 0:15 | Input | Click an example prompt. "Here's a CI pipeline that takes 40 minutes." | Tag selected, text fills in |
| 0:25 | Input | "Bob, diagnose this." | Click Diagnose button |
| 0:30 | Diagnose | "In seconds, Bob analyzes the workflow and finds three bottlenecks." | Diagnose phase active, metrics + graph + bottleneck list visible |
| 0:50 | Diagnose | "This isn't a chatbot — Bob shows its multi-step reasoning." | Point to Reasoning Panel |
| 1:10 | Diagnose | Click "See prescription" | Transition to Prescribe |
| 1:15 | Prescribe | "Granite redesigns the pipeline. 40 min becomes 13 min." | Side-by-side visible |
| 1:30 | Prescribe | "67% faster. 14 hours saved per week. Zero manual steps." | Point to impact metrics |
| 1:45 | Prescribe | Click "Review and approve" | Transition to Treat |
| 1:50 | Treat | "Bob generates the actual GitHub Actions YAML." | YAML visible |
| 2:00 | Treat | "And opens a pull request — but only with explicit approval." | Click Approve, modal opens |
| 2:10 | Treat | Confirm in modal | Success state |
| 2:15 | Treat | "PR opened. Team notified. Bob monitors execution." | Success card visible |
| 2:30 | Close | Pivot to business case | Pitch deck |

**Total active demo time: 2:30. Leaves 30 seconds for pitch close on the IBM business case (consulting pull-through, Bobcoin consumption, automation segment growth).**

---

## What's NOT in scope for UX

To be clear about boundaries with the engineering team:

- **API integration** with Bob, Granite, Orchestrate — engineering owns this. UX provides the demo data file as the fallback.
- **GitHub repo parsing** — engineering owns this.
- **Real PR creation** — engineering owns this. UX simulates with the 1.2s timeout in TreatSection.
- **Backend FastAPI routes** — engineering owns this.
- **Bobcoin tracking / cost monitoring** — engineering owns this if we add it.

**UX owns** the visual layer, the demo data, the storytelling flow, the accessibility checklist, and the demo choreography document above.

---

## Files to reference alongside this doc

- `src/styles/global.css` — every design token used throughout the app
- `src/data/demo-data.ts` — all demo content (input prompts, workflow nodes, metrics, YAML, PR details, Bob reasoning)
- `docs/accessibility-checklist.md` — pre-submission accessibility checklist
- `README.md` — project setup instructions

If anything in the working code contradicts this document, the code is the source of truth and this doc is out of date. Update both when iterating.
