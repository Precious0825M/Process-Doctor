import React from 'react';
import { Button, Tag, Tile } from '@carbon/react';
import { ArrowRight, Warning } from '@carbon/icons-react';
import MetricCard from '../components/MetricCard';
import ReasoningPanel from '../components/ReasoningPanel';
import WorkflowGraph from '../components/WorkflowGraph';
import { CURRENT_WORKFLOW, CURRENT_METRICS, BOB_REASONING_STEPS, BOTTLENECKS } from '../data/demo-data';

interface DiagnoseSectionProps {
  inputDescription: string;
  onContinue: () => void;
}

/**
 * PHASE 2 - DIAGNOSE
 * Hero moment. Visual workflow graph + metrics + Bob reasoning + bottleneck list.
 * This is where users feel the system "thinking" through real data.
 */
const DiagnoseSection: React.FC<DiagnoseSectionProps> = ({ onContinue }) => {
  return (
    <section style={{ paddingTop: 'var(--pd-space-07)' }}>
      <div style={{ marginBottom: 'var(--pd-space-07)' }}>
        <Tag type="red" renderIcon={Warning}>3 bottlenecks identified</Tag>
        <h2 style={{ marginTop: 'var(--pd-space-04)', marginBottom: 'var(--pd-space-03)' }}>
          Diagnosis: your CI/CD pipeline
        </h2>
        <p className="pd-text-secondary">
          Bob analyzed your workflow and found three significant inefficiencies costing your team time on every commit.
        </p>
      </div>

      {/* Metrics row */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: 'var(--pd-space-05)',
          marginBottom: 'var(--pd-space-08)',
        }}
        role="region"
        aria-label="Current workflow metrics"
      >
        <MetricCard label="Cycle time" value={CURRENT_METRICS.cycleTime} unit="min" variant="alert" />
        <MetricCard label="Manual steps" value={CURRENT_METRICS.manualSteps} variant="alert" />
        <MetricCard label="Bottlenecks" value={CURRENT_METRICS.bottlenecks} variant="alert" />
        <MetricCard label="Pipeline runs / week" value={CURRENT_METRICS.runsPerWeek} />
      </div>

      {/* Workflow graph */}
      <h3 style={{ marginBottom: 'var(--pd-space-04)' }}>Current workflow</h3>
      <WorkflowGraph
        nodes={CURRENT_WORKFLOW}
        ariaLabel="Current CI/CD pipeline showing six steps with three bottlenecks"
      />

      {/* Two-column: Bob's reasoning + bottleneck list */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))',
          gap: 'var(--pd-space-06)',
          marginTop: 'var(--pd-space-07)',
        }}
      >
        <ReasoningPanel
          title="Bob's analysis"
          steps={BOB_REASONING_STEPS}
        />

        <Tile style={{ padding: 'var(--pd-space-06)' }}>
          <div
            style={{
              fontSize: 'var(--pd-font-size-label)',
              fontWeight: 'var(--pd-font-weight-semibold)',
              textTransform: 'uppercase',
              letterSpacing: 'var(--pd-letter-spacing-wide)',
              marginBottom: 'var(--pd-space-04)',
            }}
          >
            Identified bottlenecks
          </div>
          <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
            {BOTTLENECKS.map((b) => {
              const sevColor =
                b.severity === 'critical' ? 'var(--pd-color-error)' :
                b.severity === 'medium' ? 'var(--pd-color-warning)' :
                'var(--pd-color-text-tertiary)';
              return (
                <li
                  key={b.id}
                  style={{
                    padding: 'var(--pd-space-04) 0',
                    borderBottom: '1px solid var(--pd-color-border-subtle)',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 'var(--pd-space-03)' }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 'var(--pd-font-weight-medium)', marginBottom: 'var(--pd-space-02)' }}>
                        <span aria-hidden="true" style={{ color: sevColor, marginRight: '0.5em' }}>●</span>
                        {b.label}
                      </div>
                      <div style={{ fontSize: 'var(--pd-font-size-label)', color: 'var(--pd-color-text-secondary)' }}>
                        Impact: {b.impact}
                      </div>
                      <div style={{ fontSize: 'var(--pd-font-size-label)', color: 'var(--pd-color-text-secondary)', marginTop: 'var(--pd-space-02)' }}>
                        Fix: {b.fix}
                      </div>
                    </div>
                    <Tag
                      type={b.severity === 'critical' ? 'red' : b.severity === 'medium' ? 'magenta' : 'gray'}
                      size="sm"
                    >
                      <span className="pd-sr-only">Severity: </span>
                      {b.severity}
                    </Tag>
                  </div>
                </li>
              );
            })}
          </ul>
        </Tile>
      </div>

      <div style={{ marginTop: 'var(--pd-space-08)', display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          kind="primary"
          size="lg"
          renderIcon={ArrowRight}
          onClick={onContinue}
        >
          See prescription
        </Button>
      </div>
    </section>
  );
};

export default DiagnoseSection;
