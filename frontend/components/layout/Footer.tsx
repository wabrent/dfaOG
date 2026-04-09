import Link from "next/link";
import { Github, Twitter, MessageCircle } from "lucide-react";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="mt-auto border-t border-gray-200 bg-white">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-purple-600">
                <span className="text-sm font-bold text-white">DRA</span>
              </div>
              <span className="text-lg font-bold text-gray-900">
                DeFi Risk Auditor
              </span>
            </div>
            <p className="text-sm text-gray-600">
              TEE-verified DeFi protocol risk analysis with on-chain cryptographic proof.
            </p>
            <div className="flex space-x-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-gray-700"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-blue-500"
              >
                <Twitter className="h-5 w-5" />
              </a>
              <a
                href="https://discord.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-purple-500"
              >
                <MessageCircle className="h-5 w-5" />
              </a>
            </div>
          </div>

          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase text-gray-900">
              Product
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="/audit"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Protocol Audit
                </Link>
              </li>
              <li>
                <Link
                  href="/protocols"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Protocol Database
                </Link>
              </li>
              <li>
                <Link
                  href="/reports"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Audit Reports
                </Link>
              </li>
              <li>
                <Link
                  href="/api"
                  className="text-gray-600 hover:text-gray-900"
                >
                  API Access
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase text-gray-900">
              Resources
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="/docs"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Documentation
                </Link>
              </li>
              <li>
                <Link
                  href="/tutorials"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Tutorials
                </Link>
              </li>
              <li>
                <Link
                  href="/blog"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Blog
                </Link>
              </li>
              <li>
                <Link
                  href="/security"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Security
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase text-gray-900">
              Legal
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="/privacy"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link
                  href="/terms"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link
                  href="/disclaimer"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Risk Disclaimer
                </Link>
              </li>
              <li>
                <Link
                  href="/attestation"
                  className="text-gray-600 hover:text-gray-900"
                >
                  TEE Attestation
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 border-t border-gray-200 pt-8">
          <div className="flex flex-col items-center justify-between md:flex-row">
            <p className="text-sm text-gray-600">
              © {currentYear} DeFi Risk Auditor. All rights reserved.
            </p>
            <p className="mt-2 text-xs text-gray-500 md:mt-0">
              Built with <span className="font-medium text-blue-600">OpenGradient</span> for TEE-verified inference.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}