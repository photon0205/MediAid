import React, { useState, useEffect } from 'react';
import { TextField, Button, Paper, Typography, Box, Autocomplete } from '@mui/material';
import './Chatbot.css';
import axios from 'axios';
import { fetchSymptoms, sendDiagnosisRequest } from '../basicAxios';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [symptoms, setSymptoms] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [showSymptomInput, setShowSymptomInput] = useState(true);

  useEffect(() => {
    const initialMessage = { text: "Are you having any symptoms? Let me help you out.", user: false };
    setMessages([initialMessage]);
    fetchAllSymptoms();
  }, []);

  const fetchAllSymptoms = async () => {
    try {
      const response = await fetchSymptoms()
      setSymptoms(response.data);
    } catch (error) {
      console.error("Error fetching symptoms:", error);
    }
  };

  const sendMessage = async () => {
    if (showSymptomInput) {
      if (selectedSymptoms.length === 0) return;

      const newMessage = { text: `Symptoms: ${selectedSymptoms.join(', ')}`, user: true };
      setMessages([...messages, newMessage]);

      try {
        const response = await sendDiagnosisRequest(selectedSymptoms);
        const { disease, probability, advice } = response.data;

        setMessages([
          ...messages,
          newMessage,
          { text: `Diagnosis: ${disease} (Probability: ${probability.toFixed(2)}%)`, user: false },
          { text: `Advice: ${advice}`, user: false }
        ]);

        setShowSymptomInput(false);

        setTimeout(() => {
          setMessages(prevMessages => [
            ...prevMessages,
            { text: "Hi! I'm here to help you with your diagnosis. What would you like to know?", user: false }
          ]);
        }, 1500);
      } catch (error) {
        console.error("Error diagnosing symptoms:", error);
      }

      setInput('');
      setSelectedSymptoms([]);
    } else {
      const newMessage = { text: input, user: true };
      setMessages([...messages, newMessage]);
      setInput('');

      try {
        const response = await axios.post('/api/openai/', { question: input });
        const { answer } = response.data;

        const typingDelay = 50;
        const responseMessages = [];
        let charsToType = answer.length;
        let charsTyped = 0;

        const typingInterval = setInterval(() => {
          const currentMessage = {
            ...newMessage,
            text: `${newMessage.text}${answer.charAt(charsTyped)}`,
          };
          responseMessages.push(currentMessage);
          setMessages([...messages, ...responseMessages]);
          charsTyped++;

          if (charsTyped >= charsToType) {
            clearInterval(typingInterval);
          }
        }, typingDelay);
      } catch (error) {
        console.error("Error getting response from OpenAI:", error);
      }
    }
  };

  const handleInputChange = (event) => {
    setInput(event.target.value);
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
        {showSymptomInput ? (
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
        ) : (
          <TextField
            variant="outlined"
            label="Type your message here"
            placeholder="Type a message"
            fullWidth
            value={input}
            onChange={handleInputChange}
          />
        )}
        <Button variant="contained" color="primary" onClick={sendMessage}>
          Send
        </Button>
      </Box>
    </Paper>
  );
};

export default Chatbot;
