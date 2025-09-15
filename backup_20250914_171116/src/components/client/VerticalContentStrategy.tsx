import React, { useState, useEffect, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { 
  Factory, 
  Banknote, 
  Truck, 
  Zap, 
  Target, 
  TrendingUp, 
  DollarSign, 
  Users, 
  Clock, 
  Award, 
  Sparkles, 
  Activity, 
  BarChart3, 
  PieChart as PieChartIcon,
  Settings,
  Bell,
  RefreshCw,
  CheckCircle,
  XCircle,
  AlertTriangle,
  ArrowUp,
  ArrowDown,
  Minus,
  Play,
  Pause,
  Calendar,
  Mail,
  Phone,
  MapPin,
  ExternalLink,
  ChevronRight,
  Plus,
  Edit,
  Search,
  Filter,
  Download,
  Upload,
  FileText,
  Database,
  Cpu,
  Network,
  Globe,
  Shield,
  Lightbulb,
  Building2,
  Briefcase,
  Calculator,
  Microscope,
  Layers,
  GitBranch,
  Workflow,
  Gauge,
  TrendingDown,
  Eye,
  EyeOff,
  Lock,
  Unlock,
  Star,
  Heart,
  ThumbsUp,
  MessageSquare,
  Share2,
  Bookmark,
  Code,
  Terminal,
  Brain,
  Cog,
  FlaskConical,
  LineChart as LineChartIcon,
  Presentation,
  FileSpreadsheet,
  Clipboard,
  Timer,
  CheckSquare,
  AlertCircle,
  Info,
  HelpCircle,
  BookOpen,
  GraduationCap,
  Wrench,
  Hammer,
  Video,
  Camera,
  Mic,
  Image,
  Film,
  PlayCircle,
  StopCircle,
  SkipForward,
  SkipBack,
  Volume2,
  VolumeX,
  Maximize,
  Minimize,
  RotateCcw,
  RotateCw,
  ZoomIn,
  ZoomOut,
  Move,
  Copy,
  Scissors,
  Clipboard as ClipboardIcon,
  Save,
  FolderOpen,
  Folder,
  File,
  Archive,
  Package2,
  Box,
  Container,
  Layers3,
  Component,
  Puzzle,
  Blocks,
  Grid3x3,
  Layout,
  Sidebar,
  PanelLeft,
  PanelRight,
  PanelTop,
  PanelBottom,
  Columns,
  Rows,
  Table,
  List,
  Grid,
  Menu,
  MoreHorizontal,
  MoreVertical,
  ChevronLeft,
  ChevronUp,
  ChevronDown,
  ChevronsLeft,
  ChevronsRight,
  ChevronsUp,
  ChevronsDown,
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  ArrowDownLeft,
  ArrowDownRight,
  ArrowUpLeft,
  CornerDownLeft,
  CornerDownRight,
  CornerUpLeft,
  CornerUpRight,
  Repeat,
  Shuffle,
  SkipForward as FastForward,
  SkipBack as Rewind,
  Pause as PauseIcon,
  Play as PlayIcon,
  Square,
  Circle,
  Triangle,
  Hexagon,
  Octagon,
  Pentagon,
  Diamond,
  Hash,
  AtSign,
  Percent,
  Ampersand,
  Asterisk,
  Slash,
  Minus as MinusIcon,
  Plus as PlusIcon,
  Equal,
  Underline,
  Quote,
  Type,
  Parentheses,
  Brackets,
  Braces
} from 'lucide-react';

// Type assertions for Lucide icons
const FactoryIcon = Factory as any;
const BanknoteIcon = Banknote as any;
const TruckIcon = Truck as any;
const ZapIcon = Zap as any;
const TargetIcon = Target as any;
const TrendingUpIcon = TrendingUp as any;
const DollarSignIcon = DollarSign as any;
const UsersIcon = Users as any;
const ClockIcon = Clock as any;
const AwardIcon = Award as any;
const SparklesIcon = Sparkles as any;
const ActivityIcon = Activity as any;
const BarChart3Icon = BarChart3 as any;
const PieChartIconComponent = PieChartIcon as any;
const SettingsIcon = Settings as any;
const BellIcon = Bell as any;
const RefreshCwIcon = RefreshCw as any;
const CheckCircleIcon = CheckCircle as any;
const XCircleIcon = XCircle as any;
const AlertTriangleIcon = AlertTriangle as any;
const ArrowUpIcon = ArrowUp as any;
const ArrowDownIcon = ArrowDown as any;
const MinusIconComponent = Minus as any;
const PlayIconComponent = Play as any;
const PauseIconComponent = Pause as any;
const CalendarIcon = Calendar as any;
const MailIcon = Mail as any;
const PhoneIcon = Phone as any;
const MapPinIcon = MapPin as any;
const ExternalLinkIcon = ExternalLink as any;
const ChevronRightIcon = ChevronRight as any;
const PlusIconComponent = Plus as any;
const EditIcon = Edit as any;
const SearchIcon = Search as any;
const FilterIcon = Filter as any;
const DownloadIcon = Download as any;
const UploadIcon = Upload as any;
const FileTextIcon = FileText as any;
const DatabaseIcon = Database as any;
const CpuIcon = Cpu as any;
const NetworkIcon = Network as any;
const GlobeIcon = Globe as any;
const ShieldIcon = Shield as any;
const LightbulbIcon = Lightbulb as any;
const Building2Icon = Building2 as any;
const BriefcaseIcon = Briefcase as any;
const CalculatorIcon = Calculator as any;
const MicroscopeIcon = Microscope as any;
const LayersIcon = Layers as any;
const GitBranchIcon = GitBranch as any;
const WorkflowIcon = Workflow as any;
const GaugeIcon = Gauge as any;
const TrendingDownIcon = TrendingDown as any;
const EyeIcon = Eye as any;
const EyeOffIcon = EyeOff as any;
const LockIcon = Lock as any;
const UnlockIcon = Unlock as any;
const StarIcon = Star as any;
const HeartIcon = Heart as any;
const ThumbsUpIcon = ThumbsUp as any;
const MessageSquareIcon = MessageSquare as any;
const Share2Icon = Share2 as any;
const BookmarkIcon = Bookmark as any;
const CodeIcon = Code as any;
const TerminalIcon = Terminal as any;
const BrainIcon = Brain as any;
const CogIcon = Cog as any;
const FlaskConicalIcon = FlaskConical as any;
const LineChartIconComponent = LineChartIcon as any;
const PresentationChartIcon = Presentation as any;
const FileSpreadsheetIcon = FileSpreadsheet as any;
const ClipboardIconComponent = Clipboard as any;
const TimerIcon = Timer as any;
const CheckSquareIcon = CheckSquare as any;
const AlertCircleIcon = AlertCircle as any;
const InfoIcon = Info as any;
const HelpCircleIcon = HelpCircle as any;
const BookOpenIcon = BookOpen as any;
const GraduationCapIcon = GraduationCap as any;
const WrenchIcon = Wrench as any;
const HammerIcon = Hammer as any;
const ScrewdriverIcon = Settings as any;
const VideoIcon = Video as any;
const CameraIcon = Camera as any;
const MicIcon = Mic as any;
const ImageIcon = Image as any;
const FilmIcon = Film as any;
const PlayCircleIcon = PlayCircle as any;
const StopCircleIcon = StopCircle as any;
const SkipForwardIcon = SkipForward as any;
const SkipBackIcon = SkipBack as any;
const Volume2Icon = Volume2 as any;
const VolumeXIcon = VolumeX as any;
const MaximizeIcon = Maximize as any;
const MinimizeIcon = Minimize as any;
const RotateCcwIcon = RotateCcw as any;
const RotateCwIcon = RotateCw as any;
const ZoomInIcon = ZoomIn as any;
const ZoomOutIcon = ZoomOut as any;
const MoveIcon = Move as any;
const CopyIcon = Copy as any;
const ScissorsIcon = Scissors as any;
const ClipboardIconAlt = ClipboardIcon as any;
const SaveIcon = Save as any;
const FolderOpenIcon = FolderOpen as any;
const FolderIcon = Folder as any;
const FileIcon = File as any;
const ArchiveIcon = Archive as any;
const Package2Icon = Package2 as any;
const BoxIcon = Box as any;
const ContainerIcon = Container as any;
const Layers3Icon = Layers3 as any;
const ComponentIcon = Component as any;
const PuzzleIcon = Puzzle as any;
const BlocksIcon = Blocks as any;
const Grid3x3Icon = Grid3x3 as any;
const LayoutIcon = Layout as any;
const SidebarIcon = Sidebar as any;
const PanelLeftIcon = PanelLeft as any;
const PanelRightIcon = PanelRight as any;
const PanelTopIcon = PanelTop as any;
const PanelBottomIcon = PanelBottom as any;
const ColumnsIcon = Columns as any;
const RowsIcon = Rows as any;
const TableIcon = Table as any;
const ListIcon = List as any;
const GridIcon = Grid as any;
const MenuIcon = Menu as any;
const MoreHorizontalIcon = MoreHorizontal as any;
const MoreVerticalIcon = MoreVertical as any;
const ChevronLeftIcon = ChevronLeft as any;
const ChevronUpIcon = ChevronUp as any;
const ChevronDownIcon = ChevronDown as any;
const ChevronsLeftIcon = ChevronsLeft as any;
const ChevronsRightIcon = ChevronsRight as any;
const ChevronsUpIcon = ChevronsUp as any;
const ChevronsDownIcon = ChevronsDown as any;
const ArrowLeftIcon = ArrowLeft as any;
const ArrowRightIcon = ArrowRight as any;
const ArrowUpRightIcon = ArrowUpRight as any;
const ArrowDownLeftIcon = ArrowDownLeft as any;
const ArrowDownRightIcon = ArrowDownRight as any;
const ArrowUpLeftIcon = ArrowUpLeft as any;
const CornerDownLeftIcon = CornerDownLeft as any;
const CornerDownRightIcon = CornerDownRight as any;
const CornerUpLeftIcon = CornerUpLeft as any;
const CornerUpRightIcon = CornerUpRight as any;
const RepeatIcon = Repeat as any;
const ShuffleIcon = Shuffle as any;
const FastForwardIcon = FastForward as any;
const RewindIcon = Rewind as any;
const PauseIconAlt = PauseIcon as any;
const PlayIconAlt = PlayIcon as any;
const SquareIcon = Square as any;
const CircleIcon = Circle as any;
const TriangleIcon = Triangle as any;
const HexagonIcon = Hexagon as any;
const OctagonIcon = Octagon as any;
const PentagonIcon = Pentagon as any;
const DiamondIcon = Diamond as any;
const HashIcon = Hash as any;
const AtSignIcon = AtSign as any;
const PercentIcon = Percent as any;
const AmpersandIcon = Ampersand as any;
const AsteriskIcon = Asterisk as any;
const SlashIcon = Slash as any;
const BackslashIcon = ArrowLeft as any;
const PipeIcon = MoreVertical as any;
const MinusIconAlt = MinusIcon as any;
const PlusIconAlt = PlusIcon as any;
const EqualIcon = Equal as any;
const UnderscoreIcon = Underline as any;
const QuoteIcon = Quote as any;
const ApostropheIcon = Type as any;
const ParenthesesIcon = Parentheses as any;
const BracketsIcon = Brackets as any;
const BracesIcon = Braces as any;
const AngleBracketsIcon = ChevronRight as any;

interface VerticalContent {
  id: string;
  name: string;
  icon: any;
  description: string;
  marketSize: string;
  painPoints: string[];
  quantumAdvantage: string;
  caseStudies: CaseStudy[];
  technicalContent: TechnicalContent[];
  businessContent: BusinessContent[];
  competitiveAnalysis: CompetitiveAnalysis;
  implementationRoadmap: RoadmapPhase[];
  roi: ROIMetrics;
  testimonials: Testimonial[];
  resources: Resource[];
  maturityLevel: number;
  traction: number;
  priority: 'high' | 'medium' | 'low';
}

interface CaseStudy {
  id: string;
  title: string;
  company: string;
  industry: string;
  challenge: string;
  solution: string;
  results: string[];
  metrics: {
    accuracy: number;
    efficiency: number;
    costSavings: number;
    timeReduction: number;
  };
  testimonial: string;
  videoUrl?: string;
  downloadUrl?: string;
  featured: boolean;
}

interface TechnicalContent {
  id: string;
  title: string;
  type: 'whitepaper' | 'technical_brief' | 'architecture' | 'benchmark' | 'demo';
  description: string;
  audience: 'data_scientist' | 'engineer' | 'architect' | 'developer';
  complexity: 'beginner' | 'intermediate' | 'advanced';
  downloadUrl: string;
  viewCount: number;
  rating: number;
  tags: string[];
}

interface BusinessContent {
  id: string;
  title: string;
  type: 'executive_brief' | 'roi_calculator' | 'business_case' | 'market_analysis';
  description: string;
  audience: 'ceo' | 'cto' | 'cfo' | 'coo' | 'vp';
  downloadUrl: string;
  viewCount: number;
  rating: number;
  tags: string[];
}

interface CompetitiveAnalysis {
  competitors: string[];
  advantages: string[];
  differentiators: string[];
  marketPosition: string;
  winRate: number;
}

interface RoadmapPhase {
  id: string;
  phase: string;
  duration: string;
  objectives: string[];
  deliverables: string[];
  success_criteria: string[];
  investment: string;
}

interface ROIMetrics {
  averageROI: number;
  paybackPeriod: string;
  netPresentValue: number;
  riskAdjustedReturn: number;
  implementationCost: number;
  annualSavings: number;
}

interface Testimonial {
  id: string;
  name: string;
  title: string;
  company: string;
  quote: string;
  rating: number;
  videoUrl?: string;
  imageUrl?: string;
}

interface Resource {
  id: string;
  title: string;
  type: 'video' | 'document' | 'demo' | 'webinar' | 'tool';
  url: string;
  description: string;
  duration?: string;
  size?: string;
  featured: boolean;
}

const VERTICAL_CONTENT: VerticalContent[] = [
  {
    id: 'manufacturing',
    name: 'Manufacturing Excellence',
    icon: Factory,
    description: 'Quantum-enhanced predictive quality control and process optimization for manufacturing operations',
    marketSize: '$2.3T global manufacturing market',
    painPoints: [
      'Unpredictable quality defects costing $20M+ annually',
      'Complex multi-variable process optimization challenges',
      'Real-time decision making with incomplete data',
      'Supply chain disruptions and inventory optimization',
      'Regulatory compliance and traceability requirements'
    ],
    quantumAdvantage: 'Quantum algorithms excel at finding non-obvious patterns in high-dimensional sensor data, achieving 34% better accuracy than classical ML while processing 100x more variables simultaneously',
    caseStudies: [
      {
        id: 'global-auto',
        title: 'Predictive Quality Control Revolution',
        company: 'Global Automotive Manufacturing Corp',
        industry: 'Automotive',
        challenge: 'Paint defect prediction in real-time production with 200+ sensor variables',
        solution: 'Quantum-enhanced ML model processing multi-dimensional sensor data with Dynex QaaS',
        results: [
          '99.2% prediction accuracy (vs 78% classical)',
          '22% reduction in scrap rates',
          '$4.3M annual cost savings',
          '15% improvement in OEE',
          '8-week implementation time'
        ],
        metrics: {
          accuracy: 99.2,
          efficiency: 87.5,
          costSavings: 4300000,
          timeReduction: 65
        },
        testimonial: 'The quantum advantage was immediately apparent. We achieved prediction accuracy we never thought possible with classical methods.',
        videoUrl: '/videos/global-auto-case-study.mp4',
        downloadUrl: '/downloads/global-auto-case-study.pdf',
        featured: true
      },
      {
        id: 'precision-manufacturing',
        title: 'Supply Chain Optimization at Scale',
        company: 'Precision Manufacturing Solutions',
        industry: 'Aerospace',
        challenge: 'Multi-tier supply chain optimization with 10,000+ components and suppliers',
        solution: 'Quantum annealing for complex constraint optimization across supply network',
        results: [
          '28% reduction in inventory costs',
          '45% faster supplier selection',
          '92% on-time delivery improvement',
          '$2.1M working capital optimization',
          '12-week ROI achievement'
        ],
        metrics: {
          accuracy: 94.7,
          efficiency: 91.2,
          costSavings: 2100000,
          timeReduction: 45
        },
        testimonial: 'Quantum optimization solved supply chain challenges that classical methods couldn\'t handle at our scale.',
        downloadUrl: '/downloads/precision-manufacturing-case-study.pdf',
        featured: true
      }
    ],
    technicalContent: [
      {
        id: 'qml-manufacturing',
        title: 'Quantum Machine Learning for Manufacturing Quality Control',
        type: 'whitepaper',
        description: 'Comprehensive technical analysis of quantum ML applications in manufacturing quality prediction',
        audience: 'data_scientist',
        complexity: 'advanced',
        downloadUrl: '/whitepapers/qml-manufacturing-quality.pdf',
        viewCount: 2847,
        rating: 4.8,
        tags: ['quantum-ml', 'quality-control', 'manufacturing', 'predictive-analytics']
      },
      {
        id: 'quantum-optimization-supply',
        title: 'Quantum Annealing for Supply Chain Optimization',
        type: 'technical_brief',
        description: 'Technical implementation guide for quantum-enhanced supply chain optimization',
        audience: 'engineer',
        complexity: 'intermediate',
        downloadUrl: '/briefs/quantum-supply-chain.pdf',
        viewCount: 1923,
        rating: 4.6,
        tags: ['quantum-annealing', 'supply-chain', 'optimization', 'logistics']
      },
      {
        id: 'manufacturing-architecture',
        title: 'NQBA Manufacturing Platform Architecture',
        type: 'architecture',
        description: 'Detailed system architecture for quantum-enhanced manufacturing platforms',
        audience: 'architect',
        complexity: 'advanced',
        downloadUrl: '/architecture/nqba-manufacturing.pdf',
        viewCount: 1456,
        rating: 4.9,
        tags: ['architecture', 'platform', 'manufacturing', 'system-design']
      }
    ],
    businessContent: [
      {
        id: 'manufacturing-roi',
        title: 'Manufacturing ROI Calculator',
        type: 'roi_calculator',
        description: 'Interactive calculator for quantum manufacturing ROI analysis',
        audience: 'cfo',
        downloadUrl: '/tools/manufacturing-roi-calculator',
        viewCount: 3421,
        rating: 4.7,
        tags: ['roi', 'calculator', 'manufacturing', 'business-case']
      },
      {
        id: 'manufacturing-executive-brief',
        title: 'Executive Brief: Quantum Advantage in Manufacturing',
        type: 'executive_brief',
        description: 'C-level focused overview of quantum computing benefits for manufacturing',
        audience: 'ceo',
        downloadUrl: '/briefs/manufacturing-executive-brief.pdf',
        viewCount: 2156,
        rating: 4.8,
        tags: ['executive', 'manufacturing', 'quantum-advantage', 'strategy']
      }
    ],
    competitiveAnalysis: {
      competitors: ['IBM Quantum', 'Google Quantum AI', 'Microsoft Azure Quantum', 'Classical ML Platforms'],
      advantages: [
        'Room temperature operation (vs cryogenic requirements)',
        'Real-time processing capabilities',
        'Industry-specific optimization',
        'Proven ROI in production environments'
      ],
      differentiators: [
        'Dynex neuromorphic quantum computing',
        'Litecoin trust chain for audit trails',
        'SigmaEQ internal optimization proof',
        'Manufacturing-specific algorithms'
      ],
      marketPosition: 'Leading quantum solution for manufacturing with proven production deployments',
      winRate: 73.2
    },
    implementationRoadmap: [
      {
        id: 'assessment',
        phase: 'Assessment & Planning',
        duration: '2-3 weeks',
        objectives: [
          'Identify high-impact use cases',
          'Assess data readiness and quality',
          'Define success metrics and KPIs',
          'Establish project governance'
        ],
        deliverables: [
          'Use case prioritization matrix',
          'Data assessment report',
          'Implementation roadmap',
          'Business case and ROI projections'
        ],
        success_criteria: [
          'Clear use case definition',
          'Stakeholder alignment',
          'Approved budget and timeline'
        ],
        investment: '$50K - $100K'
      },
      {
        id: 'pilot',
        phase: 'Pilot Implementation',
        duration: '8-12 weeks',
        objectives: [
          'Deploy quantum-enhanced solution',
          'Validate performance improvements',
          'Train operational teams',
          'Establish monitoring and governance'
        ],
        deliverables: [
          'Production-ready quantum models',
          'Integration with existing systems',
          'Performance benchmarking results',
          'Training materials and documentation'
        ],
        success_criteria: [
          'Demonstrated quantum advantage',
          'Positive ROI achievement',
          'User adoption and satisfaction'
        ],
        investment: '$200K - $500K'
      },
      {
        id: 'scale',
        phase: 'Enterprise Scaling',
        duration: '6-12 months',
        objectives: [
          'Scale across multiple facilities',
          'Integrate with enterprise systems',
          'Establish center of excellence',
          'Continuous optimization and improvement'
        ],
        deliverables: [
          'Enterprise-wide deployment',
          'Advanced analytics and reporting',
          'Quantum computing center of excellence',
          'Long-term optimization strategy'
        ],
        success_criteria: [
          'Multi-facility deployment success',
          'Sustained performance improvements',
          'Internal quantum expertise development'
        ],
        investment: '$1M - $5M'
      }
    ],
    roi: {
      averageROI: 340,
      paybackPeriod: '8-12 months',
      netPresentValue: 2400000,
      riskAdjustedReturn: 285,
      implementationCost: 750000,
      annualSavings: 3200000
    },
    testimonials: [
      {
        id: 'manufacturing-cto',
        name: 'Dr. Sarah Chen',
        title: 'Chief Technology Officer',
        company: 'Global Automotive Manufacturing Corp',
        quote: 'The quantum advantage in our quality control processes has been transformational. We\'ve achieved prediction accuracy levels that seemed impossible with classical methods.',
        rating: 5,
        videoUrl: '/testimonials/sarah-chen-video.mp4',
        imageUrl: '/testimonials/sarah-chen.jpg'
      },
      {
        id: 'manufacturing-plant-manager',
        name: 'Michael Rodriguez',
        title: 'Plant Manager',
        company: 'Precision Manufacturing Solutions',
        quote: 'The ROI was evident within weeks. Our scrap rates dropped dramatically, and the real-time insights have revolutionized our production planning.',
        rating: 5,
        imageUrl: '/testimonials/michael-rodriguez.jpg'
      }
    ],
    resources: [
      {
        id: 'manufacturing-demo',
        title: 'Interactive Manufacturing Quality Demo',
        type: 'demo',
        url: '/demos/manufacturing-quality',
        description: 'Live demonstration of quantum-enhanced quality prediction',
        featured: true
      },
      {
        id: 'manufacturing-webinar',
        title: 'Quantum Computing in Manufacturing Webinar Series',
        type: 'webinar',
        url: '/webinars/manufacturing-series',
        description: 'Comprehensive webinar series covering quantum applications in manufacturing',
        duration: '45 minutes',
        featured: true
      }
    ],
    maturityLevel: 85,
    traction: 92,
    priority: 'high'
  },
  {
    id: 'finance',
    name: 'Financial Services',
    icon: Banknote,
    description: 'Quantum-powered portfolio optimization and risk management for financial institutions',
    marketSize: '$1.8T global financial services market',
    painPoints: [
      'Complex portfolio optimization with thousands of constraints',
      'Real-time risk assessment and stress testing',
      'Regulatory compliance and reporting requirements',
      'High-frequency trading optimization challenges',
      'Credit risk modeling with incomplete data'
    ],
    quantumAdvantage: 'Quantum annealing solves complex portfolio constraints 100x faster while finding globally optimal solutions, avoiding local minima that trap classical optimizers',
    caseStudies: [
      {
        id: 'hedge-fund-alpha',
        title: 'Portfolio Optimization Revolution',
        company: 'Alpha Quantum Capital',
        industry: 'Hedge Fund',
        challenge: 'Multi-asset portfolio optimization with 5,000+ securities and complex constraints',
        solution: 'Quantum annealing for real-time portfolio rebalancing with risk constraints',
        results: [
          '28% improvement in Sharpe ratio',
          '35% reduction in maximum drawdown',
          '2.3% additional alpha generation',
          '$180M in additional returns',
          '5-minute optimization time (vs 4 hours classical)'
        ],
        metrics: {
          accuracy: 96.4,
          efficiency: 94.1,
          costSavings: 180000000,
          timeReduction: 92
        },
        testimonial: 'Quantum optimization has given us a significant competitive edge in portfolio management.',
        videoUrl: '/videos/alpha-quantum-case-study.mp4',
        downloadUrl: '/downloads/alpha-quantum-case-study.pdf',
        featured: true
      }
    ],
    technicalContent: [
      {
        id: 'quantum-portfolio-optimization',
        title: 'Quantum Algorithms for Portfolio Optimization',
        type: 'whitepaper',
        description: 'Mathematical foundations of quantum portfolio optimization algorithms',
        audience: 'data_scientist',
        complexity: 'advanced',
        downloadUrl: '/whitepapers/quantum-portfolio-optimization.pdf',
        viewCount: 3241,
        rating: 4.9,
        tags: ['quantum-algorithms', 'portfolio-optimization', 'finance', 'qubo']
      }
    ],
    businessContent: [
      {
        id: 'finance-roi-calculator',
        title: 'Financial Services ROI Calculator',
        type: 'roi_calculator',
        description: 'Calculate ROI for quantum-enhanced financial services applications',
        audience: 'cfo',
        downloadUrl: '/tools/finance-roi-calculator',
        viewCount: 2876,
        rating: 4.6,
        tags: ['roi', 'finance', 'calculator', 'portfolio-optimization']
      }
    ],
    competitiveAnalysis: {
      competitors: ['D-Wave', 'IBM Quantum', 'Rigetti', 'Classical Optimization'],
      advantages: [
        'Real-time optimization capabilities',
        'Superior solution quality',
        'Regulatory compliance features',
        'Proven alpha generation'
      ],
      differentiators: [
        'Financial-specific quantum algorithms',
        'Risk-adjusted optimization',
        'Real-time market integration',
        'Compliance and audit trails'
      ],
      marketPosition: 'Premium quantum solution for sophisticated financial institutions',
      winRate: 68.7
    },
    implementationRoadmap: [
      {
        id: 'assessment',
        phase: 'Financial Assessment',
        duration: '3-4 weeks',
        objectives: [
          'Analyze current portfolio optimization processes',
          'Identify quantum advantage opportunities',
          'Assess regulatory requirements',
          'Define performance benchmarks'
        ],
        deliverables: [
          'Current state analysis',
          'Quantum opportunity assessment',
          'Regulatory compliance framework',
          'Performance benchmarking plan'
        ],
        success_criteria: [
          'Clear quantum advantage identification',
          'Regulatory approval pathway',
          'Stakeholder buy-in'
        ],
        investment: '$75K - $150K'
      }
    ],
    roi: {
      averageROI: 280,
      paybackPeriod: '6-9 months',
      netPresentValue: 18000000,
      riskAdjustedReturn: 245,
      implementationCost: 1200000,
      annualSavings: 4800000
    },
    testimonials: [
      {
        id: 'finance-cio',
        name: 'James Patterson',
        title: 'Chief Investment Officer',
        company: 'Alpha Quantum Capital',
        quote: 'The quantum advantage in portfolio optimization is undeniable. We\'ve achieved alpha generation that was previously impossible.',
        rating: 5,
        videoUrl: '/testimonials/james-patterson-video.mp4'
      }
    ],
    resources: [
      {
        id: 'finance-demo',
        title: 'Portfolio Optimization Demo',
        type: 'demo',
        url: '/demos/portfolio-optimization',
        description: 'Interactive demonstration of quantum portfolio optimization',
        featured: true
      }
    ],
    maturityLevel: 78,
    traction: 85,
    priority: 'high'
  }
];

const COLORS = {
  primary: '#3b82f6',
  secondary: '#10b981',
  accent: '#8b5cf6',
  warning: '#f59e0b',
  error: '#ef4444',
  success: '#10b981',
  quantum: '#6366f1',
  classical: '#6b7280'
};

export const VerticalContentStrategy: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedVertical, setSelectedVertical] = useState<VerticalContent>(VERTICAL_CONTENT[0]);
  const [selectedContent, setSelectedContent] = useState<string>('case-studies');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');

  // Filter content based on search and type
  const filteredContent = useMemo(() => {
    let content = [...selectedVertical.technicalContent, ...selectedVertical.businessContent];
    
    if (searchTerm) {
      content = content.filter(item => 
        item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }
    
    if (filterType !== 'all') {
      content = content.filter(item => item.type === filterType);
    }
    
    return content;
  }, [selectedVertical, searchTerm, filterType]);

  return (
    <div className="w-full max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Target className="h-8 w-8 text-blue-600" />
              <Sparkles className="h-4 w-4 text-yellow-500 absolute -top-1 -right-1 animate-pulse" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Vertical Content Strategy
            </h1>
          </div>
          <p className="text-gray-600">Dominate specific verticals with compelling, technical case studies and proven quantum advantage</p>
        </div>
        
        <div className="flex items-center space-x-3">
          <Badge variant="outline" className="flex items-center space-x-2">
            <TrendingUp className="h-4 w-4" />
            <span>Market Leading</span>
          </Badge>
          <Button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
            <Plus className="h-4 w-4 mr-2" />
            Create Content
          </Button>
        </div>
      </div>

      {/* Vertical Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {VERTICAL_CONTENT.map((vertical) => {
          const VerticalIcon = vertical.icon;
          const isSelected = selectedVertical.id === vertical.id;
          
          return (
            <Card 
              key={vertical.id} 
              className={`cursor-pointer transition-all hover:shadow-lg ${
                isSelected ? 'ring-2 ring-blue-500 bg-blue-50' : ''
              }`}
              onClick={() => setSelectedVertical(vertical)}
            >
              <CardContent className="p-4">
                <div className="flex items-center space-x-3 mb-3">
                  <VerticalIcon className={`h-6 w-6 ${
                    isSelected ? 'text-blue-600' : 'text-gray-600'
                  }`} />
                  <div className="font-semibold">{vertical.name}</div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Maturity</span>
                    <span className="font-bold">{vertical.maturityLevel}%</span>
                  </div>
                  <Progress value={vertical.maturityLevel} className="h-2" />
                  
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Traction</span>
                    <span className="font-bold">{vertical.traction}%</span>
                  </div>
                  <Progress value={vertical.traction} className="h-2" />
                </div>
                
                <div className="mt-3 flex items-center justify-between">
                  <Badge variant={vertical.priority === 'high' ? 'default' : 'secondary'}>
                    {vertical.priority} priority
                  </Badge>
                  <div className="text-xs text-gray-500">
                    {vertical.caseStudies.length} case studies
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview" className="flex items-center space-x-2">
            <Eye className="h-4 w-4" />
            <span>Overview</span>
          </TabsTrigger>
          <TabsTrigger value="case-studies" className="flex items-center space-x-2">
            <Award className="h-4 w-4" />
            <span>Case Studies</span>
          </TabsTrigger>
          <TabsTrigger value="content" className="flex items-center space-x-2">
            <BookOpen className="h-4 w-4" />
            <span>Content</span>
          </TabsTrigger>
          <TabsTrigger value="competitive" className="flex items-center space-x-2">
            <Target className="h-4 w-4" />
            <span>Competitive</span>
          </TabsTrigger>
          <TabsTrigger value="roadmap" className="flex items-center space-x-2">
            <GitBranch className="h-4 w-4" />
            <span>Roadmap</span>
          </TabsTrigger>
          <TabsTrigger value="testimonials" className="flex items-center space-x-2">
            <MessageSquare className="h-4 w-4" />
            <span>Testimonials</span>
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Vertical Overview */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <selectedVertical.icon className="h-8 w-8 text-blue-600" />
                  <div>
                    <CardTitle className="text-2xl">{selectedVertical.name}</CardTitle>
                    <div className="text-gray-600">{selectedVertical.marketSize}</div>
                  </div>
                </div>
                <Badge className="bg-green-100 text-green-800">
                  {selectedVertical.priority} Priority
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <p className="text-gray-700">{selectedVertical.description}</p>
              
              {/* Key Metrics */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{selectedVertical.roi.averageROI}%</div>
                  <div className="text-sm text-gray-600">Average ROI</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{selectedVertical.roi.paybackPeriod}</div>
                  <div className="text-sm text-gray-600">Payback Period</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">{selectedVertical.competitiveAnalysis.winRate}%</div>
                  <div className="text-sm text-gray-600">Win Rate</div>
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">{selectedVertical.caseStudies.length}</div>
                  <div className="text-sm text-gray-600">Case Studies</div>
                </div>
              </div>
              
              {/* Pain Points */}
              <div>
                <h3 className="text-lg font-semibold mb-3">Key Pain Points</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {selectedVertical.painPoints.map((pain, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-red-50 rounded-lg">
                      <AlertTriangle className="h-5 w-5 text-red-600 mt-0.5" />
                      <span className="text-sm text-gray-700">{pain}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              {/* Quantum Advantage */}
              <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                <h3 className="text-lg font-semibold mb-2 flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-purple-600" />
                  <span>Quantum Advantage</span>
                </h3>
                <p className="text-gray-700">{selectedVertical.quantumAdvantage}</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Case Studies Tab */}
        <TabsContent value="case-studies" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {selectedVertical.caseStudies.map((caseStudy) => (
              <Card key={caseStudy.id} className={`${caseStudy.featured ? 'ring-2 ring-yellow-400' : ''}`}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="flex items-center space-x-2">
                        {caseStudy.featured && <StarIcon className="h-5 w-5 text-yellow-500" />}
                        <span>{caseStudy.title}</span>
                      </CardTitle>
                      <div className="text-sm text-gray-600">
                        {caseStudy.company} • {caseStudy.industry}
                      </div>
                    </div>
                    {caseStudy.videoUrl && (
                      <Button size="sm" variant="outline">
                        <VideoIcon className="h-4 w-4 mr-2" />
                        Watch
                      </Button>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-800 mb-1">Challenge:</h4>
                    <p className="text-sm text-gray-700">{caseStudy.challenge}</p>
                  </div>
                  
                  <div>
                    <h4 className="font-medium text-gray-800 mb-1">Solution:</h4>
                    <p className="text-sm text-gray-700">{caseStudy.solution}</p>
                  </div>
                  
                  <div>
                    <h4 className="font-medium text-gray-800 mb-2">Results:</h4>
                    <div className="space-y-1">
                      {caseStudy.results.map((result, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          <CheckCircle className="h-3 w-3 text-green-600" />
                          <span className="text-sm text-gray-700">{result}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {/* Metrics */}
                  <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                    <div className="text-center">
                      <div className="text-lg font-bold text-blue-600">{caseStudy.metrics.accuracy}%</div>
                      <div className="text-xs text-gray-600">Accuracy</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-bold text-green-600">
                        ${(caseStudy.metrics.costSavings / 1000000).toFixed(1)}M
                      </div>
                      <div className="text-xs text-gray-600">Savings</div>
                    </div>
                  </div>
                  
                  {/* Testimonial */}
                  <div className="bg-gray-50 p-3 rounded-lg italic text-sm text-gray-700">
                    "{caseStudy.testimonial}"
                  </div>
                  
                  <div className="flex items-center justify-between pt-2">
                    <Button size="sm" variant="outline">
                      <Download className="h-3 w-3 mr-2" />
                      Download PDF
                    </Button>
                    <Button size="sm">
                      <ExternalLink className="h-3 w-3 mr-2" />
                      Full Case Study
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Content Tab */}
        <TabsContent value="content" className="space-y-6">
          {/* Content Filters */}
          <div className="flex items-center space-x-4">
            <div className="flex-1">
              <Input
                placeholder="Search content..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="max-w-md"
              />
            </div>
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Content</SelectItem>
                <SelectItem value="whitepaper">Whitepapers</SelectItem>
                <SelectItem value="technical_brief">Technical Briefs</SelectItem>
                <SelectItem value="executive_brief">Executive Briefs</SelectItem>
                <SelectItem value="roi_calculator">ROI Calculators</SelectItem>
                <SelectItem value="demo">Demos</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Content Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredContent.map((content) => {
              const typeIcons = {
                whitepaper: FileText,
                technical_brief: Clipboard,
                architecture: Building2,
                benchmark: BarChart3,
                demo: PlayCircle,
                executive_brief: Briefcase,
                roi_calculator: Calculator,
                business_case: Presentation,
                market_analysis: TrendingUp
              };
              
              const TypeIcon = typeIcons[content.type as keyof typeof typeIcons] || FileText;
              
              const audienceColors = {
                data_scientist: 'bg-blue-100 text-blue-800',
                engineer: 'bg-green-100 text-green-800',
                architect: 'bg-purple-100 text-purple-800',
                developer: 'bg-orange-100 text-orange-800',
                ceo: 'bg-red-100 text-red-800',
                cto: 'bg-blue-100 text-blue-800',
                cfo: 'bg-green-100 text-green-800',
                coo: 'bg-purple-100 text-purple-800',
                vp: 'bg-orange-100 text-orange-800'
              };
              
              const complexityColors = {
                beginner: 'bg-green-100 text-green-800',
                intermediate: 'bg-yellow-100 text-yellow-800',
                advanced: 'bg-red-100 text-red-800'
              };
              
              return (
                <Card key={content.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center space-x-3">
                        <TypeIcon className="h-6 w-6 text-blue-600" />
                        <div>
                          <CardTitle className="text-lg">{content.title}</CardTitle>
                          <div className="text-sm text-gray-600 capitalize">
                            {content.type.replace('_', ' ')}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-1">
                        <StarIcon className="h-4 w-4 text-yellow-500" />
                        <span className="text-sm">{content.rating}</span>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm text-gray-700">{content.description}</p>
                    
                    <div className="flex items-center space-x-2">
                      <Badge className={audienceColors[content.audience as keyof typeof audienceColors]}>
                        {content.audience.replace('_', ' ')}
                      </Badge>
                      {'complexity' in content && (
                        <Badge className={complexityColors[content.complexity as keyof typeof complexityColors]}>
                          {content.complexity}
                        </Badge>
                      )}
                    </div>
                    
                    <div className="flex flex-wrap gap-1">
                      {content.tags.map((tag, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                    
                    <div className="flex items-center justify-between pt-4 border-t">
                      <div className="flex items-center space-x-4 text-sm text-gray-600">
                        <div className="flex items-center space-x-1">
                          <Eye className="h-3 w-3" />
                          <span>{content.viewCount.toLocaleString()}</span>
                        </div>
                      </div>
                      <Button size="sm">
                        <Download className="h-3 w-3 mr-2" />
                        Access
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        {/* Competitive Tab */}
        <TabsContent value="competitive" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Competitive Position */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Target className="h-5 w-5 text-blue-600" />
                  <span>Market Position</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center p-6 bg-blue-50 rounded-lg">
                  <div className="text-3xl font-bold text-blue-600 mb-2">
                    {selectedVertical.competitiveAnalysis.winRate}%
                  </div>
                  <div className="text-sm text-gray-600">Win Rate vs Competition</div>
                </div>
                
                <div>
                  <h4 className="font-medium mb-2">Market Position:</h4>
                  <p className="text-sm text-gray-700">
                    {selectedVertical.competitiveAnalysis.marketPosition}
                  </p>
                </div>
                
                <div>
                  <h4 className="font-medium mb-2">Key Competitors:</h4>
                  <div className="space-y-1">
                    {selectedVertical.competitiveAnalysis.competitors.map((competitor, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <Building2 className="h-3 w-3 text-gray-600" />
                        <span className="text-sm text-gray-700">{competitor}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Competitive Advantages */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Award className="h-5 w-5 text-green-600" />
                  <span>Competitive Advantages</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="font-medium mb-2">Key Advantages:</h4>
                  <div className="space-y-2">
                    {selectedVertical.competitiveAnalysis.advantages.map((advantage, index) => (
                      <div key={index} className="flex items-start space-x-2">
                        <CheckCircle className="h-4 w-4 text-green-600 mt-0.5" />
                        <span className="text-sm text-gray-700">{advantage}</span>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium mb-2">Unique Differentiators:</h4>
                  <div className="space-y-2">
                    {selectedVertical.competitiveAnalysis.differentiators.map((diff, index) => (
                      <div key={index} className="flex items-start space-x-2">
                        <Sparkles className="h-4 w-4 text-purple-600 mt-0.5" />
                        <span className="text-sm text-gray-700">{diff}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Roadmap Tab */}
        <TabsContent value="roadmap" className="space-y-6">
          <div className="space-y-6">
            {selectedVertical.implementationRoadmap.map((phase, index) => (
              <Card key={phase.id}>
                <CardHeader>
                  <div className="flex items-center space-x-4">
                    <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <CardTitle>{phase.phase}</CardTitle>
                      <div className="text-sm text-gray-600">
                        {phase.duration} • {phase.investment}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                      <h4 className="font-medium mb-2">Objectives:</h4>
                      <div className="space-y-1">
                        {phase.objectives.map((objective, idx) => (
                          <div key={idx} className="flex items-start space-x-2">
                            <Target className="h-3 w-3 text-blue-600 mt-1" />
                            <span className="text-sm text-gray-700">{objective}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-medium mb-2">Deliverables:</h4>
                      <div className="space-y-1">
                        {phase.deliverables.map((deliverable, idx) => (
                          <div key={idx} className="flex items-start space-x-2">
                            <Package2 className="h-3 w-3 text-green-600 mt-1" />
                            <span className="text-sm text-gray-700">{deliverable}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-medium mb-2">Success Criteria:</h4>
                      <div className="space-y-1">
                        {phase.success_criteria.map((criteria, idx) => (
                          <div key={idx} className="flex items-start space-x-2">
                            <CheckCircle className="h-3 w-3 text-purple-600 mt-1" />
                            <span className="text-sm text-gray-700">{criteria}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Testimonials Tab */}
        <TabsContent value="testimonials" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {selectedVertical.testimonials.map((testimonial) => (
              <Card key={testimonial.id}>
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4">
                    {testimonial.imageUrl ? (
                      <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                        <Users className="h-6 w-6 text-gray-600" />
                      </div>
                    ) : (
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <Users className="h-6 w-6 text-blue-600" />
                      </div>
                    )}
                    
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <div className="font-semibold">{testimonial.name}</div>
                        <div className="flex items-center space-x-1">
                          {[...Array(testimonial.rating)].map((_, i) => (
                            <StarIcon key={i} className="h-3 w-3 text-yellow-500 fill-current" />
                          ))}
                        </div>
                      </div>
                      
                      <div className="text-sm text-gray-600 mb-3">
                        {testimonial.title} • {testimonial.company}
                      </div>
                      
                      <blockquote className="text-gray-700 italic mb-4">
                        "{testimonial.quote}"
                      </blockquote>
                      
                      {testimonial.videoUrl && (
                        <Button size="sm" variant="outline">
                          <VideoIcon className="h-3 w-3 mr-2" />
                          Watch Video
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default VerticalContentStrategy;