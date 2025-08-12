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
} from '@mui/icons-material';
import { apiService, SwarmStatus, Agent } from '../services/api';

const Dashboard: React.FC = () => {
  const [swarmStatus, setSwarmStatus] = useState<SwarmStatus | null>(null);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      setError(null);
      const [statusData, agentsData] = await Promise.all([
        apiService.getSwarmStatus(),
        apiService.getAgents(),
      ]);
      setSwarmStatus(statusData);
      
      // Convert agents object to array
      const agentsArray = Object.values(agentsData.agents);
      setAgents(agentsArray);
    } catch (err) {
      setError('Failed to fetch system data. Please check if the backend is running.');
      console.error('Dashboard fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

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
      // Refresh data after action
      await fetchData();
    } catch (err) {
      setError(`Failed to ${action} agent. Please try again.`);
      console.error(`Agent ${action} error:`, err);
    }
  };

  useEffect(() => {
    fetchData();
    // Set up auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

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
          Loading system data...
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 600 }}>
          System Dashboard
        </Typography>
        <Box>
          <Tooltip title="Refresh Data">
            <IconButton onClick={handleRefresh} disabled={refreshing}>
              <Refresh />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* System Overview */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUp sx={{ mr: 1, color: '#2196f3' }} />
                <Typography variant="h6">Total Agents</Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#2196f3' }}>
                {swarmStatus?.total_agents || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {agents.filter(a => a.status === 'active').length} active
              </Typography>
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <CheckCircle sx={{ mr: 1, color: '#4caf50' }} />
                <Typography variant="h6">System Health</Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#4caf50' }}>
                {swarmStatus?.overall_health || 0}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={swarmStatus?.overall_health || 0} 
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Assessment sx={{ mr: 1, color: '#ff9800' }} />
                <Typography variant="h6">Active Tasks</Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#ff9800' }}>
                {swarmStatus?.active_tasks || 0}
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
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Description sx={{ mr: 1, color: '#9c27b0' }} />
                <Typography variant="h6">Core Brain</Typography>
              </Box>
              <Chip 
                label={swarmStatus?.core_brain?.status || 'Unknown'} 
                color={swarmStatus?.core_brain?.status === 'active' ? 'success' : 'default'}
                size="small"
              />
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Quick Actions */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333', mb: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Quick Actions
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            <Button
              variant="contained"
              startIcon={<Assessment />}
              sx={{ backgroundColor: '#2196f3' }}
            >
              Start Validation
            </Button>
            <Button
              variant="outlined"
              startIcon={<Description />}
              sx={{ borderColor: '#4caf50', color: '#4caf50' }}
            >
              Generate Report
            </Button>
            <Button
              variant="outlined"
              startIcon={<Settings />}
              sx={{ borderColor: '#ff9800', color: '#ff9800' }}
            >
              Manage Agents
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* Agent Status Grid */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3 }}>
            Agent Status
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            {agents.map((agent) => (
              <Box sx={{ flex: '1 1 350px', minWidth: 0 }} key={agent.agent_id}>
                <Card sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
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
    </Box>
  );
};

export default Dashboard;
