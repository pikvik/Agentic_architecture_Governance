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
  Alert,
  Divider,
} from '@mui/material';
import {
  Description,
  Download,
  TrendingUp,
  Assessment,
  Schedule,
} from '@mui/icons-material';

const Reports: React.FC = () => {
  const [reportConfig, setReportConfig] = useState({
    name: '',
    type: 'governance',
    format: 'pdf',
    dateRange: '7d',
  });

  const [reports] = useState([
    {
      id: 1,
      name: 'Architecture Governance Report - Q1 2024',
      type: 'governance',
      format: 'pdf',
      status: 'completed',
      createdAt: '2024-01-15',
      size: '2.3 MB',
    },
    {
      id: 2,
      name: 'Security Assessment Report',
      type: 'security',
      format: 'pdf',
      status: 'completed',
      createdAt: '2024-01-10',
      size: '1.8 MB',
    },
    {
      id: 3,
      name: 'Performance Analysis Report',
      type: 'performance',
      format: 'excel',
      status: 'in_progress',
      createdAt: '2024-01-12',
      size: '0.5 MB',
    },
  ]);

  const metrics = {
    totalReports: 156,
    completedReports: 142,
    pendingReports: 14,
    averageGenerationTime: '2.3 min',
  };

  const handleGenerateReport = () => {
    // Report generation logic
    console.log('Generating report:', reportConfig);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'in_progress':
        return 'warning';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600 }}>
          Reports & Analytics
        </Typography>
        <Button
          variant="contained"
          startIcon={<Description />}
          sx={{ backgroundColor: '#2196f3' }}
        >
          Generate New Report
        </Button>
      </Box>

      {/* Metrics Cards */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Description sx={{ mr: 1, color: '#2196f3' }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Total Reports
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#2196f3' }}>
                {metrics.totalReports}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                All time reports generated
              </Typography>
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingUp sx={{ mr: 1, color: '#4caf50' }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Completed
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#4caf50' }}>
                {metrics.completedReports}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Successfully generated
              </Typography>
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Schedule sx={{ mr: 1, color: '#ff9800' }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Pending
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#ff9800' }}>
                {metrics.pendingReports}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                In queue or processing
              </Typography>
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
          <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Assessment sx={{ mr: 1, color: '#9c27b0' }} />
                <Typography variant="h6" sx={{ color: '#fff' }}>
                  Avg Time
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, color: '#9c27b0' }}>
                {metrics.averageGenerationTime}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Per report generation
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Report Generation */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333', mb: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ color: '#fff', mb: 2 }}>
            Generate New Report
          </Typography>
          <Divider sx={{ mb: 2, borderColor: '#333' }} />
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
              <TextField
                fullWidth
                label="Report Name"
                value={reportConfig.name}
                onChange={(e) => setReportConfig({ ...reportConfig, name: e.target.value })}
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
                <InputLabel sx={{ color: '#888' }}>Report Type</InputLabel>
                <Select
                  value={reportConfig.type}
                  onChange={(e) => setReportConfig({ ...reportConfig, type: e.target.value })}
                  sx={{
                    color: '#fff',
                    backgroundColor: '#2a2a2a',
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#444',
                    },
                  }}
                >
                  <MenuItem value="governance">Governance</MenuItem>
                  <MenuItem value="security">Security</MenuItem>
                  <MenuItem value="performance">Performance</MenuItem>
                  <MenuItem value="compliance">Compliance</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
              <FormControl fullWidth>
                <InputLabel sx={{ color: '#888' }}>Format</InputLabel>
                <Select
                  value={reportConfig.format}
                  onChange={(e) => setReportConfig({ ...reportConfig, format: e.target.value })}
                  sx={{
                    color: '#fff',
                    backgroundColor: '#2a2a2a',
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#444',
                    },
                  }}
                >
                  <MenuItem value="pdf">PDF</MenuItem>
                  <MenuItem value="excel">Excel</MenuItem>
                  <MenuItem value="csv">CSV</MenuItem>
                  <MenuItem value="json">JSON</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <Box sx={{ flex: '1 1 200px', minWidth: 0 }}>
              <FormControl fullWidth>
                <InputLabel sx={{ color: '#888' }}>Date Range</InputLabel>
                <Select
                  value={reportConfig.dateRange}
                  onChange={(e) => setReportConfig({ ...reportConfig, dateRange: e.target.value })}
                  sx={{
                    color: '#fff',
                    backgroundColor: '#2a2a2a',
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#444',
                    },
                  }}
                >
                  <MenuItem value="1d">Last 24 Hours</MenuItem>
                  <MenuItem value="7d">Last 7 Days</MenuItem>
                  <MenuItem value="30d">Last 30 Days</MenuItem>
                  <MenuItem value="90d">Last 90 Days</MenuItem>
                </Select>
              </FormControl>
            </Box>
          </Box>
          
          <Box sx={{ mt: 2 }}>
            <Button
              variant="contained"
              onClick={handleGenerateReport}
              disabled={!reportConfig.name}
              sx={{ backgroundColor: '#4caf50' }}
            >
              Generate Report
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* Recent Reports */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
        <CardContent>
          <Typography variant="h6" sx={{ color: '#fff', mb: 2 }}>
            Recent Reports
          </Typography>
          <Divider sx={{ mb: 2, borderColor: '#333' }} />
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {reports.map((report) => (
              <Box
                key={report.id}
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  p: 2,
                  backgroundColor: '#2a2a2a',
                  borderRadius: 1,
                  border: '1px solid #444',
                }}
              >
                <Box>
                  <Typography variant="subtitle1" sx={{ color: '#fff', fontWeight: 600 }}>
                    {report.name}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                    <Chip
                      label={report.type}
                      size="small"
                      sx={{ backgroundColor: '#333', color: '#fff' }}
                    />
                    <Chip
                      label={report.format.toUpperCase()}
                      size="small"
                      sx={{ backgroundColor: '#333', color: '#fff' }}
                    />
                    <Chip
                      label={report.status}
                      color={getStatusColor(report.status) as any}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                    Created: {report.createdAt} | Size: {report.size}
                  </Typography>
                </Box>
                
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<Download />}
                    sx={{ borderColor: '#2196f3', color: '#2196f3' }}
                  >
                    Download
                  </Button>
                </Box>
              </Box>
            ))}
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Reports;
