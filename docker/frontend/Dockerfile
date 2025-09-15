# FLYFOX AI - Frontend Dockerfile
# React/Next.js application with production optimizations

FROM node:18-alpine as base

# Set environment variables
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000

# Install system dependencies
RUN apk add --no-cache \
    libc6-compat \
    curl

# Set work directory
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Dependencies stage
FROM base as deps

# Copy package files
COPY package*.json ./
COPY yarn.lock* ./

# Install dependencies
RUN if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    else npm install; fi

# Builder stage
FROM base as builder

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules

# Copy source code
COPY . .

# Set build environment variables
ENV NEXT_PUBLIC_API_URL=https://api.flyfox.ai
ENV NEXT_PUBLIC_WS_URL=wss://api.flyfox.ai
ENV NEXT_PUBLIC_SENTRY_DSN=""
ENV NEXT_PUBLIC_ENVIRONMENT=production

# Build application
RUN if [ -f yarn.lock ]; then yarn build; \
    else npm run build; fi

# Production stage
FROM base as production

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start command
CMD ["node", "server.js"]

# Development stage
FROM base as development

# Install all dependencies (including dev)
COPY package*.json ./
COPY yarn.lock* ./

RUN if [ -f yarn.lock ]; then yarn install; \
    elif [ -f package-lock.json ]; then npm ci; \
    else npm install; fi

# Copy source code
COPY --chown=nextjs:nodejs . .

# Switch to non-root user
USER nextjs

# Set development environment
ENV NODE_ENV=development
ENV NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_WS_URL=ws://localhost:8000
ENV NEXT_PUBLIC_ENVIRONMENT=development

# Expose port
EXPOSE 3000

# Start development server
CMD if [ -f yarn.lock ]; then yarn dev; else npm run dev; fi

# Static export stage for CDN deployment
FROM builder as static

# Export static files
RUN if [ -f yarn.lock ]; then yarn export; \
    else npm run export; fi

# Nginx stage for static serving
FROM nginx:alpine as nginx

# Copy static files
COPY --from=static /app/out /usr/share/nginx/html

# Copy nginx configuration
COPY docker/frontend/nginx.conf /etc/nginx/nginx.conf

# Create non-root user for nginx
RUN adduser -D -s /bin/sh nginx-user

# Set proper permissions
RUN chown -R nginx-user:nginx-user /usr/share/nginx/html && \
    chown -R nginx-user:nginx-user /var/cache/nginx && \
    chown -R nginx-user:nginx-user /var/log/nginx && \
    chown -R nginx-user:nginx-user /etc/nginx/conf.d

# Switch to non-root user
USER nginx-user

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

# Default to production
FROM production