"use client"

import { useState } from 'react'
import { Upload, Database, Zap, Target, Users, BarChart3, ArrowRight, Check, X, Rocket } from 'lucide-react'

interface Contact {
  company_name: string
  contact_name: string
  title: string
  phone: string
  email: string
  industry: string
  company_size: string
  annual_revenue: string
  notes: string
  timezone: string
  best_contact_time: string
  linkedin_url: string
  website: string
  pain_points: string
  interests: string
  budget_range: string
  decision_maker: string
  technical_contact: string
}

export default function ContactWizard() {
  const [step, setStep] = useState(1)
  const [contacts, setContacts] = useState<Contact[]>([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [selectedChannels, setSelectedChannels] = useState({
    email: true,
    sms: false,
    voice: false,
    digitalHuman: false
  })

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = (e) => {
      const csv = e.target?.result as string
      const lines = csv.split('\n')
      const headers = lines[0].split(',')
      
      const parsedContacts: Contact[] = lines.slice(1).map(line => {
        const values = line.split(',')
        const contact: any = {}
        headers.forEach((header, index) => {
          contact[header.trim()] = values[index]?.trim() || ''
        })
        return contact as Contact
      }).filter(contact => contact.email) // Filter out empty rows
      
      setContacts(parsedContacts)
      setStep(2)
    }
    reader.readAsText(file)
  }

  const handleChannelToggle = (channel: keyof typeof selectedChannels) => {
    setSelectedChannels(prev => ({
      ...prev,
      [channel]: !prev[channel]
    }))
  }

  const simulateEnrichment = async () => {
    setIsProcessing(true)
    
    // Simulate AI enrichment process
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    // Add enriched data
    const enrichedContacts = contacts.map(contact => ({
      ...contact,
      industry: contact.industry || 'Technology',
      company_size: contact.company_size || '51-200',
      annual_revenue: contact.annual_revenue || '$10M-$50M',
      pain_points: contact.pain_points || 'Lead generation, Sales automation',
      interests: contact.interests || 'AI, Automation, Growth',
      budget_range: contact.budget_range || '$50K-$200K'
    }))
    
    setContacts(enrichedContacts)
    setIsProcessing(false)
    setStep(3)
  }

  const launchCampaign = () => {
    const activeChannels = Object.entries(selectedChannels)
      .filter(([_, active]) => active)
      .map(([channel]) => channel)
    
    alert(`Campaign launched with ${contacts.length} contacts across: ${activeChannels.join(', ')}`)
  }

  const generateSampleCSV = () => {
    const sampleData = [
      'company_name,contact_name,title,phone,email,industry,company_size,annual_revenue,notes,timezone,best_contact_time,linkedin_url,website,pain_points,interests,budget_range,decision_maker,technical_contact',
      'TechCorp Inc,John Smith,CEO,555-0123,john@techcorp.com,Technology,51-200,$10M-$50M,Interested in AI solutions,EST,9AM-11AM,linkedin.com/in/johnsmith,techcorp.com,Lead generation,AI automation,$100K-$500K,Yes,No',
      'InnovateSoft,Mary Johnson,CTO,555-0124,mary@innovatesoft.com,Software,11-50,$5M-$10M,Looking for growth solutions,EST,2PM-4PM,linkedin.com/in/maryjohnson,innovatesoft.com,Sales automation,Digital transformation,$50K-$200K,Yes,Yes',
      'DataFlow Systems,David Brown,VP Sales,555-0125,david@dataflow.com,Data Analytics,201-1000,$50M-$100M,Need CRM solution,EST,10AM-12PM,linkedin.com/in/davidbrown,dataflow.com,CRM implementation,Data analytics,$200K-$1M,Yes,No'
    ]
    
    const csvContent = sampleData.join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'sample_contacts.csv'
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Steps */}
      <div className="flex items-center justify-center mb-8">
        {[1, 2, 3].map((stepNumber) => (
          <div key={stepNumber} className="flex items-center">
            <div className={`
              w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold
              ${step >= stepNumber 
                ? 'bg-goliath-600 text-white' 
                : 'bg-gray-200 text-gray-500'
              }
            `}>
              {step > stepNumber ? <Check className="w-5 h-5" /> : stepNumber}
            </div>
            {stepNumber < 3 && (
              <div className={`
                w-16 h-1 mx-2
                ${step > stepNumber ? 'bg-goliath-600' : 'bg-gray-200'}
              `} />
            )}
          </div>
        ))}
      </div>

      {/* Step 1: Upload Contacts */}
      {step === 1 && (
        <div className="card">
          <div className="card-header bg-gradient-to-br from-goliath-500 to-goliath-600 text-white">
            <h2 className="text-2xl font-bold">Step 1: Upload Your Contacts</h2>
            <p className="text-goliath-100">Import your contact list to get started</p>
          </div>
          <div className="card-content">
            <div className="text-center">
              <div className="w-24 h-24 bg-goliath-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Upload className="w-12 h-12 text-goliath-600" />
              </div>
              
              <h3 className="text-xl font-semibold mb-4">Upload Contact File</h3>
              <p className="text-gray-600 mb-6">
                Upload a CSV file with your contacts. We'll automatically enrich the data 
                using our quantum AI system.
              </p>
              
              <div className="space-y-4">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="contact-file"
                />
                <label
                  htmlFor="contact-file"
                  className="btn-primary inline-flex items-center cursor-pointer"
                >
                  <Upload className="w-5 h-5 mr-2" />
                  Choose CSV File
                </label>
                
                <div className="text-sm text-gray-500">
                  or drag and drop your file here
                </div>
              </div>
              
              <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold mb-2">Need a sample file?</h4>
                <button
                  onClick={generateSampleCSV}
                  className="text-goliath-600 hover:text-goliath-700 text-sm underline"
                >
                  Download sample CSV template
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Step 2: AI Enrichment */}
      {step === 2 && (
        <div className="card">
          <div className="card-header bg-gradient-to-br from-flyfox-500 to-flyfox-600 text-white">
            <h2 className="text-2xl font-bold">Step 2: AI-Powered Enrichment</h2>
            <p className="text-flyfox-100">Quantum AI enhances your contact data</p>
          </div>
          <div className="card-content">
            <div className="text-center">
              <div className="w-24 h-24 bg-flyfox-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Database className="w-12 h-12 text-flyfox-600" />
              </div>
              
              <h3 className="text-xl font-semibold mb-4">Enriching {contacts.length} Contacts</h3>
              <p className="text-gray-600 mb-6">
                Our Dynex quantum AI is analyzing and enriching your contact data with:
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <Target className="w-8 h-8 text-goliath-600 mx-auto mb-2" />
                  <div className="font-semibold">Smart Scoring</div>
                  <div className="text-sm text-gray-600">Lead quality assessment</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <Users className="w-8 h-8 text-flyfox-600 mx-auto mb-2" />
                  <div className="font-semibold">Data Enrichment</div>
                  <div className="text-sm text-gray-600">Missing field completion</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <BarChart3 className="w-8 h-8 text-sigma-600 mx-auto mb-2" />
                  <div className="font-semibold">Priority Ranking</div>
                  <div className="text-sm text-gray-600">Optimal contact sequence</div>
                </div>
              </div>
              
              <button
                onClick={simulateEnrichment}
                disabled={isProcessing}
                className="btn-primary"
              >
                {isProcessing ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Enriching with Quantum AI...
                  </div>
                ) : (
                  <div className="flex items-center">
                    <Zap className="w-5 h-5 mr-2" />
                    Start Quantum Enrichment
                  </div>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Step 3: Launch Campaign */}
      {step === 3 && (
        <div className="card">
          <div className="card-header bg-gradient-to-br from-sigma-500 to-sigma-600 text-white">
            <h2 className="text-2xl font-bold">Step 3: Launch Your Campaign</h2>
            <p className="text-sigma-100">Choose channels and deploy your sales agents</p>
          </div>
          <div className="card-content">
            <div className="text-center">
              <div className="w-24 h-24 bg-sigma-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Rocket className="w-12 h-12 text-sigma-600" />
              </div>
              
              <h3 className="text-xl font-semibold mb-4">Campaign Configuration</h3>
              <p className="text-gray-600 mb-6">
                Select the channels you want to use for your campaign with {contacts.length} contacts.
              </p>
              
              {/* Channel Selection */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                {Object.entries(selectedChannels).map(([channel, active]) => (
                  <button
                    key={channel}
                    onClick={() => handleChannelToggle(channel as keyof typeof selectedChannels)}
                    className={`
                      p-4 rounded-lg border-2 transition-all duration-200 text-left
                      ${active 
                        ? 'border-sigma-500 bg-sigma-50' 
                        : 'border-gray-200 hover:border-gray-300'
                      }
                    `}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-semibold capitalize">{channel}</div>
                        <div className="text-sm text-gray-600">
                          {channel === 'email' && 'Automated email sequences'}
                          {channel === 'sms' && 'Text message campaigns'}
                          {channel === 'voice' && 'AI-powered phone calls'}
                          {channel === 'digitalHuman' && 'Digital human interactions'}
                        </div>
                      </div>
                      <div className={`
                        w-6 h-6 rounded-full border-2 flex items-center justify-center
                        ${active 
                          ? 'border-sigma-500 bg-sigma-500' 
                          : 'border-gray-300'
                        }
                      `}>
                        {active && <Check className="w-4 h-4 text-white" />}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
              
              {/* Campaign Preview */}
              <div className="mb-8 p-6 bg-gray-50 rounded-lg">
                <h4 className="font-semibold mb-4">Campaign Preview</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="font-medium text-gray-700">Total Contacts</div>
                    <div className="text-2xl font-bold text-goliath-600">{contacts.length}</div>
                  </div>
                  <div>
                    <div className="font-medium text-gray-700">Active Channels</div>
                    <div className="text-2xl font-bold text-flyfox-600">
                      {Object.values(selectedChannels).filter(Boolean).length}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium text-gray-700">Estimated Reach</div>
                    <div className="text-2xl font-bold text-sigma-600">
                      {contacts.length * Object.values(selectedChannels).filter(Boolean).length}
                    </div>
                  </div>
                </div>
              </div>
              
              <button
                onClick={launchCampaign}
                className="btn-primary text-lg px-8 py-4"
              >
                <Rocket className="w-6 h-6 mr-2" />
                Launch Campaign
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
