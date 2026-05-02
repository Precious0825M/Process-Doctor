/**
 * ============================================================================
 * ProcessDoctor — Demo Data
 * ============================================================================
 * Owner: Adetutu (Tutu) Adenusi, UX Coordinator
 *
 * Pre-canned demo data for the hackathon. Use this for development, testing,
 * and the live presentation. DO NOT burn Bobcoins re-running Bob, Granite, or
 * Orchestrate for inputs we have already validated.
 *
 * Strategy:
 *   - The team has 160 Bobcoins total (40 per member). Every avoidable Bob
 *     call drains the shared budget.
 *   - This file is the "known-good" demo path. Numbers, workflow structure,
 *     and reasoning text are calibrated to land cleanly during the 3-minute
 *     demo regardless of whether the live API call fires.
 *   - For the live demo, the Diagnose phase can call Bob in real time, but
 *     the Prescribe and Treat phases should fall back to this data on any
 *     timeout or error.
 * ============================================================================
 */

import type { WorkflowNode } from '../components/WorkflowGraph';

// ---------------------------------------------------------------------------
// EXAMPLE PROMPTS — chips shown in the input section to lower friction
// ---------------------------------------------------------------------------

export const EXAMPLE_PROMPTS: string[] = [
  'Our CI takes 40 minutes, requires manual approvals, and runs tests sequentially. Code review takes 3 days on average and our deploy pipeline has 12 manual steps.',
  'Sprint planning takes half a day every two weeks. We spend hours triaging issues and re-estimating tickets that already have estimates from last sprint.',
  'Our deployment pipeline has 12 manual steps including manual smoke tests, manual environment promotion, and a manual changelog update before production release.',
  'Code reviews block our team. PRs sit for 2-3 days waiting for reviewers, and reviewers often request changes that could have been caught by linting.',
];

// ---------------------------------------------------------------------------
// CURRENT WORKFLOW (the "before" state)
// ---------------------------------------------------------------------------

export const CURRENT_WORKFLOW: WorkflowNode[] = [
  { id: 'checkout',  label: 'Checkout',          duration: '1 min'  },
  { id: 'install',   label: 'Install deps',      duration: '8 min',  isBottleneck: true },
  { id: 'lint',      label: 'Lint',              duration: '3 min'  },
  { id: 'test',      label: 'Test (sequential)', duration: '18 min', isBottleneck: true },
  { id: 'approval',  label: 'Manual approval',   duration: '8 min',  isBottleneck: true },
  { id: 'deploy',    label: 'Deploy',            duration: '2 min'  },
];

export const CURRENT_METRICS = {
  cycleTime: 40,
  manualSteps: 5,
  bottlenecks: 3,
  runsPerWeek: 32,
};

// ---------------------------------------------------------------------------
// OPTIMIZED WORKFLOW (the "after" state)
// ---------------------------------------------------------------------------

export const OPTIMIZED_WORKFLOW: WorkflowNode[] = [
  { id: 'checkout',     label: 'Checkout',                duration: '1 min', isOptimized: true },
  { id: 'install',      label: 'Install (cached)',        duration: '2 min', isOptimized: true },
  { id: 'parallel',     label: 'Lint + Test (parallel)',  duration: '7 min', isOptimized: true },
  { id: 'auto-approve', label: 'Auto-validate',           duration: '1 min', isOptimized: true },
  { id: 'deploy',       label: 'Deploy',                  duration: '2 min', isOptimized: true },
];

export const OPTIMIZED_METRICS = {
  cycleTime: 13,
  manualSteps: 0,
  bottlenecks: 0,
  runsPerWeek: 32,
};

// ---------------------------------------------------------------------------
// BOB'S REASONING — multi-step agent reasoning for the reasoning panel
// ---------------------------------------------------------------------------

export const BOB_REASONING_STEPS: string[] = [
  'Read .github/workflows/ci.yml and project package.json to map declared workflow.',
  'Pulled last 30 days of GitHub Actions run history to measure actual step durations.',
  'Identified install_dependencies as a recurring 8-minute cost with no caching layer.',
  'Detected sequential test execution where parallel matrix execution is supported.',
  'Flagged manual approval gate as an average 8-minute wait blocking 87 percent of deploys.',
  'Cross-referenced with similar repositories — top quartile resolves these in under 12 minutes.',
  'Concluded: 3 high-impact bottlenecks, all addressable with config-only changes.',
];

// ---------------------------------------------------------------------------
// IDENTIFIED BOTTLENECKS — for the bottlenecks card
// ---------------------------------------------------------------------------

export const BOTTLENECKS = [
  {
    id: 'install',
    label: 'Dependency install (no cache)',
    severity: 'critical' as const,
    impact: '8 min per run',
    fix: 'Add npm cache to setup-node action',
  },
  {
    id: 'tests',
    label: 'Sequential test execution',
    severity: 'critical' as const,
    impact: '18 min per run',
    fix: 'Convert to parallel matrix strategy',
  },
  {
    id: 'approval',
    label: 'Manual approval gate',
    severity: 'medium' as const,
    impact: '8 min average wait',
    fix: 'Replace with automated validation',
  },
];

// ---------------------------------------------------------------------------
// GENERATED YAML — the artifact shown in the treatment section
// ---------------------------------------------------------------------------

export const GENERATED_YAML: string = `name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node with cache
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      # Parallel lint and test execution — was sequential, now matrix
      - name: Lint and test (parallel)
        run: npm run validate
        env:
          PARALLEL: true

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Auto-validate deployment criteria
        run: ./scripts/auto-validate.sh
      - name: Deploy
        run: ./scripts/deploy.sh
`;

// ---------------------------------------------------------------------------
// PR DETAILS — shown in treatment section and success state
// ---------------------------------------------------------------------------

export const PR_DETAILS = {
  repository: 'team-just-ship-it/demo-app',
  number:     247,
  title:      'Optimize CI pipeline: parallel tests, dependency cache, removed manual approval',
  branch:     'processdoctor/optimize-ci-pipeline',
  description: 'ProcessDoctor diagnosed 3 bottlenecks in the existing CI workflow. This PR implements the prescribed optimizations: dependency caching reduces install time from 8 min to 2 min, lint and test now run in parallel saving 14 min, and the manual approval gate is replaced with an automated validation step. Estimated cycle time reduction: 40 min to 13 min (67 percent).',
  additions:  42,
  deletions:  18,
};
