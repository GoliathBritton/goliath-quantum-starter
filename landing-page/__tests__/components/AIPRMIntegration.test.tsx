import { render, screen } from '@testing-library/react';
import AIPRMIntegration from '../../app/components/AIPRMIntegration';

describe('AIPRMIntegration', () => {
  it('renders the component title', () => {
    render(<AIPRMIntegration />);
    expect(screen.getByText('AIPRM Integration')).toBeInTheDocument();
  });

  it('renders prompt templates tab', () => {
    render(<AIPRMIntegration />);
    expect(screen.getByText('Prompt Templates')).toBeInTheDocument();
  });

  it('renders extensions tab', () => {
    render(<AIPRMIntegration />);
    expect(screen.getByText('Extensions')).toBeInTheDocument();
  });

  it('renders AI playground tab', () => {
    render(<AIPRMIntegration />);
    expect(screen.getByText('AI Playground')).toBeInTheDocument();
  });
});