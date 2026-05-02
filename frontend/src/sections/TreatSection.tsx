import React, { useState } from 'react';
import { Button, Modal, Tag, CodeSnippet } from '@carbon/react';
import { CheckmarkFilled, Restart } from '@carbon/icons-react';
import { GENERATED_YAML, PR_DETAILS } from '../data/demo-data';

interface TreatSectionProps {
  onRestart: () => void;
}

type TreatState = 'review' | 'confirming' | 'success';

/**
 * PHASE 4 - TREAT
 * Generated artifact preview + approval gate + success state.
 * The approval gate is intentional - reinforces the human-in-the-loop
 * differentiator and IBM's enterprise-trust positioning.
 */
const TreatSection: React.FC<TreatSectionProps> = ({ onRestart }) => {
  const [state, setState] = useState<TreatState>('review');

  const handleApprove = () => setState('confirming');
  const handleConfirm = () => {
    // Simulated execution. In production, this fires the watsonx Orchestrate
    // call. For demo: deterministic 1.2s delay so the success state lands
    // predictably during the live presentation.
    setTimeout(() => setState('success'), 1200);
  };

  if (state === 'success') {
    return (
      <section
        style={{
          paddingTop: 'var(--pd-space-09)',
          paddingBottom: 'var(--pd-space-09)',
          textAlign: 'center',
        }}
      >
        <div style={{ maxWidth: '560px', margin: '0 auto' }}>
          <CheckmarkFilled
            size={64}
            style={{ color: 'var(--pd-color-success)', marginBottom: 'var(--pd-space-06)' }}
          />
          <h2 style={{ marginBottom: 'var(--pd-space-04)' }}>Pull request created</h2>
          <p
            style={{
              fontSize: 'var(--pd-font-size-body-lg)',
              color: 'var(--pd-color-text-secondary)',
              marginBottom: 'var(--pd-space-08)',
            }}
          >
            Your team will be notified. Bob will monitor execution and surface any issues for re-optimization.
          </p>

          <article
            style={{
              textAlign: 'left',
              padding: 'var(--pd-space-06)',
              border: '1px solid var(--pd-color-border-subtle)',
              background: 'var(--pd-color-surface)',
              borderRadius: 'var(--pd-radius-sm)',
              marginBottom: 'var(--pd-space-08)',
            }}
          >
            <div
              style={{
                fontSize: 'var(--pd-font-size-label)',
                color: 'var(--pd-color-text-secondary)',
                marginBottom: 'var(--pd-space-02)',
              }}
            >
              {PR_DETAILS.repository}
            </div>
            <div
              style={{
                fontSize: 'var(--pd-font-size-heading-03)',
                fontWeight: 'var(--pd-font-weight-medium)',
                marginBottom: 'var(--pd-space-04)',
              }}
            >
              {PR_DETAILS.title}
            </div>
            <div style={{ display: 'flex', gap: 'var(--pd-space-03)', flexWrap: 'wrap' }}>
              <Tag type="green">PR #{PR_DETAILS.number} opened</Tag>
              <Tag type="blue">{PR_DETAILS.branch}</Tag>
            </div>
          </article>

          <Button kind="tertiary" renderIcon={Restart} onClick={onRestart}>
            Diagnose another workflow
          </Button>
        </div>
      </section>
    );
  }

  return (
    <section style={{ paddingTop: 'var(--pd-space-07)' }}>
      <div style={{ marginBottom: 'var(--pd-space-07)' }}>
        <Tag type="blue">Ready for approval</Tag>
        <h2 style={{ marginTop: 'var(--pd-space-04)', marginBottom: 'var(--pd-space-03)' }}>
          Treatment: generated CI/CD pipeline
        </h2>
        <p className="pd-text-secondary">
          Bob has generated the optimized GitHub Actions workflow. Review the file before we open the pull request.
        </p>
      </div>

      {/* Generated YAML preview */}
      <h3 style={{ marginBottom: 'var(--pd-space-04)' }}>
        Generated file: .github/workflows/ci.yml
      </h3>
      <CodeSnippet type="multi" feedback="Copied">
        {GENERATED_YAML}
      </CodeSnippet>

      {/* PR preview card */}
      <div style={{ marginTop: 'var(--pd-space-07)' }}>
        <h3 style={{ marginBottom: 'var(--pd-space-04)' }}>Pull request preview</h3>
        <article
          style={{
            padding: 'var(--pd-space-06)',
            border: '1px solid var(--pd-color-border-subtle)',
            background: 'var(--pd-color-background)',
            borderRadius: 'var(--pd-radius-sm)',
          }}
        >
          <div
            style={{
              fontSize: 'var(--pd-font-size-label)',
              color: 'var(--pd-color-text-secondary)',
              marginBottom: 'var(--pd-space-02)',
            }}
          >
            {PR_DETAILS.repository}
          </div>
          <div
            style={{
              fontSize: 'var(--pd-font-size-heading-03)',
              fontWeight: 'var(--pd-font-weight-medium)',
              marginBottom: 'var(--pd-space-03)',
            }}
          >
            {PR_DETAILS.title}
          </div>
          <p className="pd-text-secondary" style={{ marginBottom: 'var(--pd-space-04)' }}>
            {PR_DETAILS.description}
          </p>
          <div style={{ display: 'flex', gap: 'var(--pd-space-03)', flexWrap: 'wrap' }}>
            <Tag type="blue">{PR_DETAILS.branch}</Tag>
            <Tag type="gray">+{PR_DETAILS.additions} −{PR_DETAILS.deletions}</Tag>
            <Tag type="purple">Generated by ProcessDoctor</Tag>
          </div>
        </article>
      </div>

      <div
        style={{
          marginTop: 'var(--pd-space-08)',
          display: 'flex',
          gap: 'var(--pd-space-04)',
          justifyContent: 'flex-end',
        }}
      >
        <Button kind="tertiary" onClick={onRestart}>Cancel</Button>
        <Button kind="primary" size="lg" onClick={handleApprove}>
          Approve and deploy
        </Button>
      </div>

      {/* Confirmation modal — explicit human-in-the-loop gate */}
      <Modal
        open={state === 'confirming'}
        modalHeading="Approve treatment?"
        primaryButtonText="Yes, open pull request"
        secondaryButtonText="Cancel"
        onRequestClose={() => setState('review')}
        onRequestSubmit={handleConfirm}
        size="sm"
      >
        <p>
          This will open a pull request in <strong>{PR_DETAILS.repository}</strong> on
          branch <strong>{PR_DETAILS.branch}</strong>. The pipeline change does not deploy
          automatically — your team must merge the PR before the new workflow takes effect.
        </p>
      </Modal>
    </section>
  );
};

export default TreatSection;
