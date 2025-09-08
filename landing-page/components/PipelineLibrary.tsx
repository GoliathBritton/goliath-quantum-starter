import React, { useState, useEffect } from 'react';

interface PipelineConfig {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
  tags?: string[];
}

interface PipelineLibraryProps {
  isOpen: boolean;
  onClose: () => void;
  onLoad: (pipelineId: string) => void;
}

const PipelineLibrary: React.FC<PipelineLibraryProps> = ({ isOpen, onClose, onLoad }) => {
  const [pipelines, setPipelines] = useState<PipelineConfig[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchPipelines = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        page_size: '10',
        ...(searchTerm && { search: searchTerm })
      });
      
      const response = await fetch(`http://localhost:8000/api/pipelines?${params}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch pipelines');
      }
      
      const data = await response.json();
      setPipelines(data.pipelines);
      setTotalPages(Math.ceil(data.total / 10));
    } catch (error) {
      console.error('Error fetching pipelines:', error);
      alert('Failed to load pipeline library');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchPipelines();
    }
  }, [isOpen, page, searchTerm]);

  const handleLoad = (pipelineId: string) => {
    onLoad(pipelineId);
    onClose();
  };

  const handleDelete = async (pipelineId: string, pipelineName: string) => {
    if (!confirm(`Are you sure you want to delete "${pipelineName}"?`)) {
      return;
    }
    
    try {
      const response = await fetch(`http://localhost:8000/api/pipelines/${pipelineId}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) {
        throw new Error('Failed to delete pipeline');
      }
      
      alert('Pipeline deleted successfully');
      fetchPipelines(); // Refresh the list
    } catch (error) {
      console.error('Error deleting pipeline:', error);
      alert('Failed to delete pipeline');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">📚 Pipeline Library</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          
          <div className="modal-body">
            {/* Search */}
            <div className="mb-3">
              <input
                type="text"
                className="form-control"
                placeholder="Search pipelines..."
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setPage(1);
                }}
              />
            </div>
            
            {/* Pipeline List */}
            {loading ? (
              <div className="text-center py-4">
                <div className="spinner-border" role="status">
                  <span className="visually-hidden">Loading...</span>
                </div>
              </div>
            ) : pipelines.length === 0 ? (
              <div className="text-center py-4 text-muted">
                {searchTerm ? 'No pipelines found matching your search.' : 'No saved pipelines yet.'}
              </div>
            ) : (
              <div className="list-group">
                {pipelines.map((pipeline) => (
                  <div key={pipeline.id} className="list-group-item">
                    <div className="d-flex justify-content-between align-items-start">
                      <div className="flex-grow-1">
                        <h6 className="mb-1">{pipeline.name}</h6>
                        {pipeline.description && (
                          <p className="mb-1 text-muted small">{pipeline.description}</p>
                        )}
                        <small className="text-muted">
                          Created: {new Date(pipeline.created_at).toLocaleDateString()}
                          {pipeline.updated_at !== pipeline.created_at && (
                            <> • Updated: {new Date(pipeline.updated_at).toLocaleDateString()}</>
                          )}
                        </small>
                        {pipeline.tags && pipeline.tags.length > 0 && (
                          <div className="mt-1">
                            {pipeline.tags.map((tag, index) => (
                              <span key={index} className="badge bg-secondary me-1 small">
                                {tag}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                      <div className="d-flex gap-2">
                        <button
                          className="btn btn-primary btn-sm"
                          onClick={() => handleLoad(pipeline.id)}
                        >
                          📂 Load
                        </button>
                        <button
                          className="btn btn-outline-danger btn-sm"
                          onClick={() => handleDelete(pipeline.id, pipeline.name)}
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {/* Pagination */}
            {totalPages > 1 && (
              <nav className="mt-3">
                <ul className="pagination pagination-sm justify-content-center">
                  <li className={`page-item ${page === 1 ? 'disabled' : ''}`}>
                    <button 
                      className="page-link" 
                      onClick={() => setPage(page - 1)}
                      disabled={page === 1}
                    >
                      Previous
                    </button>
                  </li>
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((pageNum) => (
                    <li key={pageNum} className={`page-item ${page === pageNum ? 'active' : ''}`}>
                      <button 
                        className="page-link" 
                        onClick={() => setPage(pageNum)}
                      >
                        {pageNum}
                      </button>
                    </li>
                  ))}
                  <li className={`page-item ${page === totalPages ? 'disabled' : ''}`}>
                    <button 
                      className="page-link" 
                      onClick={() => setPage(page + 1)}
                      disabled={page === totalPages}
                    >
                      Next
                    </button>
                  </li>
                </ul>
              </nav>
            )}
          </div>
          
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PipelineLibrary;