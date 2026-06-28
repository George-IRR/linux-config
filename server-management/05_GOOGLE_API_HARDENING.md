# 05: Google Drive API Hardening & Private Credentials
Configuring proprietary API keys in Rclone to completely isolate from the global query pool and eliminate 'Quota Exceeded' errors.

## 1. Redirect Configuration in Google Cloud Console
For local terminal applications (Rclone CLI) to intercept the OAuth token without a public web server, the loopback mechanism must be strictly configured:
1. Access Google Cloud Console -> APIs & Services -> Credentials.
2. Edit the OAuth 2.0 Client IDs key.
3. Navigate to the Authorized redirect URIs section.
4. Remove third-party URLs (e.g., Alist) and add exclusively the native local OpenSSH/Rclone address:
   `http://127.0.0.1:53682/`
5. Save changes (the application will bypass the redirect_uri_mismatch error).

## 2. Direct Injection into the rclone.conf Structure
Reconfiguring the profile from scratch is not necessary. Open `/home/george/.config/rclone/rclone.conf` and add the keys directly under the target profile:

```ini
[GoogleDriveMain190]
type = drive
client_id = YOUR_OWN_CLIENT_ID.apps.googleusercontent.com
client_secret = YOUR_OWN_CLIENT_SECRET
```

### Connection Reauthorization (Headless / Local)
Since the application identifier has changed, the old token becomes invalid. Run the refresh command:

```bash
rclone config reconnect GoogleDriveMain190:
```
Follow the link generated in your browser, accept the "Google hasn’t verified this app" warning (Advanced -> Go to Rclone), and complete the validation.

## 3. Absolute Limits and Quota Matrix
Once your own Client ID is configured, limits are dictated exclusively by Google's terms per account and cannot be modified by software:

| Parameter | Absolute Limit | Behavior on Reaching / Error |
| :--- | :--- | :--- |
| **API Queries** | 10,000 requests / minute | Fully allocated to your key. Eliminates bottlenecks for fast commands like ls / sync. |
| **Daily Upload** | 750 GB / 24 hours | Cumulative value per account. Upon reaching, upload freezes with `403 Storage/User Rate Limit Exceeded` error. |
| **Daily Download** | 10 TB / 24 hours | Maximum data extraction limit in 24-hour windows. |
| **File Size** | 5 TB maximum | If you upload a single 2 TB file (above the 750 GB threshold), Google will allow its completion but will block any other uploads for 24 hours. |
