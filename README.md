# LangGraph Social Media Creator

An AI-powered social media content planning tool that generates engaging topic ideas, captions, and hashtags for your brand using LangGraph workflow orchestration and local LLM inference.

## Features

- **AI-Powered Content Generation**: Uses Microsoft's Phi-3 model for generating creative social media content
- **Multi-Step Workflow**: LangGraph orchestrates the content creation process through distinct planning, generation, and formatting phases
- **Customizable Planning**: Generate content calendars for any number of days based on your brand theme
- **Interactive Web UI**: User-friendly Gradio interface for easy content generation
- **CSV Export**: Download your content calendar as a CSV file for easy integration with scheduling tools

## Project Structure

```
langgraph-social-media-creator/
├── src/
│   ├── agent.py          # LangGraph workflow and node definitions
│   ├── model.py          # LLM interface and content generation functions
│   ├── main.py           # Gradio web interface
│   └── __init__.py
├── models/               # Local model storage
├── results/              # Generated content calendars
├── requirements.txt      # Python dependencies
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- At least 4GB of free disk space for the model
- 8GB+ RAM recommended for smooth model inference

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sagnikpal2004/langgraph-social-media-creator.git
cd langgraph-social-media-creator
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Download the Model

The Phi-3 model will be automatically downloaded on first run to the `models/` directory. This may take a few minutes depending on your internet connection.

## Usage

### Web Interface (Recommended)

1. **Start the Gradio Interface:**
   ```bash
   python src/main.py
   ```

2. **Access the Web UI:**
   - Open your browser and go to `http://localhost:7860`
   - Enter your brand theme (e.g., "Sustainable Fashion", "Tech Startup", "Fitness Coaching")
   - Set the number of days for content planning
   - Click "Submit" to generate your content calendar

3. **Download Results:**
   - View the generated content in the web interface
   - Download the CSV file using the download button

### Command Line Interface

You can also run the agent directly:

```bash
python src/agent.py
```

Follow the prompts to enter your brand theme and number of days.

## How It Works

The system uses a LangGraph workflow with four main nodes:

1. **Day Planner**: Generates topic ideas based on your brand theme
2. **Content Generator**: Creates captions and hashtags for each topic
3. **Formatter**: Organizes content into a structured DataFrame
4. **Saver**: Exports the content calendar to CSV

The workflow uses conditional edges to process each day's content iteratively until the specified number of days is complete.

## Example Output

| Day | Topic | Caption | Hashtags |
|-----|-------|---------|----------|
| 1 | Sustainable fabric choices matter | Choose fabrics that love our planet back. Your style can make a difference! | ['#SustainableFashion', '#EcoFriendly', '#ConsciousStyle'] |
| 2 | Zero waste wardrobe essentials | Build a capsule wardrobe that creates zero waste. Quality over quantity always wins! | ['#ZeroWaste', '#CapsuleWardrobe', '#MinimalistFashion'] |

## Customization

### Model Configuration

Edit `src/model.py` to adjust:
- Model parameters (temperature, max_tokens)
- Prompt templates for different content styles
- Content generation strategies

### Workflow Modification

Modify `src/agent.py` to:
- Add new processing nodes
- Change the workflow structure
- Implement custom content validation

## Troubleshooting

### Common Issues

**Model Download Fails:**
- Check internet connection
- Ensure sufficient disk space (4GB+)
- Try restarting the application

**Memory Issues:**
- Close other applications to free RAM
- Reduce the number of days for content generation
- Consider using a smaller model variant

**Import Errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Ensure all dependencies are properly installed
3. Verify Python version compatibility (3.8+)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for workflow orchestration
- Powered by [Microsoft Phi-3](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf) language model
- UI created with [Gradio](https://gradio.app/)
