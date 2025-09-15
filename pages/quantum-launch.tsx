import React from 'react';
import Head from 'next/head';
import { QuantumLaunchDashboard } from '../components/QuantumLaunchDashboard';

// This is a Next.js page component that integrates the Quantum Launch Dashboard
// You can adapt this for other frameworks (React, Vue, etc.)

interface QuantumLaunchPageProps {
  userId?: string;
  customLaunchDate?: string;
}

const QuantumLaunchPage: React.FC<QuantumLaunchPageProps> = ({
  userId,
  customLaunchDate
}) => {
  // Parse custom launch date if provided
  const launchDate = customLaunchDate 
    ? new Date(customLaunchDate)
    : new Date('2025-12-01T00:00:00Z');

  return (
    <>
      <Head>
        <title>Quantum High Council Launch | Quantum Nexus</title>
        <meta 
          name="description" 
          content="Join the Quantum High Council launch countdown. Earn rewards, invite friends, and unlock exclusive benefits in the quantum revolution."
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        
        {/* Open Graph / Social Media */}
        <meta property="og:type" content="website" />
        <meta property="og:title" content="Quantum High Council Launch" />
        <meta property="og:description" content="Join the quantum revolution. Exclusive countdown with rewards and founder benefits." />
        <meta property="og:image" content="/quantum-nexus-og.jpg" />
        <meta property="og:url" content="https://quantum-nexus.ai/quantum-launch" />
        
        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Quantum High Council Launch" />
        <meta name="twitter:description" content="Join the quantum revolution. Exclusive countdown with rewards and founder benefits." />
        <meta name="twitter:image" content="/quantum-nexus-twitter.jpg" />
        
        {/* Fonts */}
        <link 
          href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" 
          rel="stylesheet" 
        />
        
        {/* Favicon */}
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        
        {/* Structured Data for SEO */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Event",
              "name": "Quantum High Council Launch",
              "description": "The official launch of the Quantum High Council platform",
              "startDate": launchDate.toISOString(),
              "eventStatus": "https://schema.org/EventScheduled",
              "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
              "location": {
                "@type": "VirtualLocation",
                "url": "https://quantum-nexus.ai"
              },
              "organizer": {
                "@type": "Organization",
                "name": "Quantum Nexus",
                "url": "https://quantum-nexus.ai"
              }
            })
          }}
        />
      </Head>
      
      <main className="quantum-launch-page">
        <QuantumLaunchDashboard 
          userId={userId}
          launchDate={launchDate}
          className="main-dashboard"
        />
      </main>
      
      <style jsx global>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        
        html, body {
          height: 100%;
          font-family: 'Orbitron', monospace;
          background: #000000;
          color: white;
          overflow-x: hidden;
        }
        
        #__next {
          height: 100%;
        }
        
        .quantum-launch-page {
          min-height: 100vh;
          position: relative;
        }
        
        .main-dashboard {
          position: relative;
          z-index: 1;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
          width: 8px;
        }
        
        ::-webkit-scrollbar-track {
          background: rgba(0, 0, 0, 0.5);
        }
        
        ::-webkit-scrollbar-thumb {
          background: linear-gradient(45deg, #00fff6, #8000ff);
          border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
          background: linear-gradient(45deg, #00cccc, #6600cc);
        }
        
        /* Selection styling */
        ::selection {
          background: rgba(0, 255, 246, 0.3);
          color: white;
        }
        
        ::-moz-selection {
          background: rgba(0, 255, 246, 0.3);
          color: white;
        }
        
        /* Focus styles for accessibility */
        button:focus,
        input:focus,
        textarea:focus {
          outline: 2px solid #00fff6;
          outline-offset: 2px;
        }
        
        /* Smooth animations */
        * {
          transition: color 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
        }
        
        /* Loading animation for images */
        img {
          transition: opacity 0.3s ease;
        }
        
        img[data-loading="true"] {
          opacity: 0.5;
        }
        
        /* Print styles */
        @media print {
          .quantum-launch-page {
            background: white !important;
            color: black !important;
          }
          
          .notification,
          .welcome-overlay {
            display: none !important;
          }
        }
        
        /* High contrast mode support */
        @media (prefers-contrast: high) {
          .quantum-launch-page {
            filter: contrast(1.5);
          }
        }
        
        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {
          *,
          *::before,
          *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
          }
        }
        
        /* Dark mode support (if system preference) */
        @media (prefers-color-scheme: dark) {
          .quantum-launch-page {
            background: #000000;
            color: white;
          }
        }
        
        /* Light mode fallback */
        @media (prefers-color-scheme: light) {
          .quantum-launch-page {
            background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
            color: white;
          }
        }
      `}</style>
    </>
  );
};

// Server-side props for Next.js (optional)
export async function getServerSideProps(context: any) {
  // You can fetch user data, launch date, or other dynamic content here
  const { query } = context;
  
  return {
    props: {
      userId: query.userId || null,
      customLaunchDate: query.launchDate || null,
    },
  };
}

// Static props alternative for Next.js (if you prefer static generation)
// export async function getStaticProps() {
//   return {
//     props: {
//       // Static props here
//     },
//     revalidate: 3600, // Revalidate every hour
//   };
// }

export default QuantumLaunchPage;