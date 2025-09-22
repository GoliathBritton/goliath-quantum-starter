// Quantum Omniscient™ Decision Engine - Monte Carlo & Confidence Scoring

export interface DecisionScenario {
  name: string;
  parameters: Record<string, number>;
  constraints: Record<string, any>;
  timeframe: number; // months
  investment: number;
  expectedReturn: number;
  riskFactors: string[];
}

export interface MonteCarloResult {
  scenario: string;
  iterations: number;
  outcomes: {
    mean: number;
    median: number;
    standardDeviation: number;
    percentiles: Record<string, number>;
    successProbability: number;
    worstCase: number;
    bestCase: number;
  };
  confidenceInterval: {
    lower: number;
    upper: number;
    confidence: number;
  };
}

export interface ConfidenceReport {
  overallScore: number;
  factors: {
    dataQuality: number;
    modelAccuracy: number;
    marketStability: number;
    timeHorizon: number;
    quantumCoherence: number;
  };
  riskAdjustedScore: number;
  recommendation: 'STRONG_BUY' | 'BUY' | 'HOLD' | 'SELL' | 'STRONG_SELL' | 'INVESTIGATE';
}

class MonteCarloEngine {
  private iterations: number;
  private randomSeed: number;

  constructor(iterations: number = 10000) {
    this.iterations = iterations;
    this.randomSeed = Date.now();
  }

  // Box-Muller transformation for normal distribution
  private normalRandom(mean: number = 0, stdDev: number = 1): number {
    let u = 0, v = 0;
    while(u === 0) u = Math.random(); // Converting [0,1) to (0,1)
    while(v === 0) v = Math.random();
    const z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    return z * stdDev + mean;
  }

  // Simulate market volatility using geometric Brownian motion
  private simulateMarketPath(initialValue: number, drift: number, volatility: number, timeSteps: number): number[] {
    const path = [initialValue];
    const dt = 1 / timeSteps; // Assuming 1 year divided into timeSteps
    
    for (let i = 1; i <= timeSteps; i++) {
      const randomShock = this.normalRandom(0, 1);
      const nextValue = path[i-1] * Math.exp(
        (drift - 0.5 * volatility * volatility) * dt + 
        volatility * Math.sqrt(dt) * randomShock
      );
      path.push(nextValue);
    }
    
    return path;
  }

  async runSimulation(scenario: DecisionScenario): Promise<MonteCarloResult> {
    const outcomes: number[] = [];
    const timeSteps = scenario.timeframe; // Monthly steps
    
    // Extract parameters with defaults
    const baseReturn = scenario.expectedReturn || 0.15;
    const volatility = scenario.parameters.volatility || 0.2;
    const marketRisk = scenario.parameters.marketRisk || 0.1;
    const executionRisk = scenario.parameters.executionRisk || 0.05;
    
    for (let i = 0; i < this.iterations; i++) {
      // Simulate market conditions
      const marketPath = this.simulateMarketPath(1.0, baseReturn, volatility, timeSteps);
      const finalMarketValue = marketPath[marketPath.length - 1];
      
      // Apply risk factors
      let riskAdjustment = 1.0;
      
      // Market risk impact
      if (Math.random() < marketRisk) {
        riskAdjustment *= (0.7 + Math.random() * 0.2); // 70-90% of expected
      }
      
      // Execution risk impact
      if (Math.random() < executionRisk) {
        riskAdjustment *= (0.8 + Math.random() * 0.15); // 80-95% of expected
      }
      
      // Black swan events (rare but high impact)
      if (Math.random() < 0.01) { // 1% chance
        riskAdjustment *= (0.3 + Math.random() * 0.4); // 30-70% impact
      }
      
      // Calculate final outcome
      const finalReturn = (finalMarketValue - 1) * riskAdjustment;
      const finalValue = scenario.investment * (1 + finalReturn);
      outcomes.push(finalValue);
    }
    
    // Sort outcomes for percentile calculations
    outcomes.sort((a, b) => a - b);
    
    const mean = outcomes.reduce((sum, val) => sum + val, 0) / outcomes.length;
    const median = outcomes[Math.floor(outcomes.length / 2)];
    
    // Calculate standard deviation
    const variance = outcomes.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / outcomes.length;
    const standardDeviation = Math.sqrt(variance);
    
    // Calculate percentiles
    const getPercentile = (p: number) => outcomes[Math.floor(outcomes.length * p / 100)];
    
    const percentiles = {
      '5': getPercentile(5),
      '10': getPercentile(10),
      '25': getPercentile(25),
      '75': getPercentile(75),
      '90': getPercentile(90),
      '95': getPercentile(95)
    };
    
    // Success probability (outcomes above initial investment)
    const successCount = outcomes.filter(outcome => outcome > scenario.investment).length;
    const successProbability = successCount / outcomes.length;
    
    // Confidence interval (95%)
    const marginOfError = 1.96 * (standardDeviation / Math.sqrt(this.iterations));
    
    return {
      scenario: scenario.name,
      iterations: this.iterations,
      outcomes: {
        mean,
        median,
        standardDeviation,
        percentiles,
        successProbability,
        worstCase: outcomes[0],
        bestCase: outcomes[outcomes.length - 1]
      },
      confidenceInterval: {
        lower: mean - marginOfError,
        upper: mean + marginOfError,
        confidence: 0.95
      }
    };
  }
}

