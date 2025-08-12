import React, { useState, useCallback } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Alert,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  CloudUpload,
  Description,
  Image,
  PictureAsPdf,
  Slideshow,
  Delete,
  CheckCircle,
  Error,
  Upload,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import { apiService } from '../services/api';

interface FileUploadProps {
  onFileUploaded?: (fileId: string) => void;
}

interface UploadedFile {
  file_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  status: string;
  progress?: number;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUploaded }) => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [architectureDomain, setArchitectureDomain] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [projectId, setProjectId] = useState<string>('');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setError(null);
    setUploading(true);

    const newFiles: UploadedFile[] = [];

    for (const file of acceptedFiles) {
      try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);
        
        if (architectureDomain) {
          formData.append('architecture_domain', architectureDomain);
        }
        if (description) {
          formData.append('description', description);
        }
        if (projectId) {
          formData.append('project_id', projectId);
        }

        // Upload file
        const response = await fetch('http://localhost:8000/files/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          const uploadedFile: UploadedFile = {
            file_id: result.file_id,
            filename: result.filename,
            file_type: result.file_type,
            file_size: result.file_size,
            status: result.status,
            progress: 0,
          };

          newFiles.push(uploadedFile);
          
          // Call callback if provided
          if (onFileUploaded) {
            onFileUploaded(result.file_id);
          }
        } else {
          const errorData = await response.json();
          // @ts-ignore
          throw new Error(errorData.detail || 'Upload failed');
        }
              } catch (err: any) {
          console.error('Upload error:', err);
          setError(`Failed to upload ${file.name}: ${err?.message || 'Unknown error'}`);
        }
    }

    setUploadedFiles(prev => [...prev, ...newFiles]);
    setUploading(false);
  }, [architectureDomain, description, projectId, onFileUploaded]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
    },
    multiple: true,
  });

  const getFileIcon = (fileType: string) => {
    switch (fileType.toLowerCase()) {
      case 'pdf':
        return <PictureAsPdf fontSize="small" />;
      case 'docx':
        return <Description fontSize="small" />;
      case 'pptx':
        return <Slideshow fontSize="small" />;
      case 'png':
      case 'jpg':
      case 'jpeg':
      case 'gif':
      case 'bmp':
        return <Image fontSize="small" />;
      default:
        return <Upload fontSize="small" />;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const removeFile = (fileId: string) => {
    setUploadedFiles(prev => prev.filter(file => file.file_id !== fileId));
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" component="h2" sx={{ mb: 3, fontWeight: 600 }}>
        Upload Architecture Files
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Upload Configuration */}
      <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333', mb: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Upload Configuration
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
              <FormControl fullWidth>
                <InputLabel>Architecture Domain</InputLabel>
                <Select
                  value={architectureDomain}
                  onChange={(e) => setArchitectureDomain(e.target.value)}
                  label="Architecture Domain"
                  sx={{
                    color: '#fff',
                    backgroundColor: '#2a2a2a',
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: '#444',
                    },
                  }}
                >
                  <MenuItem value="solution">Solution Architecture</MenuItem>
                  <MenuItem value="technical">Technical Architecture</MenuItem>
                  <MenuItem value="security">Security Architecture</MenuItem>
                  <MenuItem value="data">Data Architecture</MenuItem>
                  <MenuItem value="integration">Integration Architecture</MenuItem>
                  <MenuItem value="infrastructure">Infrastructure Architecture</MenuItem>
                  <MenuItem value="application">Application Architecture</MenuItem>
                  <MenuItem value="business">Business Architecture</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
              <TextField
                fullWidth
                label="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Brief description of the file"
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
              <TextField
                fullWidth
                label="Project ID"
                value={projectId}
                onChange={(e) => setProjectId(e.target.value)}
                placeholder="Optional project identifier"
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
        </CardContent>
      </Card>

      {/* File Upload Area */}
      <Card 
        {...getRootProps()} 
        sx={{ 
          backgroundColor: '#1a1a1a', 
          border: '2px dashed',
          borderColor: isDragActive ? '#2196f3' : '#333',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: '#2196f3',
            backgroundColor: '#2a2a2a',
          },
          mb: 3
        }}
      >
        <input {...getInputProps()} />
        <CardContent sx={{ textAlign: 'center', py: 4 }}>
          <CloudUpload sx={{ fontSize: 64, color: '#2196f3', mb: 2 }} />
          <Typography variant="h6" sx={{ mb: 1 }}>
            {isDragActive ? 'Drop files here' : 'Drag & drop files here'}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            or click to select files
          </Typography>
          <Button
            variant="outlined"
            startIcon={<Upload />}
            sx={{ borderColor: '#2196f3', color: '#2196f3' }}
          >
            Select Files
          </Button>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Supported formats: PDF, DOCX, PPTX, PNG, JPG, JPEG, GIF, BMP
            </Typography>
          </Box>
        </CardContent>
      </Card>

      {/* Upload Progress */}
      {uploading && (
        <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333', mb: 3 }}>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Uploading Files...
            </Typography>
            <LinearProgress sx={{ mb: 1 }} />
            <Typography variant="body2" color="text.secondary">
              Please wait while files are being processed
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <Card sx={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Uploaded Files ({uploadedFiles.length})
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {uploadedFiles.map((file) => (
                <Box
                  key={file.file_id}
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
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    {getFileIcon(file.file_type)}
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                        {file.filename}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {formatFileSize(file.file_size)} • {file.file_type.toUpperCase()}
                      </Typography>
                    </Box>
                  </Box>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Chip
                      label={file.status}
                      color={file.status === 'processed' ? 'success' : 'default'}
                      size="small"
                    />
                    <Tooltip title="Remove file">
                      <IconButton
                        size="small"
                        onClick={() => removeFile(file.file_id)}
                        sx={{ color: '#f44336' }}
                      >
                        <Delete />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </Box>
              ))}
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default FileUpload;
