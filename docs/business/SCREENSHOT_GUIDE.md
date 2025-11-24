# 📸 SCREENSHOT CAPTURE GUIDE
## **Step-by-Step Instructions for Creating Visual Assets**

*Created: October 1, 2025*

---

## 🎯 **PRIORITY ORDER**

### **HIGH PRIORITY** (Do These First - 2 hours)
1. ✅ Home page of each demo (5 screenshots)
2. ✅ Before/After comparison (1 composite image)
3. ✅ Navigation showcase (1 screenshot)
4. ✅ Theme comparison grid (1 composite image)

### **MEDIUM PRIORITY** (If Time Permits - 1 hour)
5. Content page example from each demo (5 screenshots)
6. Mobile responsive views (2-3 screenshots)
7. Search functionality demo (1 screenshot)

### **LOW PRIORITY** (Nice to Have - 1 hour)
8. Dark mode examples
9. Deployment script running
10. GitBook vs GitHub Wiki comparison

---

## 🛠️ **SETUP (One-Time, 15 minutes)**

### **Install Required Tools**

#### **Option 1: GitBook Local Server (Recommended)**
```bash
# Install GitBook CLI
npm install -g gitbook-cli

# Verify installation
gitbook --version
```

#### **Option 2: Simple HTTP Server (Alternative)**
```bash
# Python 3 (already installed)
python3 -m http.server 4000

# or Node.js
npx http-server -p 4000
```

#### **Screenshot Tool**

**macOS:**
```bash
# Built-in: Cmd+Shift+4 (select area)
# Built-in: Cmd+Shift+5 (screenshot toolbar)

# Or install for better features:
brew install --cask cleanshot
```

**Windows:**
```bash
# Built-in: Windows+Shift+S (Snipping Tool)

# Or install:
# Download ShareX (free): https://getsharex.com/
```

**Linux:**
```bash
# Install Flameshot
sudo apt install flameshot

# Or use GNOME Screenshot
gnome-screenshot -i
```

---

## 📸 **SCREENSHOT SPECIFICATIONS**

### **Desktop Screenshots**
```
Resolution: 1920×1080 (or 2560×1440 for Retina)
Format: PNG (lossless) or WebP (smaller files)
Browser: Chrome or Firefox (latest)
Zoom: 100% (no browser zoom)
Window: Maximized, remove browser chrome if possible
```

### **Mobile Screenshots**
```
Resolution: 375×812 (iPhone 14 Pro)
Format: PNG
Device: Chrome DevTools device emulation
Orientation: Portrait
```

### **File Naming Convention**
```
screenshots/
├── desktop/
│   ├── 01-api-professional-home.png
│   ├── 02-api-professional-navigation.png
│   ├── 03-webapp-modern-home.png
│   ├── 04-cli-technical-home.png
│   ├── 05-library-academic-home.png
│   ├── 06-mobile-startup-home.png
│   ├── 07-before-after-comparison.png
│   └── 08-theme-showcase.png
├── mobile/
│   ├── api-mobile.png
│   ├── webapp-mobile.png
│   └── cli-mobile.png
└── social/
    ├── twitter-comparison.png
    ├── twitter-themes.png
    └── instagram-carousel-1.png
```

---

## 📋 **STEP-BY-STEP INSTRUCTIONS**

### **SCREENSHOT 1: API Documentation (Professional Theme)**

#### **Setup (2 minutes)**
```bash
cd /mnt/c/Users/Mishka/Documents/GitHub/github-repo-manager
cd portfolio-demos/api-example/generated-docs/gitbook

# Start GitBook server
gitbook serve
# Server starts at http://localhost:4000
```

#### **Capture (1 minute)**
1. Open browser to http://localhost:4000
2. Wait for page to fully load (2 seconds)
3. Make browser window full width (1920px+)
4. Scroll to top of page
5. Take screenshot (Cmd+Shift+4 or Windows+Shift+S)
6. Select entire visible area
7. Save as: `screenshots/desktop/01-api-professional-home.png`

#### **What to Capture**
```
Should include:
✓ Page header with project name
✓ Navigation sidebar (left)
✓ Main content area (center)
✓ At least 2-3 sections visible
✓ Professional blue theme clearly visible
✓ Clean, uncluttered view
```

