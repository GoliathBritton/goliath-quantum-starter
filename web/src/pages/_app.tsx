import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import { Inter, JetBrains_Mono } from 'next/font/google'
import Head from 'next/head'
import { SessionProvider } from 'next-auth/react'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains-mono',
})

export default function App({ Component, pageProps: { session, ...pageProps } }: AppProps) {
  return (
    <SessionProvider session={session}>
      <Head>
        <title>Goliath Quantum Portal</title>
        <meta name="description" content="Next-generation quantum-powered business intelligence and partner management platform" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className={`${inter.variable} ${jetbrainsMono.variable} font-sans`}>
        <Navbar />
        <main className="min-h-screen">
          <Component {...pageProps} />
        </main>
        <Footer />
      </div>
    </SessionProvider>
  )
}