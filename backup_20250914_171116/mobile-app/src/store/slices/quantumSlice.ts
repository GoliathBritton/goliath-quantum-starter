import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface QuantumState {
  isConnected: boolean;
  currentCircuit: any;
  results: any[];
  loading: boolean;
  error: string | null;
}

const initialState: QuantumState = {
  isConnected: false,
  currentCircuit: null,
  results: [],
  loading: false,
  error: null,
};

export const connectQuantumBackend = createAsyncThunk(
  'quantum/connectBackend',
  async () => {
    // Simulate quantum backend connection
    await new Promise(resolve => setTimeout(resolve, 1000));
    return { connected: true };
  }
);

export const executeQuantumCircuit = createAsyncThunk(
  'quantum/executeCircuit',
  async (circuit: any) => {
    // Simulate quantum circuit execution
    await new Promise(resolve => setTimeout(resolve, 2000));
    return {
      results: [Math.random(), Math.random(), Math.random()],
      timestamp: new Date().toISOString(),
    };
  }
);

const quantumSlice = createSlice({
  name: 'quantum',
  initialState,
  reducers: {
    setCurrentCircuit: (state, action: PayloadAction<any>) => {
      state.currentCircuit = action.payload;
    },
    clearResults: (state) => {
      state.results = [];
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(connectQuantumBackend.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(connectQuantumBackend.fulfilled, (state) => {
        state.loading = false;
        state.isConnected = true;
      })
      .addCase(connectQuantumBackend.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to connect to quantum backend';
      })
      .addCase(executeQuantumCircuit.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(executeQuantumCircuit.fulfilled, (state, action) => {
        state.loading = false;
        state.results.push(action.payload);
      })
      .addCase(executeQuantumCircuit.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to execute quantum circuit';
      });
  },
});

export const { setCurrentCircuit, clearResults, clearError } = quantumSlice.actions;
export default quantumSlice.reducer;