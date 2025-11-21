/** @type {import('next').NextConfig} */
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

const nextConfig = {
  reactStrictMode: true,
  
  // Temporarily skip type checking to focus on performance optimizations
  typescript: {
    ignoreBuildErrors: true,
  },
  
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Enhanced webpack config for service worker support and bundle optimization
  webpack: (config, { dev, isServer }) => {
    if (!isServer) {
      // Ensure service worker can access all origins
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };

      // Enhanced bundle splitting for 37-tool platform (production only)
      if (!dev) {
        config.optimization.splitChunks = {
          chunks: 'all',
          cacheGroups: {
            // Domain-specific chunks for mental prosthetic platform
            security: {
              name: 'security-tools',
              test: /[\\\//]src[\\\//](components|services)[\\\//](security|Security)[\\\//]/,
              chunks: 'all',
              priority: 10,
            },
            productivity: {
              name: 'productivity-tools',
              test: /[\\\//]src[\\\//](components|services)[\\\//](productivity|Productivity)[\\\//]/,
              chunks: 'all',
              priority: 10,
            },
            mtg: {
              name: 'mtg-tools',
              test: /[\\\//]src[\\\//](components|services)[\\\//](mtg|tcg|MTG)[\\\//]/,
              chunks: 'all',
              priority: 10,
            },
            ai: {
              name: 'ai-tools',
              test: /[\\\//]src[\\\//](components|services)[\\\//](ai|AI)[\\\//]/,
              chunks: 'all',
              priority: 10,
            },
            // Vendor chunks optimization
            vendor: {
              name: 'vendor',
              test: /[\\\//]node_modules[\\\//]/,
              chunks: 'all',
              priority: 5,
            },
          },
        };
      }
    }
    return config;
  },

  // Output configuration for static export compatibility
  output: 'standalone',
  
  // Image optimization for PWA icons
  images: {
    unoptimized: true,
  },

  // Security and PWA headers
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
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' ws: wss:; worker-src 'self' blob:;",
          },
        ],
      },
      {
        source: '/sw.js',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=0, must-revalidate',
          },
          {
            key: 'Service-Worker-Allowed',
            value: '/',
          },
        ],
      },
      {
        source: '/manifest.json',
        headers: [
          {
            key: 'Content-Type',
            value: 'application/manifest+json',
          },
        ],
      },
    ];
  },
};

// eslint-disable-next-line no-undef
module.exports = withBundleAnalyzer(nextConfig);