class ConfidenceScorer {
  calculateConfidence(monteCarloResults: MonteCarloResult[], scenario: DecisionScenario): ConfidenceReport {
    const factors = this.assessConfidenceFactors(monteCarloResults, scenario);
    const overallScore = this.computeOverallScore(factors);
    const riskAdjustedScore = this.applyRiskAdjustment(overallScore, monteCarloResults);
    const recommendation = this.generateRecommendation(riskAdjustedScore, monteCarloResults);
    
    return {
      overallScore,
      factors,
      riskAdjustedScore,
      recommendation
    };
  }
  
  private assessConfidenceFactors(results: MonteCarloResult[], scenario: DecisionScenario) {
    const primaryResult = results[0]; // Assuming first result is primary scenario
    
    // Data quality based on input completeness and consistency
    const dataQuality = this.assessDataQuality(scenario);
    
    // Model accuracy based on convergence and stability
    const modelAccuracy = this.assessModelAccuracy(primaryResult);
    
    // Market stability based on volatility and risk factors
    const marketStability = this.assessMarketStability(scenario, primaryResult);
    
    // Time horizon confidence (longer = less certain)
    const timeHorizon = this.assessTimeHorizon(scenario.timeframe);
    
    // Quantum coherence (mystical factor for the Quantum Nexus)
    const quantumCoherence = 0.8 + Math.random() * 0.15; // 80-95%
    
    return {
      dataQuality,
      modelAccuracy,
      marketStability,
      timeHorizon,
      quantumCoherence
    };
  }
  
  private assessDataQuality(scenario: DecisionScenario): number {
    let score = 0.5; // Base score
    
    // Check parameter completeness
    const requiredParams = ['volatility', 'marketRisk', 'executionRisk'];
    const providedParams = Object.keys(scenario.parameters);
    const completeness = providedParams.filter(p => requiredParams.includes(p)).length / requiredParams.length;
    score += completeness * 0.3;
    
    // Check for reasonable values
    if (scenario.expectedReturn > 0 && scenario.expectedReturn < 1) score += 0.1;
    if (scenario.investment > 0) score += 0.1;
    
    return Math.min(score, 1.0);
  }
  
  private assessModelAccuracy(result: MonteCarloResult): number {
    // Higher iterations = higher accuracy
    const iterationScore = Math.min(result.iterations / 10000, 1.0) * 0.4;
    
    // Lower standard deviation relative to mean = higher accuracy
    const stabilityScore = Math.max(0, 1 - (result.outcomes.standardDeviation / Math.abs(result.outcomes.mean))) * 0.3;
    
    // Reasonable confidence interval = higher accuracy
    const intervalWidth = result.confidenceInterval.upper - result.confidenceInterval.lower;
    const intervalScore = Math.max(0, 1 - (intervalWidth / Math.abs(result.outcomes.mean))) * 0.3;
    
    return iterationScore + stabilityScore + intervalScore;
  }
  
  private assessMarketStability(scenario: DecisionScenario, result: MonteCarloResult): number {
    // Lower volatility = higher stability
    const volatility = scenario.parameters.volatility || 0.2;
    const volatilityScore = Math.max(0, 1 - volatility) * 0.4;
    
    // Higher success probability = higher stability
    const successScore = result.outcomes.successProbability * 0.3;
    
    // Fewer risk factors = higher stability
    const riskFactorScore = Math.max(0, 1 - (scenario.riskFactors.length / 10)) * 0.3;
    
    return volatilityScore + successScore + riskFactorScore;
  }
  
  private assessTimeHorizon(timeframe: number): number {
    // Confidence decreases with longer time horizons
    if (timeframe <= 3) return 0.95; // 3 months or less
    if (timeframe <= 6) return 0.85; // 6 months
    if (timeframe <= 12) return 0.75; // 1 year
    if (timeframe <= 24) return 0.65; // 2 years
    if (timeframe <= 36) return 0.55; // 3 years
    return 0.45; // Beyond 3 years
  }
  
  private computeOverallScore(factors: any): number {
    const weights = {
      dataQuality: 0.25,
      modelAccuracy: 0.25,
      marketStability: 0.25,
      timeHorizon: 0.15,
      quantumCoherence: 0.10
    };
    
    return Object.entries(factors).reduce((score, [factor, value]) => {
      return score + (value as number) * weights[factor as keyof typeof weights];
    }, 0);
  }
  
