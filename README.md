# KhmerGPT: A Khmer Language Chatbot

Welcome to **KhmerGPT**, a chatbot designed to understand and respond in the Khmer language. This project is powered by an LLM model with an integrated speech-to-text (STT) and text-to-speech (TTS) system using Microsoft's Speech API. The chatbot interface is built using **Streamlit** for easy interaction and deployment.

## Features
- **Khmer Language Support**: The chatbot communicates in Khmer.
- **Groq API**: Utilizes a custom LLM powered by Groq API for generating responses.
- **Speech-to-Text (STT)**: Converts user speech to text using Microsoft's Speech API.
- **Text-to-Speech (TTS)**: Converts chatbot text responses into speech using Microsoft's Speech API.
- **Streamlit Web App**: Provides a user-friendly interface to interact with the chatbot.

## Prerequisites
Before running the application, ensure you have the following:

- **Groq API Key**: Required for accessing the LLM for text generation.
- **Microsoft Speech API Key**: Required for speech-to-text (STT) and text-to-speech (TTS) functionalities.
- **Python 3.8+**: Ensure Python is installed.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/reachsak/khmergpt.git
   cd khmergpt
   streamlit run app.py
