# DeFi Risk Auditor

TEE-verified DeFi protocol risk analysis with on-chain cryptographic proof.

## Overview

DeFi Risk Auditor provides verifiable risk assessments for DeFi protocols using OpenGradient's TEE (Trusted Execution Environment) infrastructure. Each audit includes cryptographic proof recorded on-chain, ensuring transparency and auditability.

## Key Features

- **TEE-Verified Analysis**: AI risk assessment executed in Intel SGX/AMD SEV enclaves
- **On-Chain Proof**: Every audit includes transaction hash as cryptographic attestation
- **Multi-Dimensional Scoring**: TVL risk, approval risk, code complexity, governance health, economic security
- **Developer-Focused**: Actionable insights for protocol developers and security teams
- **Transparent Methodology**: All analysis criteria and confidence levels publicly documented

## Architecture

```
Frontend (Next.js) → Backend (FastAPI) → OpenGradient SDK → TEE Enclave → On-chain Proof
```

## Risk Assessment Dimensions

1. **TVL Concentration Risk** - Protocol dependency on few large depositors
2. **Approval Risk** - Unlimited token approvals and security implications
3. **Code Complexity** - Smart contract audit scores and complexity metrics
4. **Governance Health** - DAO participation, proposal velocity, voter concentration
5. **Economic Security** - Attack cost vs. profit incentives
6. **Liquidity Risk** - Depth and stability of liquidity pools

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Development Scripts (Root)

You can also run both frontend and backend concurrently using the root package.json scripts:

```bash
npm install
npm run dev
```

This will start both the backend (port 8000) and frontend (port 3000) simultaneously.

## Configuration

### Environment Variables (Backend)

```env
# OpenGradient Configuration
OPENGRADIENT_PRIVATE_KEY=your_private_key_here
OPENGRADIENT_SETTLEMENT_MODE=BATCH_HASHED  # PRIVATE, BATCH_HASHED, INDIVIDUAL_FULL
OPENGRADIENT_MODEL=GPT_5  # GPT_5, CLAUDE_SONNET_4_6, GEMINI_2_5_PRO, etc.

# API Keys (Optional - for enhanced data)
DEFILLAMA_API_KEY=your_defillama_key_here
ETHERSCAN_API_KEY=your_etherscan_key_here
ALCHEMY_API_KEY=your_alchemy_key_here

# Backend Configuration
REDIS_URL=redis://localhost:6379
CACHE_TTL=300  # seconds
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600  # seconds

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

### Frontend Environment

Create `.env.local` in frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="DeFi Risk Auditor"
NEXT_PUBLIC_APP_DESCRIPTION="TEE-verified DeFi protocol risk analysis"
```

## Supported Protocols

- Uniswap V2/V3
- Aave V2/V3
- Compound V2/V3
- MakerDAO
- Lido
- Curve
- Balancer
- Custom contract addresses

## API Reference

### POST /api/audit

Analyze a DeFi protocol's risk with TEE-verified AI.

**Request:**
```json
{
  "protocol_address": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
  "protocol_name": "Uniswap V3",
  "chain": "ethereum",
  "include_enhanced_data": true
}
```

**Response:**
```json
{
  "protocol": "Uniswap V3",
  "address": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
  "chain": "ethereum",
  "risk_score": 24,
  "risk_level": "LOW",
  "confidence": 87,
  "dimensions": {
    "tvl_risk": "LOW",
    "approval_risk": "MEDIUM",
    "code_risk": "LOW",
    "governance_risk": "LOW",
    "economic_risk": "LOW",
    "liquidity_risk": "LOW"
  },
  "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
  "recommendations": [
    {
      "priority": "HIGH",
      "title": "Implement approval limits",
      "description": "Consider implementing approval limits for users",
      "action_items": ["Add max approval amount setting", "Implement expiration for approvals"]
    }
  ],
  "proof": {
    "transaction_hash": "0x...",
    "settlement_mode": "BATCH_HASHED",
    "model": "GPT-5",
    "timestamp": "2026-04-09T20:52:00Z",
    "explorer_url": "https://sepolia.basescan.org/tx/0x..."
  }
}
```

### GET /api/health

Check API health and OpenGradient connection status.

### GET /api/protocols

Get list of known protocols for quick analysis.

### GET /api/verify/{tx_hash}

Verify an audit proof by transaction hash.

## Development

### Project Structure

