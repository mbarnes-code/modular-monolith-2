# Jane UI

The primary user interface for the Jane Monorepo. Built with Next.js 15 and React 19, providing a modern, responsive experience for interacting with LLM services.

## Purpose

Jane UI provides:
- User interface for submitting queries to LLM services
- Real-time response visualization
- Query history and management
- Multi-domain support (Cyber, MTG, Code)
- Responsive design for desktop and mobile

## Technology Stack

- **Framework**: Next.js 15.5.2
- **UI Library**: React 19.1.0
- **TypeScript**: 5.8.3
- **Node.js**: 20.x
- **Styling**: Tailwind CSS (via shared UI library)

## Setup

### Prerequisites

- Node.js 20.x
- npm

### Installation

```bash
# Install dependencies (from root)
npm install
```

### Configuration

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Key environment variables:
- `NEXT_PUBLIC_API_URL`: URL for Jane Orchestrator API
- `NODE_ENV`: Environment (development, production)
- `NEXT_PUBLIC_LOG_LEVEL`: Client-side logging level

## Running the Application

### Development

```bash
# Using NX (recommended)
npx nx serve jane-ui

# Direct with Next.js
cd apps/jane-ui
npm run dev
```

Access at: http://localhost:3000

### Production Build

```bash
# Build
npx nx build jane-ui

# Start production server
cd dist/apps/jane-ui
npm start
```

### Docker

```bash
# Build
docker build -t jane-ui:latest -f apps/jane-ui/Dockerfile .

# Run
docker run -p 3000:3000 jane-ui:latest
```

## Features

### Query Submission
- Multi-line text input
- Domain selection (Cyber, MTG, Code)
- Context and options configuration
- Real-time validation

### Response Display
- Markdown rendering
- Syntax highlighting for code
- Confidence scores
- Source attribution

### History
- Query and response history
- Search and filtering
- Export capabilities

### User Experience
- Responsive design
- Dark/light mode
- Keyboard shortcuts
- Accessibility compliant (WCAG 2.1)

## Project Structure

```
jane-ui/
├── src/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/              # Utilities and helpers
│   ├── hooks/            # Custom React hooks
│   └── styles/           # Global styles
├── public/               # Static assets
├── .env.example          # Environment template
├── next.config.js        # Next.js configuration
├── package.json          # Dependencies
└── tsconfig.json         # TypeScript config
```

## API Integration

The UI communicates with Jane Orchestrator via REST API:

```typescript
// Example query submission
const response = await fetch(`${API_URL}/query`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'User query here',
    domain: 'cyber',
  }),
});
```

## Health Endpoints

The UI exposes health endpoints for monitoring:

- **GET /api/health**: Basic health check
- Returns: `{ status: 'healthy' }`

## Deployment

### Vercel (Recommended)

```bash
vercel deploy
```

### Kubernetes

```bash
kubectl apply -k infrastructure/kubernetes/overlays/production/
```

### Docker Compose

```bash
docker-compose -f infrastructure/docker/docker-compose.yml up jane-ui
```

## Development

### Adding New Features

1. Create component in `src/components/`
2. Add route in `src/app/`
3. Integrate with API
4. Write tests
5. Update documentation

### Testing

```bash
# Run tests
npx nx test jane-ui

# E2E tests
npx nx e2e jane-ui-e2e
```

### Linting

```bash
# Lint
npx nx lint jane-ui

# Format
npx prettier --write apps/jane-ui
```

## Environment Variables

See `.env.example` for all available configuration options.

**Required:**
- `NEXT_PUBLIC_API_URL`: Orchestrator API endpoint

**Optional:**
- `NEXT_PUBLIC_ENABLE_ANALYTICS`: Enable analytics
- `NEXT_PUBLIC_ENABLE_BETA_FEATURES`: Enable beta features

## Performance

### Optimization Techniques

- Server components for static content
- Client components for interactivity
- Code splitting with dynamic imports
- Image optimization with Next.js Image
- Font optimization with next/font

### Monitoring

- Core Web Vitals tracking
- Error boundary implementation
- Performance metrics logging

## Accessibility

- WCAG 2.1 Level AA compliant
- Keyboard navigation support
- Screen reader compatible
- High contrast mode
- Focus management

## Production Operations

### Pre-Production Validation

```bash
npm run validate:phase4    # Validate all constitutional requirements
```

### Full Deployment Pipeline

```bash
npm run deploy:production  # Full production deployment pipeline
```

### Production Monitoring

```bash
npm run monitor:production # Start production monitoring
```

The production deployment process includes:

1. Pre-deployment validation checks
2. Bundle optimization and validation
3. Performance threshold verification
4. Asset optimization
5. Constitutional compliance validation
6. Health check verification

See `/docs/PRODUCTION-MAINTENANCE.md` for detailed maintenance procedures.

## Performance Monitoring

The application includes built-in performance monitoring:

- Bundle size tracking with constitutional limits
- Load time monitoring with <200ms UI interaction targets
- Memory usage tracking for executive function support
- Real-time alerts for performance degradation

### Bundle Analysis

```bash
npm run analyze-bundle     # Interactive bundle analyzer
npm run bundle-size-check  # Check current bundle sizes
npm run bundle-size-validate # Validate against limits
```

### Performance Auditing

```bash
npm run performance-audit  # Run Lighthouse audit
npm run test:e2e          # End-to-end performance tests
```

## Troubleshooting

### Common Issues

**Port 3000 already in use:**

```bash
# Change port
PORT=3001 npm run dev
```

**API connection errors:**

- Verify `NEXT_PUBLIC_API_URL` is correct
- Check orchestrator is running
- Verify CORS configuration

**Build errors:**

- Clear `.next` directory
- Remove `node_modules` and reinstall
- Check TypeScript errors

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for development workflow and guidelines.

## License

See repository root for license information.
