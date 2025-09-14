import type { NextApiRequest, NextApiResponse } from "next";
import Stripe from "stripe";

// Initialize Stripe with secret key
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || "sk_test_dummy_key", {
  apiVersion: "2025-08-27.basil",
});

interface CheckoutRequest {
  productId: "starter" | "pro" | "enterprise" | "omniscient" | "echelon" | "aeon";
  planType?: "monthly" | "yearly" | "payPerJob";
  userId?: string;
  metadata?: Record<string, any>;
}

interface CheckoutResponse {
  id: string;
  url: string;
  message: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<CheckoutResponse | { error: string }>
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { productId, planType = "monthly", userId, metadata }: CheckoutRequest = req.body;

    if (!productId) {
      return res.status(400).json({ error: "Product ID is required" });
    }

    // Define pricing structure
    const pricingConfig = {
      starter: {
        monthly: { amount: 59900, name: "FLYFOX AI Starter Monthly", tier: "starter" }, // $599
        yearly: { amount: 599000, name: "FLYFOX AI Starter Yearly", tier: "starter" }, // $5990
        payPerJob: { amount: 9900, name: "FLYFOX AI Starter Pay-per-Job", tier: "starter" } // $99
      },
      pro: {
        monthly: { amount: 299900, name: "FLYFOX AI Pro Monthly", tier: "pro" }, // $2999
        yearly: { amount: 2999000, name: "FLYFOX AI Pro Yearly", tier: "pro" }, // $29990
        payPerJob: { amount: 49900, name: "FLYFOX AI Pro Pay-per-Job", tier: "pro" } // $499
      },
      enterprise: {
        monthly: { amount: 1499900, name: "FLYFOX Enterprise Monthly", tier: "enterprise" }, // $14999
        yearly: { amount: 14999000, name: "FLYFOX Enterprise Yearly", tier: "enterprise" }, // $149990
        payPerJob: { amount: 249900, name: "FLYFOX Enterprise Pay-per-Job", tier: "enterprise" } // $2499
      },
      omniscient: {
        monthly: { amount: 2999900, name: "Omniscient Basic™ Monthly", tier: "omniscient" }, // $29999
        yearly: { amount: 29999000, name: "Omniscient Basic™ Yearly", tier: "omniscient" }, // $299990
        payPerJob: { amount: 499900, name: "Omniscient Basic™ Pay-per-Job", tier: "omniscient" } // $4999
      },
      echelon: {
        monthly: { amount: 14999900, name: "Echelon Pro™ Monthly", tier: "echelon" }, // $149999
        yearly: { amount: 149999000, name: "Echelon Pro™ Yearly", tier: "echelon" }, // $1499990
        payPerJob: { amount: 2499900, name: "Echelon Pro™ Pay-per-Job", tier: "echelon" } // $24999
      },
      aeon: {
        monthly: { amount: 59999900, name: "Aeon Enterprise™ Monthly", tier: "aeon" }, // $599999
        yearly: { amount: 599999000, name: "Aeon Enterprise™ Yearly", tier: "aeon" }, // $5999990
        payPerJob: { amount: 9999900, name: "Aeon Enterprise™ Pay-per-Job", tier: "aeon" } // $99999
      }
    };

    const selectedPlan = pricingConfig[productId]?.[planType];
    if (!selectedPlan) {
      return res.status(400).json({ error: "Invalid product or plan type" });
    }

    // Create Stripe checkout session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      line_items: [
        {
          price_data: {
            currency: "usd",
            product_data: {
              name: selectedPlan.name,
              description: getProductDescription(productId, planType),
              images: [`${req.headers.origin}/images/quantum-logo.png`],
              metadata: {
                productId,
                planType,
                userId: userId || "anonymous"
              }
            },
            unit_amount: selectedPlan.amount,
            ...(planType !== "payPerJob" && {
              recurring: {
                interval: planType === "yearly" ? "year" : "month"
              }
            })
          },
          quantity: 1,
        },
      ],
      mode: planType === "payPerJob" ? "payment" : "subscription",
      success_url: `${req.headers.origin}/success?session_id={CHECKOUT_SESSION_ID}&product=${productId}&plan=${planType}`,
      cancel_url: `${req.headers.origin}/cancel?product=${productId}`,
      metadata: {
        productId,
        planType,
        tier: selectedPlan.tier || "premium",
        userId: userId || "anonymous",
        ...metadata
      },
      customer_email: metadata?.email,
      allow_promotion_codes: true,
      billing_address_collection: "required",
      tax_id_collection: {
        enabled: true
      }
    });

    console.log(`[Stripe] Checkout session created: ${session.id} for ${productId} ${planType}`);

    return res.status(200).json({
      id: session.id,
      url: session.url!,
      message: `Checkout session created for ${selectedPlan.name}`
    });

  } catch (error) {
    console.error("[Stripe] Error creating checkout session:", error);
    
    if (error instanceof Stripe.errors.StripeError) {
      return res.status(400).json({ 
        error: `Stripe error: ${error.message}` 
      });
    }
    
    return res.status(500).json({ 
      error: "Internal server error while creating checkout session" 
    });
  }
}

function getProductDescription(productId: string, planType: string): string {
  const descriptions = {
    starter: {
      monthly: "FLYFOX AI Starter - Chatbots & Automation with basic AI capabilities and workflow automation.",
      yearly: "Annual starter subscription with significant savings and foundational AI features.",
      payPerJob: "Pay-as-you-go starter features for small projects and testing."
    },
    pro: {
      monthly: "FLYFOX AI Pro - Voice Agents & Digital Humans with advanced conversational AI and avatar technology.",
      yearly: "Annual pro subscription with enhanced features and priority support.",
      payPerJob: "Professional-grade AI processing for specific high-value projects."
    },
    enterprise: {
      monthly: "FLYFOX Enterprise - Multi-agent AI Systems with complete enterprise solution and dedicated support.",
      yearly: "Enterprise annual plan with maximum value and dedicated account management.",
      payPerJob: "Enterprise-grade processing for mission-critical projects."
    },
    omniscient: {
      monthly: "Omniscient Basic™ - The All-Seeing Decision Engine with advanced predictive analytics and decision support.",
      yearly: "Annual omniscient subscription with comprehensive foresight capabilities.",
      payPerJob: "Omniscient-level analysis for critical decision-making projects."
    },
    echelon: {
      monthly: "Echelon Pro™ - Government-grade Black-box Intelligence with top-tier security and advanced AI capabilities.",
      yearly: "Annual echelon subscription with maximum security and intelligence features.",
      payPerJob: "Government-grade intelligence processing for sensitive operations."
    },
    aeon: {
      monthly: "Aeon Enterprise™ - Auto-execution with AGI Foresight providing ultimate AI capabilities and autonomous execution.",
      yearly: "Annual aeon subscription with cutting-edge AGI technology and foresight.",
      payPerJob: "AGI-level processing for the most complex and strategic initiatives."
    }
  };

  return descriptions[productId as keyof typeof descriptions]?.[planType as keyof typeof descriptions.starter] || 
         "Advanced AI and automation capabilities";
}