import React, { useState, useEffect } from 'react';
import { useAuth } from './auth/AuthContext';
import { Card, Button, Badge, Spinner, Alert, Modal, Table } from 'react-bootstrap';
import { Play, Save, Trash2, Eye, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

interface Pipeline {
  id: string;
  name: string;
  description: string;
  nodes: any[];
  edges: any[];
  target_runtime: string;
  created_at: string;
  updated_at: string;
  status: 'draft' | 'saved' | 'compiled';
}

interface ExecutionHistory {
  id: string;
  pipeline_id: string;
  pipeline_name: string;
  status: 'running' | 'completed' | 'failed' | 'cancelled';
  started_at: string;
  completed_at?: string;
  duration?: number;
  result?: any;
  error_message?: string;
  target_runtime: string;
}

const Dashboard: React.FC = () => {
  const { user, accessToken, isAuthenticated } = useAuth();
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [executionHistory, setExecutionHistory] = useState<ExecutionHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPipeline, setSelectedPipeline] = useState<Pipeline | null>(null);
  const [showPipelineModal, setShowPipelineModal] = useState(false);
  const [showExecutionModal, setShowExecutionModal] = useState(false);
  const [selectedExecution, setSelectedExecution] = useState<ExecutionHistory | null>(null);
  const [activeTab, setActiveTab] = useState<'pipelines' | 'history'>('pipelines');

  useEffect(() => {
    if (isAuthenticated) {
      loadDashboardData();
    }
  }, [isAuthenticated]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load saved pipelines
      const pipelinesResponse = await fetch('http://localhost:8000/api/pipelines', {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (pipelinesResponse.ok) {
        const pipelinesData = await pipelinesResponse.json();
        setPipelines(pipelinesData.pipelines || []);
      }

      // Load execution history
      const historyResponse = await fetch('http://localhost:8000/api/executions', {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (historyResponse.ok) {
        const historyData = await historyResponse.json();
        setExecutionHistory(historyData.executions || []);
      }
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard load error:', err);
    } finally {
      setLoading(false);
    }
  };

  const deletePipeline = async (pipelineId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/pipelines/${pipelineId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setPipelines(pipelines.filter(p => p.id !== pipelineId));
      } else {
        setError('Failed to delete pipeline');
      }
    } catch (err) {
      setError('Failed to delete pipeline');
      console.error('Delete pipeline error:', err);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="text-success" size={16} />;
      case 'failed':
        return <XCircle className="text-danger" size={16} />;
      case 'running':
        return <Spinner animation="border" size="sm" />;
      case 'cancelled':
        return <AlertCircle className="text-warning" size={16} />;
      default:
        return <Clock className="text-muted" size={16} />;
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: { [key: string]: string } = {
      'completed': 'success',
      'failed': 'danger',
      'running': 'primary',
      'cancelled': 'warning',
      'draft': 'secondary',
      'saved': 'info',
      'compiled': 'success'
    };
    return <Badge bg={variants[status] || 'secondary'}>{status}</Badge>;
  };

  const formatDuration = (duration?: number) => {
    if (!duration) return 'N/A';
    if (duration < 60) return `${duration}s`;
    if (duration < 3600) return `${Math.floor(duration / 60)}m ${duration % 60}s`;
    return `${Math.floor(duration / 3600)}h ${Math.floor((duration % 3600) / 60)}m`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  if (!isAuthenticated) {
    return (
      <div className="container mt-5">
        <Alert variant="info">
          <h4>Authentication Required</h4>
          <p>Please log in to access your dashboard.</p>
        </Alert>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Loading your dashboard...</p>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-12">
          <h2>Welcome back, {user?.username}!</h2>
          <p className="text-muted">Manage your quantum pipelines and view execution history.</p>
          
          {error && (
            <Alert variant="danger" dismissible onClose={() => setError(null)}>
              {error}
            </Alert>
          )}

          {/* Tab Navigation */}
          <div className="mb-4">
            <Button 
              variant={activeTab === 'pipelines' ? 'primary' : 'outline-primary'}
              className="me-2"
              onClick={() => setActiveTab('pipelines')}
            >
              Saved Pipelines ({pipelines.length})
            </Button>
            <Button 
              variant={activeTab === 'history' ? 'primary' : 'outline-primary'}
              onClick={() => setActiveTab('history')}
            >
              Execution History ({executionHistory.length})
            </Button>
          </div>

          {/* Pipelines Tab */}
          {activeTab === 'pipelines' && (
            <div>
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h4>Your Pipelines</h4>
                <Button variant="success" href="/pipeline-builder">
                  <Save size={16} className="me-2" />
                  Create New Pipeline
                </Button>
              </div>

              {pipelines.length === 0 ? (
                <Card>
                  <Card.Body className="text-center py-5">
                    <h5>No pipelines yet</h5>
                    <p className="text-muted">Create your first quantum pipeline to get started.</p>
                    <Button variant="primary" href="/pipeline-builder">
                      Create Pipeline
                    </Button>
                  </Card.Body>
                </Card>
              ) : (
                <div className="row">
                  {pipelines.map((pipeline) => (
                    <div key={pipeline.id} className="col-md-6 col-lg-4 mb-3">
                      <Card>
                        <Card.Body>
                          <div className="d-flex justify-content-between align-items-start mb-2">
                            <h6 className="card-title">{pipeline.name}</h6>
                            {getStatusBadge(pipeline.status)}
                          </div>
                          <p className="card-text text-muted small">{pipeline.description}</p>
                          <div className="small text-muted mb-3">
                            <div>Runtime: {pipeline.target_runtime}</div>
                            <div>Nodes: {pipeline.nodes.length}</div>
                            <div>Updated: {formatDate(pipeline.updated_at)}</div>
                          </div>
                          <div className="d-flex gap-2">
                            <Button 
                              size="sm" 
                              variant="outline-primary"
                              onClick={() => {
                                setSelectedPipeline(pipeline);
                                setShowPipelineModal(true);
                              }}
                            >
                              <Eye size={14} className="me-1" />
                              View
                            </Button>
                            <Button 
                              size="sm" 
                              variant="outline-success"
                              href={`/pipeline-builder?load=${pipeline.id}`}
                            >
                              <Play size={14} className="me-1" />
                              Edit
                            </Button>
                            <Button 
                              size="sm" 
                              variant="outline-danger"
                              onClick={() => deletePipeline(pipeline.id)}
                            >
                              <Trash2 size={14} />
                            </Button>
                          </div>
                        </Card.Body>
                      </Card>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Execution History Tab */}
          {activeTab === 'history' && (
            <div>
              <h4 className="mb-3">Execution History</h4>
              
              {executionHistory.length === 0 ? (
                <Card>
                  <Card.Body className="text-center py-5">
                    <h5>No executions yet</h5>
                    <p className="text-muted">Execute a pipeline to see its history here.</p>
                  </Card.Body>
                </Card>
              ) : (
                <Card>
                  <Table responsive hover>
                    <thead>
                      <tr>
                        <th>Pipeline</th>
                        <th>Status</th>
                        <th>Runtime</th>
                        <th>Started</th>
                        <th>Duration</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {executionHistory.map((execution) => (
                        <tr key={execution.id}>
                          <td>{execution.pipeline_name}</td>
                          <td>
                            <div className="d-flex align-items-center gap-2">
                              {getStatusIcon(execution.status)}
                              {getStatusBadge(execution.status)}
                            </div>
                          </td>
                          <td>
                            <Badge bg="secondary">{execution.target_runtime}</Badge>
                          </td>
                          <td>{formatDate(execution.started_at)}</td>
                          <td>{formatDuration(execution.duration)}</td>
                          <td>
                            <Button 
                              size="sm" 
                              variant="outline-primary"
                              onClick={() => {
                                setSelectedExecution(execution);
                                setShowExecutionModal(true);
                              }}
                            >
                              <Eye size={14} className="me-1" />
                              Details
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </Card>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Pipeline Details Modal */}
      <Modal show={showPipelineModal} onHide={() => setShowPipelineModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Pipeline Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedPipeline && (
            <div>
              <h5>{selectedPipeline.name}</h5>
              <p>{selectedPipeline.description}</p>
              <div className="row">
                <div className="col-md-6">
                  <strong>Status:</strong> {getStatusBadge(selectedPipeline.status)}
                </div>
                <div className="col-md-6">
                  <strong>Runtime:</strong> {selectedPipeline.target_runtime}
                </div>
                <div className="col-md-6">
                  <strong>Nodes:</strong> {selectedPipeline.nodes.length}
                </div>
                <div className="col-md-6">
                  <strong>Edges:</strong> {selectedPipeline.edges.length}
                </div>
                <div className="col-md-6">
                  <strong>Created:</strong> {formatDate(selectedPipeline.created_at)}
                </div>
                <div className="col-md-6">
                  <strong>Updated:</strong> {formatDate(selectedPipeline.updated_at)}
                </div>
              </div>
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowPipelineModal(false)}>
            Close
          </Button>
          <Button 
            variant="primary" 
            href={`/pipeline-builder?load=${selectedPipeline?.id}`}
          >
            Edit Pipeline
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Execution Details Modal */}
      <Modal show={showExecutionModal} onHide={() => setShowExecutionModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Execution Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedExecution && (
            <div>
              <h5>{selectedExecution.pipeline_name}</h5>
              <div className="row">
                <div className="col-md-6">
                  <strong>Status:</strong> {getStatusBadge(selectedExecution.status)}
                </div>
                <div className="col-md-6">
                  <strong>Runtime:</strong> {selectedExecution.target_runtime}
                </div>
                <div className="col-md-6">
                  <strong>Started:</strong> {formatDate(selectedExecution.started_at)}
                </div>
                <div className="col-md-6">
                  <strong>Duration:</strong> {formatDuration(selectedExecution.duration)}
                </div>
              </div>
              
              {selectedExecution.error_message && (
                <div className="mt-3">
                  <strong>Error:</strong>
                  <Alert variant="danger" className="mt-2">
                    {selectedExecution.error_message}
                  </Alert>
                </div>
              )}
              
              {selectedExecution.result && (
                <div className="mt-3">
                  <strong>Result:</strong>
                  <pre className="bg-light p-3 mt-2 rounded">
                    {JSON.stringify(selectedExecution.result, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowExecutionModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Dashboard;