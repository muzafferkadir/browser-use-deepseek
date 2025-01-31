from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
import asyncio
from dotenv import load_dotenv
import os
import logging
import re
import json
import io
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
load_dotenv()

# Configure agent logger specifically
agent_logger = logging.getLogger('agent')
agent_logger.setLevel(logging.DEBUG)

async def run_browser_task(task):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # Initialize the model
    llm = ChatOpenAI(
        base_url='https://api.deepseek.com/v1',
        model='deepseek-reasoner',
        api_key=SecretStr(api_key)
    )

    # Create agent with basic settings
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=False
    )

    # Run the agent
    result = await agent.run()
    return result

def format_agent_history(history):
    try:
        formatted_steps = []
        step_counter = 1
        
        # Handle string output (like what we see in console)
        if isinstance(history, str):
            # Split the output by newlines and filter empty lines
            lines = [line for line in history.split('\n') if line.strip()]
            current_content = []
            
            for line in lines:
                # Clean up the message and remove timestamps/log levels
                message = re.sub(r'^.*?\[.*?\]\s*', '', line).strip()
                if not message:
                    continue
                
                # Skip certain messages
                if any(skip in message for skip in [
                    'No history or first screenshot',
                    '[werkzeug]',
                    'all_model_outputs='
                ]):
                    continue
                
                # Clean up the message by removing emoji but keeping the text
                message = (message
                    .replace('🛠️', '')
                    .replace('📄', '')
                    .replace('✅', '')
                    .replace('🔍', '')
                    .replace('🖱️', '')
                    .replace('🎯', '')
                    .replace('🧠', '')
                    .replace('👍', '')
                    .replace('📍', ''))
                # Handle different types of messages
                if 'Starting browser task' in message:
                    formatted_steps.append({
                        'step': step_counter,
                        'content': message.strip(),
                        'type': 'start'
                    })
                    step_counter += 1
                elif 'Browser task completed' in message:
                    formatted_steps.append({
                        'step': step_counter,
                        'content': message.strip(),
                        'type': 'end'
                    })
                    step_counter += 1
                elif 'Result:' in message:
                    # Extract the result text after "Result:"
                    result_text = message.split('Result:')[1].strip()
                    formatted_steps.append({
                        'step': step_counter,
                        'content': f"Result: {result_text}",
                        'type': 'result'
                    })
                    step_counter += 1
                elif 'Action' in message and 'done' in message:
                    try:
                        # Try to extract the text from the done action
                        done_text = re.search(r'"text":\s*"([^"]+)"', message)
                        if done_text:
                            formatted_steps.append({
                                'step': step_counter,
                                'content': f"Action completed: {done_text.group(1)}",
                                'type': 'action'
                            })
                            step_counter += 1
                    except:
                        pass
                elif 'Task completed successfully' in message:
                    formatted_steps.append({
                        'step': step_counter,
                        'content': message.strip(),
                        'type': 'success'
                    })
                    step_counter += 1
                elif 'Next goal:' in message:
                    formatted_steps.append({
                        'step': step_counter,
                        'content': message.strip(),
                        'type': 'goal'
                    })
                    step_counter += 1
                elif not any(skip in message for skip in [
                    'Memory:',
                    'Eval:',
                    'Step'
                ]):
                    current_content.append(message.strip())
            
            # Add any remaining content as the final step
            if current_content:
                formatted_steps.append({
                    'step': step_counter,
                    'content': '\n'.join(current_content)
                })
        
        # If no steps were formatted, add a default message
        if not formatted_steps:
            formatted_steps.append({
                'step': 1,
                'content': 'Task completed but no output available'
            })
        
        logger.debug(f"Formatted steps: {formatted_steps}")  # Debug log to see what's being returned
        return json.dumps(formatted_steps)
    except Exception as e:
        logger.error(f"Error formatting history: {str(e)}", exc_info=True)
        return json.dumps([{'step': 1, 'content': f'Error formatting output: {str(e)}'}])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_task', methods=['POST'])
def run_task():
    logger.info("Received task request")
    task = request.json.get('task')
    logger.info(f"Task content: {task}")
    
    if not task:
        logger.warning("No task provided in request")
        return jsonify({'error': 'No task provided'}), 400
    
    try:
        # Create a string buffer to capture the output
        output_buffer = io.StringIO()
        
        # Create a custom handler to capture logs
        string_handler = logging.StreamHandler(output_buffer)
        string_handler.setLevel(logging.DEBUG)  # Changed from INFO to DEBUG
        formatter = logging.Formatter('%(message)s')
        string_handler.setFormatter(formatter)
        
        # Add the handler to the root logger and agent logger
        root_logger = logging.getLogger()
        agent_logger = logging.getLogger('agent')
        agent_logger.setLevel(logging.DEBUG)  # Ensure agent logger level is DEBUG
        root_logger.addHandler(string_handler)
        agent_logger.addHandler(string_handler)
        
        # Store original stdout
        original_stdout = sys.stdout
        sys.stdout = output_buffer
        
        try:
            logger.info("Starting browser task execution")
            result = asyncio.run(run_browser_task(task))
            logger.info("Browser task completed")
            
            # Handle the result object
            if hasattr(result, 'all_model_outputs'):
                # Extract the final result from model outputs
                for output in reversed(result.all_model_outputs):
                    if isinstance(output, dict) and 'done' in output:
                        result_text = output['done'].get('text', '')
                        if result_text:
                            logger.info(f"Result: {result_text}")
                            break
                
        finally:
            # Restore stdout and remove the handler
            sys.stdout = original_stdout
            root_logger.removeHandler(string_handler)
            agent_logger.removeHandler(string_handler)
            
            # Get the captured output
            captured_output = output_buffer.getvalue()
            output_buffer.close()
            
            # Log the captured output for debugging
            logger.debug(f"Captured output: {captured_output}")
        
        # Format the captured output
        formatted_result = format_agent_history(captured_output)
        logger.debug(f"Formatted result: {formatted_result}")
        return jsonify({'result': formatted_result})
    except Exception as e:
        logger.error(f"Error in run_task: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002) 