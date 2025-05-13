import { render, screen } from '@testing-library/react';
import App from './App';
import { BrowserRouter as Router } from 'react-router-dom';

test('renders Navbar component', () => {
  render(
    <Router>
      <App />
    </Router>
  );
  const navbarElement = screen.getByRole('navigation');
  expect(navbarElement).toBeInTheDocument();
});
