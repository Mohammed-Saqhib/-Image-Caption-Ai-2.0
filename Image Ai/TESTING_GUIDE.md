# 🧪 Testing Guide - Voice Language Selection

## ✅ Issue Fixed

The TTS engine has been completely rewritten to properly handle multi-language voice selection on macOS.

## 🔧 What Was Changed

### Updated Files:
1. **`src/tts_engine.py`** - Completely rewritten with:
   - Internal voice ID storage (`self.current_voice_id`)
   - Internal rate storage (`self.current_rate`)
   - Proper voice name extraction for macOS `say` command
   - Better error handling and debug output

## 🧪 How to Test

### Test 1: Hindi Voice
1. Open http://localhost:8501
2. Upload any image with text
3. Go to **🎧 Text-to-Speech** tab
4. Select **"Hindi"** from the language dropdown
5. You should see: `🎤 Selected Voice: **Lekha** (Hindi)`
6. Click **"🎵 Generate Audio"**
7. **Expected**: You should hear Hindi voice speaking
8. **Terminal Output**: Should show `Running command: say -v 'Lekha' -r 200 -o output_audio_xxx.wav`

### Test 2: Kannada Voice
1. Select **"Kannada"** from the language dropdown
2. You should see: `🎤 Selected Voice: **Soumya** (Kannada)`
3. Click **"🎵 Generate Audio"**
4. **Expected**: You should hear Kannada voice speaking
5. **Terminal Output**: Should show `Running command: say -v 'Soumya' -r 200 -o output_audio_xxx.wav`

### Test 3: Other Languages
Try these languages to verify:
- **English** → Should use "Aman" or "Tara" (Indian English)
- **Bengali** → Should use "Piya"
- **Tamil** → Should use "Vani"
- **Telugu** → Should use "Geeta"
- **German** → Should use "Anna"
- **French** → Should use "Thomas"

## 📋 Verification Checklist

- [ ] Voice name is displayed correctly when you select a language
- [ ] Terminal shows the correct voice name in the `say` command
- [ ] Audio is generated successfully (no errors)
- [ ] Audio plays in the selected language (not English)
- [ ] Download button works for audio files

## 🐛 If You Still Have Issues

1. **Check Terminal Output**: Look for the line `Running command: say -v '...'`
   - The voice name after `-v` should match your selected language

2. **Test Manually**:
   ```bash
   # Test Hindi
   say -v Lekha "नमस्ते"
   
   # Test Kannada
   say -v Soumya "ನಮಸ್ಕಾರ"
   ```

3. **Verify Voice is Available**:
   ```bash
   say -v ? | grep Lekha
   say -v ? | grep Soumya
   ```

## 📝 Debug Information

If audio generation fails, check the Streamlit terminal for debug output:
- `Running command: say -v 'VoiceName' -r 200 -o filename.wav`
- Any error messages from the `say` command

## ✨ Expected Behavior

**Before Fix**: All languages would speak in English (default voice)
**After Fix**: Each language uses its native voice:
- Hindi → Lekha (female Hindi voice)
- Kannada → Soumya (female Kannada voice)
- Bengali → Piya (female Bengali voice)
- etc.

## 🎯 Success Criteria

✅ Selecting "Hindi" generates audio in Hindi voice
✅ Selecting "Kannada" generates audio in Kannada voice
✅ Selecting "English" generates audio in English voice
✅ Download button provides the correct audio file
✅ No errors in terminal or UI

---

**Current Status**: App running at http://localhost:8501
**Last Updated**: November 22, 2025
