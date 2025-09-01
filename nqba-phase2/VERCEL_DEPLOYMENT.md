# 🚀 VERCEL DEPLOYMENT GUIDE

## Quick Deploy (1-Click)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FGoliathBritton%2Fgoliath-quantum-starter&project-name=nqba-phase2&root-directory=nqba-phase2%2Fweb)

## Manual Setup

### 1. Prerequisites
- Vercel account (free)
- GitHub repo with this code
- Domain ready (optional)

### 2. Deploy Steps

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to web directory
cd nqba-phase2/web

# Deploy
vercel --prod
```

### 3. Environment Variables

Set these in Vercel dashboard:
```
NEXT_PUBLIC_API_BASE=https://api.flyfoxai.io
```

### 4. Custom Domain

In Vercel dashboard:
1. Go to Domains
2. Add: `portal.goliathomniedge.com`
3. Update DNS records as shown

## 📍 Live URLs

**Frontend**: https://portal.goliathomniedge.com
**API**: Deploy separately to Render/Railway/Fly

## 🔗 Next Steps

1. **API Deployment**: Use Railway/Render for FastAPI backend
2. **Domain Setup**: Point `portal.flyfoxai.io` to Vercel
3. **Analytics**: Add Vercel Analytics
4. **Monitoring**: Enable Vercel Edge Functions

## 💰 Immediate Revenue Setup

- **Pricing Page**: `/pricing` - ready for Stripe integration
- **Demo Booking**: Calendly links active
- **Lead Capture**: Contact forms working

## 🚀 Performance Optimizations

- Next.js 14 App Router
- Static generation where possible
- Edge functions for dynamic content
- CDN-optimized assets

---

**Ready to go live in 3 minutes!** 🚀
