import React, { useState, useEffect } from 'react';
import { TextField, Button, Paper, Typography, Box, Autocomplete } from '@mui/material';
import './Chatbot.css';
import { fetchSymptoms, sendDiagnosisRequest } from '../basicAxios';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [symptoms, setSymptoms] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);

  useEffect(() => {
    const initialMessage = { text: "Are you having any symptoms? Let me help you out.", user: false };
    setMessages([initialMessage]);
    fetchAllSymptoms();
  }, []);

  const fetchAllSymptoms = async () => {
    try {
      const data = await fetchSymptoms();
      setSymptoms(data);
    } catch (error) {
      console.error("Error fetching symptoms:", error);
    }
  };

  const sendMessage = async () => {
    if (selectedSymptoms.length === 0) return;

    const newMessage = { text: `Symptoms: ${selectedSymptoms.join(', ')}`, user: true };
    setMessages([...messages, newMessage]);

    try {
      const data = await sendDiagnosisRequest(selectedSymptoms);
      setMessages([...messages, newMessage, { text: data.diagnosis, user: false }]);
    } catch (error) {
      console.error("Error diagnosing symptoms:", error);
    }

    setInput('');
    setSelectedSymptoms([]);
  };

  const handleSymptomChange = (event, value) => {
    setSelectedSymptoms(value);
  };

  return (
    <Paper elevation={3} className="chatbot-container">
      <Typography variant="h4" gutterBottom>
        Healthcare Diagnosis Chatbot
      </Typography>
      <Box className="chatbot-messages">
        {messages.map((msg, index) => (
          <Typography
            key={index}
            className={`message ${msg.user ? 'user-message' : 'bot-message'}`}
          >
            {msg.text}
          </Typography>
        ))}
      </Box>
      <Box className="chatbot-input">
        <Autocomplete
          multiple
          options={symptoms}
          getOptionLabel={(option) => option}
          value={selectedSymptoms}
          onChange={handleSymptomChange}
          renderInput={(params) => (
            <TextField
              {...params}
              variant="outlined"
              label="Enter symptoms"
              placeholder="Type a symptom"
              fullWidth
            />
          )}
        />
        <Button variant="contained" color="primary" onClick={sendMessage}>
          Send
        </Button>
      </Box>
    </Paper>
  );
};

export default Chatbot;
