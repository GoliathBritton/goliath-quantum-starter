export default function Footer() {
  return (
    <footer className="bg-gray-50 border-t">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-6 mb-4 md:mb-0">
            <span className="text-sm text-gray-600">© 2024 FLYFOX AI. All rights reserved.</span>
            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              Quantum Powered by Dynex
            </span>
          </div>
          
          <div className="flex space-x-6">
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Privacy Policy
            </a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Terms of Service
            </a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Support
            </a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Contact
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
