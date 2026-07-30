# Media Generation Service

AI-powered media generation system for the Autonomous Company OS. This engine handles image generation, video creation, audio processing, and multimedia asset management.

## Features

- **Image Generation** - AI-powered image creation using DALL-E, Stable Diffusion
- **Video Generation** - Automated video creation and editing
- **Audio Processing** - Text-to-speech, voice cloning, audio enhancement
- **Media Management** - Asset storage, organization, and retrieval
- **Template System** - Reusable media templates
- **Batch Processing** - Bulk media generation
- **Quality Control** - Automated quality checks
- **Analytics** - Media performance tracking

## Architecture

```
┌─────────────┐    Media     ┌──────────────┐
│   All       │ ────────────> │  Media       │
│  Engines    │               │  Ingestion   │
└─────────────┘               └──────┬───────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
            ┌───────▼──────┐ ┌────▼────┐ ┌────▼──────┐
            │   Image      │ │ Video   │ │   Audio    │
            │   Generator  │ │ Engine  │ │  Processor │
            └──────────────┘ └─────────┘ └───────────┘
                    │                │                │
                    └────────────────┼────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │      Media Asset Manager        │
                    │  (Storage, organization, tags)   │
                    └─────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
            ┌───────▼──────┐ ┌────▼────┐ ┌────▼──────┐
            │   Template   │ │ Batch   │ │ Quality   │
            │   System     │ │ Engine  │ │  Control   │
            └──────────────┘ └─────────┘ └───────────┘
```

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL (for media metadata)
- Redis (for caching and queues)
- OpenAI API key (for DALL-E)
- Stable Diffusion API (optional)
- Storage (AWS S3, Google Cloud Storage)

### Local Development

```bash
# Clone repository
git clone https://github.com/autonomous-company/media-generation-service.git
cd media-generation-service

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the service
uvicorn app.main:app --reload --port 8045
```

### Docker Deployment

```bash
# Build and start all services
cd docker
docker-compose up -d

# View logs
docker-compose logs -f media-generation

# Stop services
docker-compose down
```

## Configuration

Configuration is managed via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://localhost/media` | PostgreSQL connection URL |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection URL |
| `OPENAI_API_KEY` | - | OpenAI API key for DALL-E |
| `STABILITY_API_KEY` | - | Stability AI API key |
| `AWS_ACCESS_KEY` | - | AWS access key for S3 |
| `AWS_SECRET_KEY` | - | AWS secret key for S3 |
| `S3_BUCKET` | - | S3 bucket name |

## API Endpoints

### Health & Info
- `GET /health` - Health check
- `GET /` - Service information

### Image Generation
- `POST /images/generate` - Generate image
- `POST /images/batch` - Batch generate images
- `GET /images/{image_id}` - Get image details
- `GET /images` - List images

### Video Generation
- `POST /videos/generate` - Generate video
- `POST /videos/edit` - Edit video
- `GET /videos/{video_id}` - Get video details
- `GET /videos` - List videos

### Audio Processing
- `POST /audio/tts` - Text-to-speech
- `POST /audio/clone` - Voice cloning
- `POST /audio/enhance` - Audio enhancement
- `GET /audio/{audio_id}` - Get audio details

### Media Management
- `POST /media/upload` - Upload media
- `GET /media/{media_id}` - Get media details
- `GET /media` - List media assets
- `DELETE /media/{media_id}` - Delete media

### Templates
- `POST /templates/create` - Create template
- `GET /templates/{template_id}` - Get template
- `GET /templates` - List templates

## Usage Examples

### Generate Image

```python
import httpx

async def generate_image():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8045/images/generate",
            json={
                "prompt": "A futuristic city skyline at sunset",
                "size": "1024x1024",
                "style": "realistic",
                "model": "dall-e-3"
            }
        )
        return response.json()
```

### Generate Video

```python
async def generate_video():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8045/videos/generate",
            json={
                "prompt": "Product showcase video",
                "duration": 30,
                "style": "professional",
                "images": ["image_001", "image_002"]
            }
        )
        return response.json()
```

### Text-to-Speech

```python
async def text_to_speech():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8045/audio/tts",
            json={
                "text": "Welcome to our platform",
                "voice": "natural",
                "language": "en-US"
            }
        )
        return response.json()
```

## Media Types

- **Images** - PNG, JPG, WebP, SVG
- **Videos** - MP4, MOV, AVI, WebM
- **Audio** - MP3, WAV, AAC, FLAC
- **Documents** - PDF, DOCX (for media conversion)

## AI Models

- **DALL-E 3** - Image generation
- **Stable Diffusion** - Advanced image generation
- **Whisper** - Audio transcription
- **ElevenLabs** - Voice synthesis
- **Runway ML** - Video generation

## Integration with Other Engines

### Content Engine
- Provides media for content
- Generates images for articles
- Creates videos for social media

### Marketing Automation
- Generates ad creatives
- Creates marketing materials
- Produces campaign assets

### Sales Engine
- Generates proposal visuals
- Creates sales presentations
- Produces demo videos

## Monitoring

### Metrics
- Generation volume by type
- Generation success rate
- Average generation time
- Storage usage
- Quality scores

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
