import React, { useEffect, useState } from 'react';
import { Button, Tag, Loading } from '@carbon/react';
import { ArrowRight } from '@carbon/icons-react';
import MetricCard from '../components/MetricCard';
import { api, AnalyzeResponse, FixResponse } from '../services/api';

interface PrescribeSectionProps {
  onApprove: () => void;
  analysisData: AnalyzeResponse | null;
  onFixComplete: (data: FixResponse) => void;
  fixData: FixResponse | null;
}

/**
 * PHASE 3 - PRESCRIBE
 * Side-by-side before/after view. The numbers tell the story.
 */
const PrescribeSection: React.FC<PrescribeSectionProps> = ({
  onApprove,
  analysisData,
  onFixComplete,
  fixData
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Only generate fix if we have analysis data but no fix data yet
    if (analysisData && !fixData) {
      generateFix();
    }
  }, [analysisData]);

  const generateFix = async () => {
    if (!analysisData) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.generateFix({
        analysis_id: analysisData.analysis_id,
        optimization_strategy: 'balanced',
      });
      
      onFixComplete(result);
    } catch (err: any) {
      setError(err.message || 'Failed to generate optimization');
      console.error('Fix generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <section style={{ paddingTop: 'var(--pd-space-07)', textAlign: 'center' }}>
        <Loading description="Generating optimization..." withOverlay={false} />
        <h2 style={{ marginTop: 'var(--pd-space-06)' }}>Bob is optimizing your workflow...</h2>
        <p className="pd-text-secondary" style={{ marginTop: 'var(--pd-space-03)' }}>
          Generating an optimized pipeline based on the identified bottlenecks.
        </p>
      </section>
    );
  }

  if (error) {
    return (
      <section style={{ paddingTop: 'var(--pd-space-07)' }}>
        <Tag type="red">Optimization failed</Tag>
        <h2 style={{ marginTop: 'var(--pd-space-04)' }}>Unable to generate optimization</h2>
        <p className="pd-text-secondary" style={{ marginTop: 'var(--pd-space-03)' }}>
          {error}
        </p>
        <Button
          kind="primary"
          onClick={generateFix}
          style={{ marginTop: 'var(--pd-space-06)' }}
        >
          Retry optimization
        </Button>
      </section>
    );
  }

  // Use only real API data
  if (!fixData) {
    return null; // Should never happen as loading/error states are handled above
  }

  const timeReduction = fixData.improvements?.efficiency_gain
    ? parseInt(fixData.improvements.efficiency_gain)
    : 0;
  
  const timeSaved = fixData.improvements?.time_saved || 'Unknown';
  const optimizationsApplied = fixData.improvements?.optimizations_applied || 0;

  return (
    <section style={{ paddingTop: 'var(--pd-space-07)' }}>
      <div style={{ marginBottom: 'var(--pd-space-07)' }}>
        <Tag type="green">{timeReduction}% improvement</Tag>
        <h2 style={{ marginTop: 'var(--pd-space-04)', marginBottom: 'var(--pd-space-03)' }}>
          Optimized Workflow Generated
        </h2>
        <p className="pd-text-secondary">
          {optimizationsApplied} optimization{optimizationsApplied !== 1 ? 's' : ''} applied to improve your workflow efficiency.
        </p>
      </div>

      {/* Changes applied */}
      <h3 style={{ marginBottom: 'var(--pd-space-04)' }}>Changes Applied</h3>
      <div style={{ marginBottom: 'var(--pd-space-08)' }}>
        {fixData.changes && fixData.changes.length > 0 ? (
          <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
            {fixData.changes.map((change, idx) => (
              <li
                key={idx}
                style={{
                  padding: 'var(--pd-space-04)',
                  marginBottom: 'var(--pd-space-03)',
                  background: 'var(--pd-color-success-subtle)',
                  border: '1px solid var(--pd-color-success-border)',
                  borderRadius: 'var(--pd-radius-sm)',
                }}
              >
                <div style={{ fontWeight: 'var(--pd-font-weight-medium)', marginBottom: 'var(--pd-space-02)' }}>
                  {change.type || 'Optimization'}
                </div>
                <div style={{ color: 'var(--pd-color-text-secondary)' }}>
                  {change.description}
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="pd-text-secondary">No specific changes documented.</p>
        )}
      </div>

      {/* Impact metrics */}
      <h3 style={{ marginBottom: 'var(--pd-space-04)' }}>Estimated Impact</h3>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: 'var(--pd-space-05)',
        }}
      >
        <MetricCard label="Time Saved" value={timeSaved} variant="success" />
        <MetricCard label="Efficiency Gain" value={`${timeReduction}%`} variant="success" />
        <MetricCard label="Optimizations Applied" value={optimizationsApplied} variant="success" />
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
