import React from 'react';
import Head from 'next/head';
import { Shield, Lock, Eye, Database, Users, AlertCircle } from 'lucide-react';

const Privacy = () => {
  const lastUpdated = 'January 15, 2024';

  return (
    <>
      <Head>
        <title>Privacy Policy - Goliath QUANTUM</title>
        <meta name="description" content="Privacy Policy for Goliath QUANTUM. Learn how we collect, use, and protect your personal information and data." />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        {/* Hero Section */}
        <section className="relative py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="text-white">Privacy </span>
              <span className="text-gradient-gold">Policy</span>
            </h1>
            <p className="text-xl text-gray-300 mb-4">
              How we collect, use, and protect your information
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
              {/* Privacy Commitment */}
              <div className="bg-green-900 bg-opacity-50 border border-green-600 rounded-lg p-6 mb-8">
                <div className="flex items-start">
                  <Shield className="w-6 h-6 text-green-400 mr-3 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-lg font-semibold text-green-400 mb-2">Our Privacy Commitment</h3>
                    <p className="text-green-200 text-sm">
                      At Goliath QUANTUM, we are committed to protecting your privacy and ensuring the security of your personal information. 
                      This policy explains how we collect, use, and safeguard your data.
                    </p>
                  </div>
                </div>
              </div>

              <div className="prose prose-invert max-w-none">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
                  <Eye className="w-6 h-6 text-goliath-gold mr-2" />
                  1. Information We Collect
                </h2>
                <p className="text-gray-300 mb-4">
                  We collect information you provide directly to us, such as when you create an account, use our services, or contact us for support.
                </p>
                
                <h3 className="text-xl font-semibold text-white mb-3">Personal Information</h3>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• Name and contact information (email, phone number)</li>
                  <li>• Company information and job title</li>
                  <li>• Account credentials and authentication data</li>
                  <li>• Payment and billing information</li>
                  <li>• Communication preferences</li>
                </ul>

                <h3 className="text-xl font-semibold text-white mb-3">Usage Information</h3>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• Platform usage data and analytics</li>
                  <li>• Quantum computation requests and results</li>
                  <li>• API calls and integration data</li>
                  <li>• Performance metrics and system logs</li>
                  <li>• Device and browser information</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
                  <Database className="w-6 h-6 text-goliath-gold mr-2" />
                  2. How We Use Your Information
                </h2>
                <p className="text-gray-300 mb-4">
                  We use the information we collect to provide, maintain, and improve our services:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• Provide and operate the Goliath QUANTUM platform</li>
                  <li>• Process quantum computations and deliver results</li>
                  <li>• Authenticate users and maintain account security</li>
                  <li>• Send important service updates and notifications</li>
                  <li>• Provide customer support and technical assistance</li>
                  <li>• Improve our services and develop new features</li>
                  <li>• Comply with legal obligations and prevent fraud</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
                  <Lock className="w-6 h-6 text-goliath-gold mr-2" />
                  3. Data Security and Protection
                </h2>
                <p className="text-gray-300 mb-4">
                  We implement comprehensive security measures to protect your information:
                </p>
                
                <h3 className="text-xl font-semibold text-white mb-3">Encryption</h3>
                <ul className="text-gray-300 mb-4 space-y-2">
                  <li>• All data is encrypted in transit using TLS 1.3</li>
                  <li>• Data at rest is encrypted using AES-256</li>
                  <li>• Post-quantum cryptography for future-proof security</li>
                </ul>

                <h3 className="text-xl font-semibold text-white mb-3">Access Controls</h3>
                <ul className="text-gray-300 mb-4 space-y-2">
                  <li>• Multi-factor authentication for all accounts</li>
                  <li>• Role-based access control (RBAC)</li>
                  <li>• Regular security audits and penetration testing</li>
                </ul>

                <h3 className="text-xl font-semibold text-white mb-3">Quantum Security</h3>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• Quantum computations are performed in isolated environments</li>
                  <li>• Quantum-safe key exchange protocols</li>
                  <li>• Secure quantum result transmission</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
                  <Users className="w-6 h-6 text-goliath-gold mr-2" />
                  4. Information Sharing
                </h2>
                <p className="text-gray-300 mb-4">
                  We do not sell, trade, or otherwise transfer your personal information to third parties, except in the following circumstances:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• With your explicit consent</li>
                  <li>• To trusted service providers who assist in operating our platform</li>
                  <li>• When required by law or to protect our rights</li>
                  <li>• In connection with a business transfer or acquisition</li>
                </ul>

                <h3 className="text-xl font-semibold text-white mb-3">Third-Party Services</h3>
                <p className="text-gray-300 mb-4">
                  We work with trusted partners to provide our quantum computing services:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• DYNEX for quantum computing infrastructure</li>
                  <li>• Cloud providers for secure data storage</li>
                  <li>• Payment processors for billing (data is tokenized)</li>
                  <li>• Analytics providers (data is anonymized)</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4">5. Data Retention</h2>
                <p className="text-gray-300 mb-4">
                  We retain your information for as long as necessary to provide our services and comply with legal obligations:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• Account information: Retained while your account is active</li>
                  <li>• Quantum computation data: Retained for 90 days unless requested otherwise</li>
                  <li>• Usage logs: Retained for 12 months for security and analytics</li>
                  <li>• Billing information: Retained for 7 years for tax and legal compliance</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4">6. Your Rights and Choices</h2>
                <p className="text-gray-300 mb-4">
                  You have several rights regarding your personal information:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• Access: Request a copy of your personal information</li>
                  <li>• Correction: Update or correct inaccurate information</li>
                  <li>• Deletion: Request deletion of your personal information</li>
                  <li>• Portability: Request your data in a portable format</li>
                  <li>• Opt-out: Unsubscribe from marketing communications</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4">7. Cookies and Tracking</h2>
                <p className="text-gray-300 mb-4">
                  We use cookies and similar technologies to enhance your experience:
                </p>
                <ul className="text-gray-300 mb-6 space-y-2">
                  <li>• Essential cookies for platform functionality</li>
                  <li>• Analytics cookies to understand usage patterns</li>
                  <li>• Preference cookies to remember your settings</li>
                  <li>• Security cookies for fraud prevention</li>
                </ul>

                <h2 className="text-2xl font-bold text-white mb-4">8. International Data Transfers</h2>
                <p className="text-gray-300 mb-6">
                  Your information may be transferred to and processed in countries other than your own. We ensure appropriate safeguards are in place, including standard contractual clauses and adequacy decisions.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4">9. Children's Privacy</h2>
                <p className="text-gray-300 mb-6">
                  Our services are not intended for children under 13. We do not knowingly collect personal information from children under 13. If we become aware that we have collected such information, we will take steps to delete it.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4">10. Changes to This Policy</h2>
                <p className="text-gray-300 mb-6">
                  We may update this privacy policy from time to time. We will notify you of any material changes by posting the new policy on this page and updating the "last updated" date.
                </p>

                <h2 className="text-2xl font-bold text-white mb-4">11. Contact Us</h2>
                <p className="text-gray-300 mb-4">
                  If you have any questions about this privacy policy or our data practices, please contact us:
                </p>
                <div className="bg-gray-800 rounded-lg p-4 mb-6">
                  <p className="text-gray-300">Privacy Officer: privacy@goliathquantum.com</p>
                  <p className="text-gray-300">General Inquiries: hello@goliathquantum.com</p>
                  <p className="text-gray-300">Phone: +1-555-QUANTUM</p>
                  <p className="text-gray-300">Address: New York, NY, United States</p>
                </div>

                <div className="border-t border-gray-700 pt-6 mt-8">
                  <div className="flex items-start">
                    <AlertCircle className="w-5 h-5 text-yellow-400 mr-2 mt-1 flex-shrink-0" />
                    <p className="text-gray-400 text-sm">
                      This privacy policy is effective as of {lastUpdated}. We encourage you to review this policy periodically to stay informed about how we protect your information.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="card-quantum">
              <Lock className="w-16 h-16 text-goliath-gold mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-white mb-4">
                Questions About Your Privacy?
              </h2>
              <p className="text-gray-300 mb-6">
                Our privacy team is committed to transparency and protecting your rights. 
                Don't hesitate to reach out with any questions or concerns.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="/contact" className="btn-primary">
                  Contact Privacy Team
                </a>
                <a href="/terms" className="btn-secondary">
                  View Terms of Service
                </a>
              </div>
            </div>
          </div>
        </section>
      </div>
    </>
  );
};

export default Privacy;