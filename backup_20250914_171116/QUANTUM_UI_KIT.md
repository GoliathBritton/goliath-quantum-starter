# 🚀 Quantum UI Kit - Phase 1

A premium React component library built for Next.js + Tailwind CSS, featuring quantum-enhanced animations and futuristic design elements.

## 📦 Components Included

### 1. ⚛️ QuantumBadge
A premium visual indicator with gradient styling and pulse animation.

```tsx
import QuantumBadge from "./components/QuantumBadge";

<QuantumBadge />
```

### 2. 🧑‍🚀 AgentCard
Interactive agent cards with hover effects and quantum badge integration.

```tsx
import AgentCard from "./components/AgentCard";

<AgentCard 
  name="Quantum Digital Agent" 
  role="Autonomous Deal Closer" 
  img="/agents/placeholder.svg" 
  quantum={true} 
/>
```

### 3. 💡 RoleTooltip
Contextual tooltips with role insights and elegant hover interactions.

```tsx
import RoleTooltip from "./components/RoleTooltip";

<RoleTooltip 
  label="Quantum Enhanced" 
  roleInsight="Powered by quantum algorithms for superior performance." 
/>
```

## 🎨 Quantum Animations

The kit includes several CSS animations in `src/styles/globals.css`:

- **gradient-x**: Flowing background gradients
- **quantum-pulse**: Subtle pulsing effects
- **quantum-glow**: Glowing border animations
- **quantum-float**: Floating particle effects

### Usage:
```tsx
// Quantum background
<div className="bg-quantum" />

// Quantum effects
<div className="quantum-pulse quantum-glow quantum-float" />
```

## 📁 File Structure

```
src/
├── components/
│   ├── QuantumBadge.tsx
│   ├── AgentCard.tsx
│   └── RoleTooltip.tsx
├── pages/
│   ├── agents.tsx          # Agent marketplace demo
│   └── quantum-demo.tsx    # Full component showcase
├── styles/
│   └── globals.css         # Quantum animations
└── index.tsx               # Component exports

public/
└── agents/
    └── placeholder.svg     # Agent avatar placeholder
```

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Import Components**
   ```tsx
   import { QuantumBadge, AgentCard, RoleTooltip } from './src';
   import './src/styles/globals.css';
   ```

3. **Use in Your App**
   ```tsx
   export default function MyApp() {
     return (
       <div className="bg-quantum min-h-screen">
         <QuantumBadge />
         <AgentCard name="AI Agent" role="Assistant" img="/avatar.svg" quantum />
         <RoleTooltip label="Info" roleInsight="Helpful information" />
       </div>
     );
   }
   ```

## 🎯 Demo Pages

- **Agent Marketplace**: `/src/pages/agents.tsx`
- **Component Showcase**: `/src/pages/quantum-demo.tsx`
- **Integration Demo**: `/src/index.tsx`

## ✨ Features

✅ **Quantum Badges** - Premium visual indicators with upsell signals  
✅ **Interactive Agent Marketplace** - Hover animations and quantum auras  
✅ **Role-based Tooltips** - Contextual insights with elegant animations  
✅ **Quantum Background** - Living gradient animations for premium feel  
✅ **Responsive Design** - Mobile-first approach with Tailwind CSS  
✅ **TypeScript Support** - Full type safety and IntelliSense  

## 🔮 Phase 2 Roadmap

- 🛠️ Quantum Workflow Builder with drag & drop
- 🌐 3D Entanglement Network Visualization
- 🎮 Interactive QUBO Solver Interface
- 🚀 Holographic UI Elements
- 🎯 Advanced Animation System

## 🎨 Color Palette

- **Quantum Violet**: `#8B5CF6`
- **Quantum Teal**: `#14B8A6`
- **Deep Space**: `#0f0f1f`
- **Cosmic Purple**: `#3b0764`
- **Quantum Gray**: `#1e293b`

---

**Ready for deployment** 🚀 Drop these files into your Next.js project and experience the quantum difference!