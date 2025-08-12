import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  LinearProgress,
  Alert,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Divider,
} from '@mui/material';
import {
  PlayArrow,
  Stop,
  Refresh,
  Settings,
  Assessment,
  Description,
  TrendingUp,
  Warning,
  CheckCircle,
  Error,
  Add,
  Edit,
  Delete,
} from '@mui/icons-material';
import { apiService, Agent } from '../services/api';

const AgentManagement: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [showConfigDialog, setShowConfigDialog] = useState(false);
  const [showAddDialog, setShowAddDialog] = useState(false);

  const fetchAgents = async () => {
    try {
      const response = await apiService.getAgents();
      const agentsArray = Object.values(response.agents);
      setAgents(agentsArray);
    } catch (err) {
      setError('Failed to fetch agents');
      console.error('Agent fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const handleAgentAction = async (agentId: string, action: 'start' | 'stop' | 'restart') => {
    try {
      switch (action) {
        case 'start':
          await apiService.startAgent(agentId);
          break;
        case 'stop':
          await apiService.stopAgent(agentId);
          break;
        case 'restart':
          await apiService.restartAgent(agentId);
          break;
      }
      await fetchAgents();
    } catch (err) {
      setError(`Failed to ${action} agent`);
      console.error(`Agent ${action} error:`, err);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
      case 'running':
        return 'success';
      case 'idle':
        return 'default';
      case 'error':
      case 'failed':
        return 'error';
      case 'warning':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
      case 'running':
        return <CheckCircle fontSize="small" />;
      case 'error':
      case 'failed':
        return <Error fontSize="small" />;
      case 'warning':
        return <Warning fontSize="small" />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Loading agents...
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600 }}>
          Agent Management
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchAgents}
            sx={{ borderColor: '#2196f3', color: '#2196f3' }}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setShowAddDialog(true)}
            sx={{ backgroundColor: '#4caf50' }}
          >
            Add Agent
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Agent Overview Cards */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingUp sx={{ mr: 1, color: '#2196f3' }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Total Agents
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#2196f3' }}>
                {agents.length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                All registered agents
              </Typography>
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <CheckCircle sx={{ mr: 1, color: '#4caf50' }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Active Agents
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#4caf50' }}>
                {agents.filter(a => a.status === 'active').length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Currently running
              </Typography>
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Warning sx={{ mr: 1, color: '#ff9800' }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Idle Agents
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#ff9800' }}>
                {agents.filter(a => a.status === 'idle').length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Available for tasks
              </Typography>
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Error sx={{ mr: 1, color: '#f44336' }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Error Agents
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#f44336' }}>
                {agents.filter(a => a.status === 'error').length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Need attention
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Agent List */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
        <CardContent>
          <Typography variant="h6" sx={{ color: '#fff', mb: 3 }}>
            Agent Details
          </Typography>
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            {agents.map((agent) => (
              <Box sx={{ flex: '1 1 400px', minWidth: 0 }} key={agent.agent_id}>
                <Card sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#fff' }}>
                          {agent.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {agent.agent_type}
                        </Typography>
                      </Box>
                      <Chip
                        label={agent.status}
                        color={getStatusColor(agent.status) as any}
                        size="small"
                        icon={getStatusIcon(agent.status) || undefined}
                      />
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Health: {agent.health_score}%
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={agent.health_score} 
                        sx={{ mt: 0.5 }}
                      />
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Requests: {agent.total_requests} | Success: {agent.successful_requests}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Avg Response: {agent.average_response_time.toFixed(2)}s
                      </Typography>
                    </Box>

                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      <Tooltip title="Start Agent">
                        <IconButton
                          size="small"
                          onClick={() => handleAgentAction(agent.agent_id, 'start')}
                          disabled={agent.status === 'active'}
                        >
                          <PlayArrow fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Stop Agent">
                        <IconButton
                          size="small"
                          onClick={() => handleAgentAction(agent.agent_id, 'stop')}
                          disabled={agent.status === 'idle'}
                        >
                          <Stop fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Restart Agent">
                        <IconButton
                          size="small"
                          onClick={() => handleAgentAction(agent.agent_id, 'restart')}
                        >
                          <Refresh fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Configure Agent">
                        <IconButton
                          size="small"
                          onClick={() => {
                            setSelectedAgent(agent);
                            setShowConfigDialog(true);
                          }}
                        >
                          <Settings fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </Box>

                    <Typography variant="caption" color="text.secondary">
                      Last activity: {agent.last_activity ? new Date(agent.last_activity).toLocaleString() : 'Never'}
                    </Typography>
                  </CardContent>
                </Card>
              </Box>
            ))}
          </Box>
        </CardContent>
      </Card>

      {/* Configuration Dialog */}
      <Dialog 
        open={showConfigDialog} 
        onClose={() => setShowConfigDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle sx={{ backgroundColor: '#1a1a1a', color: '#fff' }}>
          Configure Agent: {selectedAgent?.name}
        </DialogTitle>
        <DialogContent sx={{ backgroundColor: '#1a1a1a', color: '#fff' }}>
          <Box sx={{ mt: 2 }}>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
              <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                <TextField
                  fullWidth
                  label="Agent Name"
                  defaultValue={selectedAgent?.name}
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
                  <InputLabel sx={{ color: '#888' }}>Agent Type</InputLabel>
                  <Select
                    defaultValue={selectedAgent?.agent_type}
                    sx={{
                      color: '#fff',
                      backgroundColor: '#2a2a2a',
                      '& .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#444',
                      },
                    }}
                  >
                    <MenuItem value="solution_architecture">Solution Architecture</MenuItem>
                    <MenuItem value="technical_architecture">Technical Architecture</MenuItem>
                    <MenuItem value="security_architecture">Security Architecture</MenuItem>
                    <MenuItem value="data_architecture">Data Architecture</MenuItem>
                    <MenuItem value="integration_architecture">Integration Architecture</MenuItem>
                    <MenuItem value="infrastructure_architecture">Infrastructure Architecture</MenuItem>
                    <MenuItem value="costing">Costing</MenuItem>
                    <MenuItem value="application_portfolio">Application Portfolio</MenuItem>
                    <MenuItem value="generic">Generic</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            </Box>
            
            <Box sx={{ mt: 2 }}>
              <FormControlLabel
                control={<Switch defaultChecked />}
                label="Enable Auto-Recovery"
                sx={{ color: '#fff' }}
              />
            </Box>
            
            <Box sx={{ mt: 1 }}>
              <FormControlLabel
                control={<Switch defaultChecked />}
                label="Enable Monitoring"
                sx={{ color: '#fff' }}
              />
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ backgroundColor: '#1a1a1a' }}>
          <Button 
            onClick={() => setShowConfigDialog(false)}
            sx={{ color: '#888' }}
          >
            Cancel
          </Button>
          <Button 
            variant="contained"
            sx={{ backgroundColor: '#2196f3' }}
          >
            Save Configuration
          </Button>
        </DialogActions>
      </Dialog>

      {/* Add Agent Dialog */}
      <Dialog 
        open={showAddDialog} 
        onClose={() => setShowAddDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle sx={{ backgroundColor: '#1a1a1a', color: '#fff' }}>
          Add New Agent
        </DialogTitle>
        <DialogContent sx={{ backgroundColor: '#1a1a1a', color: '#fff' }}>
          <Box sx={{ mt: 2 }}>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
              <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                <TextField
                  fullWidth
                  label="Agent Name"
                  placeholder="Enter agent name"
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
                  <InputLabel sx={{ color: '#888' }}>Agent Type</InputLabel>
                  <Select
                    sx={{
                      color: '#fff',
                      backgroundColor: '#2a2a2a',
                      '& .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#444',
                      },
                    }}
                  >
                    <MenuItem value="solution_architecture">Solution Architecture</MenuItem>
                    <MenuItem value="technical_architecture">Technical Architecture</MenuItem>
                    <MenuItem value="security_architecture">Security Architecture</MenuItem>
                    <MenuItem value="data_architecture">Data Architecture</MenuItem>
                    <MenuItem value="integration_architecture">Integration Architecture</MenuItem>
                    <MenuItem value="infrastructure_architecture">Infrastructure Architecture</MenuItem>
                    <MenuItem value="costing">Costing</MenuItem>
                    <MenuItem value="application_portfolio">Application Portfolio</MenuItem>
                    <MenuItem value="generic">Generic</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            </Box>
            
            <Box sx={{ mt: 2 }}>
              <TextField
                fullWidth
                label="Description"
                placeholder="Enter agent description"
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
            
            <Box sx={{ mt: 2 }}>
              <FormControlLabel
                control={<Switch defaultChecked />}
                label="Enable Auto-Recovery"
                sx={{ color: '#fff' }}
              />
            </Box>
            
            <Box sx={{ mt: 1 }}>
              <FormControlLabel
                control={<Switch defaultChecked />}
                label="Enable Monitoring"
                sx={{ color: '#fff' }}
              />
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ backgroundColor: '#1a1a1a' }}>
          <Button 
            onClick={() => setShowAddDialog(false)}
            sx={{ color: '#888' }}
          >
            Cancel
          </Button>
          <Button 
            variant="contained"
            startIcon={<Add />}
            sx={{ backgroundColor: '#4caf50' }}
          >
            Add Agent
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AgentManagement;
