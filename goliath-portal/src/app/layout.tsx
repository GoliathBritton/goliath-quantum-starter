import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/Navbar'
import Sidebar from '@/components/Sidebar'
import NQBAInitializer from '@/components/NQBAInitializer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Goliath Portal - Quantum-Powered CRM & Sales Division Factory',
  description: 'Transform your business with the Q-Sales Division™ - autonomous sales agents powered by Dynex quantum computing and NVIDIA acceleration.',
  keywords: 'CRM, Sales Automation, Quantum Computing, Dynex, NVIDIA, Goliath, FLYFOX AI, Sigma Select, NQBA',
  authors: [{ name: 'Goliath Family' }],
  openGraph: {
    title: 'Goliath Portal - Quantum-Powered CRM & Sales Division Factory',
    description: 'Transform your business with autonomous sales agents powered by quantum computing.',
    url: 'https://portal.goliath.com',
    siteName: 'Goliath Portal',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Goliath Portal - Quantum-Powered CRM',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Goliath Portal - Quantum-Powered CRM & Sales Division Factory',
    description: 'Transform your business with autonomous sales agents powered by quantum computing.',
    images: ['/og-image.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full bg-gray-50`}>
        <NQBAInitializer />
        <div className="flex h-full">
          <Sidebar />
          <div className="flex-1 flex flex-col">
            <Navbar />
            <main className="flex-1 overflow-y-auto">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}
