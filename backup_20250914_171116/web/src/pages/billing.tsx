import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  CreditCard,
  Plus,
  TrendingUp,
  DollarSign,
  Calendar,
  Download,
  RefreshCw,
  Building,
  Zap,
} from 'lucide-react';
import { toast } from 'sonner';
import { StripePayment, CreditPurchase } from '@/components/StripePayment';
import { StripeConnect } from '@/components/StripeConnect';

interface CreditTransaction {
  id: string;
  transaction_type: string;
  amount: number;
  balance_before: number;
  balance_after: number;
  unit_cost_usd: number;
  total_cost_usd: number;
  description: string;
  created_at: string;
  expires_at: string | null;
  expired: boolean;
  stripe_payment_intent_id: string | null;
}

interface CreditHistory {
  success: boolean;
  credits: CreditTransaction[];
  total_count: number;
  current_balance: number;
}

interface PartnerInfo {
  id: string;
  name: string;
  email: string;
  quantum_credits: number;
  stripe_account_id?: string;
}

export default function BillingPage() {
  const [creditHistory, setCreditHistory] = useState<CreditHistory | null>(null);
  const [partnerInfo, setPartnerInfo] = useState<PartnerInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isPurchaseDialogOpen, setIsPurchaseDialogOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadBillingData();
  }, []);

  const loadBillingData = async () => {
    try {
      setIsLoading(true);
      
      // Load credit history
      const creditResponse = await fetch('/api/stripe/credits/history', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      
      if (creditResponse.ok) {
        const creditData = await creditResponse.json();
        setCreditHistory(creditData);
      }
      
      // Load partner info (assuming there's an endpoint for this)
      const partnerResponse = await fetch('/api/partner/profile', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      
      if (partnerResponse.ok) {
        const partnerData = await partnerResponse.json();
        setPartnerInfo(partnerData);
      }
      
    } catch (error) {
      console.error('Failed to load billing data:', error);
      toast.error('Failed to load billing information');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePurchaseSuccess = (paymentIntentId: string) => {
    toast.success('Payment successful! Your credits have been added.');
    setIsPurchaseDialogOpen(false);
    loadBillingData(); // Refresh data
  };

  const handlePurchaseError = (error: string) => {
    toast.error(`Payment failed: ${error}`);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getTransactionTypeColor = (type: string) => {
    switch (type) {
      case 'purchase':
        return 'bg-green-100 text-green-800';
      case 'usage':
        return 'bg-blue-100 text-blue-800';
      case 'bonus':
        return 'bg-purple-100 text-purple-800';
      case 'refund':
        return 'bg-yellow-100 text-yellow-800';
      case 'expiry':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const calculateMonthlySpend = () => {
    if (!creditHistory) return 0;
    
    const now = new Date();
    const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
    
    return creditHistory.credits
      .filter(credit => {
        const creditDate = new Date(credit.created_at);
        return creditDate >= monthStart && credit.transaction_type === 'purchase';
      })
      .reduce((total, credit) => total + (credit.total_cost_usd || 0), 0);
  };

  const calculateMonthlyUsage = () => {
    if (!creditHistory) return 0;
    
    const now = new Date();
    const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
    
    return creditHistory.credits
      .filter(credit => {
        const creditDate = new Date(credit.created_at);
        return creditDate >= monthStart && credit.transaction_type === 'usage';
      })
      .reduce((total, credit) => total + Math.abs(credit.amount), 0);
  };

  if (isLoading) {
    return (
      <div className="container mx-auto py-8">
        <div className="flex items-center justify-center h-64">
          <RefreshCw className="h-8 w-8 animate-spin" />
          <span className="ml-2">Loading billing information...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Billing & Credits</h1>
          <p className="text-gray-600 mt-1">
            Manage your quantum credits and payment settings
          </p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" onClick={loadBillingData}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Dialog open={isPurchaseDialogOpen} onOpenChange={setIsPurchaseDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Buy Credits
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Purchase Quantum Credits</DialogTitle>
                <DialogDescription>
                  Add credits to your account to use quantum computing services
                </DialogDescription>
              </DialogHeader>
              {partnerInfo && (
                <CreditPurchase
                  customerEmail={partnerInfo.email}
                  customerName={partnerInfo.name}
                  onSuccess={handlePurchaseSuccess}
                  onError={handlePurchaseError}
                />
              )}
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Current Balance</CardTitle>
            <Zap className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {creditHistory?.current_balance?.toLocaleString() || 0}
            </div>
            <p className="text-xs text-gray-600 mt-1">Quantum Credits</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Spend</CardTitle>
            <DollarSign className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${calculateMonthlySpend().toFixed(2)}
            </div>
            <p className="text-xs text-gray-600 mt-1">This month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Usage</CardTitle>
            <TrendingUp className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {calculateMonthlyUsage().toLocaleString()}
            </div>
            <p className="text-xs text-gray-600 mt-1">Credits used</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Transactions</CardTitle>
            <Calendar className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {creditHistory?.total_count || 0}
            </div>
            <p className="text-xs text-gray-600 mt-1">All time</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="overview">Transaction History</TabsTrigger>
          <TabsTrigger value="payment">Payment Methods</TabsTrigger>
          <TabsTrigger value="connect">Stripe Connect</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Recent Transactions</span>
                <Button variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </CardTitle>
              <CardDescription>
                Your quantum credit transaction history
              </CardDescription>
            </CardHeader>
            <CardContent>
              {creditHistory && creditHistory.credits.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Date</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Description</TableHead>
                      <TableHead className="text-right">Amount</TableHead>
                      <TableHead className="text-right">Cost</TableHead>
                      <TableHead className="text-right">Balance</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {creditHistory.credits.map((transaction) => (
                      <TableRow key={transaction.id}>
                        <TableCell className="text-sm">
                          {formatDate(transaction.created_at)}
                        </TableCell>
                        <TableCell>
                          <Badge className={getTransactionTypeColor(transaction.transaction_type)}>
                            {transaction.transaction_type}
                          </Badge>
                        </TableCell>
                        <TableCell className="max-w-xs truncate">
                          {transaction.description}
                        </TableCell>
                        <TableCell className="text-right font-mono">
                          <span className={transaction.amount >= 0 ? 'text-green-600' : 'text-red-600'}>
                            {transaction.amount >= 0 ? '+' : ''}{transaction.amount.toLocaleString()}
                          </span>
                        </TableCell>
                        <TableCell className="text-right font-mono">
                          {transaction.total_cost_usd ? `$${transaction.total_cost_usd.toFixed(2)}` : '-'}
                        </TableCell>
                        <TableCell className="text-right font-mono">
                          {transaction.balance_after.toLocaleString()}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <div className="text-center py-8">
                  <CreditCard className="h-16 w-16 mx-auto text-gray-400 mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No Transactions Yet</h3>
                  <p className="text-gray-600 mb-4">
                    Purchase your first quantum credits to get started
                  </p>
                  <Button onClick={() => setIsPurchaseDialogOpen(true)}>
                    <Plus className="h-4 w-4 mr-2" />
                    Buy Credits
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="payment" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Payment Methods</CardTitle>
              <CardDescription>
                Manage your payment methods and billing preferences
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-center py-8">
                  <CreditCard className="h-16 w-16 mx-auto text-gray-400 mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No Saved Payment Methods</h3>
                  <p className="text-gray-600 mb-4">
                    Payment methods are securely stored by Stripe during checkout
                  </p>
                  <Button onClick={() => setIsPurchaseDialogOpen(true)}>
                    <Plus className="h-4 w-4 mr-2" />
                    Add Payment Method
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="connect" className="space-y-6">
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Building className="mr-2 h-5 w-5" />
                  Payment Processing Setup
                </CardTitle>
                <CardDescription>
                  Set up Stripe Connect to receive payments from your customers
                </CardDescription>
              </CardHeader>
              <CardContent>
                <StripeConnect
                  onAccountSetup={(accountId) => {
                    toast.success('Stripe Connect account created successfully!');
                    loadBillingData();
                  }}
                  refreshUrl={`${window.location.origin}/billing?tab=connect&refresh=true`}
                  returnUrl={`${window.location.origin}/billing?tab=connect&success=true`}
                />
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}