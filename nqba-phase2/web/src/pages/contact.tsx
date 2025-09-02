import { useState } from "react";
import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function Contact() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    businessUnit: "",
    message: ""
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setIsSubmitting(false);
    setSubmitSuccess(true);
    
    // Reset form after 3 seconds
    setTimeout(() => {
      setSubmitSuccess(false);
      setFormData({
        name: "",
        email: "",
        company: "",
        businessUnit: "",
        message: ""
      });
    }, 3000);
  };

  const businessUnits = [
    { value: "", label: "Select a business unit" },
    { value: "flyfox-ai", label: "FLYFOX AI - AI Platform & Automation" },
    { value: "goliath-capital", label: "Goliath Capital - Financial Services" },
    { value: "sigma-select", label: "Sigma Select - Lead Generation" },
    { value: "general", label: "General Inquiry" }
  ];

  return (
    <>
      <Header />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Contact Us
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
              Ready to transform your business with quantum-powered AI?
              Get in touch with our team to discuss your needs and explore our solutions.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Form & Information */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            
            {/* Contact Form */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-8">Send us a message</h2>
              
              {submitSuccess ? (
                <div className="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
                  <div className="text-5xl mb-4">✅</div>
                  <h3 className="text-xl font-bold text-green-800 mb-2">Message Sent Successfully!</h3>
                  <p className="text-green-700">We'll get back to you within 24 hours.</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                        Full Name *
                      </label>
                      <input
                        type="text"
                        id="name"
                        name="name"
                        required
                        value={formData.name}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter your full name"
                      />
                    </div>
                    
                    <div>
                      <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                        Email Address *
                      </label>
                      <input
                        type="email"
                        id="email"
                        name="email"
                        required
                        value={formData.email}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter your email"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
                        Company
                      </label>
                      <input
                        type="text"
                        id="company"
                        name="company"
                        value={formData.company}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter your company name"
                      />
                    </div>
                    
                    <div>
                      <label htmlFor="businessUnit" className="block text-sm font-medium text-gray-700 mb-2">
                        Business Unit
                      </label>
                      <select
                        id="businessUnit"
                        name="businessUnit"
                        value={formData.businessUnit}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        {businessUnits.map((unit) => (
                          <option key={unit.value} value={unit.value}>
                            {unit.label}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div>
                    <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                      Message *
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      required
                      rows={6}
                      value={formData.message}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Tell us about your needs and how we can help..."
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-full btn-primary py-4 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isSubmitting ? "Sending Message..." : "Send Message"}
                  </button>
                </form>
              )}
            </div>

            {/* Contact Information */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-8">Get in touch</h2>
              
              <div className="space-y-8">
                {/* General Contact */}
                <div className="bg-gray-50 rounded-xl p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-4">General Inquiries</h3>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                        <span className="text-white text-sm">📧</span>
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">Email</p>
                        <p className="text-gray-600">info@flyfoxai.com</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                        <span className="text-white text-sm">📞</span>
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">Phone</p>
                        <p className="text-gray-600">+1 (555) 123-4567</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Business Units Contact */}
                <div className="space-y-4">
                  <h3 className="text-xl font-bold text-gray-900">Business Unit Contacts</h3>
                  
                  <div className="bg-gradient-to-br from-orange-500 to-red-500 text-white rounded-xl p-6">
                    <h4 className="font-bold mb-2">FLYFOX AI</h4>
                    <p className="text-orange-100 mb-3">AI Platform & Business Automation</p>
                    <p className="text-sm">ai@flyfoxai.com</p>
                  </div>
                  
                  <div className="bg-gradient-to-br from-green-500 to-emerald-500 text-white rounded-xl p-6">
                    <h4 className="font-bold mb-2">Goliath Capital</h4>
                    <p className="text-green-100 mb-3">Financial Services & Investment</p>
                    <p className="text-sm">capital@goliath.com</p>
                  </div>
                  
                  <div className="bg-gradient-to-br from-blue-500 to-cyan-500 text-white rounded-xl p-6">
                    <h4 className="font-bold mb-2">Sigma Select</h4>
                    <p className="text-blue-100 mb-3">Lead Generation & Sales</p>
                    <p className="text-sm">sales@sigmaselect.com</p>
                  </div>
                </div>

                {/* Office Location */}
                <div className="bg-gray-50 rounded-xl p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-4">Office Location</h3>
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
                      <span className="text-white text-sm">📍</span>
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">Headquarters</p>
                      <p className="text-gray-600">
                        123 Quantum Boulevard<br />
                        Tech District<br />
                        San Francisco, CA 94105<br />
                        United States
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h2>
            <p className="text-xl text-gray-600">Common questions about our platform and services</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-3">What is the NQBA platform?</h3>
              <p className="text-gray-600">
                NQBA (Neuromorphic Quantum Business Architecture) is our core platform that combines quantum computing, 
                artificial intelligence, and neuromorphic computing to deliver 410x performance boost for business operations.
              </p>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-3">How does quantum computing improve performance?</h3>
              <p className="text-gray-600">
                Our Dynex quantum computing integration provides 410x performance boost for complex optimization problems, 
                machine learning tasks, and business analytics.
              </p>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-3">Can I integrate with existing systems?</h3>
              <p className="text-gray-600">
                Yes! Our platform is designed for seamless integration with existing business systems through our 
                comprehensive API suite and connector framework.
              </p>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-3">What industries do you serve?</h3>
              <p className="text-gray-600">
                We serve multiple industries including financial services, technology, healthcare, energy, 
                and more through our specialized business units.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Get Started?</h2>
          <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
            Join the future of business with our quantum-powered AI platform. 
            Schedule a consultation or demo to see how we can transform your operations.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/platform-dashboard" className="bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold hover:bg-gray-100 transition-colors">
              Access Platform Dashboard
            </Link>
            <Link href="/business-units" className="bg-blue-700 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-800 transition-colors">
              Explore Business Units
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
