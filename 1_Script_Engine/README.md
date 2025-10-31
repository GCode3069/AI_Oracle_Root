# Script Engine - Jupyter Notebooks

This directory contains Jupyter notebooks for managing scripts, data, and voiceovers for the AI Oracle project.

## Notebooks

### 01_Sheets_Integration.ipynb
**Purpose:** Integrate Google Sheets for script management, data tracking, and analytics.

**Features:**
- Google Sheets API authentication using service accounts
- Read/write data to Google Sheets
- pandas integration for data analysis
- Batch operations and error handling
- AI Oracle-specific use cases (script tracking, ARG elements, video production logs)

**Prerequisites:**
1. Google Cloud project with Sheets API enabled
2. Service account credentials JSON file
3. Google Sheet shared with service account email

**Setup:**
```bash
# Install dependencies
pip install gspread oauth2client google-auth pandas python-dotenv

# Configure environment
cp .env.example .env
# Edit .env and add:
# GOOGLE_SHEETS_CREDENTIALS_PATH=credentials/google_sheets_credentials.json
# GOOGLE_SHEET_ID=your_sheet_id_here
```

**Use Cases:**
- Store and manage video scripts
- Track content performance metrics
- Coordinate ARG storyline elements
- Manage multi-channel content calendars
- Log production status and workflows

---

### 02_SSML_Generator.ipynb
**Purpose:** Generate high-quality voiceovers using Google Cloud Text-to-Speech with SSML markup.

**Features:**
- Google Cloud Text-to-Speech API integration
- SSML markup for advanced speech control
- Multiple voice options and presets
- Batch audio generation for video scripts
- Voice effects and customization
- Audio playback in Jupyter

**Prerequisites:**
1. Google Cloud project with Text-to-Speech API enabled
2. API key or service account credentials
3. Audio output directory (`2_Voiceover_Vault/`)

**Setup:**
```bash
# Install dependencies
pip install google-cloud-texttospeech python-dotenv IPython

# Configure environment
cp .env.example .env
# Edit .env and add ONE of:
# Option 1 (Recommended): GOOGLE_APPLICATION_CREDENTIALS=credentials/google_cloud_tts_credentials.json
# Option 2 (Simpler): GOOGLE_CLOUD_API_KEY=your_api_key_here
```

**Voice Presets:**
- **mysterious**: Slow, low-pitched for suspense
- **dramatic**: Very slow and deep for reveals
- **urgent**: Faster pace for urgent messages
- **neutral**: Normal speaking voice
- **whisper**: Soft and quiet for secrets

**Recommended Voices for AI Oracle:**
- `en-US-Neural2-D` (Male) - Deep and mysterious
- `en-US-Neural2-J` (Male) - Calm and measured
- `en-US-Studio-M` (Male) - Premium quality, dramatic
- `en-GB-Neural2-B` (Male) - British, sophisticated

**Cost Management:**
- Neural2 voices: $16 per 1M characters (best quality/cost ratio)
- Studio voices: $160 per 1M characters (premium)
- Keep requests under 5000 characters for best performance

---

## Quick Start Guide

### 1. Install Dependencies
```bash
cd /home/runner/work/AI_Oracle_Root/AI_Oracle_Root
pip install -r requirements.txt
```

### 2. Set Up Credentials
```bash
# Copy example environment file
cp .env.example .env

# Create credentials directory
mkdir -p credentials

# Add your Google Cloud credentials to credentials/
# - google_sheets_credentials.json (for Sheets API)
# - google_cloud_tts_credentials.json (for TTS API)
```

### 3. Configure Environment Variables
Edit `.env` file with your actual values:
```env
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials/google_sheets_credentials.json
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_APPLICATION_CREDENTIALS=credentials/google_cloud_tts_credentials.json
```

### 4. Launch Jupyter
```bash
# Start Jupyter notebook server
jupyter notebook

# Or use JupyterLab
jupyter lab
```

