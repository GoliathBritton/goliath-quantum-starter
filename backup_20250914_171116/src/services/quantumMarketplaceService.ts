import { EventEmitter } from 'events';

// Interfaces for quantum marketplace
export interface QuantumAlgorithm {
  id: string;
  name: string;
  description: string;
  category: AlgorithmCategory;
  tags: string[];
  version: string;
  author: Developer;
  publisher: Publisher;
  pricing: PricingModel;
  performance: PerformanceMetrics;
  compatibility: CompatibilityInfo;
  documentation: Documentation;
  reviews: Review[];
  downloads: number;
  rating: number;
  featured: boolean;
  verified: boolean;
  createdAt: Date;
  updatedAt: Date;
  status: 'draft' | 'pending' | 'approved' | 'rejected' | 'deprecated';
  license: License;
  dependencies: Dependency[];
  examples: Example[];
  benchmarks: Benchmark[];
  quantumResources: QuantumResourceRequirements;
}

export interface Developer {
  id: string;
  username: string;
  displayName: string;
  email: string;
  avatar?: string;
  bio?: string;
  website?: string;
  github?: string;
  linkedin?: string;
  reputation: number;
  badges: Badge[];
  joinedAt: Date;
  totalAlgorithms: number;
  totalDownloads: number;
  averageRating: number;
  verified: boolean;
}

export interface Publisher {
  id: string;
  name: string;
  type: 'individual' | 'organization' | 'enterprise';
  description?: string;
  logo?: string;
  website?: string;
  verified: boolean;
  algorithms: string[]; // algorithm IDs
  revenue: number;
  subscribers: number;
}

export interface PricingModel {
  type: 'free' | 'one_time' | 'subscription' | 'usage_based' | 'freemium';
  price: number;
  currency: string;
  billingPeriod?: 'monthly' | 'yearly';
  usageLimit?: number;
  freeTier?: {
    limit: number;
    features: string[];
  };
  premiumTier?: {
    price: number;
    features: string[];
  };
  enterpriseTier?: {
    price: number;
    features: string[];
    customization: boolean;
    support: string;
  };
}

export interface PerformanceMetrics {
  complexity: {
    time: string; // Big O notation
    space: string; // Big O notation
    quantum: string; // Quantum complexity
  };
  benchmarks: {
    classicalSpeedup: number;
    quantumAdvantage: number;
    accuracy: number;
    scalability: number;
  };
  resourceUsage: {
    qubits: number;
    gates: number;
    depth: number;
    executionTime: number; // milliseconds
  };
  testResults: TestResult[];
}

export interface TestResult {
  testCase: string;
  input: any;
  expectedOutput: any;
  actualOutput: any;
  passed: boolean;
  executionTime: number;
  quantumResources: {
    qubits: number;
    gates: number;
    depth: number;
  };
}

export interface CompatibilityInfo {
  quantumBackends: string[];
  frameworks: string[];
  languages: string[];
  minQubits: number;
  maxQubits?: number;
  gateSet: string[];
  topology?: string;
  noiseModel?: string;
  calibrationRequirements?: string[];
}

export interface Documentation {
  readme: string;
  apiReference: string;
  tutorials: Tutorial[];
  examples: Example[];
  changelog: ChangelogEntry[];
  faq: FAQ[];
}

export interface Tutorial {
  id: string;
  title: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedTime: number; // minutes
  content: string;
  codeExamples: CodeExample[];
  prerequisites: string[];
}

export interface Example {
  id: string;
  title: string;
  description: string;
  code: string;
  language: string;
  input: any;
  output: any;
  explanation: string;
}

export interface CodeExample {
  language: string;
  code: string;
  description: string;
}

export interface ChangelogEntry {
  version: string;
  date: Date;
  changes: {
    type: 'added' | 'changed' | 'deprecated' | 'removed' | 'fixed' | 'security';
    description: string;
  }[];
}

export interface FAQ {
  question: string;
  answer: string;
  category: string;
}

export interface Review {
  id: string;
  userId: string;
  username: string;
  rating: number; // 1-5
  title: string;
  content: string;
  pros: string[];
  cons: string[];
  createdAt: Date;
  helpful: number;
  verified: boolean; // verified purchase
  response?: {
    content: string;
    author: string;
    createdAt: Date;
  };
}

