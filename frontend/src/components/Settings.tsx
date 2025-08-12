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
  Switch,
  FormControlLabel,
  Divider,
  Alert,
} from '@mui/material';
import {
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Security as SecurityIcon,
  Settings as SettingsIcon,
  Notifications as NotificationsIcon,
  Storage as StorageIcon,
} from '@mui/icons-material';

const Settings: React.FC = () => {
  const [settings, setSettings] = useState({
    system: {
      maxConcurrentAgents: 50,
      agentTimeout: 300,
      batchSize: 10,
      debugMode: false,
      logLevel: 'INFO',
    },
    security: {
      enableEncryption: true,
      enableAuditLogging: true,
      sessionTimeout: 3600,
      maxLoginAttempts: 5,
    },
    notifications: {
      emailNotifications: true,
      slackNotifications: false,
      validationAlerts: true,
      systemAlerts: true,
    },
    storage: {
      maxReportSize: 100,
      retentionDays: 90,
      backupEnabled: true,
      compressionEnabled: true,
    },
  });

  const handleSave = () => {
    // Save settings logic
    console.log('Saving settings:', settings);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ color: '#fff', fontWeight: 'bold' }}>
          System Settings
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            sx={{ color: '#2196f3', borderColor: '#2196f3' }}
          >
            Reset to Defaults
          </Button>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            sx={{ backgroundColor: '#4caf50' }}
          >
            Save Settings
          </Button>
        </Box>
      </Box>

      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        {/* System Settings */}
        <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SettingsIcon sx={{ color: '#2196f3', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  System Configuration
                </Typography>
              </Box>
              <Divider sx={{ mb: 2, borderColor: '#333' }} />
              
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
                  <TextField
                    fullWidth
                    label="Max Concurrent Agents"
                    type="number"
                    value={settings.system.maxConcurrentAgents}
                    onChange={(e) => setSettings({
                      ...settings,
                      system: {
                        ...settings.system,
                        maxConcurrentAgents: parseInt(e.target.value) || 50
                      }
                    })}
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
                <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
                  <TextField
                    fullWidth
                    label="Agent Timeout (seconds)"
                    type="number"
                    value={settings.system.agentTimeout}
                    onChange={(e) => setSettings({
                      ...settings,
                      system: {
                        ...settings.system,
                        agentTimeout: parseInt(e.target.value) || 300
                      }
                    })}
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
                <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
                  <TextField
                    fullWidth
                    label="Batch Size"
                    type="number"
                    value={settings.system.batchSize}
                    onChange={(e) => setSettings({
                      ...settings,
                      system: {
                        ...settings.system,
                        batchSize: parseInt(e.target.value) || 10
                      }
                    })}
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
                <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
                  <FormControl fullWidth>
                    <InputLabel sx={{ color: '#888' }}>Log Level</InputLabel>
                    <Select
                      value={settings.system.logLevel}
                      onChange={(e) => setSettings({
                        ...settings,
                        system: {
                          ...settings.system,
                          logLevel: e.target.value
                        }
                      })}
                      sx={{
                        color: '#fff',
                        backgroundColor: '#2a2a2a',
                        '& .MuiOutlinedInput-notchedOutline': {
                          borderColor: '#444',
                        },
                      }}
                    >
                      <MenuItem value="DEBUG">DEBUG</MenuItem>
                      <MenuItem value="INFO">INFO</MenuItem>
                      <MenuItem value="WARNING">WARNING</MenuItem>
                      <MenuItem value="ERROR">ERROR</MenuItem>
                    </Select>
                  </FormControl>
                </Box>
              </Box>
              
              <Box sx={{ mt: 2 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.system.debugMode}
                      onChange={(e) => setSettings({
                        ...settings,
                        system: {
                          ...settings.system,
                          debugMode: e.target.checked
                        }
                      })}
                    />
                  }
                  label="Debug Mode"
                  sx={{ color: '#fff' }}
                />
              </Box>
            </CardContent>
          </Card>
        </Box>

        {/* Security Settings */}
        <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SecurityIcon sx={{ color: '#f44336', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Security Settings
                </Typography>
              </Box>
              <Divider sx={{ mb: 2, borderColor: '#333' }} />
              
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
                  <TextField
                    fullWidth
                    label="Session Timeout (seconds)"
                    type="number"
                    value={settings.security.sessionTimeout}
                    onChange={(e) => setSettings({
                      ...settings,
                      security: {
                        ...settings.security,
                        sessionTimeout: parseInt(e.target.value) || 3600
                      }
                    })}
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
                <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
                  <TextField
                    fullWidth
                    label="Max Login Attempts"
                    type="number"
                    value={settings.security.maxLoginAttempts}
                    onChange={(e) => setSettings({
                      ...settings,
                      security: {
                        ...settings.security,
                        maxLoginAttempts: parseInt(e.target.value) || 5
                      }
                    })}
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
              
              <Box sx={{ mt: 2 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.security.enableEncryption}
                      onChange={(e) => setSettings({
                        ...settings,
                        security: {
                          ...settings.security,
                          enableEncryption: e.target.checked
                        }
                      })}
                    />
                  }
                  label="Enable Encryption"
                  sx={{ color: '#fff' }}
                />
              </Box>
              
              <Box sx={{ mt: 1 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.security.enableAuditLogging}
                      onChange={(e) => setSettings({
                        ...settings,
                        security: {
                          ...settings.security,
                          enableAuditLogging: e.target.checked
                        }
                      })}
                    />
                  }
                  label="Enable Audit Logging"
                  sx={{ color: '#fff' }}
                />
              </Box>
            </CardContent>
          </Card>
        </Box>

        {/* Notification Settings */}
        <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <NotificationsIcon sx={{ color: '#ff9800', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Notification Settings
                </Typography>
              </Box>
              <Divider sx={{ mb: 2, borderColor: '#333' }} />
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.emailNotifications}
                      onChange={(e) => setSettings({
                        ...settings,
                        notifications: {
                          ...settings.notifications,
                          emailNotifications: e.target.checked
                        }
                      })}
                    />
                  }
                  label="Email Notifications"
                  sx={{ color: '#fff' }}
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.slackNotifications}
                      onChange={(e) => setSettings({
                        ...settings,
                        notifications: {
                          ...settings.notifications,
                          slackNotifications: e.target.checked
                        }
                      })}
                    />
                  }
                  label="Slack Notifications"
                  sx={{ color: '#fff' }}
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.validationAlerts}
                      onChange={(e) => setSettings({
                        ...settings,
                        notifications: {
                          ...settings.notifications,
                          validationAlerts: e.target.checked
                        }
                      })}
                    />
                  }
                  label="Validation Alerts"
                  sx={{ color: '#fff' }}
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.systemAlerts}
                      onChange={(e) => setSettings({
                        ...settings,
                        notifications: {
                          ...settings.notifications,
                          systemAlerts: e.target.checked
                        }
                      })}
                    />
                  }
                  label="System Alerts"
                  sx={{ color: '#fff' }}
                />
              </Box>
            </CardContent>
          </Card>
        </Box>

        {/* Storage Settings */}
        <Box sx={{ flex: '1 1 400px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <StorageIcon sx={{ color: '#9c27b0', mr: 1 }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Storage Settings
                </Typography>
              </Box>
              <Divider sx={{ mb: 2, borderColor: '#333' }} />
              
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
                  <TextField
                    fullWidth
                    label="Max Report Size (MB)"
                    type="number"
                    value={settings.storage.maxReportSize}
                    onChange={(e) => setSettings({
                      ...settings,
                      storage: {
                        ...settings.storage,
                        maxReportSize: parseInt(e.target.value) || 100
                      }
                    })}
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
                <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
                  <TextField
                    fullWidth
                    label="Retention Days"
                    type="number"
                    value={settings.storage.retentionDays}
                    onChange={(e) => setSettings({
                      ...settings,
                      storage: {
                        ...settings.storage,
                        retentionDays: parseInt(e.target.value) || 90
                      }
                    })}
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
              
              <Box sx={{ mt: 2 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.storage.backupEnabled}
                      onChange={(e) => setSettings({
                        ...settings,
                        storage: {
                          ...settings.storage,
                          backupEnabled: e.target.checked
                        }
                      })}
                    />
                  }
                  label="Enable Backup"
                  sx={{ color: '#fff' }}
                />
              </Box>
              
              <Box sx={{ mt: 1 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.storage.compressionEnabled}
                      onChange={(e) => setSettings({
                        ...settings,
                        storage: {
                          ...settings.storage,
                          compressionEnabled: e.target.checked
                        }
                      })}
                    />
                  }
                  label="Enable Compression"
                  sx={{ color: '#fff' }}
                />
              </Box>
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Save Alert */}
      <Box sx={{ mt: 3 }}>
        <Alert severity="info" sx={{ backgroundColor: '#1a1a1a', color: '#fff', border: '1px solid #333' }}>
          Changes will be applied immediately. Some settings may require a system restart to take effect.
        </Alert>
      </Box>
    </Box>
  );
};

export default Settings;
