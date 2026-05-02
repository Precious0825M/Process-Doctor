# ProcessDoctor — Frontend Project Setup

**Owner:** Adetutu (Tutu) Adenusi, UX Coordinator
**Team:** Just Ship It | IBM Bob Dev Day Hackathon | May 3, 2026

This is the React + TypeScript scaffolding for ProcessDoctor's frontend. It is pre-wired with the IBM Carbon Design System and the IBM-aligned global stylesheet. Engineers should be able to clone this, run `npm install`, and start building screens immediately.

---

## Why Carbon

Carbon is IBM's open-source React component library. We use it for three reasons:

1. **Accessibility-compliant out of the box** — every Carbon component meets WCAG 2.1 AA. We do not have to re-implement focus states, ARIA labels, or keyboard handling.
2. **Visual fidelity to IBM's ecosystem** — using Carbon makes ProcessDoctor look like a real IBM product to judges. This is a free differentiator.
3. **Speed** — buttons, forms, modals, tables, and dropdowns are pre-built. We do not waste hackathon hours on standard components.

Documentation: <https://carbondesignsystem.com/developing/frameworks/react/>

---

## Setup

```bash
npm install
npm start
```

The app runs at <http://localhost:3000>.

---

## File Structure

```
src/
├── styles/
│   └── global.css            # IBM-aligned design tokens (single source of truth)
├── components/
│   ├── StageIndicator.tsx    # Diagnose → Prescribe → Treat header
│   ├── MetricCard.tsx        # Numerical KPI cards
│   ├── ReasoningPanel.tsx    # "Bob is thinking" panel
│   └── WorkflowGraph.tsx     # Visual workflow nodes
├── screens/
│   ├── LandingScreen.tsx     # Screen 1
│   ├── InputScreen.tsx       # Screen 2
│   ├── DiagnoseScreen.tsx    # Screen 3 (hero moment)
│   ├── PrescribeScreen.tsx   # Screen 4 (before/after)
│   └── TreatScreen.tsx       # Screen 5 (PR creation)
├── data/
│   └── demo-data.ts          # Pre-canned demo data (no Bobcoins burned)
├── App.tsx
└── index.tsx
```

---

## Stylesheet Order (CRITICAL)

In `src/index.tsx`, import stylesheets in this exact order:

```tsx
import '@carbon/styles/css/styles.css';   // 1. Carbon defaults first
import './styles/global.css';              // 2. Our tokens override
import './index.tsx';
```

If you import `global.css` first, Carbon will override our tokens. Always Carbon first, ours second.

---

## Component Imports

Use the named imports from `@carbon/react`:

```tsx
import { Button, TextInput, Modal, DataTable, Tag } from '@carbon/react';
import { ArrowRight, Warning, CheckmarkFilled } from '@carbon/icons-react';
```

Do not pull in third-party UI libraries. Carbon covers everything we need.

---

## Working with the Design Tokens

Reference tokens via CSS custom properties, never hard-coded values.

```tsx
// ❌ Wrong
<div style={{ color: '#0F62FE', padding: '16px' }}>...</div>

// ✅ Right
<div style={{ color: 'var(--pd-color-primary)', padding: 'var(--pd-space-05)' }}>...</div>

// ✅ Better — use a CSS class
<div className="pd-metric">...</div>
```

This guarantees consistency across the app and makes design changes one-line.

---

## Demo Data

For testing and demo prep, use the pre-canned data in `src/data/demo-data.ts`. This is calibrated demo input that produces predictable, judge-ready output. **Do not burn Bobcoins re-running Bob for inputs we have already validated.**

---

## Accessibility

Reference `docs/accessibility-checklist.md` before submitting. Every screen must pass the checklist. WCAG 2.1 AA is non-negotiable — IBM is an accessibility leader and judges will notice if we miss this.

---

## Questions

Ping me (Tutu) on Slack. I am the UX owner.
