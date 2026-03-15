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
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Assessment,
  CheckCircle,
  Error as ErrorIcon,
  Warning,
  Schedule,
  TrendingUp,
  ExpandMore,
} from '@mui/icons-material';

interface ValidationResult {
  rule_id: string;
  rule_name: string;
  rule_description: string;
  severity: string;
  status: string;
  message: string;
  recommendations: string[];
  compliance_frameworks: string[];
  domain: string;
}

interface GovernanceResult {
  request_id: string;
  status: string;
  summary: string;
  validation_results: ValidationResult[];
  risk_score: number;
  compliance_score: number;
  recommendations: string[];
  next_steps: string[];
  processing_time_seconds: number;
  agents_used: string[];
}

interface ValidationRequest {
  id: string;
  name: string;
  scope: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  startTime: string;
  endTime?: string;
  results?: GovernanceResult;
  error?: string;
}

const VALID_SCOPES = [
  { value: 'comprehensive', label: 'Comprehensive (All Agents)' },
  { value: 'solution', label: 'Solution Architecture' },
  { value: 'technical', label: 'Technical Architecture' },
  { value: 'security', label: 'Security Architecture' },
  { value: 'data', label: 'Data Architecture' },
  { value: 'integration', label: 'Integration Architecture' },
  { value: 'infrastructure', label: 'Infrastructure Architecture' },
  { value: 'costing', label: 'Cost Analysis' },
  { value: 'application_portfolio', label: 'Application Portfolio' },
];

