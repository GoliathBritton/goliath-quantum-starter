import React, { useState, useEffect } from 'react';
import {
  Elements,
  CardElement,
  useStripe,
  useElements,
  PaymentElement,
} from '@stripe/react-stripe-js';
import { loadStripe, StripeElementsOptions } from '@stripe/stripe-js';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, CreditCard, CheckCircle, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

// Initialize Stripe
const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

interface PaymentFormProps {
  clientSecret: string;
  amount: number;
  creditsAmount: number;
  onSuccess: (paymentIntentId: string) => void;
  onError: (error: string) => void;
}

function PaymentForm({ clientSecret, amount, creditsAmount, onSuccess, onError }: PaymentFormProps) {
  const stripe = useStripe();
  const elements = useElements();
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentStatus, setPaymentStatus] = useState<'idle' | 'processing' | 'succeeded' | 'failed'>('idle');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setIsProcessing(true);
    setPaymentStatus('processing');

    try {
      const { error, paymentIntent } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: `${window.location.origin}/payment/success`,
        },
        redirect: 'if_required',
      });

      if (error) {
        console.error('Payment failed:', error);
        setPaymentStatus('failed');
        onError(error.message || 'Payment failed');
        toast.error('Payment failed: ' + (error.message || 'Unknown error'));
      } else if (paymentIntent && paymentIntent.status === 'succeeded') {
        setPaymentStatus('succeeded');
        onSuccess(paymentIntent.id);
        toast.success(`Payment successful! ${creditsAmount} quantum credits added to your account.`);
      }
    } catch (err) {
      console.error('Payment error:', err);
      setPaymentStatus('failed');
      onError('An unexpected error occurred');
      toast.error('An unexpected error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div className="p-4 bg-gray-50 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Quantum Credits:</span>
            <span className="text-lg font-bold">{creditsAmount.toLocaleString()}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium">Total Amount:</span>
            <span className="text-lg font-bold">${(amount / 100).toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center mt-1">
            <span className="text-xs text-gray-600">Price per credit:</span>
            <span className="text-xs text-gray-600">${(amount / 100 / creditsAmount).toFixed(4)}</span>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="payment-element">Payment Details</Label>
          <div className="border rounded-md p-3">
            <PaymentElement
              id="payment-element"
              options={{
                layout: 'tabs',
              }}
            />
          </div>
        </div>
      </div>

      {paymentStatus === 'failed' && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Payment failed. Please check your payment details and try again.
          </AlertDescription>
        </Alert>
      )}

      {paymentStatus === 'succeeded' && (
        <Alert className="border-green-200 bg-green-50">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-800">
            Payment successful! Your quantum credits have been added to your account.
          </AlertDescription>
        </Alert>
      )}

      <Button
        type="submit"
        disabled={!stripe || isProcessing || paymentStatus === 'succeeded'}
        className="w-full"
        size="lg"
      >
        {isProcessing ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Processing Payment...
          </>
        ) : paymentStatus === 'succeeded' ? (
          <>
            <CheckCircle className="mr-2 h-4 w-4" />
            Payment Complete
          </>
        ) : (
          <>
            <CreditCard className="mr-2 h-4 w-4" />
            Pay ${(amount / 100).toFixed(2)}
          </>
        )}
      </Button>
    </form>
  );
}

interface StripePaymentProps {
  creditsAmount: number;
  unitCostUsd: number;
  customerEmail: string;
  customerName: string;
  onSuccess?: (paymentIntentId: string) => void;
  onError?: (error: string) => void;
}

