import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import {
  Loader2,
  ExternalLink,
  CheckCircle,
  AlertCircle,
  CreditCard,
  Building,
  DollarSign,
  Clock,
  RefreshCw,
} from 'lucide-react';
import { toast } from 'sonner';

interface AccountStatus {
  account_id: string;
  charges_enabled: boolean;
  payouts_enabled: boolean;
  details_submitted: boolean;
  requirements: {
    currently_due: string[];
    eventually_due: string[];
    past_due: string[];
    pending_verification: string[];
  };
  country: string;
  default_currency: string;
  success: boolean;
}

interface StripeConnectProps {
  onAccountSetup?: (accountId: string) => void;
  refreshUrl?: string;
  returnUrl?: string;
}

export function StripeConnect({
  onAccountSetup,
  refreshUrl = `${window.location.origin}/stripe/refresh`,
  returnUrl = `${window.location.origin}/stripe/return`,
}: StripeConnectProps) {
  const [accountStatus, setAccountStatus] = useState<AccountStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreatingAccount, setIsCreatingAccount] = useState(false);
  const [error, setError] = useState<string>('');
  const [onboardingUrl, setOnboardingUrl] = useState<string>('');

  useEffect(() => {
    checkAccountStatus();
  }, []);

  const checkAccountStatus = async () => {
    try {
      setIsLoading(true);
      setError('');

      const response = await fetch('/api/stripe/connect/account-status', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.status === 404) {
        // No account exists yet
        setAccountStatus(null);
        return;
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to check account status');
      }

      const data = await response.json();
      setAccountStatus(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to check account status';
      setError(errorMessage);
      console.error('Account status error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const createConnectAccount = async (country: string = 'US') => {
    try {
      setIsCreatingAccount(true);
      setError('');

      const response = await fetch('/api/stripe/connect/create-account', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          country,
          refresh_url: refreshUrl,
          return_url: returnUrl,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create Stripe Connect account');
      }

      const data = await response.json();
      setOnboardingUrl(data.onboarding_url);
      
      // Open onboarding in new window
      window.open(data.onboarding_url, '_blank', 'width=800,height=600');
      
      toast.success('Stripe Connect account created! Complete onboarding in the new window.');
      onAccountSetup?.(data.account_id);
      
      // Refresh status after a delay to allow for onboarding completion
      setTimeout(() => {
        checkAccountStatus();
      }, 5000);
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create account';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsCreatingAccount(false);
    }
  };

  const getStatusBadge = (status: AccountStatus) => {
    if (status.charges_enabled && status.payouts_enabled && status.details_submitted) {
      return <Badge className="bg-green-100 text-green-800">Active</Badge>;
    } else if (status.details_submitted) {
      return <Badge className="bg-yellow-100 text-yellow-800">Pending Verification</Badge>;
    } else {
      return <Badge className="bg-red-100 text-red-800">Setup Required</Badge>;
    }
  };

  const getRequirementsText = (requirements: AccountStatus['requirements']) => {
    const allRequirements = [
      ...requirements.currently_due,
      ...requirements.eventually_due,
      ...requirements.past_due,
    ];
    
    if (allRequirements.length === 0) {
      return 'All requirements completed';
    }
    
    return `${allRequirements.length} requirement(s) pending`;
  };

  if (isLoading) {
    return (
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle className="flex items-center">
            <Building className="mr-2 h-5 w-5" />
            Stripe Connect Setup
          </CardTitle>
          <CardDescription>
            Set up your payment processing account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-8 w-8 animate-spin" />
            <span className="ml-2">Checking account status...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center">
            <Building className="mr-2 h-5 w-5" />
            Stripe Connect Setup
          </div>
          {accountStatus && getStatusBadge(accountStatus)}
        </CardTitle>
        <CardDescription>
          {accountStatus
            ? 'Manage your payment processing account'
            : 'Set up your payment processing account to receive payments'}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {!accountStatus ? (
          // No account exists - show setup
          <div className="space-y-4">
            <div className="text-center py-8">
              <CreditCard className="h-16 w-16 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-semibold mb-2">No Payment Account Found</h3>
              <p className="text-gray-600 mb-6">
                Create a Stripe Connect account to start receiving payments from your customers.
              </p>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-medium mb-2">What you'll need:</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Business information and tax ID</li>
                <li>• Bank account details for payouts</li>
                <li>• Business representative information</li>
                <li>• Business verification documents</li>
              </ul>
            </div>

            <Button
              onClick={() => createConnectAccount()}
              disabled={isCreatingAccount}
              className="w-full"
              size="lg"
            >
              {isCreatingAccount ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Creating Account...
                </>
              ) : (
                <>
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Create Stripe Connect Account
                </>
              )}
            </Button>
          </div>
        ) : (
          // Account exists - show status
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className={`p-2 rounded-full ${
                  accountStatus.charges_enabled ? 'bg-green-100' : 'bg-red-100'
                }`}>
                  {accountStatus.charges_enabled ? (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  ) : (
                    <AlertCircle className="h-4 w-4 text-red-600" />
                  )}
                </div>
                <div>
                  <div className="font-medium text-sm">Charges</div>
                  <div className="text-xs text-gray-600">
                    {accountStatus.charges_enabled ? 'Enabled' : 'Disabled'}
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className={`p-2 rounded-full ${
                  accountStatus.payouts_enabled ? 'bg-green-100' : 'bg-red-100'
                }`}>
                  {accountStatus.payouts_enabled ? (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  ) : (
                    <AlertCircle className="h-4 w-4 text-red-600" />
                  )}
                </div>
                <div>
                  <div className="font-medium text-sm">Payouts</div>
                  <div className="text-xs text-gray-600">
                    {accountStatus.payouts_enabled ? 'Enabled' : 'Disabled'}
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className={`p-2 rounded-full ${
                  accountStatus.details_submitted ? 'bg-green-100' : 'bg-yellow-100'
                }`}>
                  {accountStatus.details_submitted ? (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  ) : (
                    <Clock className="h-4 w-4 text-yellow-600" />
                  )}
                </div>
                <div>
                  <div className="font-medium text-sm">Details</div>
                  <div className="text-xs text-gray-600">
                    {accountStatus.details_submitted ? 'Submitted' : 'Pending'}
                  </div>
                </div>
              </div>
            </div>

            <Separator />

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="font-medium">Account Information</h4>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={checkAccountStatus}
                >
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh
                </Button>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Account ID:</span>
                  <div className="font-mono text-xs mt-1">{accountStatus.account_id}</div>
                </div>
                <div>
                  <span className="text-gray-600">Country:</span>
                  <div className="mt-1">{accountStatus.country}</div>
                </div>
                <div>
                  <span className="text-gray-600">Currency:</span>
                  <div className="mt-1">{accountStatus.default_currency.toUpperCase()}</div>
                </div>
                <div>
                  <span className="text-gray-600">Requirements:</span>
                  <div className="mt-1">{getRequirementsText(accountStatus.requirements)}</div>
                </div>
              </div>
            </div>

            {/* Show requirements if any */}
            {(accountStatus.requirements.currently_due.length > 0 ||
              accountStatus.requirements.past_due.length > 0) && (
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  <div className="space-y-2">
                    <div className="font-medium">Action Required</div>
                    {accountStatus.requirements.currently_due.length > 0 && (
                      <div>
                        <div className="text-sm font-medium">Currently Due:</div>
                        <ul className="text-sm list-disc list-inside ml-2">
                          {accountStatus.requirements.currently_due.map((req, index) => (
                            <li key={index}>{req.replace(/_/g, ' ')}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {accountStatus.requirements.past_due.length > 0 && (
                      <div>
                        <div className="text-sm font-medium text-red-600">Past Due:</div>
                        <ul className="text-sm list-disc list-inside ml-2">
                          {accountStatus.requirements.past_due.map((req, index) => (
                            <li key={index}>{req.replace(/_/g, ' ')}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </AlertDescription>
              </Alert>
            )}

            {/* Action buttons */}
            <div className="flex space-x-3">
              {!accountStatus.details_submitted && (
                <Button
                  onClick={() => createConnectAccount()}
                  disabled={isCreatingAccount}
                  className="flex-1"
                >
                  {isCreatingAccount ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Creating Link...
                    </>
                  ) : (
                    <>
                      <ExternalLink className="mr-2 h-4 w-4" />
                      Complete Setup
                    </>
                  )}
                </Button>
              )}
              
              {accountStatus.details_submitted && (
                <Button variant="outline" className="flex-1">
                  <DollarSign className="mr-2 h-4 w-4" />
                  View Stripe Dashboard
                </Button>
              )}
            </div>

            {accountStatus.charges_enabled && accountStatus.payouts_enabled && (
              <Alert className="border-green-200 bg-green-50">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <AlertDescription className="text-green-800">
                  Your Stripe Connect account is fully set up and ready to process payments!
                </AlertDescription>
              </Alert>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default StripeConnect;