export interface License {
  type: 'MIT' | 'Apache-2.0' | 'GPL-3.0' | 'BSD-3-Clause' | 'Commercial' | 'Custom';
  text: string;
  permissions: string[];
  conditions: string[];
  limitations: string[];
}

export interface Dependency {
  name: string;
  version: string;
  type: 'quantum' | 'classical' | 'framework';
  required: boolean;
  description: string;
}

export interface Benchmark {
  id: string;
  name: string;
  description: string;
  problemSize: number;
  classicalTime: number;
  quantumTime: number;
  speedup: number;
  accuracy: number;
  qubitsUsed: number;
  gatesUsed: number;
  circuitDepth: number;
  backend: string;
  date: Date;
}

export interface QuantumResourceRequirements {
  minQubits: number;
  maxQubits?: number;
  requiredGates: string[];
  optionalGates: string[];
  connectivity: 'any' | 'linear' | 'grid' | 'all-to-all' | 'custom';
  coherenceTime: number; // microseconds
  gateTime: number; // nanoseconds
  readoutFidelity: number;
  gateFidelity: number;
  errorRate: number;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  criteria: string;
  earnedAt: Date;
}

export interface AlgorithmCategory {
  id: string;
  name: string;
  description: string;
  icon: string;
  parentId?: string;
  subcategories?: AlgorithmCategory[];
}

export interface MarketplaceTransaction {
  id: string;
  algorithmId: string;
  buyerId: string;
  sellerId: string;
  amount: number;
  currency: string;
  type: 'purchase' | 'subscription' | 'usage';
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  createdAt: Date;
  completedAt?: Date;
  metadata: {
    paymentMethod: string;
    invoiceId?: string;
    subscriptionId?: string;
    usageMetrics?: any;
  };
}

export interface Subscription {
  id: string;
  algorithmId: string;
  userId: string;
  plan: 'free' | 'premium' | 'enterprise';
  status: 'active' | 'cancelled' | 'expired' | 'suspended';
  startDate: Date;
  endDate: Date;
  autoRenew: boolean;
  usageLimit: number;
  usageCount: number;
  lastUsed?: Date;
}

export interface MarketplaceAnalytics {
  totalAlgorithms: number;
  totalDevelopers: number;
  totalDownloads: number;
  totalRevenue: number;
  topCategories: CategoryStats[];
  topAlgorithms: AlgorithmStats[];
  topDevelopers: DeveloperStats[];
  revenueByMonth: RevenueStats[];
  downloadsByMonth: DownloadStats[];
  userGrowth: UserGrowthStats[];
}

export interface CategoryStats {
  category: string;
  algorithmCount: number;
  downloads: number;
  revenue: number;
  averageRating: number;
}

export interface AlgorithmStats {
  algorithmId: string;
  name: string;
  downloads: number;
  revenue: number;
  rating: number;
  reviews: number;
}

export interface DeveloperStats {
  developerId: string;
  username: string;
  algorithms: number;
  downloads: number;
  revenue: number;
  rating: number;
}

export interface RevenueStats {
  month: string;
  revenue: number;
  transactions: number;
  newCustomers: number;
}

export interface DownloadStats {
  month: string;
  downloads: number;
  uniqueUsers: number;
  topAlgorithms: string[];
}

export interface UserGrowthStats {
  month: string;
  newDevelopers: number;
  newUsers: number;
  totalDevelopers: number;
  totalUsers: number;
}

export interface SearchFilters {
  category?: string;
  tags?: string[];
  priceRange?: {
    min: number;
    max: number;
  };
  rating?: number;
  compatibility?: {
    backend?: string;
    framework?: string;
    language?: string;
  };
  performance?: {
    minQubits?: number;
    maxQubits?: number;
    minSpeedup?: number;
  };
  license?: string[];
  verified?: boolean;
  featured?: boolean;
}

export interface SearchResult {
  algorithms: QuantumAlgorithm[];
  total: number;
  page: number;
  pageSize: number;
  filters: SearchFilters;
  suggestions: string[];
  facets: {
    categories: { name: string; count: number }[];
    tags: { name: string; count: number }[];
    licenses: { name: string; count: number }[];
    frameworks: { name: string; count: number }[];
  };
}

