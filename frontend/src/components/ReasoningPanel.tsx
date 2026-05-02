import React from 'react';

interface ReasoningPanelProps {
  steps: string[];
  title?: string;
}

/**
 * "Bob is thinking" panel — shows multi-step agent reasoning.
 * This is the visible answer to the team's earlier "is this just a chatbot?"
 * concern. Showing the reasoning makes the agent value explicit.
 *
 * Accessibility:
 *   - aria-live="polite" announces new reasoning steps to screen readers
 *     without interrupting the user
 *   - Semantic <ol> for the ordered reasoning steps
 */
const ReasoningPanel: React.FC<ReasoningPanelProps> = ({ steps, title = 'Bob analysis' }) => {
  return (
    <section className="pd-reasoning" aria-label={title}>
      <header className="pd-reasoning__header">
        <span aria-hidden="true">⚙</span>
        <span>{title}</span>
      </header>
      <ol style={{ listStyle: 'none', margin: 0, padding: 0 }} aria-live="polite">
        {steps.map((step, idx) => (
          <li key={idx} className="pd-reasoning__step">
            <span className="pd-sr-only">Step {idx + 1}: </span>
            {step}
          </li>
        ))}
      </ol>
    </section>
  );
};

export default ReasoningPanel;
