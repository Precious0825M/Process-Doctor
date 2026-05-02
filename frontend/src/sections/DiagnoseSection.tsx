import React, { useEffect, useState } from 'react';
import { Button, Tag, Tile, Loading } from '@carbon/react';
import { ArrowRight, Warning } from '@carbon/icons-react';
import MetricCard from '../components/MetricCard';
import ReasoningPanel from '../components/ReasoningPanel';
import WorkflowGraph from '../components/WorkflowGraph';
import { api, AnalyzeResponse } from '../services/api';

interface DiagnoseSectionProps {
  inputDescription: string;
  inputType: 'text' | 'github';
  onContinue: () => void;
  onAnalysisComplete: (data: AnalyzeResponse) => void;
  analysisData: AnalyzeResponse | null;
}

/**
 * PHASE 2 - DIAGNOSE
 * Hero moment. Visual workflow graph + metrics + Bob reasoning + bottleneck list.
 * This is where users feel the system "thinking" through real data.
 */
const DiagnoseSection: React.FC<DiagnoseSectionProps> = ({
  inputDescription,
  inputType,
  onContinue,
  onAnalysisComplete,
  analysisData
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Only run analysis if we don't have data yet
    if (!analysisData && inputDescription) {
      analyzeWorkflow();
    }
  }, [inputDescription, inputType]);

  const analyzeWorkflow = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.analyzeWorkflow({
        workflow_input: inputDescription,
        source_type: inputType,
      });
      
      onAnalysisComplete(result);
    } catch (err: any) {
      setError(err.message || 'Failed to analyze workflow');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <section style={{ paddingTop: 'var(--pd-space-07)', textAlign: 'center' }}>
        <Loading description="Analyzing workflow..." withOverlay={false} />
        <h2 style={{ marginTop: 'var(--pd-space-06)' }}>Bob is analyzing your workflow...</h2>
        <p className="pd-text-secondary" style={{ marginTop: 'var(--pd-space-03)' }}>
          This may take a few moments as we identify bottlenecks and optimization opportunities.
        </p>
      </section>
    );
  }

  if (error) {
    return (
      <section style={{ paddingTop: 'var(--pd-space-07)' }}>
        <Tag type="red">Analysis failed</Tag>
        <h2 style={{ marginTop: 'var(--pd-space-04)' }}>Unable to analyze workflow</h2>
        <p className="pd-text-secondary" style={{ marginTop: 'var(--pd-space-03)' }}>
          {error}
        </p>
        <Button
          kind="primary"
          onClick={analyzeWorkflow}
          style={{ marginTop: 'var(--pd-space-06)' }}
        >
          Retry analysis
        </Button>
      </section>
    );
  }

  // Use only real API data - no fallbacks
  if (!analysisData) {
    return null; // Should never happen as loading/error states are handled above
  }

  const bottlenecks = analysisData.bottlenecks || [];
  const metrics = analysisData.metrics || {};
  const bottleneckCount = bottlenecks.length;

  return (
    <section style={{ paddingTop: 'var(--pd-space-07)' }}>
      <div style={{ marginBottom: 'var(--pd-space-07)' }}>
        <Tag type="red" renderIcon={Warning}>{bottleneckCount} bottleneck{bottleneckCount !== 1 ? 's' : ''} identified</Tag>
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
        <MetricCard
          label="Current Duration"
          value={metrics.current_duration || 'Unknown'}
          variant="alert"
        />
        <MetricCard
          label="Estimated Optimal"
          value={metrics.estimated_optimal || 'Unknown'}
          variant="success"
        />
        <MetricCard
          label="Efficiency Score"
          value={metrics.efficiency_score !== undefined ? `${metrics.efficiency_score}%` : 'N/A'}
          variant="alert"
        />
        <MetricCard label="Bottlenecks Found" value={bottleneckCount} variant="alert" />
      </div>

      {/* Workflow graph */}
      {/* Bottleneck list - full width */}
      <div
        style={{
          marginTop: 'var(--pd-space-07)',
        }}
      >
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
            {bottlenecks.map((b) => {
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
