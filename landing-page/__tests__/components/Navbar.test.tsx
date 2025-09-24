import { render, screen } from '@testing-library/react';
import Navbar from '../../app/components/Navbar';

describe('Navbar', () => {
  it('renders the brand name', () => {
    render(<Navbar />);
    expect(screen.getByText('Goliath')).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    render(<Navbar />);
    expect(screen.getByText('About')).toBeInTheDocument();
    expect(screen.getByText('Products')).toBeInTheDocument();
    // Add more links as per actual navigation
  });
});