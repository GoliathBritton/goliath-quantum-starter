'use client';

import { motion } from 'framer-motion';
import { ReactNode } from 'react';

const MotionDiv = motion.div as any;

// Fade in animation
export const FadeIn = ({ children, delay = 0, duration = 0.5 }: { children: ReactNode, delay?: number, duration?: number }) => {
  return (
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration, delay }}
    >
      {children}
    </MotionDiv>
  );
};

// Slide up animation
export const SlideUp = ({ children, delay = 0, duration = 0.5 }: { children: ReactNode, delay?: number, duration?: number }) => {
  return (
    <MotionDiv
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration, delay }}
    >
      {children}
    </MotionDiv>
  );
};

// Staggered children animation
export const StaggerContainer = ({ 
  children, 
  staggerDelay = 0.1,
  containerDelay = 0
}: { 
  children: ReactNode, 
  staggerDelay?: number,
  containerDelay?: number
}) => {
  return (
    <MotionDiv
      initial="hidden"
      animate="visible"
      variants={{
        hidden: { opacity: 0 },
        visible: {
          opacity: 1,
          transition: {
            delayChildren: containerDelay,
            staggerChildren: staggerDelay
          }
        }
      }}
    >
      {children}
    </MotionDiv>
  );
};

// Child item for staggered animations
export const StaggerItem = ({ children }: { children: ReactNode }) => {
  return (
    <MotionDiv
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 }
      }}
      transition={{ duration: 0.5 }}
    >
      {children}
    </MotionDiv>
  );
};

// Scale animation
export const ScaleIn = ({ children, delay = 0, duration = 0.5 }: { children: ReactNode, delay?: number, duration?: number }) => {
  return (
    <MotionDiv
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration, delay }}
    >
      {children}
    </MotionDiv>
  );
};

// Hover animation for cards and buttons
export const HoverScale = ({ children }: { children: ReactNode }) => {
  return (
    <MotionDiv
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.2 }}
    >
      {children}
    </MotionDiv>
  );
};

// Scroll-triggered animation
export const ScrollReveal = ({ children }: { children: ReactNode }) => {
  return (
    <MotionDiv
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.7 }}
    >
      {children}
    </MotionDiv>
  );
};