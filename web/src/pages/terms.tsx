import React from 'react';
import Head from 'next/head';
import { Shield, FileText, Users, AlertTriangle } from 'lucide-react';

const Terms = () => {
  const lastUpdated = 'January 15, 2024';

  return (
    <>
      <Head>
        <title>Terms of Service - Goliath QUANTUM</title>
        <meta name="description" content="Terms of Service for Goliath QUANTUM platform. Read our legal terms and conditions for using our quantum intelligence services." />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        {/* Hero Section */}
        <section className="relative py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="text-white">Terms of </span>
              <span className="text-gradient-gold">Service</span>
            </h1>
            <p className="text-xl text-gray-300 mb-4">
              Legal terms and conditions for using Goliath QUANTUM services
            </p>
            <p className="text-gray-400">
              Last updated: {lastUpdated}
            </p>
          </div>
        </section>

        {/* Content */}
        <section className="py-16 px-4">
          <div className="max-w-4xl mx-auto">
            <div className="card-quantum">
              {/* Important Notice */}
              <div className="bg-yellow-900 bg-opacity-50 border border-yellow-600 rounded-lg p-6 mb-8">
                <div className="flex items-start">
                  <AlertTriangle className="w-6 h-6 text-yellow-400 mr-3 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-lg font-semibold text-yellow-400 mb-2">Important Notice</h3>
                    <p className="text-yellow-200 text-sm">
                      Please read these Terms of Service carefully before using our platform. 
                      By accessing or using Goliath QUANTUM services, you agree to be bound by these terms.
                    </p>
                  </div>
                </div>
              </div>

              <div className="prose prose-invert max-w-none">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
                  <FileText className="w-6 h-6 text-goliath-gold mr-2" />
                  1. Acceptance of Terms
                </h2>
                <p className="text-gray-300 mb-6">
                  By accessing and using the Goliath QUANTUM platform ("Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
                  <Users className="w-6 h-6 text-goliath-gold mr-2" />
                  2. Use License
                </h2>
                <p className="text-gray-300 mb-4">
                  Permission is granted to temporarily access and use the Goliath QUANTUM platform for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• Modify or copy the materials</li>
                  <li>• Use the materials for any commercial purpose or for any public display</li>
                  <li>• Attempt to reverse engineer any software contained on the platform</li>
                  <li>• Remove any copyright or other proprietary notations from the materials</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4">3. Quantum Computing Services</h2>
                <p className="text-gray-300 mb-4">
                  Our quantum computing services are provided "as is" and are subject to the following terms:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• Quantum computations are performed on third-party quantum computing platforms</li>
                  <li>• Results may vary based on quantum hardware availability and performance</li>
                  <li>• We do not guarantee specific computation times or availability</li>
                  <li>• Users are responsible for validating quantum computation results</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4">4. User Accounts</h2>
                <p className="text-gray-300 mb-4">
                  When you create an account with us, you must provide information that is accurate, complete, and current at all times. You are responsible for safeguarding the password and for all activities that occur under your account.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4">5. Data Privacy and Security</h2>
                <p className="text-gray-300 mb-4">
                  We take data privacy seriously and implement enterprise-grade security measures:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• All data is encrypted in transit and at rest</li>
                  <li>• We use post-quantum cryptography for enhanced security</li>
                  <li>• User data is never shared with third parties without explicit consent</li>
                  <li>• Quantum computations are performed in isolated environments</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4">6. Intellectual Property</h2>
                <p className="text-gray-300 mb-6">
                  The service and its original content, features, and functionality are and will remain the exclusive property of Goliath QUANTUM and its licensors. The service is protected by copyright, trademark, and other laws.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4">7. Prohibited Uses</h2>
                <p className="text-gray-300 mb-4">
                  You may not use our service:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• For any unlawful purpose or to solicit others to perform unlawful acts</li>
                  <li>• To violate any international, federal, provincial, or state regulations, rules, laws, or local ordinances</li>
                  <li>• To infringe upon or violate our intellectual property rights or the intellectual property rights of others</li>
                  <li>• To harass, abuse, insult, harm, defame, slander, disparage, intimidate, or discriminate</li>
                  <li>• To submit false or misleading information</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4">8. Service Availability</h2>
                <p className="text-gray-300 mb-6">
                  We strive to maintain high availability but do not guarantee that the service will be available 100% of the time. Quantum computing resources may be subject to maintenance, upgrades, or third-party limitations.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4">9. Limitation of Liability</h2>
                <p className="text-gray-300 mb-6">
                  In no event shall Goliath QUANTUM, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your use of the service.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4">10. Termination</h2>
                <p className="text-gray-300 mb-6">
                  We may terminate or suspend your account and bar access to the service immediately, without prior notice or liability, under our sole discretion, for any reason whatsoever and without limitation, including but not limited to a breach of the Terms.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4">11. Changes to Terms</h2>
                <p className="text-gray-300 mb-6">
                  We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is material, we will provide at least 30 days notice prior to any new terms taking effect.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4">12. Contact Information</h2>
                <p className="text-gray-300 mb-4">
                  If you have any questions about these Terms of Service, please contact us:
                </p>
                <div className="bg-gray-800 rounded-lg p-4 mb-6">
                  <p className="text-gray-300">Email: legal@goliathquantum.com</p>
                  <p className="text-gray-300">Phone: +1-555-QUANTUM</p>
                  <p className="text-gray-300">Address: New York, NY, United States</p>
                </div>

                <div className="border-t border-gray-700 pt-6 mt-8">
                  <p className="text-gray-400 text-sm">
                    These terms of service are effective as of {lastUpdated} and will remain in effect except with respect to any changes in its provisions in the future, which will be in effect immediately after being posted on this page.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="card-quantum">
              <Shield className="w-16 h-16 text-goliath-gold mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-4">
                Questions About Our Terms?
              </h2>
              <p className="text-gray-300 mb-6">
                Our legal team is here to help clarify any questions you may have about our terms of service.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="/contact" className="btn-primary">
                  Contact Legal Team
                </a>
                <a href="/privacy" className="btn-secondary">
                  View Privacy Policy
                </a>
              </div>
            </div>
          </div>
        </section>
      </div>
    </>
  );
};

export default Terms;