# Mini COLMAP Viewer

A lightweight web-based viewer for COLMAP reconstruction results (point clouds and camera poses).

## 🎯 Project Goal

- **Showcase full-stack development skills** (Python + JavaScript + Web)
- **Improve upon the official COLMAP viewer** with better UX for texture and perspective visualization
- **Build a practical tool** for visualizing 3D reconstruction results
- **Deepen JavaScript/Web development knowledge** through this project

## ✨ Features

### MVP (Phase 1)
- ✅ Upload PLY point clouds + JSON camera data
- ✅ Display 3D point clouds with interactive controls (rotate, zoom, pan)
- ✅ Visualize camera poses and viewing directions
- ✅ Adjust point size and color
- ✅ Support original RGB colors from PLY files

### Future Features (Phase 2+)
- 📸 Export screenshots
- 🔲 Mesh visualization
- 🎨 Advanced coloring (by height, distance, intensity)
- 🌍 Textured surface rendering

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

```bash
# Clone the repository
git clone https://github.com/duanshea/mini-colmap-viewer.git
cd mini-colmap-viewer

# Install Python dependencies
pip install -r backend/requirements.txt

# Run the Flask server
python backend/app.py
