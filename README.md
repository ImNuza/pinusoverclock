# ArtSpace - Virtual Art Gallery

> **PINUS Hack 2026 | Track 4: AI for Virtual Viewing & Decision Support**

An immersive art marketplace that lets you visualize artworks in your real space using AR and LiDAR technology.

![ArtSpace Preview](https://img.shields.io/badge/AR-Enabled-blueviolet) ![LiDAR](https://img.shields.io/badge/LiDAR-Supported-green) ![Mobile](https://img.shields.io/badge/Mobile-First-orange)

## Features

### 🎨 Art Marketplace
- Browse curated artwork collections
- View detailed artwork information
- See real-world dimensions (Width × Height × Depth)
- Filter by category

### 📱 AR Visualization
- **No marker required** - Point and place anywhere
- Works on iOS (Safari) and Android (Chrome)
- Automatic LiDAR support on iPhone Pro/iPad Pro
- Real-scale artwork placement

### 📐 Dimension Display
- Accurate artwork measurements in centimeters
- Visual dimension breakdown
- Scale reference for your space

## Quick Start

### Option 1: Live Demo
Visit: **https://imnuza.github.io/pinusoverclock/**

### Option 2: Run Locally
```bash
git clone https://github.com/ImNuza/pinusoverclock.git
cd pinusoverclock
python3 -m http.server 8000
```
Open `http://localhost:8000` on your phone.

## How to Use

1. **Browse** - Scroll through the artwork gallery
2. **Select** - Tap any artwork card to see details
3. **View in AR** - Tap the "View in AR" button
4. **Place** - Point your camera and tap to place the artwork
5. **Explore** - Walk around to see the artwork from different angles

## AR Compatibility

| Device | AR Support | LiDAR |
|--------|------------|-------|
| iPhone 12 Pro+ | ✅ Full | ✅ Yes |
| iPhone 12/13/14 | ✅ Full | ❌ No |
| Android (ARCore) | ✅ Full | ❌ No |
| Desktop | ⚠️ 3D Only | ❌ No |

## Technology Stack

- **Model-Viewer** - Google's 3D/AR web component
- **WebXR** - Immersive web experiences
- **AR Quick Look** - Apple's native AR (iOS)
- **Scene Viewer** - Google's native AR (Android)

## Project Structure

```
pinusoverclock/
├── index.html          # Main application
├── models/             # 3D artwork models (.glb)
│   └── decor_wall.glb
├── markers/            # Legacy AR markers
└── README.md
```

## Adding New Artworks

1. Export your 3D model as `.glb` format
2. Place in the `models/` directory
3. Add entry to the `artworks` array in `index.html`:

```javascript
{
    id: 5,
    title: "Your Artwork",
    artist: "Artist Name",
    medium: "Medium Type",
    year: "2024",
    price: "$1,000",
    dimensions: { width: 50, height: 70, depth: 10 },
    model: "models/your_model.glb",
    badge: "New",
    category: "modern"
}
```

## Team Pinusoverclock

| Name | Role |
|------|------|
| Nuza | Project Lead, UX |
| Matthew | Business Logic, Demo |
| Michael | Lead Developer |
| Bryan | Frontend Developer |
| Noah | Backend, AI Integration |

## Acknowledgments

- PINUS Hack 2026 Organizers
- Manus & Xtremax (Sponsors)
- Google Model-Viewer Team

---

**Made with ❤️ for PINUS Hack 2026**
