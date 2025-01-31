# Browser Use with DeepSeek Example

This project demonstrates how to use the browser-use library with DeepSeek's language model for web automation tasks. It showcases a simple example of navigating to Reddit, performing a search, and extracting content.

## Features

- Web automation using browser-use library
- Integration with DeepSeek's powerful language model
- Automated browser interactions (navigation, search, clicking)
- Content extraction capabilities
- Simple and modern web interface for task execution

## Installation

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your DeepSeek API key:
   - Get your API key from DeepSeek
   - Create a `.env` file in the project root
   - Add your API key: `DEEPSEEK_API_KEY=your_deepseek_api_key_here`

## Usage

### Command Line
Run the example script:
```bash
python main.py
```

The script will:
1. Navigate to Reddit
2. Search for "browser-use"
3. Click on the first post
4. Extract and return the first comment

### Web Interface
Run the web application:
```bash
python app.py
```

Then open your browser and go to one of these URLs:
- Local access: http://localhost:5001
- Network access: http://YOUR_IP_ADDRESS:5001 (replace YOUR_IP_ADDRESS with your computer's IP address)

Using the web interface:
1. Enter your task in the text area (e.g., "Go to Reddit and search for 'Python'")
2. Click the "Run Task" button
3. Watch the progress in real-time
4. See the results or any errors in the output section

Example tasks you can try:
- "Go to Reddit, search for 'browser-use' and return the first post's title"
- "Go to YouTube, search for 'browser automation' and get the first video's description"
- "Go to Wikipedia, search for 'Python programming' and return the first paragraph"

## Requirements

- Python 3.8+
- DeepSeek API key
- Required Python packages (see requirements.txt)

## License

MIT License

## Acknowledgments

- [browser-use](https://github.com/browser-use/browser-use) library
- DeepSeek for their language model API 