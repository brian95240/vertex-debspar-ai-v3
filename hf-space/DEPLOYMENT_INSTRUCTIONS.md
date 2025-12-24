# Hugging Face Space Deployment Instructions

## Manual Deployment Steps

Since automated deployment requires Hugging Face CLI authentication, follow these manual steps:

### Step 1: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name:** `vertex-debspar-ai-v3-demo`
   - **License:** `gpl-3.0`
   - **SDK:** `Gradio`
   - **Visibility:** `Public`
4. Click **"Create Space"**

### Step 2: Upload Files

Upload the following files from the `hf-space/` directory to your new Space:

1. `app.py` - Main application file
2. `requirements.txt` - Python dependencies
3. `README.md` - Space description and metadata

### Step 3: Wait for Build

Hugging Face will automatically:
1. Install dependencies from `requirements.txt`
2. Launch the Gradio app from `app.py`
3. Provide a public URL (e.g., `https://huggingface.co/spaces/YOUR_USERNAME/vertex-debspar-ai-v3-demo`)

### Step 4: Test the Demo

1. Visit your Space URL
2. Try the example arguments
3. Watch pressure detection and routing in action

### Step 5: Update GitHub Repository

Once deployed, add the Space URL to:
- `README.md` (main repository)
- `demo/INTERACTIVE_DEMO.md`

## Alternative: Git-based Deployment

If you have Hugging Face CLI configured:

```bash
# Install Hugging Face CLI
pip install huggingface_hub[cli]

# Login to Hugging Face
huggingface-cli login

# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/vertex-debspar-ai-v3-demo
cd vertex-debspar-ai-v3-demo

# Copy files
cp /home/ubuntu/vertex-debspar-ai-v3/hf-space/* .

# Commit and push
git add .
git commit -m "Initial deployment of Vertex DebSpar AI v3.0 demo"
git push
```

## Files Overview

- **app.py**: Gradio application with mock debate logic
- **requirements.txt**: Single dependency (gradio)
- **README.md**: Space metadata and description

## Expected Result

A live, interactive demo at:
`https://huggingface.co/spaces/YOUR_USERNAME/vertex-debspar-ai-v3-demo`

Users can:
- Enter debate arguments
- See real-time pressure analysis
- Watch routing decisions (LOCAL_WARM vs APEX_CLOUD)
- Experience mock debate responses

## Troubleshooting

**Build fails:**
- Check `requirements.txt` syntax
- Ensure `app.py` has no syntax errors
- Verify Gradio version compatibility

**App doesn't launch:**
- Check Space logs in Hugging Face UI
- Ensure `app.py` ends with `demo.launch()`
- Verify no port conflicts

**Slow responses:**
- This is expected for free tier
- Consider upgrading to paid tier for better performance

## Next Steps

1. Deploy to Hugging Face Spaces (manual or CLI)
2. Get public URL
3. Update GitHub repository with demo link
4. Share with community!