### 5. Open and Run Notebooks
- Navigate to `1_Script_Engine/Google_Sheets_Integration/01_Sheets_Integration.ipynb`
- Navigate to `1_Script_Engine/02_SSML_Generator.ipynb`
- Follow the step-by-step instructions in each notebook

---

## Workflow Integration

### Typical AI Oracle Content Creation Workflow:

1. **Script Development** (01_Sheets_Integration.ipynb)
   - Write and organize scripts in Google Sheets
   - Track production status
   - Manage ARG elements and hidden messages

2. **Voiceover Generation** (02_SSML_Generator.ipynb)
   - Add SSML markup to script for dramatic effect
   - Generate audio files with appropriate voice and settings
   - Save to `2_Voiceover_Vault/` directory

3. **Video Production** (5_Video_Production/)
   - Combine voiceover with visuals
   - Add ARG layers and hidden messages
   - Export final video

4. **Analytics Tracking** (01_Sheets_Integration.ipynb)
   - Log video performance metrics
   - Track ARG engagement
   - Analyze audience patterns

---

## Troubleshooting

### Common Issues:

**"Credentials file not found"**
- Ensure credentials JSON files are in the correct location
- Check that paths in `.env` are correct
- Verify file permissions

**"Spreadsheet not found"**
- Confirm the sheet ID is correct
- Share the Google Sheet with your service account email
- Check API is enabled in Google Cloud Console

**"API Error: PERMISSION_DENIED"**
- Enable the required API in Google Cloud Console
- Wait a few minutes for API activation
- Check service account has correct permissions

**"Audio generation fails"**
- Verify Text-to-Speech API is enabled
- Check API quotas and billing
- Validate SSML markup syntax
- Ensure credentials are valid

**JSON parsing errors in notebooks**
- Notebooks are valid JSON - do not edit raw JSON directly
- Use Jupyter to edit notebooks
- If corrupted, restore from git

---

## Best Practices

### Security:
- ✅ Keep credentials in `credentials/` directory (gitignored)
- ✅ Never commit `.env` or credentials to git
- ✅ Use service accounts for production
- ✅ Rotate API keys regularly
- ✅ Set up billing alerts in Google Cloud

### Cost Optimization:
- ✅ Use Neural2 voices for best quality/cost ratio
- ✅ Batch operations to minimize API calls
- ✅ Monitor API usage in Google Cloud Console
- ✅ Test with shorter scripts before full generation
- ✅ Cache generated audio files

### Code Quality:
- ✅ Use error handling in production code
- ✅ Log API calls and errors
- ✅ Validate data before writing to sheets
- ✅ Test SSML markup before batch generation
- ✅ Keep backups of working configurations

---

## Resources

### Documentation:
- [gspread Documentation](https://docs.gspread.org/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/docs)
- [SSML Reference](https://cloud.google.com/text-to-speech/docs/ssml)
- [pandas Documentation](https://pandas.pydata.org/docs/)

### Tutorials:
- [Setting up Google Cloud credentials](https://cloud.google.com/docs/authentication/getting-started)
- [SSML Tutorial](https://cloud.google.com/text-to-speech/docs/ssml-tutorial)
- [Voice Gallery](https://cloud.google.com/text-to-speech/docs/voices)

### Pricing:
- [Google Sheets API Quotas](https://developers.google.com/sheets/api/limits)
- [Text-to-Speech Pricing](https://cloud.google.com/text-to-speech/pricing)

---

## Support

For issues specific to these notebooks:
1. Check the troubleshooting section above
2. Review the inline documentation in each notebook
3. Verify your credentials and API enablement
4. Check the AI Oracle project documentation

For Google Cloud issues:
- [Google Cloud Support](https://cloud.google.com/support)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-cloud-platform)

---

## Contributing

When enhancing these notebooks:
1. Maintain clear documentation
2. Add error handling for edge cases
3. Test with various data types and sizes
4. Update this README with new features
5. Follow existing code style
6. Add examples for new functionality

---

**Last Updated:** 2024-01-15
**Version:** 1.0.0
**Maintainer:** AI Oracle Project Team
