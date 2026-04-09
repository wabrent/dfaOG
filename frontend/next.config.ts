import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  images: {
    domains: ['sepolia.basescan.org'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_APP_NAME: 'DeFi Risk Auditor',
    NEXT_PUBLIC_APP_DESCRIPTION: 'TEE-verified DeFi protocol risk analysis with on-chain proof',
  },
};

export default nextConfig;