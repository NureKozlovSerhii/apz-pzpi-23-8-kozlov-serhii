import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from kafka_producer import SpotifyEventProducer


app = FastAPI(title="Spotify API Gateway Mock", version="1.0")
event_bus = SpotifyEventProducer()


class TrackRequest(BaseModel):
    user_id: str
    track_id: str


@app.post("/api/v1/stream/play")
async def play_audio_stream(
    request: TrackRequest,
    background_tasks: BackgroundTasks
):
    if not request.user_id or not request.track_id:
        raise HTTPException(status_code=400, detail="Відсутні параметри")

    event_payload = {
        "event_id": str(uuid.uuid4()),
        "event_type": "TRACK_PLAYED",
        "user_id": request.user_id,
        "track_id": request.track_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Фонова відправка події, щоб не блокувати відповідь клієнту
    background_tasks.add_task(event_bus.emit_event, event_payload)

    return {
        "status": "STREAM_STARTED",
        "cdn_url": f"https://cdn.spotify.mock/audio/{request.track_id}.mp3",
        "latency_ms": 42
    }