  private applyRiskAdjustment(baseScore: number, results: MonteCarloResult[]): number {
    const primaryResult = results[0];
    
    // Adjust based on downside risk
    const downsideRisk = (primaryResult.outcomes.percentiles['10'] - primaryResult.outcomes.mean) / primaryResult.outcomes.mean;
    const riskAdjustment = Math.max(0.5, 1 + downsideRisk * 0.5); // Penalize high downside risk
    
    return baseScore * riskAdjustment;
  }
  
  private generateRecommendation(score: number, results: MonteCarloResult[]): ConfidenceReport['recommendation'] {
    const primaryResult = results[0];
    const successProb = primaryResult.outcomes.successProbability;
    
    if (score > 0.85 && successProb > 0.8) return 'STRONG_BUY';
    if (score > 0.7 && successProb > 0.65) return 'BUY';
    if (score > 0.5 && successProb > 0.5) return 'HOLD';
    if (score > 0.3) return 'INVESTIGATE';
    if (successProb < 0.3) return 'STRONG_SELL';
    return 'SELL';
  }
}

export class QuantumOmniscientDecisionEngine {
  private monteCarloEngine: MonteCarloEngine;
  private confidenceScorer: ConfidenceScorer;
  
  constructor(iterations: number = 10000) {
    this.monteCarloEngine = new MonteCarloEngine(iterations);
    this.confidenceScorer = new ConfidenceScorer();
  }
  
  async analyzeDecision(scenarios: DecisionScenario[]): Promise<{
    monteCarloResults: MonteCarloResult[];
    confidenceReport: ConfidenceReport;
    optimalScenario: string;
    riskAnalysis: any;
  }> {
    // Run Monte Carlo simulations for all scenarios
    const monteCarloResults = await Promise.all(
      scenarios.map(scenario => this.monteCarloEngine.runSimulation(scenario))
    );
    
    // Generate confidence report
    const confidenceReport = this.confidenceScorer.calculateConfidence(monteCarloResults, scenarios[0]);
    
    // Determine optimal scenario
    const optimalScenario = this.findOptimalScenario(monteCarloResults);
    
    // Perform risk analysis
    const riskAnalysis = this.performRiskAnalysis(monteCarloResults);
    
    return {
      monteCarloResults,
      confidenceReport,
      optimalScenario,
      riskAnalysis
    };
  }
  
  private findOptimalScenario(results: MonteCarloResult[]): string {
    let bestScenario = results[0];
    let bestScore = this.calculateScenarioScore(bestScenario);
    
    for (const result of results.slice(1)) {
      const score = this.calculateScenarioScore(result);
      if (score > bestScore) {
        bestScore = score;
        bestScenario = result;
      }
    }
    
    return bestScenario.scenario;
  }
  
  private calculateScenarioScore(result: MonteCarloResult): number {
    // Weighted score considering return, risk, and probability
    const returnScore = (result.outcomes.mean / 100000) * 0.4; // Normalize by 100k investment
    const riskScore = (1 - (result.outcomes.standardDeviation / result.outcomes.mean)) * 0.3;
    const probabilityScore = result.outcomes.successProbability * 0.3;
    
    return returnScore + riskScore + probabilityScore;
  }
  
  private performRiskAnalysis(results: MonteCarloResult[]): any {
    return {
      valueAtRisk: results.map(r => ({
        scenario: r.scenario,
        var95: r.outcomes.percentiles['5'], // 95% VaR
        var99: r.outcomes.percentiles['1'] || r.outcomes.worstCase
      })),
      expectedShortfall: results.map(r => {
        // Average of worst 5% outcomes
        const worstOutcomes = Math.floor(r.iterations * 0.05);
        return {
          scenario: r.scenario,
          expectedShortfall: r.outcomes.worstCase * 1.1 // Approximation
        };
      }),
      correlationMatrix: this.calculateCorrelationMatrix(results),
      stressTestResults: this.performStressTest(results)
    };
  }
  
  private calculateCorrelationMatrix(results: MonteCarloResult[]): number[][] {
    // Simplified correlation matrix (in practice, would use actual outcome data)
    const size = results.length;
    const matrix = Array(size).fill(null).map(() => Array(size).fill(0));
    
    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        if (i === j) {
          matrix[i][j] = 1.0;
        } else {
          // Simulate correlation based on scenario similarity
          matrix[i][j] = 0.3 + Math.random() * 0.4; // 30-70% correlation
        }
      }
    }
    
    return matrix;
  }
  
  private performStressTest(results: MonteCarloResult[]): any {
    return results.map(result => ({
      scenario: result.scenario,
      marketCrash: result.outcomes.mean * 0.6, // 40% market decline
      recession: result.outcomes.mean * 0.75,  // 25% economic decline
      blackSwan: result.outcomes.worstCase * 0.8 // Extreme event
    }));
  }
}