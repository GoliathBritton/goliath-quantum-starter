import React from 'react';

const PlatformOverview = () => {
  return (
    <div className="bg-white min-h-screen">
      {/* Header Navigation */}
      <header className="bg-indigo-600 text-white py-4 px-6">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Prismatic</h1>
          <nav>
            <ul className="flex space-x-6">
              <li><a href="#" className="hover:underline">Platform</a></li>
              <li><a href="#" className="hover:underline">Pricing</a></li>
              <li><a href="#" className="hover:underline">Resources</a></li>
              <li><a href="#" className="hover:underline">Company</a></li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Content Container */}
      <div className="max-w-7xl mx-auto flex py-8 px-6">
        {/* Left Sidebar */}
        <aside className="w-64 pr-8">
          <nav>
            <ul className="space-y-4">
              <li><a href="#our-platform" className="text-indigo-600 hover:text-indigo-800">Our Platform</a></li>
              <li><a href="#build" className="text-indigo-600 hover:text-indigo-800">Build</a></li>
              <li><a href="#deploy" className="text-indigo-600 hover:text-indigo-800">Deploy</a></li>
              <li><a href="#manage" className="text-indigo-600 hover:text-indigo-800">Manage</a></li>
            </ul>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1">
          <section id="our-platform" className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Our Platform</h2>
            <p className="text-gray-600">Integrated platform for AI-driven business decisions and coding assistance.</p>
          </section>
          <section id="build" className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Build</h2>
            <p className="text-gray-600">Tools and prompts to build applications efficiently.</p>
          </section>
          <section id="deploy" className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Deploy</h2>
            <p className="text-gray-600">Seamless deployment options for your projects.</p>
          </section>
          <section id="manage" className="mb-12">
            <h2 className="text-3xl font-bold mb-4">Manage</h2>
            <p className="text-gray-600">Manage your AI assistants and tasks.</p>
          </section>
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4">How We Compare</h2>
            <div className="grid grid-cols-4 gap-4 bg-gray-100 p-4 rounded-lg">
              <div className="font-bold">Feature</div>
              <div className="font-bold">Prismatic</div>
              <div className="font-bold">Competitor A</div>
              <div className="font-bold">Competitor B</div>
              <div>AI Prompt Integration</div>
              <div>Yes</div>
              <div>No</div>
              <div>Yes</div>
              <div>Decision Making Tools</div>
              <div>Advanced</div>
              <div>Basic</div>
              <div>None</div>
              <div>UI Conversion</div>
              <div>Yes</div>
              <div>Yes</div>
              <div>No</div>
            </div>
          </section>
          <section>
            <h2 className="text-3xl font-bold mb-4">Our Customers</h2>
            <div className="flex space-x-8">
              <img src="/placeholder-logo1.svg" alt="Customer 1" className="h-16" />
              <img src="/placeholder-logo2.svg" alt="Customer 2" className="h-16" />
              <img src="/placeholder-logo3.svg" alt="Customer 3" className="h-16" />
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default PlatformOverview;