import React, { useState } from 'react';
import { Modal, Button, Form, Alert, Spinner } from 'react-bootstrap';
import { useAuth } from './AuthContext';

const ModalComponent = Modal as any;
const ModalHeader = Modal.Header as any;
const ModalTitle = Modal.Title as any;
const ModalBody = Modal.Body as any;
const AlertComponent = Alert as any;
const ButtonComponent = Button as any;
const FormComponent = Form as any;
const FormGroup = Form.Group as any;
const FormLabel = Form.Label as any;
const FormControl = Form.Control as any;
const SpinnerComponent = Spinner as any;

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

interface LoginFormData {
  username: string;
  password: string;
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const { login } = useAuth();
  const [formData, setFormData] = useState<LoginFormData>({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const success = await login(formData.username, formData.password);
      
      if (success) {
        // Call success callback
        onSuccess();
        
        // Reset form and close modal
        setFormData({ username: '', password: '' });
        onClose();
      } else {
        setError('Invalid username or password');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({ username: '', password: '' });
    setError(null);
    onClose();
  };

  return (
    <ModalComponent show={isOpen} onHide={handleClose} centered>
      <ModalHeader closeButton>
        <ModalTitle>Login to NQBA Platform</ModalTitle>
      </ModalHeader>
      <ModalBody>
        {error && (
          <AlertComponent variant="danger" className="mb-3">
            {error}
          </AlertComponent>
        )}
        
        <FormComponent onSubmit={handleSubmit}>
          <FormGroup className="mb-3">
            <FormLabel>Username</FormLabel>
            <FormControl
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Enter your username"
              required
              disabled={loading}
            />
          </FormGroup>
          
          <FormGroup className="mb-3">
            <FormLabel>Password</FormLabel>
            <FormControl
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </FormGroup>
          
          <div className="d-grid gap-2">
            <ButtonComponent 
              variant="primary" 
              type="submit" 
              disabled={loading}
              size="lg"
            >
              {loading ? (
                <>
                  <SpinnerComponent
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                    className="me-2"
                  />
                  Logging in...
                </>
              ) : (
                'Login'
              )}
            </ButtonComponent>
          </div>
        </FormComponent>
        
        <div className="mt-3 text-center">
          <small className="text-muted">
            Demo credentials: admin / admin123
          </small>
        </div>
      </ModalBody>
    </ModalComponent>
  );
};

export default LoginModal;