**Expected Result:**
- File size: 200-500 KB
- Resolution: 1920×1080 or similar
- Clear, readable text
- Professional appearance

---

### **SCREENSHOT 2: Web App Documentation (Modern Theme)**

#### **Setup**
```bash
cd /mnt/c/Users/Mishka/Documents/GitHub/github-repo-manager
cd portfolio-demos/webapp-example/generated-docs/gitbook

gitbook serve
# Opens at http://localhost:4000
```

#### **Capture**
Same process as Screenshot 1, but:
- **Focus**: Capture the gradient header
- **Key Element**: Modern vibrant colors should be prominent
- Save as: `screenshots/desktop/03-webapp-modern-home.png`

**What Makes This Different:**
- Vibrant gradient colors (purple/pink)
- Modern visual style
- Bold typography
- Contemporary design elements

---

### **SCREENSHOT 3: CLI Tool Documentation (Technical Theme)**

#### **Setup**
```bash
cd /mnt/c/Users/Mishka/Documents/GitHub/github-repo-manager
cd portfolio-demos/cli-example/generated-docs/gitbook

gitbook serve
```

#### **Capture**
Same process, but:
- **Focus**: Dark background with terminal-style text
- **Key Element**: Monospace fonts, code blocks
- Save as: `screenshots/desktop/04-cli-technical-home.png`

**What Makes This Different:**
- Dark theme (dark navy/black background)
- Terminal green text accents
- Monospace typography
- Technical, code-focused design

---

### **SCREENSHOT 4: Library Documentation (Academic Theme)**

#### **Setup**
```bash
cd /mnt/c/Users/Mishka/Documents/GitHub/github-repo-manager
cd portfolio-demos/library-example/generated-docs/gitbook

gitbook serve
```

#### **Capture**
- **Focus**: Scholarly appearance with serif fonts
- **Key Element**: Clean, academic formatting
- Save as: `screenshots/desktop/05-library-academic-home.png`

---

### **SCREENSHOT 5: Mobile App Documentation (Startup Theme)**

#### **Setup**
```bash
cd /mnt/c/Users/Mishka/Documents/GitHub/github-repo-manager
cd portfolio-demos/mobile-example/generated-docs/gitbook

gitbook serve
```

#### **Capture**
- **Focus**: Bold, energetic colors (orange/purple/pink)
- **Key Element**: Fun, playful design
- Save as: `screenshots/desktop/06-mobile-startup-home.png`

---

### **SCREENSHOT 6: Navigation Showcase**

#### **Setup**
Use any of the above demos (recommend API example)

#### **Capture (Special)**
1. Open documentation site
2. **Click to expand all navigation items**
3. Make sure sidebar is fully visible
4. Capture with sidebar prominent
5. Save as: `screenshots/desktop/02-navigation-showcase.png`

**Should Show:**
- Full navigation tree expanded
- Multiple sections visible
- Clean hierarchy
- Easy-to-use interface

---

### **SCREENSHOT 7: Before/After Comparison** ⭐ **MOST IMPORTANT**

This requires creating a composite image.

#### **Method A: Side-by-Side Screenshot**

**Before Side (Left):**
```bash
# Open the basic README.md in GitHub
# Show: portfolio-demos/api-example/README.md
# Capture: Just the README content (raw text)
```

**After Side (Right):**
```bash
# Open the generated GitBook
cd portfolio-demos/api-example/generated-docs/gitbook
gitbook serve
# Capture: The beautiful documentation site
```

#### **Method B: Create Composite in Figma/Photoshop**

1. Take screenshot of basic README.md
2. Take screenshot of generated docs
3. Open in image editor
4. Create 1920×1080 canvas
5. Place screenshots side-by-side
6. Add dividing line
7. Add labels: "BEFORE" (left) and "AFTER" (right)
8. Add metrics below each:

```
BEFORE:
- 50 lines
- 30 minutes
- $50 value
- No navigation
- No search

AFTER:
- 15 pages
- 5 minutes
- $2,000 value
- Full navigation
- Built-in search
```

