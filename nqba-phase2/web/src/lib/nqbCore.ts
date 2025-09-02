// Mock NQB Core Module for Testing
export const getNQBA = () => {
  console.log('Mock NQBA: Getting NQBA instance');
  return {
    version: '2.0.0',
    status: 'operational',
    components: ['quantum', 'ai', 'business', 'security']
  };
};