```
defi_risk_auditor/
├── backend/
│   ├── app/
│   │   ├── api/routes.py           # API endpoints
│   │   ├── core/config.py          # Configuration
│   │   ├── models/schemas.py       # Pydantic schemas
│   │   └── services/               # Business logic
│   │       ├── opengradient_client.py
│   │       ├── protocol_data.py
│   │       └── audit_pipeline.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/                        # Next.js app router
│   ├── components/                 # React components
│   ├── lib/                        # Utilities and types
│   ├── package.json
│   └── tailwind.config.ts
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

### Adding New Protocols

1. Add protocol address to `known_protocols` in `backend/app/services/protocol_data.py`
2. Implement protocol-specific data collection if needed
3. Update frontend protocol dropdown if applicable

## Deployment

### Backend (Railway/Fly.io)

```bash
# Build command
pip install -r requirements.txt

# Start command
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel)

Set environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`: Your backend API URL
- `NEXT_PUBLIC_APP_NAME`: Application name
- `NEXT_PUBLIC_APP_DESCRIPTION`: Application description

### Full Stack (Render.com)

Deploy the complete application stack (backend, frontend, and Redis) on Render.com:

1. **Create a Render Account**: Sign up at [render.com](https://render.com)

2. **Connect GitHub Repository**: Connect your GitHub repository containing this project

3. **Deploy using render.yaml**: Render will automatically detect the `render.yaml` file and provision all services:
   - Backend API service (Python)
   - Frontend web service (Node.js)
   - Redis cache service

4. **Configure Environment Variables**:
   - Set `OPENGRADIENT_PRIVATE_KEY` in the backend service
   - Other variables are pre-configured in `render.yaml`

5. **Access Your Application**:
   - Frontend: `https://defi-risk-auditor-frontend.onrender.com`
   - Backend API: `https://defi-risk-auditor-backend.onrender.com`
   - API Documentation: `https://defi-risk-auditor-backend.onrender.com/docs`

The `render.yaml` file includes:
- Auto-deployment on git push
- Health checks for backend service
- Redis cache for rate limiting and session storage
- CORS configuration for frontend-backend communication

### Troubleshooting Render Deployment

If the Blueprint deployment fails, you can manually create the services:

**Manual Deployment Steps:**

1. **Create Backend Web Service (Python):**
   - **Name**: `defi-risk-auditor-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/api/health`
   - **Environment Variables**:
     ```
     OPENGRADIENT_PRIVATE_KEY=your_opengradient_private_key_here
     OPENGRADIENT_SETTLEMENT_MODE=BATCH_HASHED
     OPENGRADIENT_MODEL=GPT_5
     REDIS_URL=redis://localhost:6379
     CORS_ORIGINS=["https://*.onrender.com", "http://localhost:3000"]
     ```

2. **Create Frontend Web Service (Node.js):**
   - **Name**: `defi-risk-auditor-frontend`
   - **Runtime**: `Node`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Start Command**: `cd frontend && npm start`
   - **Environment Variables**:
     ```
     NEXT_PUBLIC_API_URL=https://defi-risk-auditor-backend.onrender.com
     NEXT_PUBLIC_APP_NAME=DeFi Risk Auditor
     NEXT_PUBLIC_APP_DESCRIPTION=TEE-verified DeFi protocol risk analysis with on-chain proof
     NODE_ENV=production
     ```

3. **Optional: Create Redis Service** (only if needed for caching):
   - **Name**: `redis`
   - **Type**: `Redis`
   - **Plan**: `Free`

**Common Issues:**
- **Frontend fails to build**: Ensure Node.js version >=18 (specified in `frontend/package.json`)
- **Backend fails to start**: Check if OpenGradient package installed correctly
- **CORS errors**: Update `CORS_ORIGINS` to include your frontend URL
- **Health check fails**: The `/api/health` endpoint may fail if OpenGradient isn't configured

## Verification

Every audit can be independently verified:

1. **Check on-chain proof**: Visit the transaction hash on Base Sepolia explorer
2. **Replicate analysis**: Use the same protocol address and parameters
3. **Validate methodology**: All prompts and scoring criteria are open-source

## Security Considerations

- Private keys are never transmitted to OpenGradient (only signatures)
- All sensitive data is processed within TEE enclaves
- Audit results are immutable once recorded on-chain
- No personal or wallet data is collected

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool provides risk assessments for informational purposes only. It does not constitute financial, investment, or security advice. Always conduct your own research and consult with professional security auditors before making decisions.