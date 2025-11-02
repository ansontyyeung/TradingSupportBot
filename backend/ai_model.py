import re
import torch
from database import Database
from csv_processor import csv_processor
from typing import Dict, Any
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
from datetime import date
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIModel:
    def __init__(self):
        self.db = Database()
        self.csv_processor = csv_processor
        self.classifier = None
        self.chat_model = None
        self.tokenizer = None
        self.sentence_model = None
        self._setup_models()
        
    def _setup_models(self):
        """Setup Hugging Face models for classification and chat"""
        try:
            logger.info("Loading sentence transformer model for classification...")
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            logger.info("Loading chat model...")
            model_name = "microsoft/DialoGPT-small"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.chat_model = AutoModelForCausalLM.from_pretrained(model_name)
            
            self.chat_pipeline = pipeline(
                "text-generation",
                model=self.chat_model,
                tokenizer=self.tokenizer,
                max_new_tokens=100,
                do_sample=True,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            logger.info("All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.chat_pipeline = None
    
    def extract_stock_code(self, query: str) -> str:
        """Extract stock code from natural language query"""
        patterns = [
            r'(\d{4}\.HK)',  # 0148.HK format
            r'stock\s+(\d{4}\.HK)',  # "stock 0148.HK"
            r'for\s+(\d{4}\.HK)',  # "for 0148.HK"
            r'(\d{4}\.HK)',  # General pattern
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def classify_intent(self, query: str) -> str:
        """Classify user intent"""
        query_lower = query.lower()
        
        intents = {
            'notional_query': [
                "notional", "traded amount", "trading value", "amount traded",
                "total value", "trade value", "notional amount", "how much was traded"
            ],
            'price_query': [
                "price", "current price", "stock price", "how much", "cost"
            ],
            'volume_query': [
                "volume", "trading volume", "shares traded", "quantity"
            ],
            'date_query': [
                "yesterday", "today", "specific date", "on date", "for date"
            ],
            'general_query': [
                "hello", "hi", "help", "what can you do", "hey"
            ]
        }
        
        # Simple keyword matching
        for intent, keywords in intents.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        
        return 'general_query'
    
    def generate_chat_response(self, context: str) -> str:
        """Generate response using the chat model"""
        if not self.chat_pipeline:
            return "I understand your query. How can I assist you with stock information?"
        
        try:
            prompt = f"User: {context}\nAssistant:"
            
            response = self.chat_pipeline(
                prompt,
                max_new_tokens=80,
                do_sample=True,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1
            )
            
            generated_text = response[0]['generated_text']
            if "Assistant:" in generated_text:
                assistant_response = generated_text.split("Assistant:")[-1].strip()
                assistant_response = re.sub(r'User:.*', '', assistant_response).strip()
                return assistant_response
            else:
                return generated_text.replace(prompt, "").strip()
                
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return "I understand your query. How can I assist you with stock information?"
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process user query and return response"""
        logger.info(f"Processing query: {query}")
        
        # Extract stock code
        stock_code = self.extract_stock_code(query)
        
        # Extract date from query
        query_date = self.csv_processor.parse_date_from_query(query)
        
        # Classify intent
        intent = self.classify_intent(query)
        logger.info(f"Detected intent: {intent}, Stock code: {stock_code}, Date: {query_date}")
        
        # Handle date-specific queries
        if intent == 'notional_query' and stock_code:
            result = self.csv_processor.get_stock_notional(stock_code, query_date)
            
            if result['success']:
                notional = result['notional']
                response = f"The total notional traded for {stock_code} on {query_date} was HK${notional:,.2f}\n"
                response += f"• Total Quantity: {result['quantity']:,.0f} shares\n"
                response += f"• Average Price: HK${result['average_price']:.2f}\n"
                response += f"• Number of Trades: {result['trade_count']}"
                
                return {
                    "success": True,
                    "response": response,
                    "stock_code": stock_code,
                    "notional_amount": notional,
                    "query_date": query_date.isoformat()
                }
            else:
                return {
                    "success": False,
                    "response": result['message'],
                    "stock_code": stock_code,
                    "query_date": query_date.isoformat()
                }
        
        elif intent == 'date_query':
            available_dates = self.csv_processor.get_available_dates()
            if available_dates:
                dates_str = ", ".join([d.strftime("%Y-%m-%d") for d in available_dates])
                response = f"I have trading data available for the following dates: {dates_str}"
            else:
                response = "No trading data files found in the data directory."
            
            return {
                "success": True,
                "response": response,
                "stock_code": None
            }
        
        elif not stock_code and intent != 'general_query':
            response = "I couldn't identify a stock code in your query. Please specify a stock like '0148.HK'."
            return {
                "success": False,
                "response": response,
                "stock_code": None
            }
        
        else:
            # Generate contextual response
            context = f"User is asking about stocks. Query: {query}"
            if stock_code:
                context += f" Stock code: {stock_code}"
            if query_date:
                context += f" Date: {query_date}"
            
            chat_response = self.generate_chat_response(context)
            response = f"{chat_response} I specialize in stock trading information including notional amounts, prices, and volumes for specific dates."
            
            return {
                "success": True,
                "response": response,
                "stock_code": stock_code,
                "query_date": query_date.isoformat() if query_date else None
            }