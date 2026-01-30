"""
ArtSpace AI Room Analyzer Backend
Simple Flask server to proxy OpenAI Vision API calls securely
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize OpenAI client (uses OPENAI_API_KEY from environment)
client = OpenAI()

# Artwork database for matching
ARTWORKS = [
    {"id": 101, "title": "Starry Night", "artist": "Vincent van Gogh", "colors": ["blue", "yellow", "dark"], "mood": ["dramatic", "expressive"], "style": "Post-Impressionism"},
    {"id": 102, "title": "Water Lilies", "artist": "Claude Monet", "colors": ["green", "blue", "pink"], "mood": ["calm", "serene"], "style": "Impressionism"},
    {"id": 103, "title": "Café Terrace at Night", "artist": "Vincent van Gogh", "colors": ["yellow", "blue", "warm"], "mood": ["cozy", "inviting"], "style": "Post-Impressionism"},
    {"id": 104, "title": "Mona Lisa", "artist": "Leonardo da Vinci", "colors": ["brown", "earth", "neutral"], "mood": ["mysterious", "elegant"], "style": "Renaissance"},
    {"id": 105, "title": "Improvisation 4", "artist": "Wassily Kandinsky", "colors": ["multicolor", "vibrant"], "mood": ["energetic", "dynamic"], "style": "Abstract"},
    {"id": 106, "title": "Abstract Blue Composition", "artist": "Contemporary Artist", "colors": ["blue", "white"], "mood": ["calm", "peaceful"], "style": "Abstract"},
    {"id": 107, "title": "Colorful Abstract", "artist": "Modern Studio", "colors": ["multicolor", "bright"], "mood": ["playful", "energetic"], "style": "Abstract"},
    {"id": 108, "title": "Golden Abstract", "artist": "Luxe Arts", "colors": ["gold", "warm", "neutral"], "mood": ["luxurious", "sophisticated"], "style": "Contemporary"},
    {"id": 109, "title": "Botanical Study", "artist": "Nature Arts", "colors": ["green", "natural"], "mood": ["fresh", "natural"], "style": "Botanical"},
    {"id": 110, "title": "Classic Portrait", "artist": "Portrait Masters", "colors": ["brown", "dark", "warm"], "mood": ["traditional", "dignified"], "style": "Classical"},
    {"id": 111, "title": "The Great Wave", "artist": "Hokusai", "colors": ["blue", "white"], "mood": ["powerful", "dramatic"], "style": "Japanese"},
    {"id": 112, "title": "Minimalist Lines", "artist": "Line Studio", "colors": ["black", "white", "neutral"], "mood": ["clean", "modern"], "style": "Minimalist"},
    {"id": 113, "title": "Geometric Patterns", "artist": "Geo Arts", "colors": ["multicolor", "bold"], "mood": ["structured", "modern"], "style": "Geometric"},
    {"id": 114, "title": "Neon Dreams", "artist": "Digital Visions", "colors": ["neon", "pink", "blue"], "mood": ["futuristic", "vibrant"], "style": "Digital"},
    {"id": 115, "title": "Traditional Oil Landscape", "artist": "Heritage Arts", "colors": ["green", "blue", "earth"], "mood": ["peaceful", "traditional"], "style": "Traditional"},
]

SYSTEM_PROMPT = """You are an expert interior designer and art consultant. Analyze the room photo and recommend artworks.

Your response MUST be valid JSON with this exact structure:
{
    "analysis": {
        "description": "2-3 sentences describing the room's style, colors, and atmosphere",
        "dominantColors": ["color1", "color2", "color3"],
        "style": "modern/traditional/minimalist/eclectic/etc",
        "mood": "calm/energetic/cozy/sophisticated/etc",
        "lighting": "bright/dim/natural/warm/cool"
    },
    "recommendations": [
        {
            "artworkId": 101,
            "matchScore": 95,
            "reason": "Why this artwork fits the room"
        }
    ]
}

Available artwork IDs and their characteristics:
- 101: Starry Night (blue, dramatic, expressive)
- 102: Water Lilies (green, calm, natural)
- 103: Café Terrace (yellow, warm, cozy)
- 104: Mona Lisa (brown, classic, elegant)
- 105: Kandinsky (colorful, energetic, bold)
- 106: Abstract Blue (blue, calm, modern)
- 107: Colorful Abstract (vibrant, playful, fun)
- 108: Golden Abstract (gold, luxurious, warm)
- 109: Botanical Study (green, fresh, natural)
- 110: Classic Portrait (brown, traditional, dignified)
- 111: Great Wave (blue, dramatic, powerful)
- 112: Minimalist Lines (black/white, clean, simple)
- 113: Geometric Patterns (colorful, structured, modern)
- 114: Neon Dreams (neon, futuristic, edgy)
- 115: Traditional Landscape (green, peaceful, scenic)

Recommend 3-5 artworks that best match the room. Consider color harmony, style compatibility, and mood."""


@app.route('/api/analyze-room', methods=['POST'])
def analyze_room():
    """
    Analyze a room image and return artwork recommendations
    Expects JSON body with 'image' field containing base64 encoded image
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        image_data = data['image']
        
        # Handle data URL format (data:image/jpeg;base64,...)
        if image_data.startswith('data:'):
            # Extract the base64 part
            image_data = image_data.split(',')[1] if ',' in image_data else image_data
        
        # Call OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this room and recommend artworks from the available collection."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        # Parse the response
        content = response.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Find JSON in the response
            json_match = None
            if '{' in content and '}' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_str = content[start:end]
                result = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except json.JSONDecodeError:
            # Return a default response if parsing fails
            result = get_default_recommendations()
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # Return default recommendations on error
        return jsonify(get_default_recommendations())


def get_default_recommendations():
    """Return default recommendations as fallback"""
    return {
        "analysis": {
            "description": "This appears to be a well-lit room with a contemporary feel. The space has potential for various art styles depending on your preference.",
            "dominantColors": ["neutral", "white", "gray"],
            "style": "contemporary",
            "mood": "versatile",
            "lighting": "natural"
        },
        "recommendations": [
            {"artworkId": 106, "matchScore": 90, "reason": "Abstract Blue would add a calming focal point to your space"},
            {"artworkId": 112, "matchScore": 85, "reason": "Minimalist Lines would complement a clean, modern aesthetic"},
            {"artworkId": 108, "matchScore": 82, "reason": "Golden Abstract adds warmth and sophistication"},
            {"artworkId": 102, "matchScore": 78, "reason": "Water Lilies brings natural tranquility to any room"}
        ]
    }


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'ArtSpace AI Room Analyzer'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
