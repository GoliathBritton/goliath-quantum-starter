// Mock SigmaEQ Module for Testing
export const computeQEI = (params: any) => {
  console.log('Mock SigmaEQ: Computing QEI', params);
  return 0.87; // Mock QEI score
};

export const momentumScore = (data: number[]) => {
  console.log('Mock SigmaEQ: Computing momentum', data);
  return 15.6; // Mock momentum score
};
