/**
 * Stripe Integration Utilities
 * Handles payment processing and checkout sessions
 */

import { loadStripe, Stripe } from '@stripe/stripe-js'

// Initialize Stripe
let stripePromise: Promise<Stripe | null>

export const getStripe = () => {
  if (!stripePromise) {
    stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!)
  }
  return stripePromise
}

export interface CheckoutSession {
  id: string
  url: string
}

export interface PackageConfig {
  name: string
  price: string
  setup: string
  stripePriceId: string
  stripeSetupPriceId?: string
}

export const packages: Record<string, PackageConfig> = {
  DIY: {
    name: 'DIY',
    price: '$2,500',
    setup: '$20,000',
    stripePriceId: 'price_diy_monthly',
    stripeSetupPriceId: 'price_diy_setup'
  },
  DFY: {
    name: 'DFY',
    price: '$15,000',
    setup: '$50,000',
    stripePriceId: 'price_dfy_monthly',
    stripeSetupPriceId: 'price_dfy_setup'
  },
  Enterprise: {
    name: 'Enterprise',
    price: '$50,000',
    setup: '$250,000',
    stripePriceId: 'price_enterprise_monthly',
    stripeSetupPriceId: 'price_enterprise_setup'
  }
}

/**
 * Create a checkout session for a package
 */
export async function createCheckoutSession(
  packageName: string,
  customerEmail: string,
  includeSetup: boolean = true
): Promise<CheckoutSession> {
  const packageConfig = packages[packageName]
  if (!packageConfig) {
    throw new Error(`Unknown package: ${packageName}`)
  }

  try {
    const response = await fetch('/api/create-checkout-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        package: packageName,
        customerEmail,
        includeSetup,
        stripePriceId: packageConfig.stripePriceId,
        stripeSetupPriceId: packageConfig.stripeSetupPriceId
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to create checkout session')
    }

    const session = await response.json()
    return session
  } catch (error) {
    console.error('Error creating checkout session:', error)
    throw error
  }
}

/**
 * Redirect to Stripe checkout
 */
export async function redirectToCheckout(packageName: string, customerEmail: string, includeSetup: boolean = true) {
  try {
    const stripe = await getStripe()
    if (!stripe) {
      throw new Error('Stripe failed to load')
    }

    const session = await createCheckoutSession(packageName, customerEmail, includeSetup)
    
    const { error } = await stripe.redirectToCheckout({
      sessionId: session.id,
    })

    if (error) {
      throw error
    }
  } catch (error) {
    console.error('Error redirecting to checkout:', error)
    throw error
  }
}

/**
 * Handle successful payment
 */
export function handlePaymentSuccess(sessionId: string) {
  // Redirect to success page or dashboard
  window.location.href = `/success?session_id=${sessionId}`
}

/**
 * Handle payment cancellation
 */
export function handlePaymentCancellation() {
  // Redirect back to packages page
  window.location.href = '/packages'
}

/**
 * Format currency
 */
export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount)
}

/**
 * Calculate monthly payment with setup fee
 */
export function calculateMonthlyPayment(packageName: string, months: number = 12): {
  monthly: number
  setup: number
  total: number
  monthlyWithSetup: number
} {
  const packageConfig = packages[packageName]
  if (!packageConfig) {
    throw new Error(`Unknown package: ${packageName}`)
  }

  const monthly = parseFloat(packageConfig.price.replace(/[$,]/g, ''))
  const setup = parseFloat(packageConfig.setup.replace(/[$,]/g, ''))
  const total = (monthly * months) + setup
  const monthlyWithSetup = total / months

  return {
    monthly,
    setup,
    total,
    monthlyWithSetup
  }
}
