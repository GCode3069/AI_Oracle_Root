# Connecting Cursor IDE to GitHub Copilot through the MCP Server

## Step-by-Step Instructions

### 1. Locate Your Configuration File
- For standard Cursor IDE users, your configuration file is located at:
  `C:\Users\[username]\AppData\Roaming\Cursor\User\settings.json`  
- For MCP-specific configurations, modify the same file to match the required settings.

### 2. JSON Configuration
Here’s the exact JSON configuration needed for the oracle-horror server setup:
```json
{
    "api": "key_e253fd568364ec9e18d4709396ae18b67da3c5f5dc964203c6407f4f1684d543",
    "local_file_path": "F:\AI_Oracle_Root\scarify\mcp_server\oracle_mcp_server.py"
}
```

### 3. Install Python Dependencies
Run the following commands in your terminal to install the necessary Python dependencies:
```bash
pip install -r requirements.txt
```
(Note: Ensure you have a `requirements.txt` file prepared with the necessary dependencies listed.)

### 4. Verify the Connection
- To ensure that Cursor IDE is properly connected to the MCP server:</br>
  - Open the Cursor IDE.
  - Navigate to the settings and ensure that the configuration matches the above setup.

### 5. Test Commands to Use Once Connected
Once connected, you can test using the following commands in the IDE:
```bash
echo "Test connection successful!"
```  
- If you see this output, your connection is successful!  

**Note:** If you encounter issues, double-check your configuration settings and API key validity.
