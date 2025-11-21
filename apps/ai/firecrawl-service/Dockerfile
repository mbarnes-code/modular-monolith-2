# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY nx.json ./
COPY tsconfig.base.json ./

# Copy source code for the app and its dependencies
COPY apps/firecrawl-service ./apps/firecrawl-service
COPY libs/firecrawl-core ./libs/firecrawl-core
COPY libs/firecrawl-types ./libs/firecrawl-types

# Install dependencies
RUN npm ci

# Build the application
RUN npx nx build firecrawl-service --prod

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Copy built application
COPY --from=builder /app/dist/apps/firecrawl-service ./
COPY --from=builder /app/node_modules ./node_modules

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S firecrawl -u 1001

USER firecrawl

EXPOSE 3002

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3002/health || exit 1

CMD ["node", "main.js"]