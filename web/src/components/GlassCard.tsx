'use client';

import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';
import { cn } from '@/lib/utils';

interface GlassCardProps extends Omit<HTMLMotionProps<'div'>, 'children'> {
  children: React.ReactNode;
  variant?: 'default' | 'primary' | 'secondary' | 'accent';
  intensity?: 'light' | 'medium' | 'strong';
  border?: boolean;
  glow?: boolean;
  hover?: boolean;
  className?: string;
}

const variants = {
  default: {
    light: 'bg-white/5 backdrop-blur-sm',
    medium: 'bg-white/10 backdrop-blur-md',
    strong: 'bg-white/15 backdrop-blur-lg'
  },
  primary: {
    light: 'bg-blue-500/10 backdrop-blur-sm',
    medium: 'bg-blue-500/15 backdrop-blur-md',
    strong: 'bg-blue-500/20 backdrop-blur-lg'
  },
  secondary: {
    light: 'bg-purple-500/10 backdrop-blur-sm',
    medium: 'bg-purple-500/15 backdrop-blur-md',
    strong: 'bg-purple-500/20 backdrop-blur-lg'
  },
  accent: {
    light: 'bg-emerald-500/10 backdrop-blur-sm',
    medium: 'bg-emerald-500/15 backdrop-blur-md',
    strong: 'bg-emerald-500/20 backdrop-blur-lg'
  }
};

const borderVariants = {
  default: 'border border-white/20',
  primary: 'border border-blue-400/30',
  secondary: 'border border-purple-400/30',
  accent: 'border border-emerald-400/30'
};

const glowVariants = {
  default: 'shadow-lg shadow-white/10',
  primary: 'shadow-lg shadow-blue-500/20',
  secondary: 'shadow-lg shadow-purple-500/20',
  accent: 'shadow-lg shadow-emerald-500/20'
};

export default function GlassCard({
  children,
  variant = 'default',
  intensity = 'medium',
  border = true,
  glow = false,
  hover = true,
  className,
  ...props
}: GlassCardProps) {
  const baseClasses = cn(
    'rounded-xl relative overflow-hidden',
    variants[variant][intensity],
    border && borderVariants[variant],
    glow && glowVariants[variant],
    className
  );

  const hoverAnimation = hover ? {
    scale: 1.02,
    y: -2,
    transition: { duration: 0.2, ease: 'easeOut' }
  } : {};

  const tapAnimation = hover ? {
    scale: 0.98,
    transition: { duration: 0.1 }
  } : {};

  return (
    <motion.div
      className={baseClasses}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={hoverAnimation}
      whileTap={tapAnimation}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      {...props}
    >
      {/* Gradient overlay for extra depth */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent pointer-events-none" />
      
      {/* Content */}
      <div className="relative z-10">
        {children}
      </div>
      
      {/* Animated border glow */}
      {glow && (
        <motion.div
          className={cn(
            'absolute inset-0 rounded-xl opacity-0',
            variant === 'primary' && 'bg-gradient-to-r from-blue-400/20 to-cyan-400/20',
            variant === 'secondary' && 'bg-gradient-to-r from-purple-400/20 to-pink-400/20',
            variant === 'accent' && 'bg-gradient-to-r from-emerald-400/20 to-teal-400/20',
            variant === 'default' && 'bg-gradient-to-r from-white/10 to-gray-200/10'
          )}
          animate={{
            opacity: [0, 0.5, 0],
            scale: [1, 1.02, 1]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut'
          }}
        />
      )}
    </motion.div>
  );
}

// Specialized glass components
export function GlassButton({
  children,
  variant = 'primary',
  size = 'md',
  className,
  ...props
}: {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'accent' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
} & HTMLMotionProps<'button'>) {
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  const variantClasses = {
    primary: 'bg-blue-500/20 border-blue-400/30 text-blue-100 hover:bg-blue-500/30',
    secondary: 'bg-purple-500/20 border-purple-400/30 text-purple-100 hover:bg-purple-500/30',
    accent: 'bg-emerald-500/20 border-emerald-400/30 text-emerald-100 hover:bg-emerald-500/30',
    ghost: 'bg-white/10 border-white/20 text-white hover:bg-white/20'
  };

  return (
    <motion.button
      className={cn(
        'rounded-lg backdrop-blur-md border font-medium transition-all duration-200',
        'focus:outline-none focus:ring-2 focus:ring-white/20',
        sizeClasses[size],
        variantClasses[variant],
        className
      )}
      whileHover={{ scale: 1.05, y: -1 }}
      whileTap={{ scale: 0.95 }}
      transition={{ duration: 0.1 }}
      {...props}
    >
      {children}
    </motion.button>
  );
}

export function GlassInput({
  className,
  ...props
}: {
  className?: string;
} & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <motion.input
      className={cn(
        'w-full px-4 py-3 rounded-lg',
        'bg-white/10 backdrop-blur-md border border-white/20',
        'text-white placeholder-white/60',
        'focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50',
        'transition-all duration-200',
        className
      )}
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
      {...props}
    />
  );
}

export function GlassSelect({
  children,
  className,
  ...props
}: {
  children: React.ReactNode;
  className?: string;
} & React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <motion.select
      className={cn(
        'w-full px-4 py-3 rounded-lg',
        'bg-white/10 backdrop-blur-md border border-white/20',
        'text-white',
        'focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50',
        'transition-all duration-200',
        className
      )}
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
      {...props}
    >
      {children}
    </motion.select>
  );
}

export function GlassModal({
  children,
  isOpen,
  onClose,
  className
}: {
  children: React.ReactNode;
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}) {
  if (!isOpen) return null;

  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />
      
      {/* Modal content */}
      <motion.div
        className={cn(
          'relative max-w-lg w-full max-h-[90vh] overflow-auto',
          'bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl',
          'shadow-2xl shadow-black/50',
          className
        )}
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.9, y: 20 }}
        transition={{ duration: 0.2 }}
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </motion.div>
    </motion.div>
  );
}

export function GlassTooltip({
  children,
  content,
  position = 'top'
}: {
  children: React.ReactNode;
  content: string;
  position?: 'top' | 'bottom' | 'left' | 'right';
}) {
  const [isVisible, setIsVisible] = React.useState(false);

  const positionClasses = {
    top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 transform -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 transform -translate-y-1/2 ml-2'
  };

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}
      {isVisible && (
        <motion.div
          className={cn(
            'absolute z-50 px-3 py-2 text-sm text-white',
            'bg-black/80 backdrop-blur-md border border-white/20 rounded-lg',
            'whitespace-nowrap pointer-events-none',
            positionClasses[position]
          )}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          transition={{ duration: 0.1 }}
        >
          {content}
        </motion.div>
      )}
    </div>
  );
}