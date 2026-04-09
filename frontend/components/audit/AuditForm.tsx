"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/shared/Button";
import { Input } from "@/components/shared/Input";
import { Label } from "@/components/shared/Label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/shared/Select";
import { Textarea } from "@/components/shared/Textarea";
import { Checkbox } from "@/components/shared/Checkbox";
import { Loader2, Search, ExternalLink } from "lucide-react";

const auditFormSchema = z.object({
  protocolAddress: z.string().min(1, "Protocol address is required"),
  chain: z.string().min(1, "Chain selection is required"),
  analysisTypes: z.array(z.string()).min(1, "Select at least one analysis type"),
  notes: z.string().optional(),
});

type AuditFormData = z.infer<typeof auditFormSchema>;

const CHAINS = [
  { id: "ethereum", name: "Ethereum" },
  { id: "polygon", name: "Polygon" },
  { id: "arbitrum", name: "Arbitrum" },
  { id: "optimism", name: "Optimism" },
  { id: "base", name: "Base" },
  { id: "avalanche", name: "Avalanche" },
  { id: "bnb", name: "BNB Chain" },
];

const ANALYSIS_TYPES = [
  { id: "security", label: "Smart Contract Security", description: "Code vulnerabilities, access controls, upgrade risks" },
  { id: "economic", label: "Economic Security", description: "Tokenomics, incentives, value flows, attack vectors" },
  { id: "governance", label: "Governance & DAO", description: "Voting power distribution, proposal process, decentralization" },
  { id: "financial", label: "Financial Risk", description: "TVL concentration, liquidity, oracle dependencies" },
  { id: "operational", label: "Operational Risk", description: "Team, documentation, disaster recovery plans" },
];

export function AuditForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedProtocol, setSelectedProtocol] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<AuditFormData>({
    resolver: zodResolver(auditFormSchema),
    defaultValues: {
      protocolAddress: "",
      chain: "ethereum",
      analysisTypes: ["security", "economic"],
      notes: "",
    },
  });

  const selectedAnalysisTypes = watch("analysisTypes");

  const onSubmit = async (data: AuditFormData) => {
    setIsSubmitting(true);
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 2000));
      console.log("Audit submitted:", data);
      // In a real app, you would call your backend API here
    } catch (error) {
      console.error("Submission error:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleProtocolSearch = () => {
    const address = watch("protocolAddress");
    if (address) {
      // Simulate protocol lookup
      setSelectedProtocol("Uniswap V3");
      // In a real app, you would call an API to verify the protocol
    }
  };

  const toggleAnalysisType = (typeId: string) => {
    const current = selectedAnalysisTypes;
    const newTypes = current.includes(typeId)
      ? current.filter((id) => id !== typeId)
      : [...current, typeId];
    setValue("analysisTypes", newTypes, { shouldValidate: true });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Protocol Address */}
      <div className="space-y-2">
        <Label htmlFor="protocolAddress">Protocol Address or Name</Label>
        <div className="flex space-x-2">
          <div className="flex-1">
            <Input
              id="protocolAddress"
              placeholder="0x... or protocol name"
              {...register("protocolAddress")}
              className={errors.protocolAddress ? "border-red-300" : ""}
            />
          </div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={handleProtocolSearch}
            disabled={!watch("protocolAddress")}
          >
            <Search className="h-4 w-4" />
          </Button>
        </div>
        {errors.protocolAddress && (
          <p className="text-sm text-red-600">{errors.protocolAddress.message}</p>
        )}
        {selectedProtocol && (
          <div className="rounded-lg bg-blue-50 p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-blue-900">Identified: {selectedProtocol}</p>
                <p className="text-sm text-blue-700">This appears to be a known DeFi protocol</p>
              </div>
              <Button type="button" variant="ghost" size="sm">
                <ExternalLink className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Chain Selection */}
      <div className="space-y-2">
        <Label htmlFor="chain">Blockchain Network</Label>
        <Select
          value={watch("chain")}
          onValueChange={(value) => setValue("chain", value, { shouldValidate: true })}
        >
          <SelectTrigger className={errors.chain ? "border-red-300" : ""}>
            <SelectValue placeholder="Select chain" />
          </SelectTrigger>
          <SelectContent>
            {CHAINS.map((chain) => (
              <SelectItem key={chain.id} value={chain.id}>
                {chain.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {errors.chain && <p className="text-sm text-red-600">{errors.chain.message}</p>}
      </div>

      {/* Analysis Types */}
      <div className="space-y-3">
        <Label>Analysis Types</Label>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {ANALYSIS_TYPES.map((type) => (
            <div
              key={type.id}
              className={`cursor-pointer rounded-lg border p-4 transition-colors ${
                selectedAnalysisTypes.includes(type.id)
                  ? "border-blue-300 bg-blue-50"
                  : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
              }`}
              onClick={() => toggleAnalysisType(type.id)}
            >
              <div className="flex items-start space-x-3">
                <Checkbox
                  checked={selectedAnalysisTypes.includes(type.id)}
                  onCheckedChange={() => toggleAnalysisType(type.id)}
                  id={`analysis-${type.id}`}
                />
                <div className="flex-1">
                  <Label
                    htmlFor={`analysis-${type.id}`}
                    className="cursor-pointer font-medium text-gray-900"
                  >
                    {type.label}
                  </Label>
                  <p className="mt-1 text-sm text-gray-600">{type.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
        {errors.analysisTypes && (
          <p className="text-sm text-red-600">{errors.analysisTypes.message}</p>
        )}
      </div>

      {/* Additional Notes */}
      <div className="space-y-2">
        <Label htmlFor="notes">Additional Notes (Optional)</Label>
        <Textarea
          id="notes"
          placeholder="Any specific concerns or areas to focus on..."
          rows={3}
          {...register("notes")}
        />
      </div>

      {/* Submit Button */}
      <div className="pt-4">
        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Processing Audit Request...
            </>
          ) : (
            <>
              Start TEE-Verified Audit
            </>
          )}
        </Button>
        <p className="mt-3 text-center text-sm text-gray-600">
          This audit will be processed in a Trusted Execution Environment with cryptographic proof recorded on-chain.
        </p>
      </div>
    </form>
  );
}