const GovernanceValidation: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [validationConfig, setValidationConfig] = useState({
    name: '',
    scope: 'comprehensive',
    priority: 'medium',
    description: '',
    architectureContent: '',
  });
  const [validationRequests, setValidationRequests] = useState<ValidationRequest[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const steps = [
    { label: 'Validation Scope', description: 'Define the scope and type of validation' },
    { label: 'Configuration', description: 'Set validation parameters and priorities' },
    { label: 'Review & Launch', description: 'Review settings and start validation' },
  ];

  const handleNext = () => setActiveStep((prev) => prev + 1);
  const handleBack = () => setActiveStep((prev) => prev - 1);

  const handleReset = () => {
    setActiveStep(0);
    setValidationConfig({ name: '', scope: 'comprehensive', priority: 'medium', description: '', architectureContent: '' });
    setSubmitError(null);
  };

  const startValidation = async () => {
    setSubmitting(true);
    setSubmitError(null);

    const requestId = crypto.randomUUID();
    const newValidation: ValidationRequest = {
      id: requestId,
      name: validationConfig.name || `Validation ${new Date().toLocaleTimeString()}`,
      scope: validationConfig.scope,
      status: 'running',
      progress: 0,
      startTime: new Date().toISOString(),
    };

    setValidationRequests((prev) => [newValidation, ...prev]);
    handleReset();

    try {
      const payload = {
        request_id: requestId,
        scope: newValidation.scope,
        priority: validationConfig.priority,
        target_components: [],
        business_context: { name: newValidation.name, description: validationConfig.description },
        technical_context: validationConfig.architectureContent
          ? { architecture_content: validationConfig.architectureContent }
          : {},
        compliance_requirements: [],
      };

      const response = await fetch('http://localhost:8000/governance/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(String(err?.detail || `HTTP ${response.status}`));
      }

      const result: GovernanceResult = await response.json();

      setValidationRequests((prev) =>
        prev.map((v) =>
          v.id === requestId
            ? { ...v, status: 'completed', progress: 100, endTime: new Date().toISOString(), results: result }
            : v
        )
      );
    } catch (err: any) {
      const msg = err?.message || 'Unknown error';
      setSubmitError(msg);
      setValidationRequests((prev) =>
        prev.map((v) => (v.id === requestId ? { ...v, status: 'failed', error: msg } : v))
      );
    } finally {
      setSubmitting(false);
    }
  };

  const getStatusColor = (status: string): any => {
    switch (status) {
      case 'completed': case 'passed': return 'success';
      case 'running': return 'primary';
      case 'failed': case 'failed_validation': return 'error';
      case 'warning': return 'warning';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': case 'passed': return <CheckCircle fontSize="small" />;
      case 'running': return <TrendingUp fontSize="small" />;
      case 'failed': return <ErrorIcon fontSize="small" />;
      case 'warning': return <Warning fontSize="small" />;
      default: return <Schedule fontSize="small" />;
    }
  };

  const getSeverityColor = (severity: string): any => {
    switch (severity) {
      case 'critical': return 'error';
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'info';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Governance Validation
      </Typography>

      {submitError && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setSubmitError(null)}>
          Validation failed: {submitError}
        </Alert>
      )}

      {/* Active Validations */}
      {validationRequests.filter((v) => v.status === 'running').length > 0 && (
        <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333', mb: 4 }}>
          <CardContent>
            <Typography variant="h6" sx={{ color: '#fff', mb: 2 }}>Active Validations</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
              {validationRequests.filter((v) => v.status === 'running').map((v) => (
                <Box sx={{ flex: '1 1 400px', minWidth: 0 }} key={v.id}>
                  <Card sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#fff' }}>{v.name}</Typography>
                        <Chip label={v.status} color="primary" size="small" icon={<TrendingUp fontSize="small" />} />
                      </Box>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Scope: {v.scope} • Started: {new Date(v.startTime).toLocaleString()}
                      </Typography>
                      <LinearProgress sx={{ mb: 1 }} />
                      <Typography variant="body2" color="text.secondary">Processing by AI agents...</Typography>
                    </CardContent>
                  </Card>
                </Box>
              ))}
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Completed / Failed Validations */}
      {validationRequests.filter((v) => v.status !== 'running').length > 0 && (
        <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333', mb: 4 }}>
          <CardContent>
            <Typography variant="h6" sx={{ color: '#fff', mb: 2 }}>Validation Results</Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
              {validationRequests.filter((v) => v.status !== 'running').map((v) => (
                <Box key={v.id}>
                  {/* Header */}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#fff' }}>{v.name}</Typography>
                    <Chip
                      label={v.status}
                      color={getStatusColor(v.status)}
                      size="small"
                      icon={getStatusIcon(v.status) || undefined}
                    />
                  </Box>

                  {v.status === 'failed' && v.error && (
                    <Alert severity="error" sx={{ mb: 2 }}>{v.error}</Alert>
                  )}

                  {v.results && (
                    <>
                      {/* Scores */}
                      <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
                        <Card sx={{ flex: 1, minWidth: 150, backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                          <CardContent sx={{ py: 1.5, '&:last-child': { pb: 1.5 } }}>
                            <Typography variant="body2" color="text.secondary">Risk Score</Typography>
                            <Typography variant="h5" sx={{ color: v.results.risk_score > 50 ? '#f44336' : '#4caf50', fontWeight: 700 }}>
                              {v.results.risk_score.toFixed(1)}
                            </Typography>
                          </CardContent>
                        </Card>
                        <Card sx={{ flex: 1, minWidth: 150, backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                          <CardContent sx={{ py: 1.5, '&:last-child': { pb: 1.5 } }}>
                            <Typography variant="body2" color="text.secondary">Compliance Score</Typography>
                            <Typography variant="h5" sx={{ color: v.results.compliance_score >= 80 ? '#4caf50' : '#ff9800', fontWeight: 700 }}>
                              {v.results.compliance_score.toFixed(1)}
                            </Typography>
                          </CardContent>
                        </Card>
                        <Card sx={{ flex: 1, minWidth: 150, backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                          <CardContent sx={{ py: 1.5, '&:last-child': { pb: 1.5 } }}>
                            <Typography variant="body2" color="text.secondary">Agents Used</Typography>
                            <Typography variant="h5" sx={{ color: '#2196f3', fontWeight: 700 }}>
                              {v.results.agents_used.length}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Box>

                      {/* Summary */}
                      <Alert severity={v.results.risk_score > 50 ? 'warning' : 'success'} sx={{ mb: 2, whiteSpace: 'pre-line' }}>
                        {v.results.summary}
                      </Alert>

                      {/* Validation Results */}
                      {v.results.validation_results.length > 0 && (
                        <Accordion sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444', mb: 1 }}>
                          <AccordionSummary expandIcon={<ExpandMore />}>
                            <Typography sx={{ color: '#fff' }}>
                              Validation Details ({v.results.validation_results.length} checks)
                            </Typography>
                          </AccordionSummary>
                          <AccordionDetails>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                              {v.results.validation_results.map((r, i) => (
                                <Box key={i} sx={{ p: 1.5, backgroundColor: '#1a1a1a', borderRadius: 1, border: '1px solid #333' }}>
                                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                                    <Typography variant="body2" sx={{ color: '#fff', fontWeight: 600 }}>{r.rule_name}</Typography>
                                    <Box sx={{ display: 'flex', gap: 1 }}>
                                      <Chip label={r.severity} color={getSeverityColor(r.severity)} size="small" />
                                      <Chip label={r.status} color={getStatusColor(r.status)} size="small" />
                                    </Box>
                                  </Box>
                                  <Typography variant="body2" color="text.secondary">{r.message}</Typography>
                                </Box>
                              ))}
                            </Box>
                          </AccordionDetails>
                        </Accordion>
                      )}

                      {/* Recommendations */}
                      {v.results.recommendations.length > 0 && (
                        <Accordion sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444', mb: 1 }}>
                          <AccordionSummary expandIcon={<ExpandMore />}>
                            <Typography sx={{ color: '#fff' }}>Recommendations</Typography>
                          </AccordionSummary>
                          <AccordionDetails>
                            {v.results.recommendations.map((rec, i) => (
                              <Typography key={i} variant="body2" sx={{ color: '#ccc', mb: 0.5 }}>• {rec}</Typography>
                            ))}
                          </AccordionDetails>
                        </Accordion>
                      )}

                      {/* Next Steps */}
                      {v.results.next_steps.length > 0 && (
                        <Accordion sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                          <AccordionSummary expandIcon={<ExpandMore />}>
                            <Typography sx={{ color: '#fff' }}>Next Steps</Typography>
                          </AccordionSummary>
                          <AccordionDetails>
                            {v.results.next_steps.map((step, i) => (
                              <Typography key={i} variant="body2" sx={{ color: '#ccc', mb: 0.5 }}>{i + 1}. {step}</Typography>
                            ))}
                          </AccordionDetails>
                        </Accordion>
                      )}
                    </>
                  )}
                  <Divider sx={{ mt: 2, borderColor: '#333' }} />
                </Box>
              ))}
            </Box>
          </CardContent>
        </Card>
      )}

      {/* New Validation Wizard */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
        <CardContent>
          <Typography variant="h6" sx={{ color: '#fff', mb: 3 }}>Start New Validation</Typography>

          <Stepper activeStep={activeStep} orientation="vertical">
            {steps.map((step, index) => (
              <Step key={step.label}>
                <StepLabel>
                  <Typography variant="subtitle1" sx={{ color: '#fff' }}>{step.label}</Typography>
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
                            placeholder="e.g. Q1 Architecture Review"
                            sx={{ '& .MuiInputBase-root': { color: '#fff', backgroundColor: '#2a2a2a' }, '& .MuiOutlinedInput-notchedOutline': { borderColor: '#444' }, '& .MuiInputLabel-root': { color: '#888' } }}
                          />
                        </Box>
                        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                          <FormControl fullWidth>
                            <InputLabel sx={{ color: '#888' }}>Validation Scope</InputLabel>
                            <Select
                              value={validationConfig.scope}
                              onChange={(e) => setValidationConfig({ ...validationConfig, scope: e.target.value })}
                              label="Validation Scope"
                              sx={{ color: '#fff', backgroundColor: '#2a2a2a', '& .MuiOutlinedInput-notchedOutline': { borderColor: '#444' } }}
                            >
                              {VALID_SCOPES.map((s) => (
                                <MenuItem key={s.value} value={s.value}>{s.label}</MenuItem>
                              ))}
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
                              label="Priority"
                              sx={{ color: '#fff', backgroundColor: '#2a2a2a', '& .MuiOutlinedInput-notchedOutline': { borderColor: '#444' } }}
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
                            sx={{ '& .MuiInputBase-root': { color: '#fff', backgroundColor: '#2a2a2a' }, '& .MuiOutlinedInput-notchedOutline': { borderColor: '#444' }, '& .MuiInputLabel-root': { color: '#888' } }}
                          />
                        </Box>
                        <Box sx={{ flex: '1 1 100%', minWidth: 0 }}>
                          <TextField
                            fullWidth
                            label="Architecture Content (paste document text or describe your architecture)"
                            value={validationConfig.architectureContent}
                            onChange={(e) => setValidationConfig({ ...validationConfig, architectureContent: e.target.value })}
                            placeholder="Paste architecture document content, system description, or key components here..."
                            multiline
                            rows={5}
                            sx={{ '& .MuiInputBase-root': { color: '#fff', backgroundColor: '#2a2a2a' }, '& .MuiOutlinedInput-notchedOutline': { borderColor: '#444' }, '& .MuiInputLabel-root': { color: '#888' } }}
                          />
                        </Box>
                      </Box>
                    )}

                    {index === 2 && (
                      <Box>
                        <Typography variant="body1" sx={{ color: '#fff', mb: 2 }}>Review your validation configuration:</Typography>
                        <Box sx={{ backgroundColor: '#2a2a2a', p: 2, borderRadius: 1, mb: 2 }}>
                          <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}><strong>Name:</strong> {validationConfig.name || '(auto-generated)'}</Typography>
                          <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}><strong>Scope:</strong> {VALID_SCOPES.find(s => s.value === validationConfig.scope)?.label}</Typography>
                          <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}><strong>Priority:</strong> {validationConfig.priority}</Typography>
                          {validationConfig.description && <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}><strong>Description:</strong> {validationConfig.description}</Typography>}
                          {validationConfig.architectureContent && <Typography variant="body2" sx={{ color: '#fff' }}><strong>Architecture content:</strong> {validationConfig.architectureContent.length} characters provided</Typography>}
                        </Box>
                      </Box>
                    )}
                  </Box>

                  <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                    <Button
                      variant="contained"
                      onClick={index === steps.length - 1 ? startValidation : handleNext}
                      disabled={submitting}
                      sx={{ backgroundColor: '#2196f3' }}
                      startIcon={submitting && index === steps.length - 1 ? <CircularProgress size={16} color="inherit" /> : undefined}
                    >
                      {index === steps.length - 1 ? (submitting ? 'Running...' : 'Start Validation') : 'Continue'}
                    </Button>
                    <Button disabled={index === 0} onClick={handleBack} sx={{ color: '#888' }}>Back</Button>
                  </Box>
                </StepContent>
              </Step>
            ))}
          </Stepper>

          {activeStep === steps.length && (
            <Box sx={{ mt: 2 }}>
              <Alert severity="success" sx={{ mb: 2 }}>Validation submitted — check results above.</Alert>
              <Button onClick={handleReset} sx={{ color: '#888' }}>Start Another</Button>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default GovernanceValidation;
