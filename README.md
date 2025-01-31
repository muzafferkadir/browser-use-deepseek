# Browser Use with DeepSeek Example

This project demonstrates how to use the browser-use library with DeepSeek's language model for web automation tasks. It showcases a simple example of navigating to Reddit, performing a search, and extracting content.

## Features

- Web automation using browser-use library
- Integration with DeepSeek's powerful language model
- Automated browser interactions (navigation, search, clicking)
- Content extraction capabilities
- Simple and modern web interface for task execution

## Installation

### Prerequisites

1. Install Python 3.11:
   - Download and install from [Python.org](https://www.python.org/downloads/)

2. Install Git:
   - Download and install from [Git Downloads](https://git-scm.com/downloads)

3. Install uv:
   - Follow instructions at [uv Documentation](https://docs.astral.sh/uv/#highlights)

### Setup

1. Clone the repository:
```bash
git clone git@github.com:muzafferkadir/browser-use-deepseek.git
cd browser-use-deepseek
```

2. Create and activate virtual environment using uv:
```bash
uv venv --python 3.11
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Set up API keys:
   - Get your API key from [DeepSeek Platform](https://platform.deepseek.com/usage)
   - Or get your API key from [OpenRouter](https://openrouter.ai/settings/keys)
   - Create a `.env` file in the project root (copy from .env.example)
   - Add your API key to the `.env` file

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
1. Enter your task in the text area
2. Click the "Run Task" button
3. Watch the progress in real-time
4. See the results or any errors in the output section

Example tasks you can try:
- "Go to Reddit, search for 'browser-use' and return the first post's title"
- "Go to YouTube, search for 'browser automation' and get the first video's description"
- "Go to Wikipedia, search for 'Python programming' and return the first paragraph"
- "Go to https://www.youtube.com/@muzafferkadir and return the channel name"

## Requirements

- Python 3.8+
- DeepSeek API key
- Required Python packages (see requirements.txt)

## License

MIT License

## Acknowledgments

- [browser-use](https://github.com/browser-use/browser-use) library
- DeepSeek for their language model API 