**Save as:** `screenshots/desktop/07-before-after-comparison.png`

**This is your #1 marketing asset!**

---

### **SCREENSHOT 8: Theme Showcase Grid**

Create a composite showing all 5 themes.

#### **Method A: Multiple Browser Windows**
1. Open all 5 demos in separate browser windows
2. Arrange in grid pattern (2×3)
3. Use tool like "Shift It" (Mac) or "FancyZones" (Windows)
4. Capture entire screen
5. Crop to show just the windows

#### **Method B: Individual Screenshots → Composite**
1. Take individual screenshots of each theme
2. Resize each to 600×400px
3. Create composite in image editor:
   - Canvas: 1920×1080
   - Arrange 5 screenshots in grid
   - Add labels for each theme
4. Save as: `screenshots/desktop/08-theme-showcase.png`

**Grid Layout:**
```
┌─────────────┬─────────────┬─────────────┐
│ Professional│   Modern    │  Technical  │
│   (API)     │  (Web App)  │    (CLI)    │
├─────────────┼─────────────┴─────────────┤
│  Academic   │     Startup                │
│  (Library)  │    (Mobile)                │
└─────────────┴───────────────────────────┘
```

---

## 📱 **MOBILE SCREENSHOTS** (Medium Priority)

### **Setup Chrome DevTools**
1. Open any demo in Chrome
2. Press F12 (open DevTools)
3. Click device icon (top-left of DevTools)
4. Select "iPhone 14 Pro" from dropdown
5. Set zoom to 100%

### **Capture**
1. Right-click on the mobile preview
2. Select "Capture screenshot" or use regular screenshot tool
3. Crop to just the device frame
4. Save as: `screenshots/mobile/[project]-mobile.png`

**Recommended**: Capture 2-3 mobile views to show responsive design

---

## 🎨 **SOCIAL MEDIA GRAPHICS** (High Priority)

### **Twitter/X Post Image (1200×675)**

#### **Before/After Comparison**
Use the composite from Screenshot 7, but:
1. Resize to 1200×675
2. Add text overlay:
   - Top: "DOCUMENTATION: BEFORE vs AFTER"
   - Bottom: "240× faster | $500 vs $2,000"
3. Increase font sizes for readability
4. Save as: `screenshots/social/twitter-comparison.png`

#### **Theme Showcase**
1. Create 1200×675 canvas
2. Add title: "8 PROFESSIONAL THEMES"
3. Show 3-4 theme previews (scaled down)
4. Add text: "Choose the perfect style for your docs"
5. Save as: `screenshots/social/twitter-themes.png`

---

## 🖼️ **CREATING COMPOSITES** (For Non-Designers)

### **Option 1: Figma (Free)**
1. Sign up at figma.com
2. Create new file (1920×1080)
3. Import screenshots (drag & drop)
4. Arrange and add text
5. Export as PNG

### **Option 2: Canva (Free)**
1. Go to canva.com
2. Create "Custom Size" (1920×1080)
3. Upload screenshots
4. Use templates or create from scratch
5. Download as PNG

### **Option 3: PowerPoint/Keynote**
1. Create slide (16:9 ratio)
2. Insert screenshots
3. Add text and shapes
4. Export as image (File → Export → PNG)

---

## ✅ **QUALITY CHECKLIST**

Before saving each screenshot:

**Technical Quality:**
- [ ] Resolution is 1920×1080 or higher
- [ ] Image is sharp and clear (not blurry)
- [ ] Text is readable
- [ ] No browser UI visible (unless intentional)
- [ ] No personal information visible
- [ ] File size is reasonable (< 1 MB)

**Content Quality:**
- [ ] Shows the key theme/feature
- [ ] Represents the product well
- [ ] Looks professional
- [ ] Colors are accurate
- [ ] Layout is clean and uncluttered

**Naming:**
- [ ] Follows naming convention
- [ ] Numbered for easy sorting
- [ ] Descriptive name
- [ ] In correct folder

---

## 🚀 **QUICK BATCH PROCESS** (If Short on Time)

### **30-Minute Speed Run**

**Minute 0-10: Setup**
- Start all 5 GitBook servers in separate terminals
- Open all 5 in browser tabs
- Open screenshot tool

