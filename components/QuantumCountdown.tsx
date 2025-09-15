import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface CountdownState {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
  isLaunched: boolean;
}

interface RewardTier {
  threshold: number; // days remaining
  title: string;
  description: string;
  credits: number;
  unlocked: boolean;
}

interface QuantumCountdownProps {
  launchDate?: string;
  onRewardUnlock?: (tier: RewardTier) => void;
  className?: string;
}

const QuantumCountdown: React.FC<QuantumCountdownProps> = ({
  launchDate = "2025-12-01T00:00:00Z",
  onRewardUnlock,
  className = ""
}) => {
  const [countdown, setCountdown] = useState<CountdownState>({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
    isLaunched: false
  });

  const [superpositionDigits, setSuperpositionDigits] = useState<{
    [key: string]: number[]
  }>({});

  const [unlockedGlyphs, setUnlockedGlyphs] = useState<string[]>([]);
  const [mysteryPhrase, setMysteryPhrase] = useState<string>("");

  const rewardTiers: RewardTier[] = [
    {
      threshold: 30,
      title: "Quantum Initiate",
      description: "Free access to Quantum Agent templates",
      credits: 100,
      unlocked: false
    },
    {
      threshold: 14,
      title: "Quantum Adept",
      description: "Early-bird premium trial extension",
      credits: 250,
      unlocked: false
    },
    {
      threshold: 7,
      title: "Quantum Master",
      description: "Unlock Quantum Glyphs NFT-style badges",
      credits: 500,
      unlocked: false
    },
    {
      threshold: 0,
      title: "QHC Founder",
      description: "Access to Quantum High Council private event",
      credits: 1000,
      unlocked: false
    }
  ];

  const quantumGlyphs = [
    "⟨ψ|φ⟩", "∫∞", "⊗", "∇²", "ℏ", "∆E∆t", "⟨0|1⟩", "∑∞"
  ];

  const mysteryPhrases = [
    "Time is collapsing...",
    "The entanglement begins...",
    "Quantum states align...",
    "The High Council assembles...",
    "Reality shifts..."
  ];

  // Generate superposition effect for digits
  const generateSuperposition = (actualValue: number): number[] => {
    const variations = [];
    for (let i = 0; i < 5; i++) {
      variations.push(Math.floor(Math.random() * 10));
    }
    variations.push(actualValue); // Collapse to actual value
    return variations;
  };

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date().getTime();
      const launch = new Date(launchDate).getTime();
      const distance = launch - now;

      if (distance < 0) {
        setCountdown({
          days: 0,
          hours: 0,
          minutes: 0,
          seconds: 0,
          isLaunched: true
        });
        setMysteryPhrase("🚀 The Quantum High Council has launched!");
        return;
      }

      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);

      // Generate superposition for each digit
      setSuperpositionDigits({
        days: generateSuperposition(days),
        hours: generateSuperposition(hours),
        minutes: generateSuperposition(minutes),
        seconds: generateSuperposition(seconds)
      });

      setCountdown({ days, hours, minutes, seconds, isLaunched: false });

      // Unlock glyphs based on time remaining
      const totalHours = Math.floor(distance / (1000 * 60 * 60));
      const glyphsToUnlock = Math.max(0, quantumGlyphs.length - Math.floor(totalHours / 24));
      setUnlockedGlyphs(quantumGlyphs.slice(0, glyphsToUnlock));

      // Update mystery phrase
      const phraseIndex = Math.min(
        mysteryPhrases.length - 1,
        Math.floor((30 - days) / 6)
      );
      if (phraseIndex >= 0) {
        setMysteryPhrase(mysteryPhrases[phraseIndex]);
      }

      // Check for reward unlocks
      rewardTiers.forEach(tier => {
        if (days <= tier.threshold && !tier.unlocked && onRewardUnlock) {
          tier.unlocked = true;
          onRewardUnlock(tier);
        }
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [launchDate, onRewardUnlock]);

  const SuperpositionDigit: React.FC<{ value: number; label: string }> = ({ value, label }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const digits = superpositionDigits[label.toLowerCase()] || [value];

    useEffect(() => {
      if (digits.length > 1) {
        const superpositionInterval = setInterval(() => {
          setCurrentIndex(prev => (prev + 1) % digits.length);
        }, 100);

        const collapseTimeout = setTimeout(() => {
          clearInterval(superpositionInterval);
          setCurrentIndex(digits.length - 1); // Collapse to actual value
        }, 900);

        return () => {
          clearInterval(superpositionInterval);
          clearTimeout(collapseTimeout);
        };
      }
    }, [digits]);

    return (
      <motion.div
        className="quantum-digit-container"
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.span
          className="quantum-digit"
          key={`${label}-${currentIndex}`}
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 20, opacity: 0 }}
          transition={{ duration: 0.1 }}
        >
          {String(digits[currentIndex] || value).padStart(2, '0')}
        </motion.span>
        <span className="quantum-label">{label}</span>
      </motion.div>
    );
  };

  if (countdown.isLaunched) {
    return (
      <motion.div
        className={`quantum-countdown launched ${className}`}
        initial={{ scale: 0.5, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 1, type: "spring" }}
      >
        <div className="quantum-nexus-animation">
          <div className="nexus-core"></div>
          <div className="nexus-rings">
            {[...Array(3)].map((_, i) => (
              <div key={i} className={`nexus-ring ring-${i + 1}`}></div>
            ))}
          </div>
        </div>
        <h2 className="launch-message">{mysteryPhrase}</h2>
        <div className="quantum-glyphs-final">
          {quantumGlyphs.map((glyph, index) => (
            <motion.span
              key={index}
              className="glyph"
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              {glyph}
            </motion.span>
          ))}
        </div>
      </motion.div>
    );
  }

  return (
    <div className={`quantum-countdown ${className}`}>
      <div className="countdown-header">
        <h2 className="countdown-title">
          <span className="quantum-text">Quantum High Council</span>
          <span className="launch-text">Launch Sequence</span>
        </h2>
        {mysteryPhrase && (
          <motion.p
            className="mystery-phrase"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            key={mysteryPhrase}
          >
            {mysteryPhrase}
          </motion.p>
        )}
      </div>

      <div className="countdown-display">
        <div className="entanglement-rings">
          {[...Array(3)].map((_, i) => (
            <div key={i} className={`entanglement-ring ring-${i + 1}`}></div>
          ))}
        </div>
        
        <div className="digits-container">
          <SuperpositionDigit value={countdown.days} label="Days" />
          <span className="separator">:</span>
          <SuperpositionDigit value={countdown.hours} label="Hours" />
          <span className="separator">:</span>
          <SuperpositionDigit value={countdown.minutes} label="Minutes" />
          <span className="separator">:</span>
          <SuperpositionDigit value={countdown.seconds} label="Seconds" />
        </div>
      </div>

      {unlockedGlyphs.length > 0 && (
        <motion.div
          className="quantum-glyphs"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <p className="glyphs-label">Quantum Glyphs Unlocked:</p>
          <div className="glyphs-grid">
            <AnimatePresence>
              {unlockedGlyphs.map((glyph, index) => (
                <motion.span
                  key={glyph}
                  className="glyph"
                  initial={{ opacity: 0, scale: 0, rotate: 180 }}
                  animate={{ opacity: 1, scale: 1, rotate: 0 }}
                  exit={{ opacity: 0, scale: 0 }}
                  transition={{ delay: index * 0.1, type: "spring" }}
                >
                  {glyph}
                </motion.span>
              ))}
            </AnimatePresence>
          </div>
        </motion.div>
      )}

      <div className="quantum-energy-field"></div>
    </div>
  );
};

export default QuantumCountdown;