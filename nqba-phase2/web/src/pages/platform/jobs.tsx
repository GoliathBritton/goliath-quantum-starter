import Link from "next/link";
import Header from "../../components/Header";
import Footer from "../../components/Footer";

export default function PlatformJobs() {
  const jobs = [
    {
      id: "JOB_001",
      name: "Portfolio Optimization",
      algorithm: "QUBO",
      status: "completed",
      submitted: "2025-01-02 10:30",
      completed: "2025-01-02 10:32",
      performance: "410x",
      result: "Optimal portfolio weights calculated"
    },
    {
      id: "JOB_002",
      name: "Database Search",
      algorithm: "Grover",
      status: "running",
      submitted: "2025-01-02 11:15",
      completed: null,
      performance: "24x",
      result: "Search in progress..."
    },
    {
      id: "JOB_003",
      name: "Factorization Test",
      algorithm: "Shor",
      status: "queued",
      submitted: "2025-01-02 11:45",
      completed: null,
      performance: "Pending",
      result: "Waiting in queue..."
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed": return "bg-green-100 text-green-800";
      case "running": return "bg-blue-100 text-blue-800";
      case "queued": return "bg-yellow-100 text-yellow-800";
      case "failed": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed": return "✅";
      case "running": return "🔄";
      case "queued": return "⏳";
      case "failed": return "❌";
      default: return "❓";
    }
  };

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center space-x-4 mb-6">
            <Link href="/platform" className="text-flyfoxSilver-300 hover:text-white transition-colors">
              ← Back to Platform
            </Link>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Quantum Job Management
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-4xl leading-relaxed">
            Submit, monitor, and manage quantum computing jobs with real-time performance tracking 
            and 410x quantum advantage.
          </p>
        </div>
      </section>

      {/* Job Submission */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-br from-cyan-50 to-purple-50 rounded-2xl p-8 border border-cyan-200">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Submit New Quantum Job</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Job Name
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                  placeholder="e.g., Portfolio Optimization"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Algorithm Type
                </label>
                <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                  <option>QUBO Optimization</option>
                  <option>Grover Search</option>
                  <option>Shor Factorization</option>
                  <option>Quantum Fourier Transform</option>
                  <option>Custom Algorithm</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Priority
                </label>
                <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                  <option>Normal</option>
                  <option>High</option>
                  <option>Urgent</option>
                </select>
              </div>
            </div>
            
            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Parameters (JSON)
              </label>
              <textarea
                rows={4}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent font-mono text-sm"
                placeholder='{"database_size": 1000, "target_item": "solution"}'
              ></textarea>
            </div>
            
            <div className="mt-6">
              <button className="bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105">
                🚀 Submit Quantum Job
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Job List */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Recent Jobs</h2>
            <div className="flex space-x-2">
              <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                Refresh
              </button>
              <button className="px-4 py-2 text-sm font-medium text-white bg-cyan-600 rounded-lg hover:bg-cyan-700">
                Export
              </button>
            </div>
          </div>
          
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Job ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Algorithm
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Submitted
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Performance
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Result
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {jobs.map((job) => (
                    <tr key={job.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {job.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {job.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {job.algorithm}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(job.status)}`}>
                          {getStatusIcon(job.status)} {job.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {job.submitted}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        <span className="font-semibold text-cyan-600">{job.performance}</span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                        {job.result}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* Performance Metrics */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Platform Performance</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-gradient-to-br from-cyan-50 to-purple-50 rounded-2xl p-6 border border-cyan-200 text-center">
              <div className="text-3xl font-bold text-cyan-600 mb-2">410x</div>
              <div className="text-sm text-gray-600">Average Performance Boost</div>
            </div>
            
            <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl p-6 border border-green-200 text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">99.9%</div>
              <div className="text-sm text-gray-600">Uptime</div>
            </div>
            
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-200 text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">2.3s</div>
              <div className="text-sm text-gray-600">Average Job Time</div>
            </div>
            
            <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-6 border border-orange-200 text-center">
              <div className="text-3xl font-bold text-orange-600 mb-2">1,247</div>
              <div className="text-sm text-gray-600">Jobs Completed</div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