export function StripePayment({
  creditsAmount,
  unitCostUsd,
  customerEmail,
  customerName,
  onSuccess,
  onError,
}: StripePaymentProps) {
  const [clientSecret, setClientSecret] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [paymentIntentId, setPaymentIntentId] = useState<string>('');

  const totalAmount = Math.round(creditsAmount * unitCostUsd * 100); // Convert to cents

  useEffect(() => {
    createPaymentIntent();
  }, [creditsAmount, unitCostUsd, customerEmail, customerName]);

  const createPaymentIntent = async () => {
    try {
      setIsLoading(true);
      setError('');

      const response = await fetch('/api/stripe/payment-intent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          credits_amount: creditsAmount,
          unit_cost_usd: unitCostUsd,
          customer_email: customerEmail,
          customer_name: customerName,
          metadata: {
            source: 'web_portal',
            timestamp: new Date().toISOString(),
          },
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create payment intent');
      }

      const data = await response.json();
      setClientSecret(data.client_secret);
      setPaymentIntentId(data.payment_intent_id);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to initialize payment';
      setError(errorMessage);
      onError?.(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePaymentSuccess = (paymentIntentId: string) => {
    setPaymentIntentId(paymentIntentId);
    onSuccess?.(paymentIntentId);
  };

  const handlePaymentError = (error: string) => {
    setError(error);
    onError?.(error);
  };

  if (isLoading) {
    return (
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle className="flex items-center">
            <CreditCard className="mr-2 h-5 w-5" />
            Purchase Quantum Credits
          </CardTitle>
          <CardDescription>
            Secure payment powered by Stripe
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-8 w-8 animate-spin" />
            <span className="ml-2">Initializing payment...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle className="flex items-center text-red-600">
            <AlertCircle className="mr-2 h-5 w-5" />
            Payment Error
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
          <Button
            onClick={createPaymentIntent}
            className="w-full mt-4"
            variant="outline"
          >
            Try Again
          </Button>
        </CardContent>
      </Card>
    );
  }

  const options: StripeElementsOptions = {
    clientSecret,
    appearance: {
      theme: 'stripe',
      variables: {
        colorPrimary: '#0570de',
        colorBackground: '#ffffff',
        colorText: '#30313d',
        colorDanger: '#df1b41',
        fontFamily: 'system-ui, sans-serif',
        spacingUnit: '4px',
        borderRadius: '6px',
      },
    },
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center">
          <CreditCard className="mr-2 h-5 w-5" />
          Purchase Quantum Credits
        </CardTitle>
        <CardDescription>
          Secure payment powered by Stripe
        </CardDescription>
      </CardHeader>
      <CardContent>
        {clientSecret && (
          <Elements options={options} stripe={stripePromise}>
            <PaymentForm
              clientSecret={clientSecret}
              amount={totalAmount}
              creditsAmount={creditsAmount}
              onSuccess={handlePaymentSuccess}
              onError={handlePaymentError}
            />
          </Elements>
        )}
      </CardContent>
    </Card>
  );
}

// Credit purchase presets component
interface CreditPackage {
  credits: number;
  unitCost: number;
  popular?: boolean;
  savings?: string;
}

const CREDIT_PACKAGES: CreditPackage[] = [
  {
    credits: 1000,
    unitCost: 0.01,
  },
  {
    credits: 5000,
    unitCost: 0.009,
    savings: '10%',
  },
  {
    credits: 10000,
    unitCost: 0.008,
    popular: true,
    savings: '20%',
  },
  {
    credits: 50000,
    unitCost: 0.007,
    savings: '30%',
  },
];

interface CreditPurchaseProps {
  customerEmail: string;
  customerName: string;
  onSuccess?: (paymentIntentId: string) => void;
  onError?: (error: string) => void;
}

export function CreditPurchase({
  customerEmail,
  customerName,
  onSuccess,
  onError,
}: CreditPurchaseProps) {
  const [selectedPackage, setSelectedPackage] = useState<CreditPackage | null>(null);
  const [customCredits, setCustomCredits] = useState<number>(0);
  const [customUnitCost, setCustomUnitCost] = useState<number>(0.01);
  const [useCustom, setUseCustom] = useState(false);

  const handlePackageSelect = (pkg: CreditPackage) => {
    setSelectedPackage(pkg);
    setUseCustom(false);
  };

  const handleCustomPurchase = () => {
    if (customCredits > 0 && customUnitCost > 0) {
      setSelectedPackage({
        credits: customCredits,
        unitCost: customUnitCost,
      });
      setUseCustom(true);
    }
  };

  if (selectedPackage) {
    return (
      <div className="space-y-4">
        <Button
          variant="outline"
          onClick={() => setSelectedPackage(null)}
          className="mb-4"
        >
          ← Back to Packages
        </Button>
        <StripePayment
          creditsAmount={selectedPackage.credits}
          unitCostUsd={selectedPackage.unitCost}
          customerEmail={customerEmail}
          customerName={customerName}
          onSuccess={onSuccess}
          onError={onError}
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Choose Your Credit Package</h2>
        <p className="text-gray-600">Select a package or customize your purchase</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {CREDIT_PACKAGES.map((pkg, index) => (
          <Card
            key={index}
            className={`cursor-pointer transition-all hover:shadow-lg ${
              pkg.popular ? 'ring-2 ring-blue-500 relative' : ''
            }`}
            onClick={() => handlePackageSelect(pkg)}
          >
            {pkg.popular && (
              <div className="absolute -top-2 left-1/2 transform -translate-x-1/2">
                <span className="bg-blue-500 text-white px-3 py-1 rounded-full text-xs font-medium">
                  Most Popular
                </span>
              </div>
            )}
            <CardHeader className="text-center">
              <CardTitle className="text-lg">
                {pkg.credits.toLocaleString()} Credits
              </CardTitle>
              {pkg.savings && (
                <div className="text-green-600 font-medium text-sm">
                  Save {pkg.savings}
                </div>
              )}
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-2xl font-bold mb-2">
                ${(pkg.credits * pkg.unitCost).toFixed(2)}
              </div>
              <div className="text-sm text-gray-600">
                ${pkg.unitCost.toFixed(4)} per credit
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Custom Amount</CardTitle>
          <CardDescription>
            Purchase a custom number of credits
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="custom-credits">Number of Credits</Label>
              <Input
                id="custom-credits"
                type="number"
                min="1"
                value={customCredits || ''}
                onChange={(e) => setCustomCredits(parseInt(e.target.value) || 0)}
                placeholder="Enter amount"
              />
            </div>
            <div>
              <Label htmlFor="custom-unit-cost">Price per Credit ($)</Label>
              <Input
                id="custom-unit-cost"
                type="number"
                min="0.001"
                step="0.001"
                value={customUnitCost}
                onChange={(e) => setCustomUnitCost(parseFloat(e.target.value) || 0.01)}
              />
            </div>
          </div>
          {customCredits > 0 && customUnitCost > 0 && (
            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">Total Cost:</div>
              <div className="text-xl font-bold">
                ${(customCredits * customUnitCost).toFixed(2)}
              </div>
            </div>
          )}
          <Button
            onClick={handleCustomPurchase}
            disabled={!customCredits || !customUnitCost}
            className="w-full"
          >
            Purchase Custom Amount
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

export default StripePayment;