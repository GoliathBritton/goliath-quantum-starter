import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '../components/auth/AuthContext'
import Nav from '../components/Nav'
import Footer from '../components/Footer'
import { brand } from '../lib/brand'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: {
    default: brand.name,
    template: `%s | ${brand.name}`
  },
  description: brand.description,
  keywords: [
    'FLYFOX AI',
    'NQBA',
    'quantum computing',
    'neuromorphic computing',
    'AI agents',
    'business intelligence',
    'quantum optimization',
    'QUBO',
    'Dynex',
    'Intelligence Economy'
  ],
  authors: [{ name: 'FLYFOX AI Team' }],
  creator: 'FLYFOX AI',
  publisher: 'FLYFOX AI',
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
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://flyfox.ai',
    siteName: brand.name,
    title: brand.name,
    description: brand.description,
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: `${brand.name} - ${brand.tagline}`,
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: brand.name,
    description: brand.description,
    images: ['/og-image.png'],
    creator: '@flyfoxai',
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} antialiased bg-white text-black`}>
        <AuthProvider>
          <div className="min-h-screen flex flex-col bg-white">
            <Nav />
            <main className="flex-1 bg-white">
              {children}
            </main>
            <Footer />
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}