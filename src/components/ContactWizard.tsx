"use client"

import { useState } from 'react'
import { 
  Upload, 
  Database, 
  Zap, 
  Target, 
  Users, 
  BarChart3, 
  CheckCircle, 
  ArrowRight,
  FileText,
  Mail,
  MessageSquare,
  Phone,
  Globe,
  Brain,
  Rocket
} from 'lucide-react'

interface ContactData {
  company_name: string
  contact_name: string
  title?: string
  phone?: string
  email: string
  industry?: string
  company_size?: string
  annual_revenue?: string
}

interface WizardStep {
  id: string
  title: string
  description: string
  icon: any
  completed: boolean
}

export default function ContactWizard() {
  const [currentStep, setCurrentStep] = useState(0)
  const [contacts, setContacts] = useState<ContactData[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [selectedChannels, setSelectedChannels] = useState<string[]>([])
  const [campaignName, setCampaignName] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)

  const steps: WizardStep[] = [
    {
      id: 'upload',
      title: 'Upload Contacts',
      description: 'Import your contact list via CSV or API',
      icon: Upload,
      completed: contacts.length > 0
    },
    {
      id: 'enrich',
      title: 'AI Enrichment',
      description: 'Quantum AI enhances your contact data',
      icon: Brain,
      completed: false
    },
    {
      id: 'channels',
      title: 'Campaign Channels',
      description: 'Choose your outreach methods',
      icon: Target,
      completed: selectedChannels.length > 0
    },
    {
      id: 'deploy',
      title: 'Deploy Campaign',
      description: 'Launch your quantum-powered sales campaign',
      icon: Rocket,
      completed: false
    }
  ]

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    setUploadProgress(0)

    // Simulate file processing
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 10
      })
    }, 200)

    // Simulate CSV parsing
    setTimeout(() => {
      const mockContacts: ContactData[] = [
        {
          company_name: 'TechCorp Inc',
          contact_name: 'John Smith',
          title: 'CEO',
          phone: '+1-555-0123',
          email: 'john@techcorp.com',
          industry: 'Technology',
          company_size: '50-100',
          annual_revenue: '$1M-$5M'
        },
        {
          company_name: 'Innovate Solutions',
          contact_name: 'Sarah Johnson',
          title: 'VP Sales',
          phone: '+1-555-0456',
          email: 'sarah@innovate.com',
          industry: 'Software',
          company_size: '100-250',
          annual_revenue: '$5M-$10M'
        },
        {
          company_name: 'Global Dynamics',
          contact_name: 'Mike Chen',
          title: 'CTO',
          phone: '+1-555-0789',
          email: 'mike@global.com',
          industry: 'Consulting',
          company_size: '250-500',
          annual_revenue: '$10M-$25M'
        }
      ]

      setContacts(mockContacts)
      setIsUploading(false)
      setUploadProgress(100)
      setCurrentStep(1)
    }, 2000)
  }

  const handleEnrichment = async () => {
    setIsProcessing(true)
    
    // Simulate AI enrichment
    setTimeout(() => {
      setIsProcessing(false)
      setCurrentStep(2)
    }, 3000)
  }

  const handleChannelToggle = (channel: string) => {
    setSelectedChannels(prev => 
      prev.includes(channel) 
        ? prev.filter(c => c !== channel)
        : [...prev, channel]
    )
  }

  const handleDeploy = async () => {
    setIsProcessing(true)
    
    // Simulate campaign deployment
    setTimeout(() => {
      setIsProcessing(false)
      setCurrentStep(3)
    }, 2000)
  }

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const getStepStatus = (stepIndex: number) => {
    if (stepIndex < currentStep) return 'completed'
    if (stepIndex === currentStep) return 'current'
    return 'upcoming'
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => {
            const Icon = step.icon
            const status = getStepStatus(index)
            
            return (
              <div key={step.id} className="flex items-center">
                <div className={`flex items-center justify-center w-12 h-12 rounded-full border-2 transition-colors ${
                  status === 'completed' 
                    ? 'bg-goliath-600 border-goliath-600 text-white'
                    : status === 'current'
                    ? 'bg-goliath-100 border-goliath-600 text-goliath-600'
                    : 'bg-gray-100 border-gray-300 text-gray-400'
                }`}>
                  {status === 'completed' ? (
                    <CheckCircle className="w-6 h-6" />
                  ) : (
                    <Icon className="w-6 h-6" />
                  )}
                </div>
                
                {index < steps.length - 1 && (
                  <div className={`w-16 h-1 mx-4 transition-colors ${
                    status === 'completed' ? 'bg-goliath-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            )
          })}
        </div>
        
        <div className="flex justify-between mt-4">
          {steps.map((step, index) => (
            <div key={step.id} className="text-center flex-1">
              <div className={`text-sm font-medium ${
                getStepStatus(index) === 'current' ? 'text-goliath-600' : 'text-gray-500'
              }`}>
                {step.title}
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {step.description}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Step Content */}
      <div className="card">
        <div className="card-content">
          {/* Step 1: Upload Contacts */}
          {currentStep === 0 && (
            <div className="text-center">
              <div className="w-20 h-20 bg-goliath-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Upload className="w-10 h-10 text-goliath-600" />
              </div>
              
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Upload Your Contact List
              </h3>
              
              <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
                Import your contacts via CSV file or connect directly to your CRM. 
                Our quantum AI will automatically enrich and score your contacts for optimal campaign performance.
              </p>

              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 mb-6">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="contact-upload"
                  disabled={isUploading}
                />
                <label
                  htmlFor="contact-upload"
                  className="cursor-pointer block"
                >
                  <div className="text-center">
                    <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <div className="text-lg font-medium text-gray-900 mb-2">
                      {isUploading ? 'Processing...' : 'Click to upload CSV'}
                    </div>
                    <div className="text-sm text-gray-500">
                      or drag and drop your file here
                    </div>
                  </div>
                </label>
              </div>

              {isUploading && (
                <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                  <div 
                    className="bg-goliath-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
              )}

              <div className="text-sm text-gray-500">
                Supported formats: CSV, Excel. Max file size: 10MB
              </div>
            </div>
          )}

          {/* Step 2: AI Enrichment */}
          {currentStep === 1 && (
            <div className="text-center">
              <div className="w-20 h-20 bg-flyfox-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Brain className="w-10 h-10 text-flyfox-600" />
              </div>
              
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Quantum AI Enrichment
              </h3>
              
              <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
                Our Dynex-powered AI is analyzing and enriching your {contacts.length} contacts. 
                This includes data validation, scoring, and identifying decision makers.
              </p>

              {/* Contact Preview */}
              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <h4 className="font-semibold text-gray-900 mb-4">Contact Preview</h4>
                <div className="space-y-3">
                  {contacts.slice(0, 3).map((contact, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-white rounded-lg">
                      <div className="text-left">
                        <div className="font-medium text-gray-900">{contact.contact_name}</div>
                        <div className="text-sm text-gray-500">{contact.company_name}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-gray-600">{contact.title}</div>
                        <div className="text-sm text-gray-500">{contact.email}</div>
                      </div>
                    </div>
                  ))}
                  {contacts.length > 3 && (
                    <div className="text-sm text-gray-500 text-center">
                      +{contacts.length - 3} more contacts...
                    </div>
                  )}
                </div>
              </div>

              <button
                onClick={handleEnrichment}
                disabled={isProcessing}
                className="btn-primary"
              >
                {isProcessing ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Enriching Contacts...
                  </div>
                ) : (
                  <>
                    Start AI Enrichment
                    <ArrowRight className="ml-2 w-5 h-5" />
                  </>
                )}
              </button>
            </div>
          )}

          {/* Step 3: Campaign Channels */}
          {currentStep === 2 && (
            <div>
              <div className="text-center mb-8">
                <div className="w-20 h-20 bg-sigma-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Target className="w-10 h-10 text-sigma-600" />
                </div>
                
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  Choose Your Campaign Channels
                </h3>
                
                <p className="text-gray-600 max-w-2xl mx-auto">
                  Select the channels you want to use for your outreach campaign. 
                  Our quantum AI will optimize the mix for maximum engagement.
                </p>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Campaign Name
                </label>
                <input
                  type="text"
                  value={campaignName}
                  onChange={(e) => setCampaignName(e.target.value)}
                  placeholder="Enter campaign name (e.g., Q4 Enterprise Outreach)"
                  className="input-field"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                {[
                  { id: 'email', name: 'Email Campaigns', icon: Mail, description: 'Personalized email sequences' },
                  { id: 'sms', name: 'SMS Outreach', icon: MessageSquare, description: 'Text message campaigns' },
                  { id: 'voice', name: 'Voice Calls', icon: Phone, description: 'AI-powered phone calls' },
                  { id: 'social', name: 'Social Media', icon: Globe, description: 'LinkedIn and social outreach' }
                ].map((channel) => (
                  <div
                    key={channel.id}
                    className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                      selectedChannels.includes(channel.id)
                        ? 'border-sigma-500 bg-sigma-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => handleChannelToggle(channel.id)}
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                        selectedChannels.includes(channel.id)
                          ? 'bg-sigma-100 text-sigma-600'
                          : 'bg-gray-100 text-gray-400'
                      }`}>
                        <channel.icon className="w-5 h-5" />
                      </div>
                      <div>
                        <div className="font-medium text-gray-900">{channel.name}</div>
                        <div className="text-sm text-gray-500">{channel.description}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex justify-between">
                <button onClick={prevStep} className="btn-secondary">
                  Previous
                </button>
                <button
                  onClick={nextStep}
                  disabled={selectedChannels.length === 0 || !campaignName}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next: Deploy Campaign
                  <ArrowRight className="ml-2 w-5 h-5" />
                </button>
              </div>
            </div>
          )}

          {/* Step 4: Deploy Campaign */}
          {currentStep === 3 && (
            <div className="text-center">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Rocket className="w-10 h-10 text-green-600" />
              </div>
              
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Campaign Deployed Successfully!
              </h3>
              
              <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
                Your quantum-powered sales campaign is now live! Our autonomous agents 
                are working 24/7 to engage your {contacts.length} contacts across {selectedChannels.length} channels.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="text-center">
                  <div className="text-3xl font-bold text-goliath-600 mb-2">{contacts.length}</div>
                  <div className="text-sm text-gray-600">Contacts</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-flyfox-600 mb-2">{selectedChannels.length}</div>
                  <div className="text-sm text-gray-600">Channels</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-sigma-600 mb-2">24/7</div>
                  <div className="text-sm text-gray-600">Availability</div>
                </div>
              </div>

              <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
                <h4 className="font-semibold text-green-800 mb-2">What Happens Next?</h4>
                <ul className="text-sm text-green-700 space-y-1 text-left">
                  <li>• AI agents begin outreach within 5 minutes</li>
                  <li>• Real-time analytics and performance tracking</li>
                  <li>• Automated follow-up sequences</li>
                  <li>• Lead scoring and qualification</li>
                  <li>• Performance optimization via quantum computing</li>
                </ul>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="btn-primary">
                  View Campaign Dashboard
                  <BarChart3 className="ml-2 w-5 h-5" />
                </button>
                <button className="btn-secondary">
                  Deploy Another Campaign
                  <Rocket className="ml-2 w-5 h-5" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
