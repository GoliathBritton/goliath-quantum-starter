import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/">
              <a className="flex items-center">
                <span className="text-xl font-bold text-gray-900">FLYFOX AI</span>
              </a>
            </Link>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <Link href="/dashboard">
              <a className="text-gray-700 hover:text-indigo-600 px-3 py-2 text-sm font-medium">
                Dashboard
              </a>
            </Link>
            <Link href="/integrations">
              <a className="text-gray-700 hover:text-indigo-600 px-3 py-2 text-sm font-medium">
                Integrations
              </a>
            </Link>
            <Link href="/security">
              <a className="text-gray-700 hover:text-indigo-600 px-3 py-2 text-sm font-medium">
                Security
              </a>
            </Link>
            <Link href="/pricing">
              <a className="text-gray-700 hover:text-indigo-600 px-3 py-2 text-sm font-medium">
                Pricing
              </a>
            </Link>
          </nav>
          
          <div className="flex items-center space-x-4">
            <div className="text-xs text-gray-500">
              Quantum Powered by Dynex
            </div>
            <button className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700">
              Get Started
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
