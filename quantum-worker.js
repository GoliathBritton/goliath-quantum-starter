// Simulated Dynex Worker — replace with real Dynex SDK later
import { v4 as uuidv4 } from "uuid";
import EventEmitter from "events";

// In-memory queue for quantum jobs
const jobs = [];
const jobEvents = new EventEmitter();

/**
 * Add a new quantum job to the processing queue
 * @param {Object} payload - Job payload containing workflowId and nodes
 * @returns {string} - Unique job ID
 */
function addJob(payload) {
  const id = uuidv4();
  const job = {
    id,
    status: "queued",
    created: Date.now(),
    payload,
    progress: 0,
    estimatedDuration: Math.floor(Math.random() * 10000) + 5000 // 5-15 seconds
  };
  
  jobs.push(job);
  console.log(`[Quantum Worker] Job ${id} queued for processing`);

  // Simulate quantum processing pipeline
  setTimeout(() => {
    job.status = "initializing";
    job.progress = 10;
    jobEvents.emit("update", job);
    console.log(`[Quantum Worker] Job ${id} initializing quantum circuits`);
    
    setTimeout(() => {
      job.status = "running";
      job.progress = 30;
      jobEvents.emit("update", job);
      console.log(`[Quantum Worker] Job ${id} running QUBO optimization`);
      
      // Simulate progressive updates
      const progressInterval = setInterval(() => {
        if (job.progress < 90) {
          job.progress += Math.floor(Math.random() * 20) + 5;
          jobEvents.emit("update", job);
        }
      }, 1000);
      
      setTimeout(() => {
        clearInterval(progressInterval);
        job.status = "completed";
        job.progress = 100;
        job.completedAt = Date.now();
        
        // Generate realistic quantum optimization results
        job.result = {
          score: Math.random() * 100,
          optimizationGain: (Math.random() * 0.4 + 0.1).toFixed(3), // 10-50% improvement
          quantumAdvantage: (Math.random() * 0.3 + 0.2).toFixed(3), // 20-50% quantum speedup
          details: "Simulated Dynex neuromorphic quantum optimization",
          energyEfficiency: (Math.random() * 0.6 + 0.4).toFixed(3), // 40-100% energy efficiency
          processingTime: job.completedAt - job.created,
          qubitsUsed: Math.floor(Math.random() * 50) + 10,
          iterations: Math.floor(Math.random() * 1000) + 500,
          convergenceRate: (Math.random() * 0.05 + 0.95).toFixed(4) // 95-100% convergence
        };
        
        jobEvents.emit("update", job);
        console.log(`[Quantum Worker] Job ${id} completed successfully`);
      }, job.estimatedDuration - 2000);
    }, 2000);
  }, 1000);

  return id;
}

/**
 * Get job status by ID
 * @param {string} id - Job ID
 * @returns {Object|null} - Job object or null if not found
 */
function getJob(id) {
  return jobs.find((j) => j.id === id) || null;
}

/**
 * Get all jobs (for admin/debugging)
 * @returns {Array} - Array of all jobs
 */
function getAllJobs() {
  return jobs;
}

/**
 * Get jobs by status
 * @param {string} status - Job status to filter by
 * @returns {Array} - Array of jobs with matching status
 */
function getJobsByStatus(status) {
  return jobs.filter(job => job.status === status);
}

/**
 * Cancel a job (if still in queue or running)
 * @param {string} id - Job ID to cancel
 * @returns {boolean} - Success status
 */
function cancelJob(id) {
  const job = getJob(id);
  if (!job) return false;
  
  if (job.status === "queued" || job.status === "initializing" || job.status === "running") {
    job.status = "cancelled";
    job.cancelledAt = Date.now();
    jobEvents.emit("update", job);
    console.log(`[Quantum Worker] Job ${id} cancelled`);
    return true;
  }
  
  return false;
}

// Cleanup completed jobs older than 1 hour
setInterval(() => {
  const oneHourAgo = Date.now() - (60 * 60 * 1000);
  const initialLength = jobs.length;
  
  for (let i = jobs.length - 1; i >= 0; i--) {
    const job = jobs[i];
    if ((job.status === "completed" || job.status === "cancelled") && 
        (job.completedAt || job.cancelledAt) < oneHourAgo) {
      jobs.splice(i, 1);
    }
  }
  
  if (jobs.length < initialLength) {
    console.log(`[Quantum Worker] Cleaned up ${initialLength - jobs.length} old jobs`);
  }
}, 10 * 60 * 1000); // Run every 10 minutes

export {
  addJob,
  getJob,
  getAllJobs,
  getJobsByStatus,
  cancelJob,
  jobEvents
};

export default {
  addJob,
  getJob,
  getAllJobs,
  getJobsByStatus,
  cancelJob,
  jobEvents
};