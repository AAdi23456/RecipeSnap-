# RecipeSnap 🍳📸

**AI-Powered Smart Cooking Assistant**

RecipeSnap is an intelligent web application that analyzes photos of your fridge ingredients and generates personalized recipes using local AI models. No cloud APIs required!

![RecipeSnap Demo](https://img.shields.io/badge/Status-Ready-green) ![AI Models](https://img.shields.io/badge/AI-Local%20Models-blue) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

## ✨ Features

### 🎯 Core Features
- **Smart Ingredient Detection**: Upload or capture photos of your fridge contents
- **AI-Powered Recipe Generation**: Get personalized recipes based on available ingredients
- **Interactive Ingredient Management**: Mark ingredients as available/unavailable
- **Clean Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS

### 🎁 Bonus Features
- **Recipe Regeneration**: Get alternative recipes with the same ingredients
- **Voice Output**: Listen to recipes with text-to-speech functionality
- **Real-time Processing**: Fast AI inference with visual feedback

## 🏗️ Architecture

```
RecipeSnap/
├── frontend/          # Next.js React application
├── backend/           # FastAPI Python server
├── models/           # AI model implementations
└── setup.py          # Automated setup script
```

## 🤖 AI Models Used

All models run **locally** using Hugging Face Transformers:

### Image Analysis
- **nlpconnect/vit-gpt2-image-captioning**: Vision Transformer + GPT-2 for image captioning
- **facebook/detr-resnet-50**: DETR (Detection Transformer) for object detection

### Recipe Generation
- **microsoft/DialoGPT-medium**: Conversational AI for recipe generation
- **Template-based fallback**: Structured recipe templates for reliable output

### Text-to-Speech
- **Google Text-to-Speech (gTTS)**: High-quality voice synthesis

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- 4GB+ RAM (for AI models)
- 2GB+ free disk space

### Automated Setup

```bash
# Clone the repository
git clone https://github.com/your-username/RecipeSnap.git
cd RecipeSnap

# Run automated setup
python setup.py
```

The setup script will:
1. Install all Python and Node.js dependencies
2. Download and cache AI models (~1-2GB)
3. Create convenient start scripts
4. Verify installation

### Manual Setup

If you prefer manual setup:

#### Backend Setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Download AI models (first run only)
python start.py

# Start the backend server
python main.py
```

#### Frontend Setup
```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

## 🎮 Usage

1. **Start the Backend**: 
   ```bash
   cd backend && python main.py
   ```
   Backend runs on `http://localhost:8000`

2. **Start the Frontend**:
   ```bash
   cd frontend && npm run dev
   ```
   Frontend runs on `http://localhost:3000`

3. **Upload Photo**: Take or upload a photo of your fridge ingredients

4. **Review Ingredients**: Check detected ingredients and mark availability

5. **Get Recipe**: Receive AI-generated recipes with instructions

6. **Bonus Features**:
   - Click 🔄 to regenerate recipes
   - Click 🔊 to hear the recipe aloud
   - Toggle ingredients on/off to customize recipes

## 📁 Project Structure

```
RecipeSnap/
├── frontend/                    # Next.js Application
│   ├── app/                    # App router pages
│   │   ├── globals.css         # Global styles
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Main page component
│   ├── components/             # Reusable components
│   ├── package.json            # Node.js dependencies
│   ├── tailwind.config.js      # Tailwind CSS config
│   └── next.config.js          # Next.js configuration
│
├── backend/                     # FastAPI Server
│   ├── models/                 # AI model implementations
│   │   ├── __init__.py
│   │   ├── ingredient_detector.py  # Image analysis
│   │   ├── recipe_generator.py     # Recipe generation
│   │   └── text_to_speech.py       # TTS functionality
│   ├── main.py                 # FastAPI application
│   ├── start.py                # Model download script
│   └── requirements.txt        # Python dependencies
│
├── setup.py                    # Automated setup script
├── start-backend.sh            # Backend start script
├── start-frontend.sh           # Frontend start script
└── README.md                   # This file
```

## 🔧 API Endpoints

### Backend API (`http://localhost:8000`)

- `POST /detect-ingredients`: Upload image for ingredient detection
- `POST /generate-recipe`: Generate recipe from ingredients list
- `POST /text-to-speech`: Convert text to speech audio
- `GET /health`: Health check and model status

### Example API Usage

```javascript
// Detect ingredients
const formData = new FormData();
formData.append('image', imageFile);
const response = await fetch('/api/backend/detect-ingredients', {
  method: 'POST',
  body: formData
});

// Generate recipe
const recipe = await fetch('/api/backend/generate-recipe', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ ingredients: ['tomato', 'onion', 'garlic'] })
});
```

## ⚙️ Configuration

### Environment Variables

Create `.env` files for custom configuration:

**Backend (.env)**:
```bash
# Model settings
IMAGE_CAPTION_MODEL=nlpconnect/vit-gpt2-image-captioning
OBJECT_DETECTION_MODEL=facebook/detr-resnet-50
RECIPE_MODEL=microsoft/DialoGPT-medium

# Server settings
HOST=0.0.0.0
PORT=8000
```

**Frontend (.env.local)**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Model Configuration

You can swap models by editing the model names in:
- `backend/models/ingredient_detector.py`
- `backend/models/recipe_generator.py`

## 🐛 Troubleshooting

### Common Issues

**1. Models not downloading**
```bash
cd backend
python start.py
# Check your internet connection and disk space
```

**2. CORS errors**
- Ensure backend is running on port 8000
- Check Next.js proxy configuration in `next.config.js`

**3. Out of memory errors**
- Close other applications
- Consider using smaller models
- Ensure 4GB+ RAM available

**4. Module not found errors**
```bash
# Reinstall dependencies
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

### Performance Tips

- **First run**: Model download takes 5-10 minutes
- **Inference**: 2-5 seconds per image on modern hardware
- **Memory**: Models use ~2GB RAM when loaded
- **Storage**: Models cache requires ~1.5GB disk space

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face**: For the amazing Transformers library and model hub
- **Next.js**: For the excellent React framework
- **FastAPI**: For the high-performance Python web framework
- **Tailwind CSS**: For the utility-first CSS framework

## 🔗 Links

- [Hugging Face Models](https://huggingface.co/models)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Built with ❤️ using local AI models**

*No cloud dependencies • Privacy-focused • Open source*