import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Box,
  Typography,
  Divider,
} from '@mui/material';
import {
  Dashboard,
  Psychology,
  Assessment,
  Description,
  Settings,
  CloudUpload,
  SmartToy,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <Dashboard />, path: '/' },
  { text: 'Agent Management', icon: <Psychology />, path: '/agents' },
  { text: 'Governance Validation', icon: <Assessment />, path: '/governance' },
  { text: 'File Upload', icon: <CloudUpload />, path: '/upload' },
  { text: 'LLM Management', icon: <SmartToy />, path: '/llm' },
  { text: 'Reports', icon: <Description />, path: '/reports' },
  { text: 'Settings', icon: <Settings />, path: '/settings' },
];

const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          backgroundColor: '#1a1a1a',
          borderRight: '1px solid #333',
        },
      }}
    >
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" sx={{ color: '#fff', fontWeight: 600 }}>
          AI Swarm
        </Typography>
        <Typography variant="caption" sx={{ color: '#888' }}>
          Architecture Governance
        </Typography>
      </Box>
      <Divider sx={{ borderColor: '#333' }} />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              onClick={() => navigate(item.path)}
              selected={location.pathname === item.path}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: '#2196f3',
                  '&:hover': {
                    backgroundColor: '#1976d2',
                  },
                },
                '&:hover': {
                  backgroundColor: '#2a2a2a',
                },
              }}
            >
              <ListItemIcon sx={{ color: location.pathname === item.path ? '#fff' : '#888' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.text} 
                sx={{ 
                  color: location.pathname === item.path ? '#fff' : '#ccc',
                  '& .MuiTypography-root': {
                    fontWeight: location.pathname === item.path ? 600 : 400,
                  },
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Navigation;
