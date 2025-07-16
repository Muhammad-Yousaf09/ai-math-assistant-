# Text To Math Problems Solver Data Search Assistant

A powerful AI-powered application that combines mathematical problem-solving capabilities with Wikipedia search functionality. Built with Streamlit, LangChain, and Groq's Gemma2 model.

## 🌟 Features

- **Mathematical Problem Solving**: Solve complex math problems with step-by-step explanations
- **Wikipedia Integration**: Search and retrieve information from Wikipedia
- **Interactive Chat Interface**: User-friendly chat-based interaction
- **Real-time Processing**: Get instant responses with streaming callbacks
- **Reasoning Engine**: Logical problem-solving with detailed explanations

## 🚀 Demo

The application provides three main tools:
1. **Calculator**: Solves mathematical expressions and equations
2. **Wikipedia Search**: Retrieves relevant information from Wikipedia
3. **Reasoning Tool**: Provides logical step-by-step problem-solving

## 📋 Prerequisites

- Python 3.8+
- Groq API Key
- Internet connection for Wikipedia searches

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Muhammad-Yousaf09/math-ai-assistant.git
   cd math-ai-assistant
   ```

2. **Install required packages**
   ```bash
   pip install streamlit langchain-groq langchain langchain-community
   ```

3. **Set up environment variables**
   ```bash
   export GROQ_API_KEY="your_groq_api_key_here"
   ```

   Or create a `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🔧 Configuration

### Groq API Key Setup

1. Visit [Groq Console](https://console.groq.com/)
2. Create an account and generate an API key
3. Set the API key as an environment variable or in your deployment platform

### For Hugging Face Deployment

1. Go to your Hugging Face Space
2. Navigate to Settings → Secrets
3. Add `GROQ_API_KEY` with your API key value

## 💻 Usage

1. **Run the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Start asking questions!**
   - Math problems: "What is the derivative of x² + 3x + 2?"
   - Wikipedia searches: "Tell me about quantum physics"
   - Complex reasoning: "If a train travels at 60 mph for 2 hours, how far does it go?"

## 🏗️ Project Structure

```
math-ai-assistant/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .env                  # Environment variables (optional)
```

## 🔍 How It Works

The application uses LangChain's agent framework to orchestrate between different tools:

1. **Input Processing**: User questions are processed through the agent
2. **Tool Selection**: The agent decides which tool(s) to use based on the question
3. **Execution**: The selected tool(s) process the request
4. **Response Generation**: Results are formatted and presented to the user

### Available Tools

- **Wikipedia Tool**: Searches Wikipedia for factual information
- **Calculator Tool**: Solves mathematical expressions using LLMMathChain
- **Reasoning Tool**: Provides logical problem-solving with custom prompts

## 🧠 Model Information

- **Model**: Gemma2-9b-it (via Groq)
- **Agent Type**: Zero-shot React Description
- **Framework**: LangChain

## 📱 Deployment

### Local Deployment
```bash
streamlit run app.py
```

### Hugging Face Spaces
1. Create a new Space on Hugging Face
2. Upload your code
3. Set the `GROQ_API_KEY` in Secrets
4. Deploy!

### Other Platforms
The app can be deployed on:
- Streamlit Cloud
- Heroku
- AWS
- Google Cloud Platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Example Usage

```python
# Example questions you can ask:
"What is 25 * 47 + 123?"
"Explain the concept of machine learning from Wikipedia"
"If I have $1000 and invest it at 5% annual interest, how much will I have after 10 years?"
"What is the quadratic formula and how do you use it?"
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Groq API key is correctly set
2. **Module Not Found**: Install all required packages using pip
3. **Connection Issues**: Check your internet connection for Wikipedia searches

### Debug Mode

To enable verbose logging, the application already includes `verbose=True` in the agent configuration.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for the powerful language model
- [LangChain](https://langchain.com/) for the agent framework
- [Streamlit](https://streamlit.io/) for the web interface
- [Wikipedia API](https://wikipedia.org/) for knowledge retrieval

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Contact: [yousafzadran50@gmail.com]

## 🔄 Version History

- **v1.0.0**: Initial release with basic math solving and Wikipedia search
- **v1.1.0**: Added reasoning capabilities and improved UI
- **v1.2.0**: Enhanced error handling and streaming responses

---

**Made with ❤️ and AI**
