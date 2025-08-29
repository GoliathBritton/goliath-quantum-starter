// Framer-ready export of pricing structure
// Import this file into Framer as a data module

export const pricing = {
  hero: {
    title: "The World’s First Quantum-Powered Intelligence Economy",
    subtitle: "FLYFOX AI and the Goliath family of companies unite quantum AI, blockchain, finance, energy, insurance, and education into one adaptive platform.",
    cta: [
      { label: "🚀 See Live Demos", href: "/demos" },
      { label: "📞 Book a Discovery Call", href: "/contact" }
    ]
  },
  onramp: {
    title: "✨ On-Ramp: Free Access",
    features: [
      "Quantum Demos (Limited Access)",
      "EduVerse AI Lite",
      "Instant Insurance Quotes (SFG)",
      "Discovery Call w/ SigmaEQ scoring"
    ],
    cta: { label: "🚀 Enter the Economy (Free)", href: "/signup" }
  },
  tiers: [
    {
      name: "Pro",
      price: "$1,500/mo",
      desc: "For ambitious SMBs ready to scale.",
      features: [
        "Sigma Select Copilot (Lite)",
        "Energy Scheduling (1 facility)",
        "EduVerse access for 100 learners",
        "Insurance & Capital pre-qual integrations"
      ],
      cta: { label: "Start My Pro Journey", href: "/signup?plan=pro" }
    },
    {
      name: "Growth",
      price: "$7,500/mo",
      desc: "For mid-market innovators.",
      highlight: true,
      features: [
        "Full Sigma Select Copilot",
        "Multi-facility Energy Optimization",
        "Capital pre-qualification engine",
        "EduVerse campus license"
      ],
      cta: { label: "Scale with Growth", href: "/signup?plan=growth" }
    },
    {
      name: "Enterprise Pilot",
      price: "$50,000/mo",
      desc: "For large enterprises testing quantum edge.",
      features: [
        "Quantum optimization workflows (Dynex-powered)",
        "Cross-pod orchestration",
        "Private EduVerse district instance",
        "Dedicated success manager"
      ],
      cta: { label: "Launch Enterprise Pilot", href: "/signup?plan=enterprise" }
    },
    {
      name: "Enterprise+",
      price: "$150,000/mo",
      desc: "For leaders shaping industries.",
      premium: true,
      features: [
        "6M FCUs + custom AI Pods",
        "Cross-border risk & finance modeling",
        "Energy + Insurance hedging bundles",
        "Annual Sigma Select leadership training",
        "24/7 AI Concierge"
      ],
      cta: { label: "Join Enterprise+", href: "/signup?plan=enterpriseplus" }
    },
    {
      name: "Strategic License",
      price: "$500k+/yr",
      desc: "For governments & Fortune 100 giants.",
      ultra: true,
      features: [
        "Private NQBA instance",
        "Gov/Defense-grade LTC compliance",
        "Global enterprise rollout",
        "On-premise deployment"
      ],
      cta: { label: "Request Private Access", href: "/contact?plan=strategic" }
    }
  ],
  upsells: {
    title: "🏛 Value-Add Upsells & Services",
    items: [
      "Implementation & Integration: $75k–$500k",
      "Sigma Select Training: $75k cohort / $500k annual",
      "EduVerse Expansion: $99 learner / $999 campus / $15k district",
      "Custom AI Pods: $100k–$1M bespoke builds"
    ]
  },
  successFees: {
    title: "📈 Aligned Success Fees",
    items: [
      "Capital: 4% of funded amounts",
      "Energy: 20% of verified savings",
      "Insurance (SFG): 15% of premiums",
      "Quantum Services: Usage-based credits ($0.25–$1/FCU)"
    ]
  },
  investors: {
    title: "👑 Investor & Partner Access",
    desc: "Exclusive access to ARR dashboards, pitch decks, and private showcases.",
    cta: { label: "Book Investor Meeting", href: "/investors" }
  }
};
