from playwright.sync_api import sync_playwright
import ollama

def get_ai_response(prompt):
    response = ollama.chat(model='deepseek-r1:8b', messages=[{
        'role': 'user',
        'content': prompt
    }])
    return response['message']['content']

def browse_with_ai():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to a website
        page.goto('https://mkdir.dev')
        
        # Get page content
        content = page.content()
        
        # Ask AI to analyze the content
        prompt = f"Analyze this webpage content and give me a summary: {content}"
        ai_analysis = get_ai_response(prompt)
        print("AI Analysis:", ai_analysis)
        
        # You can add more interactions here
        
        browser.close()

if __name__ == "__main__":
    browse_with_ai()
