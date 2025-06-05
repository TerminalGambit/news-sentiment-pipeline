import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Container,
  Button,
  MenuItem,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AssessmentIcon from '@mui/icons-material/Assessment';
import BarChartIcon from '@mui/icons-material/BarChart';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import TimelineIcon from '@mui/icons-material/Timeline';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [anchorElNav, setAnchorElNav] = useState<null | HTMLElement>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleNavigate = (path: string) => {
    navigate(path);
    handleCloseNavMenu();
  };

  const pages = [
    { name: 'Home', path: '/' },
    {
      name: 'NVIDIA Indicators',
      path: '/market/NVDA',
      submenu: [
        { name: 'Overview', path: '/market/NVDA', icon: <AssessmentIcon /> },
        { name: 'SMA', path: '/market/NVDA/sma', icon: <ShowChartIcon /> },
        { name: 'RSI', path: '/market/NVDA/rsi', icon: <BarChartIcon /> },
        { name: 'MACD', path: '/market/NVDA/macd', icon: <TimelineIcon /> },
      ],
    },
  ];

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static" sx={{ background: 'linear-gradient(135deg, #2563eb, #1e40af)' }}>
        <Container maxWidth="xl">
          <Toolbar disableGutters>
            <TrendingUpIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
            <Typography
              variant="h6"
              noWrap
              component="a"
              href="/"
              sx={{
                mr: 2,
                display: { xs: 'none', md: 'flex' },
                fontFamily: 'Inter',
                fontWeight: 700,
                color: 'inherit',
                textDecoration: 'none',
              }}
            >
              Financial News Sentiment Analysis
            </Typography>

            <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
              <IconButton
                size="large"
                aria-label="menu"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleOpenNavMenu}
                color="inherit"
              >
                <MenuIcon />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorElNav}
                anchorOrigin={{
                  vertical: 'bottom',
                  horizontal: 'left',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'left',
                }}
                open={Boolean(anchorElNav)}
                onClose={handleCloseNavMenu}
                sx={{
                  display: { xs: 'block', md: 'none' },
                }}
              >
                {pages.map((page) => (
                  <MenuItem key={page.name} onClick={() => handleNavigate(page.path)}>
                    <Typography textAlign="center">{page.name}</Typography>
                  </MenuItem>
                ))}
              </Menu>
            </Box>

            <TrendingUpIcon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }} />
            <Typography
              variant="h5"
              noWrap
              component="a"
              href="/"
              sx={{
                mr: 2,
                display: { xs: 'flex', md: 'none' },
                flexGrow: 1,
                fontFamily: 'Inter',
                fontWeight: 700,
                color: 'inherit',
                textDecoration: 'none',
              }}
            >
              Financial News
            </Typography>

            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, justifyContent: 'flex-end' }}>
              {pages.map((page) => (
                <Button
                  key={page.name}
                  onClick={() => handleNavigate(page.path)}
                  sx={{
                    my: 2,
                    color: 'white',
                    display: 'block',
                    fontWeight: location.pathname === page.path ? 700 : 500,
                  }}
                >
                  {page.name}
                </Button>
              ))}
            </Box>
          </Toolbar>
        </Container>
      </AppBar>

      <Container component="main" maxWidth="xl" sx={{ flexGrow: 1, py: 4 }}>
        {children}
      </Container>

      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: (theme) => theme.palette.grey[100],
        }}
      >
        <Container maxWidth="xl">
          <Typography variant="body2" color="text.secondary" align="center">
            © {new Date().getFullYear()} Financial News Sentiment Analysis
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default Layout; 