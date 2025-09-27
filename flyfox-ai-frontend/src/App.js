import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const MainPage = lazy(() => import('./pages/MainPage'));
const Solutions = lazy(() => import('./pages/Solutions'));
const Products = lazy(() => import('./pages/Products'));
const ServicesSupport = lazy(() => import('./pages/ServicesSupport'));
const Resources = lazy(() => import('./pages/Resources'));
const Company = lazy(() => import('./pages/Company'));
const Blog = lazy(() => import('./pages/Blog'));
const CustomerPortal = lazy(() => import('./pages/CustomerPortal'));

function App() {
  return (
    <Router>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/solutions" element={<Solutions />} />
          <Route path="/products" element={<Products />} />
          <Route path="/services" element={<ServicesSupport />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/company" element={<Company />} />
          <Route path="/blog" element={<Blog />} />
          <Route path="/customer-portal" element={<CustomerPortal />} />
          <Route path="/contact" element={<div>Contact Page (Placeholder)</div>} />
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;
