import React, { useState } from 'react';
import { Button, TextArea, TextInput, Tag, ContentSwitcher, Switch } from '@carbon/react';
import { ArrowRight } from '@carbon/icons-react';
import { EXAMPLE_PROMPTS } from '../data/demo-data';

interface InputSectionProps {
  onDiagnose: (input: string) => void;
}

/**
 * PHASE 1 - INPUT
 * Workflow description text area OR GitHub repository URL.
 * Example prompts as clickable chips to lower friction.
 */
const InputSection: React.FC<InputSectionProps> = ({ onDiagnose }) => {
  const [mode, setMode] = useState<'text' | 'github'>('text');
  const [textValue, setTextValue] = useState('');
  const [urlValue, setUrlValue] = useState('');

  const canSubmit = mode === 'text'
    ? textValue.trim().length > 20
    : urlValue.startsWith('https://github.com/');

  const handleSubmit = () => {
    if (!canSubmit) return;
    onDiagnose(mode === 'text' ? textValue : urlValue);
  };

  return (
    <section style={{ paddingTop: 'var(--pd-space-07)' }}>
      <h2 style={{ marginBottom: 'var(--pd-space-03)' }}>
        Tell us about your workflow
      </h2>
      <p className="pd-text-secondary" style={{ marginBottom: 'var(--pd-space-06)' }}>
        Describe a broken workflow in plain English, or connect a GitHub repository for direct analysis. Bob will diagnose it.
      </p>

      <ContentSwitcher
        selectedIndex={mode === 'text' ? 0 : 1}
        onChange={({ index }) => setMode(index === 0 ? 'text' : 'github')}
        size="md"
      >
        <Switch name="text" text="Workflow description" />
        <Switch name="github" text="GitHub repository" />
      </ContentSwitcher>

      <div style={{ marginTop: 'var(--pd-space-06)' }}>
        {mode === 'text' ? (
          <>
            <TextArea
              id="workflow-description"
              labelText="Workflow description"
              placeholder="Example: Our CI takes 40 minutes, requires manual approvals, and runs tests sequentially..."
              rows={6}
              value={textValue}
              onChange={(e) => setTextValue(e.target.value)}
              helperText="Plain English. Be specific about pain points."
            />

            {/* Example prompts to lower input friction */}
            <div style={{ marginTop: 'var(--pd-space-05)' }}>
              <div
                style={{
                  fontSize: 'var(--pd-font-size-label)',
                  color: 'var(--pd-color-text-secondary)',
                  marginBottom: 'var(--pd-space-03)',
                }}
              >
                Or try one of these examples:
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--pd-space-03)' }}>
                {EXAMPLE_PROMPTS.map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => setTextValue(prompt)}
                    style={{ cursor: 'pointer', border: 'none', padding: 0, background: 'transparent' }}
                    aria-label={`Use example: ${prompt.substring(0, 60)}...`}
                  >
                    <Tag type="blue" style={{ cursor: 'pointer' }}>
                      {prompt.length > 70 ? prompt.substring(0, 67) + '...' : prompt}
                    </Tag>
                  </button>
                ))}
              </div>
            </div>
          </>
        ) : (
          <TextInput
            id="github-url"
            labelText="GitHub repository URL"
            placeholder="https://github.com/your-org/your-repo"
            value={urlValue}
            onChange={(e) => setUrlValue(e.target.value)}
            helperText="Public repositories only. Bob will read .github/workflows and project structure."
          />
        )}
      </div>

      <div style={{ marginTop: 'var(--pd-space-08)', display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          kind="primary"
          size="lg"
          renderIcon={ArrowRight}
          disabled={!canSubmit}
          onClick={handleSubmit}
        >
          Diagnose workflow
        </Button>
      </div>
    </section>
  );
};

export default InputSection;