class QuantumMarketplaceService extends EventEmitter {
  private algorithms: Map<string, QuantumAlgorithm> = new Map();
  private developers: Map<string, Developer> = new Map();
  private publishers: Map<string, Publisher> = new Map();
  private transactions: Map<string, MarketplaceTransaction> = new Map();
  private subscriptions: Map<string, Subscription> = new Map();
  private categories: Map<string, AlgorithmCategory> = new Map();
  private reviews: Map<string, Review[]> = new Map();

  constructor() {
    super();
    this.initializeCategories();
    this.initializeSampleData();
  }

  private initializeCategories(): void {
    const categories: AlgorithmCategory[] = [
      {
        id: 'optimization',
        name: 'Optimization',
        description: 'Quantum algorithms for optimization problems',
        icon: 'optimization',
      },
      {
        id: 'machine_learning',
        name: 'Machine Learning',
        description: 'Quantum machine learning algorithms',
        icon: 'ml',
      },
      {
        id: 'cryptography',
        name: 'Cryptography',
        description: 'Quantum cryptographic algorithms',
        icon: 'security',
      },
      {
        id: 'simulation',
        name: 'Simulation',
        description: 'Quantum simulation algorithms',
        icon: 'simulation',
      },
      {
        id: 'search',
        name: 'Search',
        description: 'Quantum search algorithms',
        icon: 'search',
      },
      {
        id: 'finance',
        name: 'Finance',
        description: 'Quantum algorithms for financial applications',
        icon: 'finance',
      },
      {
        id: 'chemistry',
        name: 'Chemistry',
        description: 'Quantum algorithms for chemical simulations',
        icon: 'chemistry',
      },
      {
        id: 'utilities',
        name: 'Utilities',
        description: 'Utility algorithms and tools',
        icon: 'utilities',
      },
    ];

    categories.forEach(category => {
      this.categories.set(category.id, category);
    });
  }

