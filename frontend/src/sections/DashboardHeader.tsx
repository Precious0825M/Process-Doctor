import React from 'react';

/**
 * Top-of-dashboard branding header. Stays visible across all phases.
 * Sparse on purpose - enterprise tools earn trust through restraint.
 */
const DashboardHeader: React.FC = () => {
  return (
    <header
      style={{
        background: 'var(--pd-color-background)',
        borderBottom: '1px solid var(--pd-color-border-subtle)',
        padding: 'var(--pd-space-06) 0',
        marginBottom: 'var(--pd-space-07)',
      }}
    >
      <div className="pd-container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', flexWrap: 'wrap', gap: 'var(--pd-space-04)' }}>
          <div>
            <div
              style={{
                fontSize: 'var(--pd-font-size-label)',
                fontWeight: 'var(--pd-font-weight-semibold)',
                color: 'var(--pd-color-primary)',
                letterSpacing: '0.16em',
                textTransform: 'uppercase',
                marginBottom: 'var(--pd-space-02)',
              }}
            >
              ProcessDoctor
            </div>
            <h1
              style={{
                fontSize: 'var(--pd-font-size-heading-04)',
                margin: 0,
                fontWeight: 'var(--pd-font-weight-light)',
              }}
            >
              A workflow doctor for engineering teams.
            </h1>
          </div>

          <div
            style={{
              fontSize: 'var(--pd-font-size-caption)',
              color: 'var(--pd-color-text-tertiary)',
              textAlign: 'right',
            }}
          >
            Powered by IBM Bob, IBM Granite, and<br />IBM watsonx Orchestrate
          </div>
        </div>
      </div>
    </header>
  );
};

export default DashboardHeader;
