import { useState } from "react";

interface AlgorithmRunnerProps {
  algorithmName: string;
  algorithmType: string;
  onRun: (algorithmName: string) => void;
}

export default function AlgorithmRunner({ algorithmName, algorithmType, onRun }: AlgorithmRunnerProps) {
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<string | null>(null);

  const handleRun = async () => {
    setIsRunning(true);
    setProgress(0);
    setResult(null);
    
    // Simulate algorithm execution
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsRunning(false);
          // Generate mock results based on algorithm type
          const results = {
            "Deutsch-Jozsa": "Function is balanced (quantum advantage: 1 query vs 2^n classical queries)",
            "Grover": "Found target item in 23 iterations (classical would need 1000 iterations)",
            "Shor": "Factors found: 3, 5 (quantum advantage: exponential speedup)",
            "QFT": "Fourier transform completed in O(n²) vs O(n2ⁿ) classical complexity",
            "QML": "Training completed with 28% accuracy improvement over classical ML",
            "Custom": "Custom algorithm executed successfully with quantum advantage"
          };
          setResult(results[algorithmName as keyof typeof results] || "Algorithm completed successfully");
          return 100;
        }
        return prev + Math.random() * 15;
      });
    }, 200);

    onRun(algorithmName);
  };

  return (
    <div className="space-y-4">
      <button
        onClick={handleRun}
        disabled={isRunning}
        className="w-full bg-gradient-to-r from-cyan-500 to-purple-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:from-cyan-600 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isRunning ? "🔄 Running..." : "🚀 Run Algorithm"}
      </button>
      
      {isRunning && (
        <div className="space-y-2">
          <div className="flex justify-between text-xs text-gray-600">
            <span>Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-cyan-500 to-purple-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      )}
      
      {result && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-3">
          <p className="text-green-800 text-sm font-medium">✅ Results:</p>
          <p className="text-green-700 text-xs mt-1">{result}</p>
        </div>
      )}
    </div>
  );
}
