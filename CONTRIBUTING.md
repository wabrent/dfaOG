# Contributing to DeFi Risk Auditor

Thank you for your interest in contributing to DeFi Risk Auditor! This document outlines the process for contributing to the project.

## Development Environment

### Prerequisites

- Python 3.11+ for backend development
- Node.js 18+ for frontend development
- Git for version control
- OpenGradient API access (testnet tokens from faucet)

### Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/dfaOG.git
   cd dfaOG
   ```

3. **Set up backend**:
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
   ```

4. **Set up frontend**:
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

5. **Run development servers**:
   ```bash
   # Terminal 1: Backend
   cd backend
   uvicorn app.main:app --reload --port 8000
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

## Development Workflow

### 1. Create a Branch

Create a feature branch from `main`:
```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation changes
- `refactor/` for code refactoring

### 2. Make Changes

Follow the existing code style and conventions:

#### Backend (Python)
- Use type hints for all function signatures
- Follow Pydantic schemas for data validation
- Add docstrings for public functions and classes
- Use async/await for I/O operations

#### Frontend (TypeScript/React)
- Use TypeScript strict mode
- Follow React hooks best practices
- Use Tailwind CSS for styling
- Implement responsive design

### 3. Test Your Changes

#### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

#### Frontend Tests
```bash
cd frontend
npm test
```

### 4. Commit Your Changes

Use conventional commit messages:
```bash
git commit -m "feat: add protocol data collection from DeFiLlama"
```

Commit message format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots for UI changes
- Test results

## Project Structure

### Backend Architecture

```
backend/
├── app/
│   ├── api/           # FastAPI routes
│   ├── core/          # Configuration and utilities
│   ├── models/        # Pydantic schemas
│   └── services/      # Business logic
│       ├── opengradient_client.py    # OpenGradient integration
│       ├── protocol_data.py          # Protocol data collection
│       └── audit_pipeline.py         # Main audit pipeline
├── tests/             # Test files
└── requirements.txt   # Python dependencies
```

### Frontend Architecture

```
frontend/
├── app/               # Next.js app router pages
├── components/        # Reusable React components
│   ├── ui/           # Basic UI components
│   ├── audit/        # Audit-specific components
│   └── layout/       # Layout components
├── lib/              # Utilities and hooks
│   ├── api.ts        # API client
│   ├── types.ts      # TypeScript types
│   └── utils.ts      # Helper functions
└── styles/           # CSS and Tailwind configuration
```

## Adding New Features

### 1. New Protocol Data Source

1. Create a new service in `backend/app/services/`
2. Implement data collection and transformation
3. Add to `ProtocolDataService` in `protocol_data.py`
4. Update API response schemas if needed
5. Add tests for the new data source

### 2. New Risk Dimension

1. Update `DimensionAnalysis` schema in `schemas.py`
2. Add to risk analysis prompt in `opengradient_client.py`
3. Update frontend components to display new dimension
4. Add visualization if applicable

### 3. UI Component

1. Create component in `frontend/components/`
2. Add TypeScript interfaces
3. Implement with Tailwind CSS
4. Add Storybook stories if applicable
5. Export from appropriate index file

## Code Standards

### Python
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

### TypeScript
- Prettier for code formatting
- ESLint for linting
- TypeScript strict mode enabled

### Git
- Keep commits focused and atomic
- Write meaningful commit messages
- Rebase feature branches before merging
- Squash fixup commits

## Testing

### Backend Tests
- Use pytest for testing
- Mock external API calls
- Test both success and error cases
- Aim for >80% code coverage

### Frontend Tests
- Use Jest and React Testing Library
- Test component rendering and interactions
- Mock API responses
- Test accessibility

### Integration Tests
- Test complete audit pipeline
- Verify OpenGradient integration
- Test error handling and edge cases

## Documentation

### Code Documentation
- Document all public functions and classes
- Include examples for complex functionality
- Keep README and CONTRIBUTING updated

### API Documentation
- Keep OpenAPI schema updated
- Document all endpoints and parameters
- Include example requests and responses

## Release Process

1. **Version Bump**: Update version in `package.json` and `pyproject.toml`
2. **Changelog**: Update CHANGELOG.md with changes
3. **Tests**: Run full test suite
4. **Build**: Verify build process works
5. **Tag**: Create Git tag for release
6. **Deploy**: Deploy to production environments

## Getting Help

- Open an issue for bug reports or feature requests
- Join the discussion in GitHub Discussions
- Check existing documentation and examples

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.