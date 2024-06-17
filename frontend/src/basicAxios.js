import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchSymptoms = async () => {
  try {
    const response = await axiosInstance.get('/api/symptoms/');
    return response.data;
  } catch (error) {
    console.error('Error fetching symptoms:', error);
    throw error;
  }
};

export const sendDiagnosisRequest = async (symptoms) => {
  try {
    const response = await axiosInstance.post('/api/diagnose/', { symptoms });
    return response.data;
  } catch (error) {
    console.error('Error sending diagnosis request:', error);
    throw error;
  }
};
