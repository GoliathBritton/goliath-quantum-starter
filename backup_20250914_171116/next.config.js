/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Using pages directory (default for Next.js 13+)
  webpack: (config) => {
    // Handle three.js and other 3D libraries
    config.module.rules.push({
      test: /\.(glsl|vs|fs|vert|frag)$/,
      use: 'raw-loader'
    });
    
    return config;
  },
  transpilePackages: ['three', 'react-force-graph-3d']
};

module.exports = nextConfig;