import { AuditForm } from "@/components/audit/AuditForm";
import { AuditResults } from "@/components/audit/AuditResults";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/shared/Card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/shared/Tabs";
import { BarChart3, ShieldCheck, FileText, Cpu } from "lucide-react";

export default function HomePage() {
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
          TEE-Verified{" "}
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            DeFi Risk Analysis
          </span>
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
          Audit any DeFi protocol with Trusted Execution Environment verification.
          Receive comprehensive risk assessments with cryptographic proof recorded on-chain.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <div className="inline-flex items-center rounded-full bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 text-sm font-medium text-blue-800">
            <ShieldCheck className="mr-2 h-4 w-4" />
            Smart Contract Security
          </div>
          <div className="inline-flex items-center rounded-full bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 text-sm font-medium text-blue-800">
            <BarChart3 className="mr-2 h-4 w-4" />
            Economic Risk Analysis
          </div>
          <div className="inline-flex items-center rounded-full bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 text-sm font-medium text-blue-800">
            <Cpu className="mr-2 h-4 w-4" />
            TEE-Attested Results
          </div>
          <div className="inline-flex items-center rounded-full bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 text-sm font-medium text-blue-800">
            <FileText className="mr-2 h-4 w-4" />
            On-Chain Proof
          </div>
        </div>
      </div>

      {/* Main Audit Interface */}
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        {/* Left Column - Audit Form */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Protocol Audit Request</CardTitle>
              <CardDescription>
                Enter a DeFi protocol address, name, or select from our database.
                Our TEE-verified AI will analyze security, economics, and governance risks.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <AuditForm />
            </CardContent>
          </Card>

          {/* Recent Audits */}
          <Card className="mt-8">
            <CardHeader>
              <CardTitle>Recent Audits</CardTitle>
              <CardDescription>
                Latest protocol audits performed by the community
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { name: "Uniswap V3", score: 92, risk: "Low", date: "2 hours ago" },
                  { name: "Aave V3", score: 88, risk: "Medium", date: "5 hours ago" },
                  { name: "Compound V3", score: 85, risk: "Medium", date: "1 day ago" },
                  { name: "Curve Finance", score: 90, risk: "Low", date: "2 days ago" },
                  { name: "MakerDAO", score: 94, risk: "Low", date: "3 days ago" },
                ].map((protocol) => (
                  <div
                    key={protocol.name}
                    className="flex items-center justify-between rounded-lg border border-gray-200 p-4 hover:bg-gray-50"
                  >
                    <div className="flex items-center space-x-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-100 to-purple-100">
                        <span className="text-sm font-bold text-blue-800">
                          {protocol.name.charAt(0)}
                        </span>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900">{protocol.name}</h4>
                        <p className="text-sm text-gray-500">Audited {protocol.date}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-gray-900">{protocol.score}</div>
                        <div className="text-xs text-gray-500">Score</div>
                      </div>
                      <div className={`rounded-full px-3 py-1 text-xs font-medium ${protocol.risk === "Low" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}`}>
                        {protocol.risk} Risk
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Results & Info */}
        <div className="space-y-8">
          <Card>
            <CardHeader>
              <CardTitle>Audit Results</CardTitle>
              <CardDescription>
                Live results from your audit request will appear here
              </CardDescription>
            </CardHeader>
            <CardContent>
              <AuditResults />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>How It Works</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">1. Submit Protocol</h4>
                <p className="text-sm text-gray-600">
                  Enter a protocol address or select from our verified database.
                </p>
              </div>
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">2. TEE Analysis</h4>
                <p className="text-sm text-gray-600">
                  Our AI runs in a Trusted Execution Environment, ensuring tamper-proof analysis.
                </p>
              </div>
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">3. Receive Report</h4>
                <p className="text-sm text-gray-600">
                  Get detailed risk assessment across security, economics, and governance.
                </p>
              </div>
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">4. On-Chain Proof</h4>
                <p className="text-sm text-gray-600">
                  Cryptographic attestation is recorded on-chain via OpenGradient x402.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}