  private initializeSampleData(): void {
    // Sample developer
    const sampleDeveloper: Developer = {
      id: 'dev_001',
      username: 'quantum_pioneer',
      displayName: 'Dr. Alice Quantum',
      email: 'alice@quantum-dev.com',
      bio: 'Quantum computing researcher and algorithm developer',
      reputation: 4.8,
      badges: [
        {
          id: 'verified_dev',
          name: 'Verified Developer',
          description: 'Verified quantum algorithm developer',
          icon: 'verified',
          color: '#1976d2',
          criteria: 'Published 5+ verified algorithms',
          earnedAt: new Date(),
        },
      ],
      joinedAt: new Date('2023-01-01'),
      totalAlgorithms: 12,
      totalDownloads: 15000,
      averageRating: 4.7,
      verified: true,
    };

    this.developers.set(sampleDeveloper.id, sampleDeveloper);

    // Sample algorithm
    const sampleAlgorithm: QuantumAlgorithm = {
      id: 'algo_001',
      name: 'Quantum Portfolio Optimization',
      description: 'Advanced quantum algorithm for portfolio optimization using QAOA',
      category: this.categories.get('optimization')!,
      tags: ['portfolio', 'finance', 'QAOA', 'optimization'],
      version: '2.1.0',
      author: sampleDeveloper,
      publisher: {
        id: 'pub_001',
        name: 'Quantum Finance Labs',
        type: 'organization',
        verified: true,
        algorithms: ['algo_001'],
        revenue: 50000,
        subscribers: 250,
      },
      pricing: {
        type: 'freemium',
        price: 0,
        currency: 'USD',
        freeTier: {
          limit: 100,
          features: ['Basic optimization', 'Up to 10 assets'],
        },
        premiumTier: {
          price: 99,
          features: ['Advanced optimization', 'Unlimited assets', 'Risk analysis'],
        },
        enterpriseTier: {
          price: 999,
          features: ['Custom optimization', 'White-label', 'Priority support'],
          customization: true,
          support: '24/7',
        },
      },
      performance: {
        complexity: {
          time: 'O(n²)',
          space: 'O(n)',
          quantum: 'O(√n)',
        },
        benchmarks: {
          classicalSpeedup: 15.7,
          quantumAdvantage: 8.3,
          accuracy: 0.95,
          scalability: 0.88,
        },
        resourceUsage: {
          qubits: 20,
          gates: 1500,
          depth: 100,
          executionTime: 2500,
        },
        testResults: [],
      },
      compatibility: {
        quantumBackends: ['qasm_simulator', 'ibmq_qasm_simulator', 'rigetti'],
        frameworks: ['qiskit', 'cirq', 'pennylane'],
        languages: ['python', 'julia'],
        minQubits: 10,
        maxQubits: 50,
        gateSet: ['X', 'Y', 'Z', 'H', 'CNOT', 'RZ', 'RY'],
        topology: 'any',
      },
      documentation: {
        readme: 'Comprehensive portfolio optimization using quantum computing...',
        apiReference: 'API documentation for quantum portfolio optimization...',
        tutorials: [],
        examples: [],
        changelog: [],
        faq: [],
      },
      reviews: [],
      downloads: 5420,
      rating: 4.6,
      featured: true,
      verified: true,
      createdAt: new Date('2023-06-01'),
      updatedAt: new Date(),
      status: 'approved',
      license: {
        type: 'MIT',
        text: 'MIT License text...',
        permissions: ['Commercial use', 'Modification', 'Distribution'],
        conditions: ['License and copyright notice'],
        limitations: ['Liability', 'Warranty'],
      },
      dependencies: [
        {
          name: 'qiskit',
          version: '>=0.45.0',
          type: 'quantum',
          required: true,
          description: 'Quantum computing framework',
        },
        {
          name: 'numpy',
          version: '>=1.21.0',
          type: 'classical',
          required: true,
          description: 'Numerical computing library',
        },
      ],
      examples: [],
      benchmarks: [],
      quantumResources: {
        minQubits: 10,
        maxQubits: 50,
        requiredGates: ['X', 'Y', 'Z', 'H', 'CNOT'],
        optionalGates: ['RZ', 'RY', 'U3'],
        connectivity: 'any',
        coherenceTime: 100,
        gateTime: 20,
        readoutFidelity: 0.98,
        gateFidelity: 0.999,
        errorRate: 0.001,
      },
    };

    this.algorithms.set(sampleAlgorithm.id, sampleAlgorithm);
  }

  // Algorithm Management
  async publishAlgorithm(algorithm: Omit<QuantumAlgorithm, 'id' | 'createdAt' | 'updatedAt'>): Promise<QuantumAlgorithm> {
    const id = `algo_${Date.now()}`;
    const newAlgorithm: QuantumAlgorithm = {
      ...algorithm,
      id,
      createdAt: new Date(),
      updatedAt: new Date(),
      status: 'pending',
      downloads: 0,
      rating: 0,
      reviews: [],
    };

    this.algorithms.set(id, newAlgorithm);
    this.emit('algorithmPublished', newAlgorithm);

    // Start review process
    await this.reviewAlgorithm(id);

    return newAlgorithm;
  }

  async updateAlgorithm(id: string, updates: Partial<QuantumAlgorithm>): Promise<QuantumAlgorithm | null> {
    const algorithm = this.algorithms.get(id);
    if (!algorithm) return null;

    const updated = {
      ...algorithm,
      ...updates,
      updatedAt: new Date(),
    };

    this.algorithms.set(id, updated);
    this.emit('algorithmUpdated', updated);

    return updated;
  }

  async deleteAlgorithm(id: string): Promise<boolean> {
    const algorithm = this.algorithms.get(id);
    if (!algorithm) return false;

    this.algorithms.delete(id);
    this.emit('algorithmDeleted', { id, algorithm });

    return true;
  }

  getAlgorithm(id: string): QuantumAlgorithm | null {
    return this.algorithms.get(id) || null;
  }

  getAllAlgorithms(): QuantumAlgorithm[] {
    return Array.from(this.algorithms.values());
  }

