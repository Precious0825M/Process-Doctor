import React from 'react';
import { Button, Tag } from '@carbon/react';
import { ArrowRight } from '@carbon/icons-react';
import MetricCard from '../components/MetricCard';
import WorkflowGraph from '../components/WorkflowGraph';
import {
  CURRENT_WORKFLOW,
  OPTIMIZED_WORKFLOW,
  CURRENT_METRICS,
  OPTIMIZED_METRICS,
} from '../data/demo-data';

interface PrescribeSectionProps {
  onApprove: () => void;
}

/**
 * PHASE 3 - PRESCRIBE
 * Side-by-side before/after view. The numbers tell the story.
 */
const PrescribeSection: React.FC<PrescribeSectionProps> = ({ onApprove }) => {
  const timeReduction = Math.round(
    ((CURRENT_METRICS.cycleTime - OPTIMIZED_METRICS.cycleTime) / CURRENT_METRICS.cycleTime) * 100
  );
  const minutesSaved = CURRENT_METRICS.cycleTime - OPTIMIZED_METRICS.cycleTime;
  const hoursSavedPerWeek = Math.round((minutesSaved * CURRENT_METRICS.runsPerWeek) / 60);

  return (
    <section style={{ paddingTop: 'var(--pd-space-07)' }}>
      <div style={{ marginBottom: 'var(--pd-space-07)' }}>
        <Tag type="green">Estimated {timeReduction}% time reduction</Tag>
        <h2 style={{ marginTop: 'var(--pd-space-04)', marginBottom: 'var(--pd-space-03)' }}>
          Prescription: an optimized pipeline
        </h2>
        <p className="pd-text-secondary">
          IBM Granite restructured your workflow to parallelize tests, eliminate manual approvals, and cache dependencies.
        </p>
      </div>

      {/* Before / After comparison */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))',
          gap: 'var(--pd-space-06)',
          marginBottom: 'var(--pd-space-08)',
        }}
      >
        {/* BEFORE */}
        <section
          aria-label="Current workflow"
          style={{
            padding: 'var(--pd-space-06)',
            background: 'var(--pd-color-error-subtle)',
            border: '1px solid var(--pd-color-error-border)',
            borderRadius: 'var(--pd-radius-sm)',
          }}
        >
          <div
            style={{
              fontSize: 'var(--pd-font-size-label)',
              fontWeight: 'var(--pd-font-weight-semibold)',
              color: 'var(--pd-color-error)',
              textTransform: 'uppercase',
              letterSpacing: 'var(--pd-letter-spacing-wide)',
              marginBottom: 'var(--pd-space-04)',
            }}
          >
            Before
          </div>
          <div
            style={{
              fontSize: 'var(--pd-font-size-display)',
              fontWeight: 'var(--pd-font-weight-light)',
              color: 'var(--pd-color-error)',
              fontFeatureSettings: '"tnum" 1',
              lineHeight: 1,
              marginBottom: 'var(--pd-space-02)',
            }}
          >
            {CURRENT_METRICS.cycleTime}
            <span style={{ fontSize: '0.4em', marginLeft: '0.25em', color: 'var(--pd-color-text-secondary)' }}>min</span>
          </div>
          <div className="pd-text-secondary" style={{ marginBottom: 'var(--pd-space-05)' }}>
            {CURRENT_METRICS.manualSteps} manual steps · {CURRENT_METRICS.bottlenecks} bottlenecks
          </div>
          <WorkflowGraph
            nodes={CURRENT_WORKFLOW}
            ariaLabel="Original workflow with bottlenecks"
          />
        </section>

        {/* AFTER */}
        <section
          aria-label="Optimized workflow"
          style={{
            padding: 'var(--pd-space-06)',
            background: 'var(--pd-color-success-subtle)',
            border: '1px solid var(--pd-color-success-border)',
            borderRadius: 'var(--pd-radius-sm)',
          }}
        >
          <div
            style={{
              fontSize: 'var(--pd-font-size-label)',
              fontWeight: 'var(--pd-font-weight-semibold)',
              color: 'var(--pd-color-success)',
              textTransform: 'uppercase',
              letterSpacing: 'var(--pd-letter-spacing-wide)',
              marginBottom: 'var(--pd-space-04)',
            }}
          >
            After
          </div>
          <div
            style={{
              fontSize: 'var(--pd-font-size-display)',
              fontWeight: 'var(--pd-font-weight-light)',
              color: 'var(--pd-color-success)',
              fontFeatureSettings: '"tnum" 1',
              lineHeight: 1,
              marginBottom: 'var(--pd-space-02)',
            }}
          >
            {OPTIMIZED_METRICS.cycleTime}
            <span style={{ fontSize: '0.4em', marginLeft: '0.25em', color: 'var(--pd-color-text-secondary)' }}>min</span>
          </div>
          <div className="pd-text-secondary" style={{ marginBottom: 'var(--pd-space-05)' }}>
            {OPTIMIZED_METRICS.manualSteps} manual steps · {OPTIMIZED_METRICS.bottlenecks} bottlenecks
          </div>
          <WorkflowGraph
            nodes={OPTIMIZED_WORKFLOW}
            ariaLabel="Optimized workflow with parallelized steps"
          />
        </section>
      </div>

      {/* Detailed impact metrics */}
      <h3 style={{ marginBottom: 'var(--pd-space-04)' }}>Estimated impact</h3>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: 'var(--pd-space-05)',
        }}
      >
        <MetricCard label="Time saved per run" value={minutesSaved} unit="min" variant="success" />
        <MetricCard label="Hours saved per week" value={hoursSavedPerWeek} unit="hrs" variant="success" />
        <MetricCard label="Time reduction" value={`${timeReduction}%`} variant="success" />
        <MetricCard
          label="Manual steps removed"
          value={CURRENT_METRICS.manualSteps - OPTIMIZED_METRICS.manualSteps}
          variant="success"
        />
      </div>

      <div style={{ marginTop: 'var(--pd-space-08)', display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          kind="primary"
          size="lg"
          renderIcon={ArrowRight}
          onClick={onApprove}
        >
          Review and approve treatment
        </Button>
      </div>
    </section>
  );
};

export default PrescribeSection;
