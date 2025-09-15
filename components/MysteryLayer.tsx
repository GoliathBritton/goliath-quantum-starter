import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface MysteryLayerProps {
  timeRemaining: number; // milliseconds until launch
  className?: string;
  onGlyphUnlock?: (glyph: string, index: number) => void;
  onMysteryComplete?: () => void;
}

interface Glyph {
  id: string;
  symbol: string;
  name: string;
  unlockThreshold: number; // hours before launch
  description: string;
  power: string;
  unlocked: boolean;
}

interface MysteryPhrase {
  id: string;
  text: string;
  unlockThreshold: number;
  revealed: boolean;
}

const QUANTUM_GLYPHS: Glyph[] = [
  {
    id: 'nexus',
    symbol: '⧬',
    name: 'Nexus Core',
    unlockThreshold: 720, // 30 days
    description: 'The fundamental connection point of all quantum realities',
    power: 'Grants access to the Quantum Network',
    unlocked: false
  },
  {
    id: 'entanglement',
    symbol: '⟐',
    name: 'Entanglement Matrix',
    unlockThreshold: 336, // 14 days
    description: 'Binds consciousness across dimensional barriers',
    power: 'Enables quantum communication protocols',
    unlocked: false
  },
  {
    id: 'superposition',
    symbol: '⧨',
    name: 'Superposition Gate',
    unlockThreshold: 168, // 7 days
    description: 'Exists in multiple states simultaneously',
    power: 'Unlocks parallel processing capabilities',
    unlocked: false
  },
  {
    id: 'observer',
    symbol: '◉',
    name: 'Observer Lens',
    unlockThreshold: 72, // 3 days
    description: 'Collapses probability waves through conscious observation',
    power: 'Reveals hidden quantum patterns',
    unlocked: false
  },
  {
    id: 'catalyst',
    symbol: '⟡',
    name: 'Quantum Catalyst',
    unlockThreshold: 24, // 1 day
    description: 'Accelerates quantum state transitions',
    power: 'Amplifies all quantum abilities',
    unlocked: false
  },
  {
    id: 'singularity',
    symbol: '◈',
    name: 'Singularity Key',
    unlockThreshold: 1, // 1 hour
    description: 'The final key to unlock the Quantum High Council',
    power: 'Opens the gateway to infinite possibilities',
    unlocked: false
  }
];

const MYSTERY_PHRASES: MysteryPhrase[] = [
  {
    id: 'phase1',
    text: 'The quantum field awakens...',
    unlockThreshold: 720,
    revealed: false
  },
  {
    id: 'phase2',
    text: 'Reality bends to conscious will...',
    unlockThreshold: 336,
    revealed: false
  },
  {
    id: 'phase3',
    text: 'The Council stirs in the void...',
    unlockThreshold: 168,
    revealed: false
  },
  {
    id: 'phase4',
    text: 'Dimensions collapse into unity...',
    unlockThreshold: 72,
    revealed: false
  },
  {
    id: 'phase5',
    text: 'The final transformation begins...',
    unlockThreshold: 24,
    revealed: false
  },
  {
    id: 'phase6',
    text: 'Welcome to the Quantum High Council.',
    unlockThreshold: 0,
    revealed: false
  }
];

