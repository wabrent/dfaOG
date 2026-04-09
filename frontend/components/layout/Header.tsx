import Link from "next/link";
import { Button } from "@/components/shared/Button";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200 bg-white/80 backdrop-blur-sm">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <div className="flex items-center space-x-2">
          <Link href="/" className="flex items-center space-x-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-purple-600">
              <span className="text-sm font-bold text-white">DRA</span>
            </div>
            <span className="text-xl font-bold text-gray-900">
              DeFi Risk Auditor
            </span>
          </Link>
          <span className="hidden rounded-full bg-gradient-to-r from-blue-100 to-purple-100 px-3 py-1 text-xs font-medium text-blue-800 sm:inline">
            TEE-Verified
          </span>
        </div>

        <nav className="hidden items-center space-x-1 md:flex">
          <Link
            href="/audit"
            className="rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900"
          >
            Audit
          </Link>
          <Link
            href="/protocols"
            className="rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900"
          >
            Protocols
          </Link>
          <Link
            href="/reports"
            className="rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900"
          >
            Reports
          </Link>
          <Link
            href="/docs"
            className="rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900"
          >
            Documentation
          </Link>
        </nav>

        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm">
            Connect Wallet
          </Button>
          <Button size="sm">New Audit</Button>
        </div>
      </div>
    </header>
  );
}