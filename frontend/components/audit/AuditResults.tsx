"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/shared/Card";
import { Button } from "@/components/shared/Button";
import { Progress } from "@/components/shared/Progress";
import { Shield, TrendingUp, Users, AlertTriangle, CheckCircle, XCircle } from "lucide-react";

export function AuditResults() {
  const [hasResults, setHasResults] = useState(false);

  // Mock data
  const mockResults = {
    overallScore: 88,
    riskLevel: "Medium",
    categories: [
      { name: "Smart Contract Security", score: 92, risk: "Low" },
      { name: "Economic Security", score: 85, risk: "Medium" },
      { name: "Governance & DAO", score: 78, risk: "Medium" },
      { name: "Financial Risk", score: 90, risk: "Low" },
      { name: "Operational Risk", score: 82, risk: "Medium" },
    ],
    findings: {
      critical: 1,
      high: 3,
      medium: 7,
      low: 12,
    },
    attestation: {
      teeVerified: true,
      transactionHash: "0x1234...5678",
      timestamp: "2024-03-15T14:30:00Z",
    },
  };

  if (!hasResults) {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-r from-blue-100 to-purple-100">
            <Shield className="h-8 w-8 text-blue-600" />
          </div>
          <h3 className="mt-4 text-lg font-medium text-gray-900">No Audit Results Yet</h3>
          <p className="mt-2 text-sm text-gray-600">
            Submit a protocol audit request to see TEE-verified results here.
          </p>
        </div>
        <div className="space-y-4">
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">
            <div className="flex items-center space-x-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
                <TrendingUp className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Example Report Available</h4>
                <p className="text-sm text-gray-600">View a sample audit report to see what you'll get</p>
              </div>
            </div>
          </div>
          <Button
            variant="outline"
            className="w-full"
            onClick={() => setHasResults(true)}
          >
            Load Sample Results
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <div className="text-center">
        <div className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-blue-600 to-purple-600 p-1">
          <div className="flex h-28 w-28 items-center justify-center rounded-full bg-white">
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900">{mockResults.overallScore}</div>
              <div className="text-sm font-medium text-gray-600">Overall Score</div>
            </div>
          </div>
        </div>
        <div className={`mt-4 inline-block rounded-full px-4 py-1 text-sm font-medium ${mockResults.riskLevel === "Low" ? "bg-green-100 text-green-800" : mockResults.riskLevel === "Medium" ? "bg-yellow-100 text-yellow-800" : "bg-red-100 text-red-800"}`}>
          {mockResults.riskLevel} Risk
        </div>
      </div>

      {/* Category Scores */}
      <div>
        <h4 className="mb-4 font-medium text-gray-900">Category Scores</h4>
        <div className="space-y-4">
          {mockResults.categories.map((category) => (
            <div key={category.name} className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-900">{category.name}</span>
                <span className="text-sm font-medium text-gray-900">{category.score}</span>
              </div>
              <Progress value={category.score} className="h-2" />
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-600">{category.risk} Risk</span>
                <span className="text-xs text-gray-600">{category.score}/100</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Findings Summary */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Findings Summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-lg bg-red-50 p-3">
              <div className="flex items-center space-x-2">
                <XCircle className="h-5 w-5 text-red-600" />
                <span className="text-sm font-medium text-red-900">Critical</span>
              </div>
              <div className="mt-2 text-2xl font-bold text-red-900">{mockResults.findings.critical}</div>
            </div>
            <div className="rounded-lg bg-orange-50 p-3">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="h-5 w-5 text-orange-600" />
                <span className="text-sm font-medium text-orange-900">High</span>
              </div>
              <div className="mt-2 text-2xl font-bold text-orange-900">{mockResults.findings.high}</div>
            </div>
            <div className="rounded-lg bg-yellow-50 p-3">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="h-5 w-5 text-yellow-600" />
                <span className="text-sm font-medium text-yellow-900">Medium</span>
              </div>
              <div className="mt-2 text-2xl font-bold text-yellow-900">{mockResults.findings.medium}</div>
            </div>
            <div className="rounded-lg bg-blue-50 p-3">
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-5 w-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-900">Low</span>
              </div>
              <div className="mt-2 text-2xl font-bold text-blue-900">{mockResults.findings.low}</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* TEE Attestation */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">TEE Attestation</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">TEE Verification</span>
            <span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800">
              <CheckCircle className="mr-1 h-3 w-3" />
              Verified
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">On-Chain Proof</span>
            <span className="text-sm font-medium text-gray-900">Recorded</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Transaction</span>
            <span className="truncate text-sm font-mono text-blue-600">
              {mockResults.attestation.transactionHash}
            </span>
          </div>
          <Button variant="outline" className="w-full" size="sm">
            View On-Chain Attestation
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}