export const MysteryLayer: React.FC<MysteryLayerProps> = ({
  timeRemaining,
  className = '',
  onGlyphUnlock,
  onMysteryComplete
}) => {
  const [glyphs, setGlyphs] = useState<Glyph[]>(QUANTUM_GLYPHS);
  const [phrases, setPhrases] = useState<MysteryPhrase[]>(MYSTERY_PHRASES);
  const [selectedGlyph, setSelectedGlyph] = useState<Glyph | null>(null);
  const [hologramVisible, setHologramVisible] = useState(false);
  const [mysteryComplete, setMysteryComplete] = useState(false);

  const hoursRemaining = Math.floor(timeRemaining / (1000 * 60 * 60));

  // Check for newly unlocked glyphs and phrases
  const checkUnlocks = useCallback(() => {
    let hasNewUnlocks = false;

    // Check glyphs
    setGlyphs(prevGlyphs => 
      prevGlyphs.map(glyph => {
        if (!glyph.unlocked && hoursRemaining <= glyph.unlockThreshold) {
          hasNewUnlocks = true;
          onGlyphUnlock?.(glyph.symbol, glyph.unlockThreshold);
          return { ...glyph, unlocked: true };
        }
        return glyph;
      })
    );

    // Check phrases
    setPhrases(prevPhrases => 
      prevPhrases.map(phrase => {
        if (!phrase.revealed && hoursRemaining <= phrase.unlockThreshold) {
          hasNewUnlocks = true;
          return { ...phrase, revealed: true };
        }
        return phrase;
      })
    );

    // Check if mystery is complete
    if (hoursRemaining <= 0 && !mysteryComplete) {
      setMysteryComplete(true);
      setHologramVisible(true);
      onMysteryComplete?.();
    }

    return hasNewUnlocks;
  }, [hoursRemaining, onGlyphUnlock, onMysteryComplete, mysteryComplete]);

  useEffect(() => {
    checkUnlocks();
  }, [checkUnlocks]);

  const unlockedGlyphs = glyphs.filter(g => g.unlocked);
  const currentPhrase = phrases.find(p => p.revealed && hoursRemaining <= p.unlockThreshold);
  const latestPhrase = phrases.filter(p => p.revealed).sort((a, b) => a.unlockThreshold - b.unlockThreshold)[0];

  return (
    <div className={`mystery-layer ${className}`}>
      {/* Mystery Phrase Display */}
      <AnimatePresence mode="wait">
        {(currentPhrase || latestPhrase) && (
          <motion.div
            key={(currentPhrase || latestPhrase)?.id}
            className="mystery-phrase"
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.9 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <motion.div
              className="phrase-text"
              animate={{
                textShadow: [
                  '0 0 10px #00fff6',
                  '0 0 20px #00fff6, 0 0 30px #8000ff',
                  '0 0 10px #00fff6'
                ]
              }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            >
              {(currentPhrase || latestPhrase)?.text}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Glyph Grid */}
      <div className="glyph-grid">
        {glyphs.map((glyph, index) => (
          <motion.div
            key={glyph.id}
            className={`glyph-container ${
              glyph.unlocked ? 'unlocked' : 'locked'
            } ${selectedGlyph?.id === glyph.id ? 'selected' : ''}`}
            initial={{ opacity: 0, scale: 0 }}
            animate={{
              opacity: glyph.unlocked ? 1 : 0.3,
              scale: glyph.unlocked ? 1 : 0.8,
              rotateY: glyph.unlocked ? [0, 360] : 0
            }}
            transition={{
              duration: glyph.unlocked ? 1.5 : 0.5,
              delay: glyph.unlocked ? index * 0.2 : 0,
              ease: "easeOut"
            }}
            whileHover={glyph.unlocked ? { scale: 1.1, rotateZ: 5 } : {}}
            whileTap={glyph.unlocked ? { scale: 0.95 } : {}}
            onClick={() => glyph.unlocked && setSelectedGlyph(glyph)}
          >
            <motion.div
              className="glyph-symbol"
              animate={glyph.unlocked ? {
                color: ['#00fff6', '#8000ff', '#ff0080', '#00fff6'],
                filter: [
                  'drop-shadow(0 0 10px #00fff6)',
                  'drop-shadow(0 0 20px #8000ff)',
                  'drop-shadow(0 0 15px #ff0080)',
                  'drop-shadow(0 0 10px #00fff6)'
                ]
              } : {}}
              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
            >
              {glyph.unlocked ? glyph.symbol : '◯'}
            </motion.div>
            
            {glyph.unlocked && (
              <motion.div
                className="glyph-name"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                {glyph.name}
              </motion.div>
            )}
            
            {!glyph.unlocked && (
              <div className="unlock-timer">
                {hoursRemaining > glyph.unlockThreshold 
                  ? `${glyph.unlockThreshold}h to unlock`
                  : 'Unlocking...'
                }
              </div>
            )}
          </motion.div>
        ))}
      </div>

      {/* Glyph Detail Modal */}
      <AnimatePresence>
        {selectedGlyph && (
          <motion.div
            className="glyph-modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedGlyph(null)}
          >
            <motion.div
              className="glyph-modal"
              initial={{ scale: 0.8, opacity: 0, rotateY: -90 }}
              animate={{ scale: 1, opacity: 1, rotateY: 0 }}
              exit={{ scale: 0.8, opacity: 0, rotateY: 90 }}
              transition={{ type: "spring", damping: 20, stiffness: 300 }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="modal-header">
                <motion.div
                  className="modal-glyph"
                  animate={{
                    rotateZ: [0, 360],
                    scale: [1, 1.2, 1]
                  }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                >
                  {selectedGlyph.symbol}
                </motion.div>
                <h3 className="modal-title">{selectedGlyph.name}</h3>
              </div>
              
              <div className="modal-content">
                <p className="modal-description">{selectedGlyph.description}</p>
                <div className="modal-power">
                  <strong>Quantum Power:</strong> {selectedGlyph.power}
                </div>
              </div>
              
              <button 
                className="modal-close"
                onClick={() => setSelectedGlyph(null)}
              >
                ✕
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Quantum Nexus Hologram */}
      <AnimatePresence>
        {hologramVisible && (
          <motion.div
            className="quantum-hologram"
            initial={{ opacity: 0, scale: 0, rotateY: -180 }}
            animate={{ 
              opacity: 1, 
              scale: 1, 
              rotateY: 0,
              rotateZ: [0, 360]
            }}
            exit={{ opacity: 0, scale: 0, rotateY: 180 }}
            transition={{ 
              duration: 2, 
              ease: "easeOut",
              rotateZ: { duration: 10, repeat: Infinity, ease: "linear" }
            }}
          >
            <motion.div
              className="hologram-core"
              animate={{
                boxShadow: [
                  '0 0 20px #00fff6, inset 0 0 20px #00fff6',
                  '0 0 40px #8000ff, inset 0 0 40px #8000ff',
                  '0 0 60px #ff0080, inset 0 0 60px #ff0080',
                  '0 0 20px #00fff6, inset 0 0 20px #00fff6'
                ]
              }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            >
              <div className="hologram-text">QUANTUM HIGH COUNCIL</div>
              <div className="hologram-subtext">NEXUS ACTIVATED</div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <style jsx>{`
        .mystery-layer {
          position: relative;
          padding: 2rem;
          background: rgba(0, 0, 0, 0.8);
          border-radius: 20px;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(0, 255, 246, 0.2);
        }

        .mystery-phrase {
          text-align: center;
          margin-bottom: 2rem;
        }

        .phrase-text {
          font-size: 1.5rem;
          font-weight: 700;
          color: #00fff6;
          font-style: italic;
          letter-spacing: 1px;
        }

        .glyph-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 1.5rem;
          margin: 2rem 0;
        }

        .glyph-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 1rem;
          border-radius: 15px;
          background: rgba(0, 255, 246, 0.05);
          border: 1px solid rgba(0, 255, 246, 0.2);
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
        }

        .glyph-container.unlocked {
          background: rgba(0, 255, 246, 0.1);
          border-color: rgba(0, 255, 246, 0.4);
        }

        .glyph-container.locked {
          background: rgba(128, 128, 128, 0.05);
          border-color: rgba(128, 128, 128, 0.2);
          cursor: not-allowed;
        }

        .glyph-container.selected {
          border-color: #8000ff;
          box-shadow: 0 0 20px rgba(128, 0, 255, 0.5);
        }

        .glyph-symbol {
          font-size: 3rem;
          margin-bottom: 0.5rem;
          font-weight: 900;
        }

        .glyph-name {
          font-size: 0.9rem;
          color: #00fff6;
          text-align: center;
          font-weight: 600;
        }

        .unlock-timer {
          font-size: 0.8rem;
          color: #888;
          text-align: center;
          margin-top: 0.5rem;
        }

        .glyph-modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.8);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
          backdrop-filter: blur(5px);
        }

        .glyph-modal {
          background: linear-gradient(135deg, rgba(0, 255, 246, 0.1), rgba(128, 0, 255, 0.1));
          border: 2px solid rgba(0, 255, 246, 0.3);
          border-radius: 20px;
          padding: 2rem;
          max-width: 400px;
          width: 90%;
          position: relative;
          backdrop-filter: blur(20px);
        }

        .modal-header {
          text-align: center;
          margin-bottom: 1.5rem;
        }

        .modal-glyph {
          font-size: 4rem;
          color: #00fff6;
          margin-bottom: 1rem;
        }

        .modal-title {
          font-size: 1.5rem;
          color: #8000ff;
          margin: 0;
        }

        .modal-content {
          text-align: center;
        }

        .modal-description {
          color: #ccc;
          margin-bottom: 1rem;
          line-height: 1.6;
        }

        .modal-power {
          color: #00fff6;
          font-size: 0.9rem;
          padding: 1rem;
          background: rgba(0, 255, 246, 0.1);
          border-radius: 10px;
          border: 1px solid rgba(0, 255, 246, 0.2);
        }

        .modal-close {
          position: absolute;
          top: 1rem;
          right: 1rem;
          background: none;
          border: none;
          color: #888;
          font-size: 1.5rem;
          cursor: pointer;
          transition: color 0.3s ease;
        }

        .modal-close:hover {
          color: #ff0080;
        }

        .quantum-hologram {
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          z-index: 2000;
          pointer-events: none;
        }

        .hologram-core {
          width: 300px;
          height: 300px;
          border-radius: 50%;
          background: radial-gradient(circle, rgba(0, 255, 246, 0.2), rgba(128, 0, 255, 0.2), rgba(255, 0, 128, 0.2));
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          border: 3px solid rgba(0, 255, 246, 0.5);
          position: relative;
        }

        .hologram-text {
          font-size: 1.2rem;
          font-weight: 900;
          color: #00fff6;
          text-align: center;
          letter-spacing: 2px;
        }

        .hologram-subtext {
          font-size: 0.9rem;
          color: #8000ff;
          margin-top: 0.5rem;
          letter-spacing: 1px;
        }

        @media (max-width: 768px) {
          .mystery-layer {
            padding: 1rem;
          }

          .glyph-grid {
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 1rem;
          }

          .glyph-symbol {
            font-size: 2rem;
          }

          .phrase-text {
            font-size: 1.2rem;
          }

          .hologram-core {
            width: 250px;
            height: 250px;
          }

          .hologram-text {
            font-size: 1rem;
          }
        }

        @media (max-width: 480px) {
          .glyph-grid {
            grid-template-columns: repeat(2, 1fr);
          }

          .glyph-symbol {
            font-size: 1.5rem;
          }

          .phrase-text {
            font-size: 1rem;
          }

          .hologram-core {
            width: 200px;
            height: 200px;
          }
        }
      `}</style>
    </div>
  );
};

export default MysteryLayer;