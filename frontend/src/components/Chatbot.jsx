import React, { useState } from 'react';
import { TextField, Button, Paper, Typography, Box } from '@mui/material';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const newMessage = { text: input, user: true };
    setMessages([...messages, newMessage]);

    const response = await fetch('/api/diagnose/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ symptoms: input }),
    });

    const data = await response.json();
    setMessages([...messages, newMessage, { text: data.diagnosis, user: false }]);
    setInput('');
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
        <TextField
          variant="outlined"
          fullWidth
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <Button variant="contained" color="primary" onClick={sendMessage}>
          Send
        </Button>
      </Box>
    </Paper>
  );
};

export default Chatbot;
