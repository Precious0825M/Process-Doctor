import React from 'react';

export type Stage = 'diagnose' | 'prescribe' | 'treat';

interface StageIndicatorProps {
  current: Stage;
}

const STAGES: { id: Stage; label: string }[] = [
  { id: 'diagnose',  label: 'Diagnose'  },
  { id: 'prescribe', label: 'Prescribe' },
  { id: 'treat',     label: 'Treat'     },
];

/**
 * The diagnose → prescribe → treat indicator at the top of every working screen.
 * This is one of our key UX differentiators: users always know where they are
 * in the workflow.
 *
 * Accessibility:
 *   - aria-label communicates purpose to screen readers
 *   - aria-current="step" marks the active stage
 *   - State is communicated by both color AND text label (no color-only)
 */
const StageIndicator: React.FC<StageIndicatorProps> = ({ current }) => {
  const currentIndex = STAGES.findIndex(s => s.id === current);

  return (
    <nav className="pd-stage-indicator" aria-label="Workflow progress">
      {STAGES.map((stage, idx) => {
        const isActive = idx === currentIndex;
        const isComplete = idx < currentIndex;
        const stepClass = [
          'pd-stage-indicator__step',
          isActive   && 'pd-stage-indicator__step--active',
          isComplete && 'pd-stage-indicator__step--complete',
        ].filter(Boolean).join(' ');

        const statusText = isActive ? '(current step)' : isComplete ? '(completed)' : '(upcoming)';

        return (
          <React.Fragment key={stage.id}>
            <div
              className={stepClass}
              aria-current={isActive ? 'step' : undefined}
            >
              <span className="pd-stage-indicator__number" aria-hidden="true">
                {idx + 1}
              </span>
              <span>
                {stage.label}
                <span className="pd-sr-only"> {statusText}</span>
              </span>
            </div>
            {idx < STAGES.length - 1 && (
              <div className="pd-stage-indicator__divider" aria-hidden="true" />
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
};

export default StageIndicator;