  // Search and Discovery
  async searchAlgorithms(
    query: string,
    filters: SearchFilters = {},
    page: number = 1,
    pageSize: number = 20
  ): Promise<SearchResult> {
    let algorithms = Array.from(this.algorithms.values());

    // Apply text search
    if (query) {
      const searchTerms = query.toLowerCase().split(' ');
      algorithms = algorithms.filter(algo => {
        const searchText = `${algo.name} ${algo.description} ${algo.tags.join(' ')}`.toLowerCase();
        return searchTerms.every(term => searchText.includes(term));
      });
    }

    // Apply filters
    if (filters.category) {
      algorithms = algorithms.filter(algo => algo.category.id === filters.category);
    }

    if (filters.tags && filters.tags.length > 0) {
      algorithms = algorithms.filter(algo => 
        filters.tags!.some(tag => algo.tags.includes(tag))
      );
    }

    if (filters.priceRange) {
      algorithms = algorithms.filter(algo => {
        const price = algo.pricing.price;
        return price >= filters.priceRange!.min && price <= filters.priceRange!.max;
      });
    }

    if (filters.rating) {
      algorithms = algorithms.filter(algo => algo.rating >= filters.rating!);
    }

    if (filters.verified !== undefined) {
      algorithms = algorithms.filter(algo => algo.verified === filters.verified);
    }

    if (filters.featured !== undefined) {
      algorithms = algorithms.filter(algo => algo.featured === filters.featured);
    }

    // Apply compatibility filters
    if (filters.compatibility) {
      const { backend, framework, language } = filters.compatibility;
      
      if (backend) {
        algorithms = algorithms.filter(algo => 
          algo.compatibility.quantumBackends.includes(backend)
        );
      }
      
      if (framework) {
        algorithms = algorithms.filter(algo => 
          algo.compatibility.frameworks.includes(framework)
        );
      }
      
      if (language) {
        algorithms = algorithms.filter(algo => 
          algo.compatibility.languages.includes(language)
        );
      }
    }

    // Apply performance filters
    if (filters.performance) {
      const { minQubits, maxQubits, minSpeedup } = filters.performance;
      
      if (minQubits) {
        algorithms = algorithms.filter(algo => 
          algo.performance.resourceUsage.qubits >= minQubits
        );
      }
      
      if (maxQubits) {
        algorithms = algorithms.filter(algo => 
          algo.performance.resourceUsage.qubits <= maxQubits
        );
      }
      
      if (minSpeedup) {
        algorithms = algorithms.filter(algo => 
          algo.performance.benchmarks.classicalSpeedup >= minSpeedup
        );
      }
    }

    // Sort by relevance (rating * downloads)
    algorithms.sort((a, b) => {
      const scoreA = a.rating * Math.log(a.downloads + 1);
      const scoreB = b.rating * Math.log(b.downloads + 1);
      return scoreB - scoreA;
    });

    // Pagination
    const total = algorithms.length;
    const startIndex = (page - 1) * pageSize;
    const paginatedAlgorithms = algorithms.slice(startIndex, startIndex + pageSize);

    // Generate facets
    const facets = this.generateSearchFacets(Array.from(this.algorithms.values()));

    return {
      algorithms: paginatedAlgorithms,
      total,
      page,
      pageSize,
      filters,
      suggestions: this.generateSearchSuggestions(query),
      facets,
    };
  }

