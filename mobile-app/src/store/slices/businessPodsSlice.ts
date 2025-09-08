import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { apiClient } from '../../services/apiClient';

export interface BusinessPod {
  id: string;
  name: string;
  type: 'SIGMA_SELECT' | 'FLYFOX_AI' | 'GOLIATH_TRADE' | 'SFG_SYMMETRY' | 'GHOST_NEUROQ';
  status: 'ACTIVE' | 'INACTIVE' | 'MAINTENANCE';
  quantumAdvantage: number;
  lastOptimization: string;
  metrics: {
    totalOperations: number;
    successRate: number;
    avgResponseTime: number;
    quantumCreditsUsed: number;
  };
  capabilities: string[];
}

export interface QuantumOperation {
  id: string;
  podId: string;
  type: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  progress: number;
  result?: any;
  quantumAdvantage?: number;
  startTime: string;
  endTime?: string;
  error?: string;
}

export interface LeadScore {
  leadId: string;
  score: number;
  confidence: number;
  factors: {
    demographic: number;
    behavioral: number;
    engagement: number;
    quantum_enhanced: number;
  };
  recommendations: string[];
}

export interface EnergyOptimization {
  facilityId: string;
  currentUsage: number;
  optimizedUsage: number;
  savings: number;
  savingsPercentage: number;
  recommendations: {
    action: string;
    impact: number;
    priority: 'HIGH' | 'MEDIUM' | 'LOW';
  }[];
}

interface BusinessPodsState {
  pods: BusinessPod[];
  operations: QuantumOperation[];
  isLoading: boolean;
  error: string | null;
  selectedPod: string | null;
}

const initialState: BusinessPodsState = {
  pods: [],
  operations: [],
  isLoading: false,
  error: null,
  selectedPod: null,
};

// Async thunks
export const fetchBusinessPods = createAsyncThunk(
  'businessPods/fetchPods',
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiClient.get('/business-pods');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch business pods');
    }
  }
);

export const fetchOperations = createAsyncThunk(
  'businessPods/fetchOperations',
  async (podId?: string, { rejectWithValue }) => {
    try {
      const url = podId ? `/operations?podId=${podId}` : '/operations';
      const response = await apiClient.get(url);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch operations');
    }
  }
);

export const scoreLeads = createAsyncThunk(
  'businessPods/scoreLeads',
  async (leads: any[], { rejectWithValue }) => {
    try {
      const response = await apiClient.post('/sigma-select/score-leads', { leads });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to score leads');
    }
  }
);

export const optimizeEnergy = createAsyncThunk(
  'businessPods/optimizeEnergy',
  async (facilityData: any, { rejectWithValue }) => {
    try {
      const response = await apiClient.post('/flyfox-ai/optimize-energy', facilityData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to optimize energy');
    }
  }
);

export const optimizePortfolio = createAsyncThunk(
  'businessPods/optimizePortfolio',
  async (portfolioData: any, { rejectWithValue }) => {
    try {
      const response = await apiClient.post('/goliath-trade/optimize-portfolio', portfolioData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to optimize portfolio');
    }
  }
);

export const generateFinancialPlan = createAsyncThunk(
  'businessPods/generateFinancialPlan',
  async (clientData: any, { rejectWithValue }) => {
    try {
      const response = await apiClient.post('/sfg-symmetry/generate-plan', clientData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to generate financial plan');
    }
  }
);

export const gatherIntelligence = createAsyncThunk(
  'businessPods/gatherIntelligence',
  async (query: string, { rejectWithValue }) => {
    try {
      const response = await apiClient.post('/ghost-neuroq/gather-intelligence', { query });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to gather intelligence');
    }
  }
);

const businessPodsSlice = createSlice({
  name: 'businessPods',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setSelectedPod: (state, action: PayloadAction<string | null>) => {
      state.selectedPod = action.payload;
    },
    updateOperationProgress: (state, action: PayloadAction<{ id: string; progress: number }>) => {
      const operation = state.operations.find(op => op.id === action.payload.id);
      if (operation) {
        operation.progress = action.payload.progress;
      }
    },
    addOperation: (state, action: PayloadAction<QuantumOperation>) => {
      state.operations.unshift(action.payload);
    },
    updateOperation: (state, action: PayloadAction<QuantumOperation>) => {
      const index = state.operations.findIndex(op => op.id === action.payload.id);
      if (index !== -1) {
        state.operations[index] = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    // Fetch business pods
    builder
      .addCase(fetchBusinessPods.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchBusinessPods.fulfilled, (state, action) => {
        state.isLoading = false;
        state.pods = action.payload;
        state.error = null;
      })
      .addCase(fetchBusinessPods.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch operations
      .addCase(fetchOperations.fulfilled, (state, action) => {
        state.operations = action.payload;
      })
      // Score leads
      .addCase(scoreLeads.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(scoreLeads.fulfilled, (state) => {
        state.isLoading = false;
      })
      .addCase(scoreLeads.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Optimize energy
      .addCase(optimizeEnergy.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(optimizeEnergy.fulfilled, (state) => {
        state.isLoading = false;
      })
      .addCase(optimizeEnergy.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Optimize portfolio
      .addCase(optimizePortfolio.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(optimizePortfolio.fulfilled, (state) => {
        state.isLoading = false;
      })
      .addCase(optimizePortfolio.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  clearError,
  setSelectedPod,
  updateOperationProgress,
  addOperation,
  updateOperation,
} = businessPodsSlice.actions;

export default businessPodsSlice.reducer;