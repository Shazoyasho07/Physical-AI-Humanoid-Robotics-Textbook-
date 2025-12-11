/**
 * RAG Chatbot Component
 * Provides an interface for users to ask questions about textbook content
 */
import React, { useState, useRef, useEffect } from 'react';
import './RAGChatbot.css';

const RAGChatbot = ({ textbookId }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API to get the response
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/v1/textbook/${textbookId}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          textbook_id: textbookId
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add bot response to the chat
      const botMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot',
        sources: data.sources || [],
        timestamp: new Date(),
        confidence: data.confidence
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error getting chatbot response:', error);

      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="rag-chatbot">
      <div className="chat-header">
        <h3>Textbook Assistant</h3>
        <p>Ask questions about the textbook content</p>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your textbook assistant. Ask me anything about this textbook, and I'll provide answers based on the content.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div 
              key={message.id} 
              className={`message ${message.sender}-message`}
            >
              <div className="message-content">
                <p>{message.text}</p>
                
                {message.sources && message.sources.length > 0 && (
                  <div className="sources">
                    <p><strong>Sources:</strong></p>
                    <ul>
                      {message.sources.map((source, index) => (
                        <li key={index}>
                          {source.chapter_title} ({source.page_reference})
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {message.confidence !== undefined && (
                  <div className="confidence">
                    <small>Confidence: {(message.confidence * 100).toFixed(1)}%</small>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <p>Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the textbook..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default RAGChatbot;