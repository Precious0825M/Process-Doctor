import React from 'react';

export interface WorkflowNode {
  id: string;
  label: string;
  duration?: string;
  isBottleneck?: boolean;
  isOptimized?: boolean;
}

interface WorkflowGraphProps {
  nodes: WorkflowNode[];
  ariaLabel: string;
}

/**
 * Linear horizontal workflow graph.
 *
 * The MVP renders a left-to-right sequence of nodes with arrow connectors.
 * This is intentionally simple — for the hackathon demo, a clean linear
 * flow tells the diagnose/prescribe story better than a complex DAG.
 *
 * Accessibility:
 *   - Wrapped in semantic <figure> with descriptive aria-label
 *   - Each node has bottleneck status announced via .pd-sr-only text
 *   - Arrows are aria-hidden (decorative only)
 */
const WorkflowGraph: React.FC<WorkflowGraphProps> = ({ nodes, ariaLabel }) => {
  return (
    <figure
      role="img"
      aria-label={ariaLabel}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--pd-space-04)',
        padding: 'var(--pd-space-06)',
        margin: 0,
        flexWrap: 'wrap',
        background: 'var(--pd-color-background)',
        border: '1px solid var(--pd-color-border-subtle)',
        borderRadius: 'var(--pd-radius-sm)',
      }}
    >
      {nodes.map((node, idx) => (
        <React.Fragment key={node.id}>
          <div
            className={[
              'pd-node',
              node.isBottleneck && 'pd-node--bottleneck',
              node.isOptimized  && 'pd-node--optimized',
            ].filter(Boolean).join(' ')}
          >
            {node.isBottleneck && (
              <span className="pd-sr-only">Bottleneck identified: </span>
            )}
            {node.isOptimized && (
              <span className="pd-sr-only">Optimized step: </span>
            )}
            <span className="pd-node__label">{node.label}</span>
            {node.duration && <span className="pd-node__time">{node.duration}</span>}
            {node.isBottleneck && (
              <span style={{
                fontSize: 'var(--pd-font-size-caption)',
                color: 'var(--pd-color-error)',
                fontWeight: 'var(--pd-font-weight-semibold)',
              }}>
                ⚠ Bottleneck
              </span>
            )}
          </div>
          {idx < nodes.length - 1 && (
            <span aria-hidden="true" style={{
              color: 'var(--pd-color-border-strong)',
              fontSize: '1.5rem',
            }}>→</span>
          )}
        </React.Fragment>
      ))}
    </figure>
  );
};

export default WorkflowGraph;
