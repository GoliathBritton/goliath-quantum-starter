import React from 'react';
import Head from 'next/head';
import { BookOpen, Video, FileText, Globe, Lightbulb, Users } from 'lucide-react';

const Resources = () => {
  const resourceCategories = [
    {
      title: 'Documentation',
      description: 'Comprehensive guides and technical documentation for FLYFOX AI platform.',
      icon: BookOpen,
      items: [
        { name: 'FLYFOX AI Introduction', link: '/docs/FLYFOX_AI_Introduction.md' },
        { name: 'Resource Library', link: '/docs/FLYFOX_AI_Resource_Library.md' },
        { name: 'AI Forward 2023 Summit', link: '/docs/FLYFOX_AI_Forward_2023.md' },
        { name: 'LLMOps Guide', link: '/docs/FLYFOX_LLMOps.md' },
        { name: 'API Reference', link: '/docs/api-reference.md' },
        { name: 'Deployment Guide', link: '/docs/deployment.md' }
      ]
    },
    {
      title: 'Tutorials',
      description: 'Step-by-step tutorials to get started with FLYFOX AI and Goliath QUANTUM.',
      icon: Lightbulb,
      items: [
        { name: 'Getting Started with Goliath QUANTUM', link: '/tutorials/getting-started' },
        { name: 'Building Your First Quantum Model', link: '/tutorials/first-quantum-model' },
        { name: 'Integrating Sigma Select Analytics', link: '/tutorials/sigma-integration' },
        { name: 'Advanced LLM Monitoring', link: '/tutorials/llm-monitoring' }
      ]
    },
    {
      title: 'Videos & Webinars',
      description: 'Educational videos, webinars, and recorded sessions from FLYFOX AI experts.',
      icon: Video,
      items: [
        { name: 'AI Forward 2023 Keynote', link: 'https://www.youtube.com/watch?v=example' },
        { name: 'Quantum Computing Basics', link: 'https://www.youtube.com/watch?v=quantum-basics' },
        { name: 'LLM Security Best Practices', link: 'https://www.youtube.com/watch?v=llm-security' },
        { name: 'Goliath QUANTUM Demo', link: 'https://www.youtube.com/watch?v=goliath-demo' }
      ]
    },
    {
      title: 'Blog & Articles',
      description: 'Latest insights, case studies, and thought leadership from FLYFOX AI.',
      icon: FileText,
      items: [
        { name: 'The Future of AI Observability', link: '/blog/ai-observability' },
        { name: 'Quantum-Enhanced Business Intelligence', link: '/blog/quantum-bi' },
        { name: 'Securing LLMs in Enterprise', link: '/blog/llm-security' },
        { name: 'Sigma Select Success Stories', link: '/blog/sigma-success' }
      ]
    },
    {
      title: 'Community Resources',
      description: 'Join our community and access shared knowledge.',
      icon: Users,
      items: [
        { name: 'FLYFOX AI Forum', link: 'https://forum.flyfox.ai' },
        { name: 'GitHub Repository', link: 'https://github.com/flyfox-ai' },
        { name: 'Slack Community', link: 'https://slack.flyfox.ai' },
        { name: 'Quantum Architects Network', link: '/community/architects' }
      ]
    },
    {
      title: 'Global Resources',
      description: 'International documentation and multilingual support.',
      icon: Globe,
      items: [
        { name: 'Documentation in Spanish', link: '/docs/es' },
        { name: 'Documentation in Mandarin', link: '/docs/zh' },
        { name: 'International Case Studies', link: '/resources/international' }
      ]
    }
  ];

  return (
    <>
      <Head>
        <title>Resources Hub - FLYFOX AI</title>
        <meta name="description" content="Access all FLYFOX AI resources including documentation, tutorials, videos, and more for Goliath QUANTUM and Sigma Select." />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        {/* Hero Section */}
        <section className="relative py-20 px-4">
          <div className="max-w-6xl mx-auto text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="text-white">FLYFOX AI </span>
              <span className="text-gradient-gold">Resources Hub</span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-4xl mx-auto">
              Your central hub for all FLYFOX AI resources, documentation, tutorials, videos, and community support for Goliath QUANTUM and Sigma Select.
            </p>
          </div>
        </section>

        {/* Resources Grid */}
        <section className="py-16 px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {resourceCategories.map((category, index) => {
                const IconComponent = category.icon;
                return (
                  <div key={index} className="card-quantum p-6">
                    <div className="flex items-center mb-4">
                      <div className="w-12 h-12 bg-gradient-to-r from-goliath-gold to-yellow-400 rounded-full flex items-center justify-center mr-4">
                        <IconComponent className="w-6 h-6 text-gray-900" />
                      </div>
                      <h2 className="text-2xl font-bold text-white">{category.title}</h2>
                    </div>
                    <p className="text-gray-300 mb-6">{category.description}</p>
                    <ul className="space-y-3">
                      {category.items.map((item, i) => (
                        <li key={i}>
                          <a 
                            href={item.link} 
                            className="text-goliath-gold hover:text-yellow-300 transition-colors flex items-center"
                          >
                            <FileText className="w-4 h-4 mr-2" />
                            {item.name}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 px-4 bg-black bg-opacity-50">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Can't Find What You're Looking For?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Our Quantum Architects are here to help with any FLYFOX AI, Goliath, or Sigma Select questions.
            </p>
            <a href="/contact" className="btn-primary">
              Contact Support
            </a>
          </div>
        </section>
      </div>
    </>
  );
};

export default Resources;