import React from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
  Box,
  Chip,
  IconButton
} from '@mui/material';
import { Edit as EditIcon } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { appointmentService, doctorService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const getStatusColor = (status: string) => {
  switch (status) {
    case 'scheduled':
      return 'primary';
    case 'confirmed':
      return 'success';
    case 'completed':
      return 'info';
    case 'cancelled':
      return 'error';
    default:
      return 'default';
  }
};

export const DoctorDashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const { data: appointments, isLoading: appointmentsLoading } = useQuery({
    queryKey: ['doctorAppointments'],
    queryFn: () => appointmentService.getDoctorAppointments(user?.id || 0),
    enabled: !!user
  });

  const { data: availability, isLoading: availabilityLoading } = useQuery({
    queryKey: ['doctorAvailability'],
    queryFn: () => doctorService.getAvailability(user?.id || 0),
    enabled: !!user
  });

  if (appointmentsLoading || availabilityLoading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3}>
          {/* Today's Appointments */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" mb={2}>Today's Appointments</Typography>
              <List>
                {appointments?.map((appointment) => (
                  <React.Fragment key={appointment.id}>
                    <ListItem>
                      <ListItemText
                        primary={`${appointment.patient.user.first_name} ${appointment.patient.user.last_name}`}
                        secondary={
                          <>
                            <Typography component="span" variant="body2">
                              {appointment.start_time} - {appointment.end_time}
                            </Typography>
                            <br />
                            <Typography component="span" variant="body2">
                              Reason: {appointment.reason}
                            </Typography>
                          </>
                        }
                      />
                      <Box display="flex" alignItems="center" gap={1}>
                        <Chip 
                          label={appointment.status} 
                          color={getStatusColor(appointment.status) as any}
                          size="small"
                        />
                        <IconButton 
                          size="small"
                          onClick={() => navigate(`/appointments/${appointment.id}`)}
                        >
                          <EditIcon />
                        </IconButton>
                      </Box>
                    </ListItem>
                    <Divider />
                  </React.Fragment>
                ))}
              </List>
            </Paper>
          </Grid>

          {/* Availability Management */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Availability</Typography>
                <Button 
                  variant="contained" 
                  onClick={() => navigate('/availability')}
                >
                  Manage Schedule
                </Button>
              </Box>
              <List>
                {availability?.map((slot) => (
                  <React.Fragment key={slot.id}>
                    <ListItem>
                      <ListItemText
                        primary={slot.day.charAt(0).toUpperCase() + slot.day.slice(1)}
                        secondary={`${slot.start_time} - ${slot.end_time}`}
                      />
                      <Chip 
                        label={slot.is_available ? 'Available' : 'Unavailable'} 
                        color={slot.is_available ? 'success' : 'error'}
                        size="small"
                      />
                    </ListItem>
                    <Divider />
                  </React.Fragment>
                ))}
              </List>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}; 