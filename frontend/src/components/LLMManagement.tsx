import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Chip,
  Alert,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Psychology,
  Cloud,
  Computer,
  CheckCircle,
  Error,
  Refresh,
  PlayArrow,
  Stop,
  Settings,
  ExpandMore,
  Download,
  Chat,
  Send,
} from '@mui/icons-material';

interface LLMHealth {
  dify: {
    status: string;
    base_url: string;
  };
  ollama: {
    status: string;
    base_url: string;
    default_model: string;
  };
  overall_status: string;
}

interface OllamaModel {
  name: string;
  size: number;
  modified_at: string;
  digest: string;
}

interface DifyWorkspace {
  id: string;
  name: string;
  created_at: string;
}

interface DifyApplication {
  id: string;
  name: string;
  type: string;
  created_at: string;
}

const LLMManagement: React.FC = () => {
  const [health, setHealth] = useState<LLMHealth | null>(null);
  const [ollamaModels, setOllamaModels] = useState<OllamaModel[]>([]);
  const [difyWorkspaces, setDifyWorkspaces] = useState<DifyWorkspace[]>([]);
  const [difyApplications, setDifyApplications] = useState<DifyApplication[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Chat state
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<Array<{role: string; content: string}>>([]);
  const [chatInput, setChatInput] = useState('');
  const [selectedLLM, setSelectedLLM] = useState<'ollama' | 'dify'>('ollama');
  const [selectedModel, setSelectedModel] = useState('');
  
  // Model pull state
  const [pullDialogOpen, setPullDialogOpen] = useState(false);
  const [newModelName, setNewModelName] = useState('');

  useEffect(() => {
    loadHealthStatus();
    loadOllamaModels();
    loadDifyData();
  }, []);

  const loadHealthStatus = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/llm/health');
      if (response.ok) {
        const data = await response.json();
        setHealth(data);
      } else {
        setError('Failed to load health status');
      }
    } catch (err) {
      setError('Error loading health status');
    } finally {
      setLoading(false);
    }
  };

  const loadOllamaModels = async () => {
    try {
      const response = await fetch('http://localhost:8000/llm/ollama/models');
      if (response.ok) {
        const data = await response.json();
        setOllamaModels(data.models || []);
      }
    } catch (err) {
      console.error('Failed to load Ollama models:', err);
    }
  };

  const loadDifyData = async () => {
    try {
      // Load workspaces
      const workspacesResponse = await fetch('http://localhost:8000/llm/dify/workspaces');
      if (workspacesResponse.ok) {
        const workspacesData = await workspacesResponse.json();
        setDifyWorkspaces(workspacesData.workspaces || []);
      }

      // Load applications
      const applicationsResponse = await fetch('http://localhost:8000/llm/dify/applications');
      if (applicationsResponse.ok) {
        const applicationsData = await applicationsResponse.json();
        setDifyApplications(applicationsData.applications || []);
      }
    } catch (err) {
      console.error('Failed to load Dify data:', err);
    }
  };

  const pullModel = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/llm/ollama/pull', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model: newModelName }),
      });

      if (response.ok) {
        setPullDialogOpen(false);
        setNewModelName('');
        loadOllamaModels(); // Refresh models list
      } else {
        setError('Failed to pull model');
      }
    } catch (err) {
      setError('Error pulling model');
    } finally {
      setLoading(false);
    }
  };

  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;

    const newMessage = { role: 'user', content: chatInput };
    setChatMessages(prev => [...prev, newMessage]);
    setChatInput('');

    try {
      let response;
      if (selectedLLM === 'ollama') {
        response = await fetch('http://localhost:8000/llm/ollama/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            messages: [...chatMessages, newMessage],
            model: selectedModel || undefined,
          }),
        });
      } else {
        response = await fetch('http://localhost:8000/llm/dify/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            messages: [...chatMessages, newMessage],
            app_id: selectedModel || undefined,
          }),
        });
      }

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setChatMessages(prev => [...prev, data.message]);
        }
      }
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  };

  const getStatusColor = (status: string) => {
    return status === 'healthy' ? 'success' : 'error';
  };

  const getStatusIcon = (status: string) => {
    return status === 'healthy' ? <CheckCircle /> : <Error />;
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 3, fontWeight: 600 }}>
        LLM Management
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Health Status */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333', mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" sx={{ color: '#fff' }}>
              Service Health
            </Typography>
            <Button
              startIcon={<Refresh />}
              onClick={loadHealthStatus}
              disabled={loading}
              sx={{ color: '#2196f3' }}
            >
              Refresh
            </Button>
          </Box>
          
          {health && (
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                <Card sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Cloud sx={{ color: '#2196f3', mr: 1 }} />
                      <Typography variant="h6" sx={{ color: '#fff' }}>
                        Dify
                      </Typography>
                    </Box>
                    <Chip
                      label={health.dify.status}
                      color={getStatusColor(health.dify.status) as any}
                      icon={getStatusIcon(health.dify.status)}
                      size="small"
                    />
                    <Typography variant="body2" sx={{ color: '#888', mt: 1 }}>
                      {health.dify.base_url}
                    </Typography>
                  </CardContent>
                </Card>
              </Box>
              
              <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                <Card sx={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Computer sx={{ color: '#4caf50', mr: 1 }} />
                      <Typography variant="h6" sx={{ color: '#fff' }}>
                        Ollama
                      </Typography>
                    </Box>
                    <Chip
                      label={health.ollama.status}
                      color={getStatusColor(health.ollama.status) as any}
                      icon={getStatusIcon(health.ollama.status)}
                      size="small"
                    />
                    <Typography variant="body2" sx={{ color: '#888', mt: 1 }}>
                      {health.ollama.base_url}
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#888' }}>
                      Default: {health.ollama.default_model}
                    </Typography>
                  </CardContent>
                </Card>
              </Box>
            </Box>
          )}
        </CardContent>
      </Card>

      <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap', mt: 3 }}>
        {/* Ollama Management */}
        <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Ollama Models
                </Typography>
                <Button
                  startIcon={<Download />}
                  onClick={() => setPullDialogOpen(true)}
                  sx={{ color: '#4caf50' }}
                >
                  Pull Model
                </Button>
              </Box>
              
              <List>
                {ollamaModels.map((model) => (
                  <ListItem key={model.name} sx={{ backgroundColor: '#2a2a2a', mb: 1, borderRadius: 1 }}>
                    <ListItemText
                      primary={model.name}
                      secondary={`Size: ${(model.size / 1024 / 1024 / 1024).toFixed(2)} GB`}
                      sx={{ color: '#fff' }}
                    />
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        onClick={() => {
                          setSelectedLLM('ollama');
                          setSelectedModel(model.name);
                          setChatOpen(true);
                        }}
                        sx={{ color: '#2196f3' }}
                      >
                        <Chat />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Box>

        {/* Dify Management */}
        <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Typography variant="h6" sx={{ color: '#fff', mb: 2 }}>
                Dify Applications
              </Typography>
              
              <List>
                {difyApplications.map((app) => (
                  <ListItem key={app.id} sx={{ backgroundColor: '#2a2a2a', mb: 1, borderRadius: 1 }}>
                    <ListItemText
                      primary={app.name}
                      secondary={`Type: ${app.type}`}
                      sx={{ color: '#fff' }}
                    />
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        onClick={() => {
                          setSelectedLLM('dify');
                          setSelectedModel(app.id);
                          setChatOpen(true);
                        }}
                        sx={{ color: '#2196f3' }}
                      >
                        <Chat />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Chat Dialog */}
      <Dialog
        open={chatOpen}
        onClose={() => setChatOpen(false)}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: { backgroundColor: '#1a1a1a', color: '#fff' }
        }}
      >
        <DialogTitle>
          Chat with {selectedLLM === 'ollama' ? 'Ollama' : 'Dify'} - {selectedModel}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ height: 400, overflowY: 'auto', mb: 2, p: 2, backgroundColor: '#2a2a2a', borderRadius: 1 }}>
            {chatMessages.map((msg, index) => (
              <Box key={index} sx={{ mb: 2 }}>
                <Typography variant="caption" sx={{ color: '#888' }}>
                  {msg.role}
                </Typography>
                <Typography variant="body2" sx={{ color: '#fff' }}>
                  {msg.content}
                </Typography>
              </Box>
            ))}
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Type your message..."
              onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
              sx={{
                '& .MuiInputBase-root': {
                  color: '#fff',
                  backgroundColor: '#2a2a2a',
                },
                '& .MuiOutlinedInput-notchedOutline': {
                  borderColor: '#444',
                },
              }}
            />
            <Button
              variant="contained"
              onClick={sendChatMessage}
              startIcon={<Send />}
              sx={{ backgroundColor: '#2196f3' }}
            >
              Send
            </Button>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setChatOpen(false)} sx={{ color: '#888' }}>
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Pull Model Dialog */}
      <Dialog
        open={pullDialogOpen}
        onClose={() => setPullDialogOpen(false)}
        PaperProps={{
          sx: { backgroundColor: '#1a1a1a', color: '#fff' }
        }}
      >
        <DialogTitle>Pull Ollama Model</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Model Name"
            value={newModelName}
            onChange={(e) => setNewModelName(e.target.value)}
            placeholder="e.g., llama2, codellama, mistral"
            sx={{
              mt: 2,
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
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPullDialogOpen(false)} sx={{ color: '#888' }}>
            Cancel
          </Button>
          <Button
            onClick={pullModel}
            disabled={!newModelName.trim() || loading}
            sx={{ backgroundColor: '#4caf50' }}
          >
            Pull
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default LLMManagement;
