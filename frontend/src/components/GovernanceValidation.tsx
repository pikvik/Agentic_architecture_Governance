import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress,
  Alert,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Divider,
} from '@mui/material';
import {
  Assessment,
  PlayArrow,
  Stop,
  Refresh,
  CheckCircle,
  Error,
  Warning,
  Schedule,
  TrendingUp,
} from '@mui/icons-material';

interface ValidationRequest {
  id: string;
  name: string;
  scope: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  startTime: string;
  endTime?: string;
  results?: any;
}

const GovernanceValidation: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [validationConfig, setValidationConfig] = useState({
    name: '',
    scope: 'comprehensive',
    priority: 'medium',
    description: '',
  });
  const [validationRequests, setValidationRequests] = useState<ValidationRequest[]>([
    {
      id: '1',
      name: 'Q1 2024 Architecture Review',
      scope: 'comprehensive',
      status: 'completed',
      progress: 100,
      startTime: '2024-01-15T10:00:00Z',
      endTime: '2024-01-15T11:30:00Z',
    },
    {
      id: '2',
      name: 'Security Architecture Audit',
      scope: 'security',
      status: 'running',
      progress: 65,
      startTime: '2024-01-15T12:00:00Z',
    },
    {
      id: '3',
      name: 'Performance Optimization Review',
      scope: 'performance',
      status: 'pending',
      progress: 0,
      startTime: '2024-01-15T14:00:00Z',
    },
  ]);

  const steps = [
    {
      label: 'Validation Scope',
      description: 'Define the scope and type of validation',
    },
    {
      label: 'Configuration',
      description: 'Set validation parameters and priorities',
    },
    {
      label: 'Review & Launch',
      description: 'Review settings and start validation',
    },
  ];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    setValidationConfig({
      name: '',
      scope: 'comprehensive',
      priority: 'medium',
      description: '',
    });
  };

  const startValidation = () => {
    const newValidation: ValidationRequest = {
      id: Date.now().toString(),
      name: validationConfig.name,
      scope: validationConfig.scope,
      status: 'running',
      progress: 0,
      startTime: new Date().toISOString(),
    };

    setValidationRequests(prev => [newValidation, ...prev]);
    handleReset();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'running':
        return 'primary';
      case 'failed':
        return 'error';
      case 'pending':
        return 'default';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle fontSize="small" />;
      case 'running':
        return <TrendingUp fontSize="small" />;
      case 'failed':
        return <Error fontSize="small" />;
      case 'pending':
        return <Schedule fontSize="small" />;
      default:
        return null;
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Governance Validation
      </Typography>

      {/* Active Validations */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333', mb: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ color: '#fff', mb: 2 }}>
            Active Validations
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 4 }}>
            {validationRequests.filter(v => v.status === 'running').map((validation) =>
              <Box sx={{ flex: '1 1 400px', minWidth: 0 }} key={validation.id}>
                <Card sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#fff' }}>
                        {validation.name}
                      </Typography>
                      <Chip
                        label={validation.status}
                        color={getStatusColor(validation.status) as any}
                        size="small"
                        icon={getStatusIcon(validation.status) || undefined}
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      Scope: {validation.scope} • Started: {new Date(validation.startTime).toLocaleString()}
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={validation.progress} 
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2" color="text.secondary">
                      {validation.progress}% complete
                    </Typography>
                  </CardContent>
                </Card>
              </Box>
            )}
          </Box>
        </CardContent>
      </Card>

      {/* Recent Validations */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333', mb: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ color: '#fff', mb: 2 }}>
            Recent Validations
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            {validationRequests.filter(v => v.status !== 'running').map((validation) =>
              <Box sx={{ flex: '1 1 400px', minWidth: 0 }} key={validation.id}>
                <Card sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#fff' }}>
                        {validation.name}
                      </Typography>
                      <Chip
                        label={validation.status}
                        color={getStatusColor(validation.status) as any}
                        size="small"
                        icon={getStatusIcon(validation.status) || undefined}
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      Scope: {validation.scope}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      Started: {new Date(validation.startTime).toLocaleString()}
                    </Typography>
                    {validation.endTime && (
                      <Typography variant="body2" color="text.secondary">
                        Completed: {new Date(validation.endTime).toLocaleString()}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Box>
            )}
          </Box>
        </CardContent>
      </Card>

      {/* New Validation Wizard */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
        <CardContent>
          <Typography variant="h6" sx={{ color: '#fff', mb: 3 }}>
            Start New Validation
          </Typography>
          
          <Stepper activeStep={activeStep} orientation="vertical">
            {steps.map((step, index) => (
              <Step key={step.label}>
                <StepLabel>
                  <Typography variant="subtitle1" sx={{ color: '#fff' }}>
                    {step.label}
                  </Typography>
                </StepLabel>
                <StepContent>
                  <Box sx={{ mb: 2 }}>
                    {index === 0 && (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                          <TextField
                            fullWidth
                            label="Validation Name"
                            value={validationConfig.name}
                            onChange={(e) => setValidationConfig({ ...validationConfig, name: e.target.value })}
                            placeholder="Enter validation name"
                            sx={{
                              '& .MuiInputBase-root': {
                                color: '#fff',
                                backgroundColor: '#2a2a2a',
                              },
                              '& .MuiOutlinedInput-notchedOutline': {
                                borderColor: '#444',
                              },
                              '& .MuiInputLabel-root': {
                                color: '#888',
                              },
                            }}
                          />
                        </Box>
                        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                          <FormControl fullWidth>
                            <InputLabel sx={{ color: '#888' }}>Validation Scope</InputLabel>
                            <Select
                              value={validationConfig.scope}
                              onChange={(e) => setValidationConfig({ ...validationConfig, scope: e.target.value })}
                              sx={{
                                color: '#fff',
                                backgroundColor: '#2a2a2a',
                                '& .MuiOutlinedInput-notchedOutline': {
                                  borderColor: '#444',
                                },
                              }}
                            >
                              <MenuItem value="comprehensive">Comprehensive</MenuItem>
                              <MenuItem value="security">Security Only</MenuItem>
                              <MenuItem value="performance">Performance Only</MenuItem>
                              <MenuItem value="compliance">Compliance Only</MenuItem>
                              <MenuItem value="cost">Cost Optimization</MenuItem>
                            </Select>
                          </FormControl>
                        </Box>
                      </Box>
                    )}
                    
                    {index === 1 && (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                          <FormControl fullWidth>
                            <InputLabel sx={{ color: '#888' }}>Priority</InputLabel>
                            <Select
                              value={validationConfig.priority}
                              onChange={(e) => setValidationConfig({ ...validationConfig, priority: e.target.value })}
                              sx={{
                                color: '#fff',
                                backgroundColor: '#2a2a2a',
                                '& .MuiOutlinedInput-notchedOutline': {
                                  borderColor: '#444',
                                },
                              }}
                            >
                              <MenuItem value="low">Low</MenuItem>
                              <MenuItem value="medium">Medium</MenuItem>
                              <MenuItem value="high">High</MenuItem>
                              <MenuItem value="critical">Critical</MenuItem>
                            </Select>
                          </FormControl>
                        </Box>
                        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                          <TextField
                            fullWidth
                            label="Description"
                            value={validationConfig.description}
                            onChange={(e) => setValidationConfig({ ...validationConfig, description: e.target.value })}
                            placeholder="Optional description"
                            multiline
                            rows={3}
                            sx={{
                              '& .MuiInputBase-root': {
                                color: '#fff',
                                backgroundColor: '#2a2a2a',
                              },
                              '& .MuiOutlinedInput-notchedOutline': {
                                borderColor: '#444',
                              },
                              '& .MuiInputLabel-root': {
                                color: '#888',
                              },
                            }}
                          />
                        </Box>
                      </Box>
                    )}
                    
                    {index === 2 && (
                      <Box>
                        <Typography variant="body1" sx={{ color: '#fff', mb: 2 }}>
                          Review your validation configuration:
                        </Typography>
                        <Box sx={{ backgroundColor: '#2a2a2a', p: 2, borderRadius: 1, mb: 2 }}>
                          <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                            <strong>Name:</strong> {validationConfig.name}
                          </Typography>
                          <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                            <strong>Scope:</strong> {validationConfig.scope}
                          </Typography>
                          <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                            <strong>Priority:</strong> {validationConfig.priority}
                          </Typography>
                          {validationConfig.description && (
                            <Typography variant="body2" sx={{ color: '#fff' }}>
                              <strong>Description:</strong> {validationConfig.description}
                            </Typography>
                          )}
                        </Box>
                      </Box>
                    )}
                  </Box>
                  
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                      variant="contained"
                      onClick={index === steps.length - 1 ? startValidation : handleNext}
                      sx={{ backgroundColor: '#2196f3' }}
                    >
                      {index === steps.length - 1 ? 'Start Validation' : 'Continue'}
                    </Button>
                    <Button
                      disabled={index === 0}
                      onClick={handleBack}
                      sx={{ color: '#888' }}
                    >
                      Back
                    </Button>
                  </Box>
                </StepContent>
              </Step>
            ))}
          </Stepper>
          
          {activeStep === steps.length && (
            <Box sx={{ mt: 2 }}>
              <Alert severity="success" sx={{ mb: 2 }}>
                All steps completed - you're finished!
              </Alert>
              <Button onClick={handleReset} sx={{ color: '#888' }}>
                Reset
              </Button>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default GovernanceValidation;
