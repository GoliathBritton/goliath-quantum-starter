import { render, screen } from '@testing-library/react';
import Footer from '../../app/components/Footer';

describe('Footer', () => {
  it('renders the copyright notice', () => {
    render(<Footer />);
    expect(screen.getByText(/© \d{4} Goliath of All Trade. All rights reserved./i)).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    render(<Footer />);
    expect(screen.getByText('Privacy Policy')).toBeInTheDocument();
    expect(screen.getByText('Terms of Service')).toBeInTheDocument();
    expect(screen.getByText('Privacy Policy')).toBeInTheDocument();
  });
});