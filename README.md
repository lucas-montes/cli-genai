1. Export your key from google
```bash
export API_KEY=<YOUR_API_KEY>
```

2. Create and activate a virtual env
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependency
```bash
pip install google-generativeai
```

4. Run the script with the files that you want to use
```bash
python3 app.py --files "text.txt"
```

5. To end the conversation type stop