**Minute 10-20: Capture**
- Rapid screenshot of each homepage (5 screenshots)
- One navigation showcase
- That's 6 screenshots done

**Minute 20-30: Composites**
- Create quick before/after in PowerPoint
- Export as image
- Done!

**Result**: 7 essential images ready for marketing

---

## 📂 **FINAL FILE STRUCTURE**

```
github-repo-manager/
└── screenshots/
    ├── desktop/
    │   ├── 01-api-professional-home.png
    │   ├── 02-navigation-showcase.png
    │   ├── 03-webapp-modern-home.png
    │   ├── 04-cli-technical-home.png
    │   ├── 05-library-academic-home.png
    │   ├── 06-mobile-startup-home.png
    │   ├── 07-before-after-comparison.png ⭐ KEY
    │   └── 08-theme-showcase.png
    ├── mobile/
    │   ├── api-mobile.png
    │   ├── webapp-mobile.png
    │   └── cli-mobile.png
    └── social/
        ├── twitter-comparison.png ⭐ KEY
        ├── twitter-themes.png
        ├── linkedin-post.png
        └── instagram-carousel-1.png
```

---

## 🎯 **NEXT STEPS AFTER SCREENSHOTS**

Once you have your screenshots:

1. **Upload to Landing Page**
   - Hero section: Before/after comparison
   - Portfolio section: All 5 theme screenshots
   - Features section: Navigation showcase

2. **Social Media Posts**
   - Twitter: Post with before/after comparison
   - LinkedIn: Portfolio showcase
   - Reddit: Include screenshots in posts

3. **Client Presentations**
   - Create PDF deck with screenshots
   - Show during sales calls
   - Include in proposals

4. **Product Hunt Launch**
   - Gallery images (4-8 screenshots)
   - Thumbnail image
   - Video demo with screenshots

---

## 💡 **PRO TIPS**

### **For Better Screenshots:**
1. **Clean your browser**: Close unnecessary tabs
2. **Use incognito mode**: No extensions, clean UI
3. **Disable browser zoom**: Always 100%
4. **Take multiple shots**: Choose the best one
5. **Natural lighting**: If photographing screen

### **For Composites:**
1. **Maintain aspect ratios**: Don't distort images
2. **Use consistent spacing**: Looks more professional
3. **Add subtle shadows**: Creates depth
4. **Use brand colors**: Maintains consistency
5. **Keep text minimal**: Let images speak

### **Time-Saving:**
1. **Batch capture**: Do all similar shots at once
2. **Use templates**: Create once, reuse
3. **Automate**: Use tools like Puppeteer for bulk screenshots
4. **Outsource**: Fiverr for $5-20 if needed

---

## ⏱️ **TIME ESTIMATES**

| Task | Time | Priority |
|------|------|----------|
| Setup tools | 15 min | High |
| Capture 5 theme home pages | 15 min | High |
| Navigation showcase | 5 min | High |
| Before/after composite | 20 min | High |
| Theme showcase grid | 15 min | High |
| Mobile screenshots | 15 min | Medium |
| Social media graphics | 30 min | High |
| Polish and organize | 15 min | Medium |
| **TOTAL** | **2-3 hours** | - |

---

## 🎉 **COMPLETION CHECKLIST**

### **Minimum Viable Screenshots (30 min)**
- [ ] 1 before/after comparison
- [ ] 5 theme home pages
- [ ] 1 social media graphic

### **Full Portfolio (2 hours)**
- [ ] All 5 theme home pages
- [ ] Navigation showcase
- [ ] Before/after comparison
- [ ] Theme showcase grid
- [ ] 2-3 mobile views
- [ ] 3-4 social media graphics

### **Complete Marketing Assets (3 hours)**
- [ ] All desktop screenshots
- [ ] All mobile screenshots
- [ ] All social media graphics
- [ ] Video thumbnail
- [ ] Landing page hero image
- [ ] Product Hunt gallery

---

**Once screenshots are complete, move to creating the landing page and launching the free offer!** 🚀

---

*Follow this guide step-by-step and you'll have all visual assets ready for launch in 2-3 hours.* 📸
