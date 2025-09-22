/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Domain and deployment configuration
  env: {
    CUSTOM_KEY: 'quantum-omniscient',
    DOMAIN_NAME: process.env.DOMAIN_NAME || 'localhost:3000',
    APP_URL: process.env.APP_URL || 'http://localhost:3000',
  },

  // Image optimization for production domains
  images: {
    domains: [
      'localhost',
      'quantum-omniscient.com',
      'quantumomniscient.ai',
      'omniscient.quantum',
      // Add your custom domain here
    ],
    unoptimized: process.env.NODE_ENV === 'development',
  },

  // Headers for custom domain support
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
          {
            key: 'X-Powered-By',
            value: 'Quantum Omniscient',
          },
        ],
      },
    ]
  },

  // Using pages directory (default for Next.js 13+)
  webpack: (config) => {
    // Handle three.js and other 3D libraries
    config.module.rules.push({
      test: /\.(glsl|vs|fs|vert|frag)$/,
      use: 'raw-loader'
    });
    
    // Custom webpack configuration for quantum components
    config.resolve.alias = {
      ...config.resolve.alias,
      '@quantum': './src/quantum',
      '@components': './components',
      '@lib': './lib',
    }
    
    return config;
  },
  transpilePackages: ['three', 'react-force-graph-3d']
};

module.exports = nextConfig;