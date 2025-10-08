import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Check, CreditCard, X } from 'lucide-react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { API_BASE_URL } from '../utils/constants';

declare global {
  interface Window {
    PaystackPop: any;
  }
}

interface Plan {
  name: string;
  price: number;
  billing: string;
  description: string;
  features: string[];
  popular?: boolean;
  color: string;
}

const Pricing: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<string>(searchParams.get('plan') || '');

  const plans: Plan[] = [
    {
      name: 'Starter',
      price: 0,
      billing: 'Forever Free',
      description: 'Perfect for individuals and small projects',
      features: [
        '1GB Processing',
        'Basic Data Cleaning',
        'Community Support',
        '10 Datasets/month',
        'Email Support',
      ],
      color: 'from-gray-500 to-gray-700',
    },
    {
      name: 'Professional',
      price: 49,
      billing: 'per month',
      description: 'For growing teams and businesses',
      features: [
        '100GB Processing',
        'AI-Powered Cleaning',
        'Priority Support',
        '1000 Datasets/month',
        'API Access',
        'Custom Workflows',
        'Advanced Analytics',
      ],
      popular: true,
      color: 'from-cyan-500 to-blue-600',
    },
    {
      name: 'Enterprise',
      price: 299,
      billing: 'per month',
      description: 'For large organizations with custom needs',
      features: [
        'Unlimited Processing',
        'Custom AI Models',
        'Dedicated Support',
        'Unlimited Datasets',
        'Full API Access',
        'Custom Integrations',
        'SLA Guarantee',
        'On-premise Option',
      ],
      color: 'from-purple-500 to-pink-600',
    },
  ];

  const handleFreePlan = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('auth_token');
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      if (!token) {
        navigate('/auth?redirect=pricing');
        return;
      }

      const response = await fetch(`${API_BASE_URL}/payment/upgrade`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          plan: 'free',
          user_id: user.id,
        }),
      });

      const data = await response.json();
      if (data.success) {
        localStorage.setItem('user', JSON.stringify({ ...user, plan: 'free' }));
        navigate('/dashboard');
      } else {
        alert(data.message || 'Failed to select free plan');
      }
    } catch (error) {
      console.error('Free plan error:', error);
      alert('Failed to select free plan. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const initializePaystack = (plan: Plan) => {
    const token = localStorage.getItem('auth_token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (!token) {
      navigate('/auth?redirect=pricing');
      return;
    }

    if (plan.price === 0) {
      handleFreePlan();
      return;
    }

    setLoading(true);
    setSelectedPlan(plan.name);

    const handler = window.PaystackPop.setup({
      key: process.env.REACT_APP_PAYSTACK_PUBLIC_KEY || 'pk_test_xxxx',
      email: user.email,
      amount: plan.price * 100, // Paystack expects amount in kobo (cents)
      currency: 'USD',
      ref: `KEG-${Date.now()}-${Math.random().toString(36).substring(7)}`,
      metadata: {
        custom_fields: [
          {
            display_name: 'Plan',
            variable_name: 'plan',
            value: plan.name,
          },
          {
            display_name: 'User ID',
            variable_name: 'user_id',
            value: user.id,
          },
        ],
      },
      callback: async (response: any) => {
        await handlePaymentSuccess(response, plan);
      },
      onClose: () => {
        setLoading(false);
        setSelectedPlan('');
      },
    });

    handler.openIframe();
  };

  const handlePaymentSuccess = async (response: any, plan: Plan) => {
    try {
      const token = localStorage.getItem('auth_token');
      const user = JSON.parse(localStorage.getItem('user') || '{}');

      const res = await fetch(`${API_BASE_URL}/payment/verify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          reference: response.reference,
          plan: plan.name.toLowerCase(),
        }),
      });

      const data = await res.json();
      if (data.success) {
        localStorage.setItem('user', JSON.stringify({ ...user, plan: plan.name.toLowerCase() }));
        alert(`Successfully subscribed to ${plan.name} plan!`);
        navigate('/dashboard');
      } else {
        alert(data.message || 'Payment verification failed');
      }
    } catch (error) {
      console.error('Payment verification error:', error);
      alert('Payment verification failed. Please try again.');
    } finally {
      setLoading(false);
      setSelectedPlan('');
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-black text-black dark:text-white py-20 px-4">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-cyan-700 to-purple-700 dark:from-cyan-500 dark:to-purple-500 bg-clip-text text-transparent">
            Choose Your Plan
          </h1>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Select the perfect plan for your needs. Unlock advanced features and scale your data processing with Keginator.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="grid md:grid-cols-3 gap-8"
        >
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
              className={`relative p-6 bg-white/80 dark:bg-black/40 backdrop-blur-sm rounded-xl border border-gray-300/50 dark:border-gray-800/50 shadow-lg ${
                plan.popular ? 'border-cyan-500/50' : ''
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-cyan-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                    Popular
                  </span>
                </div>
              )}

              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <div className="text-4xl font-bold mb-2">
                ${plan.price}
                <span className="text-lg font-normal text-gray-600 dark:text-gray-400"> {plan.billing}</span>
              </div>
              <p className="text-gray-600 dark:text-gray-400 mb-6">{plan.description}</p>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-center space-x-2">
                    <Check className="w-5 h-5 text-green-500" />
                    <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                  </li>
                ))}
              </ul>

              <motion.button
                onClick={() => initializePaystack(plan)}
                disabled={loading && selectedPlan === plan.name}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`w-full py-3 rounded-lg font-bold flex items-center justify-center space-x-2 transition-colors ${
                  plan.popular
                    ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white hover:from-cyan-600 hover:to-blue-700'
                    : 'bg-gradient-to-r from-gray-500 to-gray-700 text-white hover:from-gray-600 hover:to-gray-800'
                } disabled:opacity-50`}
              >
                {loading && selectedPlan === plan.name ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                      className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                    />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <CreditCard className="w-5 h-5" />
                    <span>{plan.price === 0 ? 'Get Started' : 'Subscribe Now'}</span>
                  </>
                )}
              </motion.button>
            </motion.div>
          ))}
        </motion.div>

        <div className="mt-12 text-center">
          <motion.button
            onClick={() => navigate('/dashboard')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-6 py-2 text-cyan-600 dark:text-cyan-400 hover:underline flex items-center space-x-2 mx-auto"
          >
            <X className="w-5 h-5" />
            <span>Back to Dashboard</span>
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default Pricing;