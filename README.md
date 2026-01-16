# Spotify Token Generator for SpotifyPlus

This devcontainer provides a simple environment to generate Spotify OAuth2 tokens for the [SpotifyPlus Home Assistant Integration](https://github.com/thlucas1/homeassistantcomponent_spotifyplus).

## What This Does

This environment downloads and runs the official [AuthTokenGenerator.py](https://github.com/thlucas1/SpotifyWebApiPython/blob/master/docs/include/samplecode/ZeroconfConnect/AuthTokenGenerator.py) script, then starts a web server so you can easily download the generated token file.

Tokens are needed for controlling Spotify Connect devices like:
- Sonos speakers
- Google Chromecast devices
- Other devices using `authorization_code` token type

## ⚠️ Important: Use Locally, Not in Codespaces

**This tool should be run in a local VS Code Dev Container, not GitHub Codespaces.**

GitHub Codespaces uses forwarded port URLs (like `https://xyz-8080.app.github.dev`) that:
- Change with each codespace instance
- Cannot be pre-registered as Spotify OAuth redirect URIs
- Will cause the OAuth flow to fail

### Recommended Setup

**Prerequisites:**
- [VS Code](https://code.visualstudio.com/download) installed
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

**Steps:**

1. **Clone the repository locally:**
   ```bash
   git clone https://github.com/rvanmaanen/spotifyplus_token_generator.git
   cd spotifyplus_token_generator
   ```

2. **Open in VS Code and reopen in container:**
   - Open folder in VS Code
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Select "Dev Containers: Reopen in Container"
   - Wait for container to build

3. **Add Redirect URI to your Spotify Developer App:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Click your application → Settings
   - Add Redirect URI: `http://127.0.0.1:8080/` (with trailing slash!)
   - Click Save

4. **Run the setup script:**
   ```bash
   python setup_spotify_token.py
   ```

4. **Follow the prompts:**
   - The official script will run and guide you through authorization
   - Your browser will open for Spotify login
   - Authorize the application

5. **Download the token file:**
   - After successful generation, a download server starts automatically
   - Open in your browser: `http://localhost:8000/spotifyplus_tokens.json`
   - The file downloads automatically
   - Press `Ctrl+C` to stop the server when done

6. **Copy to Home Assistant:**
   - Upload the downloaded file to your HA server
   - Destination: `/config/.storage/spotifyplus_tokens.json`
   - Restart Home Assistant (if needed)

## What Happens

1. **Downloads** the official `AuthTokenGenerator.py` script
2. **Runs** the script to generate your OAuth2 token
3. **Starts** a web server on port 8000 for easy download

## Configuration (Optional)

If you want to customize settings, edit `AuthTokenGenerator.py` after it's downloaded:

- `tokenProfileId` - Your Spotify Login ID (None = auto-detect)
- `tokenStorageFile` - Output filename (default: `spotifyplus_tokens.json`)
- `redirectUriPort` - Port for OAuth callback (default: 8080)

To find your Login ID:
1. Visit [Get Current Users Profile](https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile)
2. Click "Try It"
3. Look for the `id` field

## Multiple Accounts

To add multiple Spotify accounts:
1. Run `python setup_spotify_token.py` for the first account
2. Download the token file
3. Run again for the second account
4. Both tokens will be stored in the same file

## Troubleshooting

### "Invalid redirect URI" error
- Add `http://127.0.0.1:8080/` to your Spotify Developer App settings
- Must include the trailing slash
- Case-sensitive

### Port already in use
- **Port 8080**: Close any apps using this port (needed for OAuth callback)
- **Port 8000**: Change the port in `setup_spotify_token.py` if needed

### Browser doesn't open
- The script will display a URL to copy/paste manually

### Can't access download link
- If running in a devcontainer, the URL works from your host browser
- Alternatively, just copy the `spotifyplus_tokens.json` file manually

## Manual Alternative

If you prefer to run the official script directly (this requires you to setup python):
```bash
# Download the script
curl -O https://raw.githubusercontent.com/thlucas1/SpotifyWebApiPython/master/docs/include/samplecode/ZeroconfConnect/AuthTokenGenerator.py

# Run it
python AuthTokenGenerator.py

# Copy the generated file
cp spotifyplus_tokens.json /path/to/homeassistant/config/.storage/
```

## References

- [Official Script Source](https://github.com/thlucas1/SpotifyWebApiPython/blob/master/docs/include/samplecode/ZeroconfConnect/AuthTokenGenerator.py)
- [SpotifyPlus Wiki - Token Creation](https://github.com/thlucas1/homeassistantcomponent_spotifyplus/wiki/Device-Configuration-Options#token-creation-instructions)
- [SpotifyPlus Integration](https://github.com/thlucas1/homeassistantcomponent_spotifyplus)
- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
