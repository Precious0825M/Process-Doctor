import React from 'react';

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  delta?: { value: string; positive: boolean };
  variant?: 'default' | 'alert' | 'success';
}

/**
 * KPI display card. Used heavily on Diagnose and Prescribe screens.
 *
 * Accessibility:
 *   - Uses semantic <article> with aria-labelledby
 *   - Tabular numerals for clean value alignment (set in CSS)
 *   - Variant communicated by text content, not just color
 */
const MetricCard: React.FC<MetricCardProps> = ({ label, value, unit, delta, variant = 'default' }) => {
  const labelId = `metric-${label.toLowerCase().replace(/\s+/g, '-')}`;
  const valueClass = [
    'pd-metric__value',
    variant === 'alert'   && 'pd-metric__value--alert',
    variant === 'success' && 'pd-metric__value--success',
  ].filter(Boolean).join(' ');

  return (
    <article className="pd-metric" aria-labelledby={labelId}>
      <div id={labelId} className="pd-metric__label">{label}</div>
      <div className={valueClass}>
        {value}
        {unit && <span style={{ fontSize: '0.6em', marginLeft: '0.25em', color: 'var(--pd-color-text-secondary)' }}>{unit}</span>}
      </div>
      {delta && (
        <div className={`pd-metric__delta pd-metric__delta--${delta.positive ? 'positive' : 'negative'}`}>
          {delta.positive ? '↓' : '↑'} {delta.value}
        </div>
      )}
    </article>
  );
};

export default MetricCard;
