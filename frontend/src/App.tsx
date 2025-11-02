import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  stockCode?: string;
  notionalAmount?: number;
}

interface ModelStatus {
  sentence_model_loaded: boolean;
  chat_model_loaded: boolean;
  chat_pipeline_loaded: boolean;
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [modelStatus, setModelStatus] = useState<ModelStatus | null>(null);
  const [connectionError, setConnectionError] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Check backend connection and model status on component mount
    const checkBackendStatus = async () => {
      try {
        const response = await axios.get('http://localhost:8000/models/status');
        setModelStatus(response.data);
        setConnectionError(false);
      } catch (error) {
        console.error('Backend connection failed:', error);
        setConnectionError(true);
      }
    };

    checkBackendStatus();
    
    // Set up interval to check status every 30 seconds
    const interval = setInterval(checkBackendStatus, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setConnectionError(false);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        message: inputMessage,
      });

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.response,
        isUser: false,
        timestamp: new Date(),
        stockCode: response.data.stock_code,
        notionalAmount: response.data.notional_amount,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setConnectionError(true);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please make sure the backend server is running on http://localhost:8000',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatNotional = (amount: number) => {
    return new Intl.NumberFormat('en-HK', {
      style: 'currency',
      currency: 'HKD',
      minimumFractionDigits: 2,
    }).format(amount);
  };

  const getStatusColor = () => {
    if (connectionError) return 'bg-red-100 border-red-400 text-red-700';
    if (!modelStatus) return 'bg-yellow-100 border-yellow-400 text-yellow-700';
    if (modelStatus.chat_pipeline_loaded && modelStatus.sentence_model_loaded) {
      return 'bg-green-100 border-green-400 text-green-700';
    }
    return 'bg-yellow-100 border-yellow-400 text-yellow-700';
  };

  const getStatusMessage = () => {
    if (connectionError) return 'Backend server not connected';
    if (!modelStatus) return 'Checking AI model status...';
    if (modelStatus.chat_pipeline_loaded && modelStatus.sentence_model_loaded) {
      return 'AI Models: Fully Loaded ✓';
    }
    return 'AI Models: Loading... (First time may take a few minutes)';
  };

  const getStatusIcon = () => {
    if (connectionError) return '🔴';
    if (!modelStatus) return '🟡';
    if (modelStatus.chat_pipeline_loaded && modelStatus.sentence_model_loaded) {
      return '🟢';
    }
    return '🟡';
  };

  const retryConnection = async () => {
    try {
      const response = await axios.get('http://localhost:8000/models/status');
      setModelStatus(response.data);
      setConnectionError(false);
    } catch (error) {
      setConnectionError(true);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Stock Support Chatbot
          </h1>
          <p className="text-gray-600">
            Ask me about stock trading information, like "What is the notional traded for stock 0148.HK?"
          </p>
        </div>

        {/* Status Banner */}
        <div className={`mb-6 p-4 border rounded-lg ${getStatusColor()} transition-colors duration-300`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-lg">{getStatusIcon()}</span>
              <span className="font-medium">{getStatusMessage()}</span>
            </div>
            {connectionError && (
              <button
                onClick={retryConnection}
                className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700 transition-colors"
              >
                Retry Connection
              </button>
            )}
          </div>
        
        </div>

        {/* Chat Container */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* Messages Area */}
          <div className="chat-container overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 py-12">
                <div className="text-6xl mb-4">💬</div>
                <p className="text-lg">Welcome! How can I help you with stock information today?</p>
                <div className="mt-6 space-y-2 text-sm">
                  <p className="font-medium">Try asking:</p>
                  <div className="space-y-1">
                    <p className="text-blue-600 bg-blue-50 px-3 py-2 rounded-lg">
                      "What is the notional traded for stock 0148.HK?"
                    </p>
                    <p className="text-blue-600 bg-blue-50 px-3 py-2 rounded-lg">
                      "Show me today's trading for 0700.HK"
                    </p>
                    <p className="text-blue-600 bg-blue-50 px-3 py-2 rounded-lg">
                      "How much was traded for 0148.HK today?"
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                      message.isUser
                        ? 'bg-blue-500 text-white rounded-br-none'
                        : 'bg-gray-100 text-gray-800 rounded-bl-none'
                    }`}
                  >
                    <div className="text-sm whitespace-pre-wrap">{message.text}</div>
                    
                    {/* Additional data for bot messages */}
                    {!message.isUser && message.notionalAmount && (
                      <div className="mt-2 p-2 bg-green-100 rounded-lg border border-green-200">
                        <div className="text-xs text-green-800 font-semibold">
                          💰 Notional Amount: {formatNotional(message.notionalAmount)}
                        </div>
                        {message.stockCode && (
                          <div className="text-xs text-green-600 mt-1">
                            Stock: {message.stockCode}
                          </div>
                        )}
                      </div>
                    )}
                    
                    {!message.isUser && message.stockCode && !message.notionalAmount && (
                      <div className="mt-1">
                        <div className="text-xs text-gray-500">
                          📊 Stock: {message.stockCode}
                        </div>
                      </div>
                    )}
                    
                    <div className={`text-xs mt-1 ${message.isUser ? 'text-blue-200' : 'text-gray-500'}`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              ))
            )}
            
            {/* Loading indicator */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 px-4 py-3 rounded-2xl rounded-bl-none">
                  <div className="flex items-center space-x-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                    <span className="text-sm text-gray-600">AI is thinking...</span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4 bg-white">
            <div className="flex space-x-4">
              <div className="flex-1">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type your question about stock trading..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  disabled={isLoading || connectionError}
                />
              </div>
              <button
                onClick={sendMessage}
                disabled={isLoading || !inputMessage.trim() || connectionError}
                className="px-6 py-3 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
              >
                {isLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Sending...</span>
                  </>
                ) : (
                  <span>Send</span>
                )}
              </button>
            </div>
            
            {/* Connection error hint */}
            {connectionError && (
              <div className="mt-2 text-center">
                <p className="text-sm text-red-600">
                  💡 Make sure the backend server is running on port 8000
                </p>
                <p className="text-xs text-red-500 mt-1">
                  Run 'start-backend.bat' in the backend folder first
                </p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

export default App;