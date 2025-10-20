# macOS Code Signing Setup Guide

**Use this guide once your Apple Developer Program enrollment is approved (24-48 hours).**

---

## Prerequisites

✅ Apple Developer Program membership active ($99/year)  
✅ macOS computer (for certificate generation)  
✅ Xcode Command Line Tools installed: `xcode-select --install`

---

## Step 1: Generate Developer ID Certificate

1. **Go to Apple Developer Portal:**
   - Visit: https://developer.apple.com/account/resources/certificates/list
   - Sign in with your Apple ID

2. **Create Certificate:**
   - Click the **"+"** button (or "Create a Certificate")
   - Select **"Developer ID Application"**
   - Click **"Continue"**

3. **Create Certificate Signing Request (CSR):**
   
   On your Mac:
   ```bash
   # Open Keychain Access
   open "/Applications/Utilities/Keychain Access.app"
   ```
   
   - Menu: **Keychain Access → Certificate Assistant → Request a Certificate from a Certificate Authority**
   - **User Email:** your.email@example.com
   - **Common Name:** "Todd Edwards" (or your name)
   - **CA Email:** Leave blank
   - Select: **"Saved to disk"**
   - Click **"Continue"**
   - Save as: `CertificateSigningRequest.certSigningRequest`

4. **Upload CSR to Apple:**
   - Back in the browser, click **"Choose File"**
   - Upload the `.certSigningRequest` file
   - Click **"Continue"**

5. **Download Certificate:**
   - Click **"Download"**
   - Save: `developerID_application.cer`
   - **Double-click** to install it in Keychain

6. **Verify Installation:**
   ```bash
   # List your signing identities
   security find-identity -v -p codesigning
   ```
   
   You should see something like:
   ```
   1) ABC123... "Developer ID Application: Todd Edwards (TEAM_ID)"
   ```
   
   **Copy that full identity name** - you'll need it!

---

## Step 2: Get App-Specific Password (for Notarization)

1. **Go to Apple ID:**
   - Visit: https://appleid.apple.com/account/manage
   - Sign in

2. **Generate App-Specific Password:**
   - Scroll to **"App-Specific Passwords"**
   - Click **"Generate Password"**
   - Label: "DocMiner Notarization"
   - **Save this password** - you'll need it for notarization

---

## Step 3: Set Up Environment Variables

Add these to your shell profile (`~/.zshrc` or `~/.bash_profile`):

```bash
# Apple Developer Code Signing
export APPLE_DEVELOPER_ID="Developer ID Application: Todd Edwards (TEAM_ID)"
export APPLE_ID="your.email@apple.com"
export APPLE_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"  # From Step 2
export APPLE_TEAM_ID="YOUR_TEAM_ID"  # Find at developer.apple.com/account
```

Then reload:
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

---

## Step 4: Update Build Script for Code Signing

We'll modify `build_files/DocMiner6.3.spec` to include signing:

```python
# After the BUNDLE section, add signing commands
import subprocess

# Code sign the app bundle
subprocess.run([
    'codesign',
    '--force',
    '--sign', os.environ.get('APPLE_DEVELOPER_ID'),
    '--timestamp',
    '--options', 'runtime',
    '--entitlements', 'build_files/entitlements.plist',
    '--deep',
    'dist/DocMiner6.3.app'
], check=True)

# Verify signature
subprocess.run([
    'codesign',
    '--verify',
    '--verbose',
    'dist/DocMiner6.3.app'
], check=True)
```

---

## Step 5: Create Entitlements File

Create `build_files/entitlements.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
</dict>
</plist>
```

This allows PyInstaller apps to work with hardened runtime.

---

## Step 6: Notarize the DMG

After building the DMG:

```bash
# Submit for notarization
xcrun notarytool submit \
    DocMiner-6.3.0-macOS.dmg \
    --apple-id "$APPLE_ID" \
    --password "$APPLE_APP_PASSWORD" \
    --team-id "$APPLE_TEAM_ID" \
    --wait

# Staple the notarization ticket
xcrun stapler staple DocMiner-6.3.0-macOS.dmg

# Verify
xcrun stapler validate DocMiner-6.3.0-macOS.dmg
```

---

## Step 7: Test on Clean Mac

1. **Download your signed DMG** on a different Mac (or clean user account)
2. **Double-click** to open
3. **Drag to Applications**
4. **Double-click** to launch

**Expected result:** App opens immediately with **NO security warnings!** ✅

---

## Automation: GitHub Actions

Once manual signing works, we can automate it in `.github/workflows/build-on-tag.yml`:

```yaml
- name: Import Code Signing Certificate
  env:
    CERTIFICATE_BASE64: ${{ secrets.APPLE_CERTIFICATE_BASE64 }}
    CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
  run: |
    # Create keychain and import certificate
    security create-keychain -p actions build.keychain
    security import certificate.p12 -k build.keychain -P "$CERTIFICATE_PASSWORD"
    security set-keychain-settings -lut 21600 build.keychain
    security unlock-keychain -p actions build.keychain

- name: Code Sign Application
  run: |
    codesign --force --sign "$APPLE_DEVELOPER_ID" \
      --timestamp --options runtime \
      --entitlements build_files/entitlements.plist \
      dist/DocMiner6.3.app

- name: Notarize DMG
  run: |
    xcrun notarytool submit DocMiner.dmg \
      --apple-id "$APPLE_ID" \
      --password "$APPLE_APP_PASSWORD" \
      --team-id "$APPLE_TEAM_ID" --wait
    xcrun stapler staple DocMiner.dmg
```

---

## Troubleshooting

### "No identity found"
```bash
security find-identity -v -p codesigning
```
Make sure the certificate is in your keychain.

### "Unable to validate notarization"
Check status:
```bash
xcrun notarytool log <submission-id> --apple-id "$APPLE_ID" --password "$APPLE_APP_PASSWORD"
```

### "App is damaged and can't be opened"
This means signature is broken. Rebuild and re-sign.

---

## Cost Summary

- ✅ Apple Developer Program: $99/year
- ✅ Code Signing: Included
- ✅ Notarization: Included (unlimited)
- ✅ Certificate renewal: Automatic (with active membership)

---

## Next Steps After Setup

1. ✅ Test signed build locally
2. ✅ Upload to GitHub release
3. ✅ Have a friend test download (no warnings!)
4. ✅ Automate in CI/CD
5. ✅ Update README to remove security workaround instructions

---

**Questions?** Ping me when you get the Apple approval email and we'll walk through this together!