  private generateSearchFacets(algorithms: QuantumAlgorithm[]) {
    const categories = new Map<string, number>();
    const tags = new Map<string, number>();
    const licenses = new Map<string, number>();
    const frameworks = new Map<string, number>();

    algorithms.forEach(algo => {
      // Categories
      const categoryName = algo.category.name;
      categories.set(categoryName, (categories.get(categoryName) || 0) + 1);

      // Tags
      algo.tags.forEach(tag => {
        tags.set(tag, (tags.get(tag) || 0) + 1);
      });

      // Licenses
      const license = algo.license.type;
      licenses.set(license, (licenses.get(license) || 0) + 1);

      // Frameworks
      algo.compatibility.frameworks.forEach(framework => {
        frameworks.set(framework, (frameworks.get(framework) || 0) + 1);
      });
    });

    return {
      categories: Array.from(categories.entries())
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count),
      tags: Array.from(tags.entries())
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 20),
      licenses: Array.from(licenses.entries())
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count),
      frameworks: Array.from(frameworks.entries())
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count),
    };
  }

  private generateSearchSuggestions(query: string): string[] {
    if (!query || query.length < 2) return [];

    const suggestions = new Set<string>();
    const algorithms = Array.from(this.algorithms.values());

    algorithms.forEach(algo => {
      // Add algorithm names that start with query
      if (algo.name.toLowerCase().startsWith(query.toLowerCase())) {
        suggestions.add(algo.name);
      }

      // Add tags that start with query
      algo.tags.forEach(tag => {
        if (tag.toLowerCase().startsWith(query.toLowerCase())) {
          suggestions.add(tag);
        }
      });
    });

    return Array.from(suggestions).slice(0, 5);
  }

  // Reviews and Ratings
  async addReview(algorithmId: string, review: Omit<Review, 'id' | 'createdAt'>): Promise<Review> {
    const algorithm = this.algorithms.get(algorithmId);
    if (!algorithm) throw new Error('Algorithm not found');

    const newReview: Review = {
      ...review,
      id: `review_${Date.now()}`,
      createdAt: new Date(),
      helpful: 0,
    };

    if (!this.reviews.has(algorithmId)) {
      this.reviews.set(algorithmId, []);
    }

    this.reviews.get(algorithmId)!.push(newReview);
    algorithm.reviews.push(newReview);

    // Update algorithm rating
    await this.updateAlgorithmRating(algorithmId);

    this.emit('reviewAdded', { algorithmId, review: newReview });

    return newReview;
  }

  private async updateAlgorithmRating(algorithmId: string): Promise<void> {
    const algorithm = this.algorithms.get(algorithmId);
    const reviews = this.reviews.get(algorithmId);
    
    if (!algorithm || !reviews || reviews.length === 0) return;

    const totalRating = reviews.reduce((sum, review) => sum + review.rating, 0);
    const averageRating = totalRating / reviews.length;

    algorithm.rating = Math.round(averageRating * 10) / 10; // Round to 1 decimal
    algorithm.updatedAt = new Date();

    this.algorithms.set(algorithmId, algorithm);
  }

  // Transactions and Monetization
  async purchaseAlgorithm(
    algorithmId: string,
    buyerId: string,
    paymentMethod: string
  ): Promise<MarketplaceTransaction> {
    const algorithm = this.algorithms.get(algorithmId);
    if (!algorithm) throw new Error('Algorithm not found');

    const transaction: MarketplaceTransaction = {
      id: `txn_${Date.now()}`,
      algorithmId,
      buyerId,
      sellerId: algorithm.author.id,
      amount: algorithm.pricing.price,
      currency: algorithm.pricing.currency,
      type: 'purchase',
      status: 'pending',
      createdAt: new Date(),
      metadata: {
        paymentMethod,
      },
    };

    this.transactions.set(transaction.id, transaction);

    // Simulate payment processing
    setTimeout(() => {
      this.completeTransaction(transaction.id);
    }, 2000);

    this.emit('transactionCreated', transaction);

    return transaction;
  }

  private async completeTransaction(transactionId: string): Promise<void> {
    const transaction = this.transactions.get(transactionId);
    if (!transaction) return;

    transaction.status = 'completed';
    transaction.completedAt = new Date();

    // Update algorithm download count
    const algorithm = this.algorithms.get(transaction.algorithmId);
    if (algorithm) {
      algorithm.downloads += 1;
      this.algorithms.set(algorithm.id, algorithm);
    }

    this.emit('transactionCompleted', transaction);
  }

  // Developer Management
  async registerDeveloper(developer: Omit<Developer, 'id' | 'joinedAt' | 'totalAlgorithms' | 'totalDownloads' | 'averageRating'>): Promise<Developer> {
    const id = `dev_${Date.now()}`;
    const newDeveloper: Developer = {
      ...developer,
      id,
      joinedAt: new Date(),
      totalAlgorithms: 0,
      totalDownloads: 0,
      averageRating: 0,
      badges: [],
    };

    this.developers.set(id, newDeveloper);
    this.emit('developerRegistered', newDeveloper);

    return newDeveloper;
  }

  getDeveloper(id: string): Developer | null {
    return this.developers.get(id) || null;
  }

  // Analytics
  getMarketplaceAnalytics(): MarketplaceAnalytics {
    const algorithms = Array.from(this.algorithms.values());
    const developers = Array.from(this.developers.values());
    const transactions = Array.from(this.transactions.values());

    const totalRevenue = transactions
      .filter(t => t.status === 'completed')
      .reduce((sum, t) => sum + t.amount, 0);

    const totalDownloads = algorithms.reduce((sum, a) => sum + a.downloads, 0);

    // Category stats
    const categoryStats = new Map<string, CategoryStats>();
    algorithms.forEach(algo => {
      const categoryName = algo.category.name;
      if (!categoryStats.has(categoryName)) {
        categoryStats.set(categoryName, {
          category: categoryName,
          algorithmCount: 0,
          downloads: 0,
          revenue: 0,
          averageRating: 0,
        });
      }
      
      const stats = categoryStats.get(categoryName)!;
      stats.algorithmCount += 1;
      stats.downloads += algo.downloads;
      stats.averageRating += algo.rating;
    });

    // Calculate average ratings
    categoryStats.forEach(stats => {
      stats.averageRating = stats.averageRating / stats.algorithmCount;
    });

    return {
      totalAlgorithms: algorithms.length,
      totalDevelopers: developers.length,
      totalDownloads,
      totalRevenue,
      topCategories: Array.from(categoryStats.values())
        .sort((a, b) => b.downloads - a.downloads)
        .slice(0, 10),
      topAlgorithms: algorithms
        .sort((a, b) => b.downloads - a.downloads)
        .slice(0, 10)
        .map(algo => ({
          algorithmId: algo.id,
          name: algo.name,
          downloads: algo.downloads,
          revenue: 0, // Calculate from transactions
          rating: algo.rating,
          reviews: algo.reviews.length,
        })),
      topDevelopers: developers
        .sort((a, b) => b.totalDownloads - a.totalDownloads)
        .slice(0, 10)
        .map(dev => ({
          developerId: dev.id,
          username: dev.username,
          algorithms: dev.totalAlgorithms,
          downloads: dev.totalDownloads,
          revenue: 0, // Calculate from transactions
          rating: dev.averageRating,
        })),
      revenueByMonth: [], // Implement monthly aggregation
      downloadsByMonth: [], // Implement monthly aggregation
      userGrowth: [], // Implement monthly aggregation
    };
  }

  // Algorithm Review Process
  private async reviewAlgorithm(algorithmId: string): Promise<void> {
    const algorithm = this.algorithms.get(algorithmId);
    if (!algorithm) return;

    // Simulate review process
    setTimeout(() => {
      // Auto-approve for demo (in real implementation, this would be manual)
      algorithm.status = 'approved';
      algorithm.verified = true;
      algorithm.updatedAt = new Date();
      
      this.algorithms.set(algorithmId, algorithm);
      this.emit('algorithmApproved', algorithm);
    }, 5000);
  }

  // Featured Algorithms
  async setFeatured(algorithmId: string, featured: boolean): Promise<boolean> {
    const algorithm = this.algorithms.get(algorithmId);
    if (!algorithm) return false;

    algorithm.featured = featured;
    algorithm.updatedAt = new Date();
    
    this.algorithms.set(algorithmId, algorithm);
    this.emit('algorithmFeaturedChanged', { algorithmId, featured });

    return true;
  }

  getFeaturedAlgorithms(): QuantumAlgorithm[] {
    return Array.from(this.algorithms.values())
      .filter(algo => algo.featured && algo.status === 'approved')
      .sort((a, b) => b.rating - a.rating);
  }

  // Categories
  getCategories(): AlgorithmCategory[] {
    return Array.from(this.categories.values());
  }

  getCategory(id: string): AlgorithmCategory | null {
    return this.categories.get(id) || null;
  }

  getAlgorithmsByCategory(categoryId: string): QuantumAlgorithm[] {
    return Array.from(this.algorithms.values())
      .filter(algo => algo.category.id === categoryId && algo.status === 'approved');
  }
}

export default QuantumMarketplaceService;