// Mock Dynex Adapter for Testing
export const dynex = {
  submitJob: async (params: any) => {
    console.log('Mock Dynex: Submitting job', params);
    return {
      id: `job_${Date.now()}`,
      status: 'submitted',
      params
    };
  }
};
