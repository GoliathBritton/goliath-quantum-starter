import { useState } from "react";

export default function Web3Integration() {
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectedWallet, setConnectedWallet] = useState<string | null>(null);
  const [achievements, setAchievements] = useState([
    { name: "First Algorithm Run", status: "available", unlocked: true },
    { name: "Quantum Advantage Demo", status: "locked", unlocked: false },
    { name: "Custom Circuit Builder", status: "locked", unlocked: false }
  ]);

  const connectMetaMask = async () => {
    setIsConnecting(true);
    try {
      // Simulate MetaMask connection
      await new Promise(resolve => setTimeout(resolve, 2000));
      setConnectedWallet("MetaMask");
      
      // Unlock first achievement
      setAchievements(prev => 
        prev.map(achievement => 
          achievement.name === "First Algorithm Run" 
            ? { ...achievement, status: "unlocked", unlocked: true }
            : achievement
        )
      );
      
      console.log("MetaMask connected successfully");
    } catch (error) {
      console.error("Failed to connect MetaMask:", error);
    } finally {
      setIsConnecting(false);
    }
  };

  const connectWalletConnect = async () => {
    setIsConnecting(true);
    try {
      // Simulate WalletConnect connection
      await new Promise(resolve => setTimeout(resolve, 2000));
      setConnectedWallet("WalletConnect");
      
      // Unlock first achievement
      setAchievements(prev => 
        prev.map(achievement => 
          achievement.name === "First Algorithm Run" 
            ? { ...achievement, status: "unlocked", unlocked: true }
            : achievement
        )
      );
      
      console.log("WalletConnect connected successfully");
    } catch (error) {
      console.error("Failed to connect WalletConnect:", error);
    } finally {
      setIsConnecting(false);
    }
  };

  const viewAchievements = () => {
    console.log("Opening achievements dashboard");
    // In a real implementation, this would open an achievements modal or navigate to achievements page
  };

  return (
    <div className="space-y-6">
      {/* Wallet Connection Buttons */}
      <div className="space-y-4">
        <button 
          onClick={connectMetaMask}
          disabled={isConnecting || connectedWallet === "MetaMask"}
          className="w-full bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white py-3 px-6 rounded-lg font-semibold transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isConnecting && connectedWallet !== "MetaMask" ? "🔄 Connecting..." : 
           connectedWallet === "MetaMask" ? "✅ Connected to MetaMask" : "🦊 Connect MetaMask"}
        </button>
        
        <button 
          onClick={connectWalletConnect}
          disabled={isConnecting || connectedWallet === "WalletConnect"}
          className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white py-3 px-6 rounded-lg font-semibold transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isConnecting && connectedWallet !== "WalletConnect" ? "🔄 Connecting..." : 
           connectedWallet === "WalletConnect" ? "✅ Connected to WalletConnect" : "🔗 Connect WalletConnect"}
        </button>
      </div>

      {/* Connection Status */}
      {connectedWallet && (
        <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
          <p className="text-green-300 text-sm text-center">
            <strong>Connected:</strong> {connectedWallet} - You can now earn on-chain achievements!
          </p>
        </div>
      )}

      {/* Achievements Section */}
      <div className="space-y-3">
        {achievements.map((achievement, index) => (
          <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
            <span className="text-gray-300">{achievement.name}</span>
            <span className={`${
              achievement.unlocked 
                ? "text-green-400" 
                : achievement.status === "locked" 
                  ? "text-yellow-400" 
                  : "text-red-400"
            }`}>
              {achievement.unlocked ? "✅ Unlocked" : "🔒 Locked"}
            </span>
          </div>
        ))}
      </div>

      {/* View Achievements Button */}
      <button 
        onClick={viewAchievements}
        className="w-full bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 text-white py-3 px-6 rounded-lg font-semibold transition-all transform hover:scale-105"
      >
        🎯 View Achievements
      </button>

      {/* Coming Soon Notice */}
      <div className="p-4 bg-cyan-500/10 border border-cyan-500/20 rounded-lg">
        <p className="text-cyan-300 text-sm text-center">
          <strong>Coming Soon:</strong> Multi-chain support for Polygon, Arbitrum, and Base
        </p>
      </div>
    </div>
  );
}
