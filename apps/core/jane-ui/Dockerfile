# Multi-stage build for Jane UI

# Dependencies stage
FROM node:20-alpine AS deps

RUN apk add --no-cache libc6-compat python3 make g++

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./
COPY apps/jane-ui/package.json ./apps/jane-ui/
COPY nx.json tsconfig.base.json ./

# Install dependencies
RUN npm ci

# Builder stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json ./package.json

# Copy source code
COPY . .

# Build jane-ui
RUN npx nx build jane-ui

# Runtime stage
FROM node:20-alpine AS runtime

ENV NODE_ENV=production

WORKDIR /app

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Copy built application and necessary files
COPY --from=builder --chown=appuser:appuser /app/dist/apps/jane-ui/.next ./apps/jane-ui/.next
COPY --from=builder --chown=appuser:appuser /app/apps/jane-ui/public ./apps/jane-ui/public
COPY --from=builder --chown=appuser:appuser /app/apps/jane-ui/package.json ./apps/jane-ui/
COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules

WORKDIR /app/apps/jane-ui

USER appuser

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"

CMD ["npm", "start"]
