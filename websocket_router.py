from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.pipeline_subscribers: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        # Remove from pipeline subscriptions
        for pipeline_id, subscribers in self.pipeline_subscribers.items():
            if websocket in subscribers:
                subscribers.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection)

    async def subscribe_to_pipeline(self, pipeline_id: str, websocket: WebSocket):
        if pipeline_id not in self.pipeline_subscribers:
            self.pipeline_subscribers[pipeline_id] = []
        if websocket not in self.pipeline_subscribers[pipeline_id]:
            self.pipeline_subscribers[pipeline_id].append(websocket)
        logger.info(f"WebSocket subscribed to pipeline {pipeline_id}")

    async def unsubscribe_from_pipeline(self, pipeline_id: str, websocket: WebSocket):
        if pipeline_id in self.pipeline_subscribers and websocket in self.pipeline_subscribers[pipeline_id]:
            self.pipeline_subscribers[pipeline_id].remove(websocket)
        logger.info(f"WebSocket unsubscribed from pipeline {pipeline_id}")

    async def send_pipeline_update(self, pipeline_id: str, update: dict):
        if pipeline_id in self.pipeline_subscribers:
            message = json.dumps({
                "type": "pipeline_update",
                "pipeline_id": pipeline_id,
                "data": update,
                "timestamp": datetime.now().isoformat()
            })
            
            disconnected = []
            for websocket in self.pipeline_subscribers[pipeline_id]:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending pipeline update: {e}")
                    disconnected.append(websocket)
            
            # Clean up disconnected connections
            for websocket in disconnected:
                self.disconnect(websocket)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                if message_type == "subscribe_pipeline":
                    pipeline_id = message.get("pipeline_id")
                    if pipeline_id:
                        await manager.subscribe_to_pipeline(pipeline_id, websocket)
                        await manager.send_personal_message(
                            json.dumps({
                                "type": "subscription_confirmed",
                                "pipeline_id": pipeline_id,
                                "timestamp": datetime.now().isoformat()
                            }),
                            websocket
                        )
                
                elif message_type == "unsubscribe_pipeline":
                    pipeline_id = message.get("pipeline_id")
                    if pipeline_id:
                        await manager.unsubscribe_from_pipeline(pipeline_id, websocket)
                        await manager.send_personal_message(
                            json.dumps({
                                "type": "unsubscription_confirmed",
                                "pipeline_id": pipeline_id,
                                "timestamp": datetime.now().isoformat()
                            }),
                            websocket
                        )
                
                elif message_type == "ping":
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "pong",
                            "timestamp": datetime.now().isoformat()
                        }),
                        websocket
                    )
                
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": "Invalid JSON format",
                        "timestamp": datetime.now().isoformat()
                    }),
                    websocket
                )
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}")
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": "Internal server error",
                        "timestamp": datetime.now().isoformat()
                    }),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Helper function to send pipeline execution updates
async def send_pipeline_execution_update(pipeline_id: str, status: str, progress: float = None, 
                                       message: str = None, error: str = None, 
                                       result: dict = None):
    """Send real-time pipeline execution updates to subscribed clients"""
    update = {
        "status": status,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    
    if progress is not None:
        update["progress"] = progress
    if error:
        update["error"] = error
    if result:
        update["result"] = result
    
    await manager.send_pipeline_update(pipeline_id, update)

# Helper function to send system-wide notifications
async def send_system_notification(notification_type: str, message: str, data: dict = None):
    """Send system-wide notifications to all connected clients"""
    notification = {
        "type": "system_notification",
        "notification_type": notification_type,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    
    if data:
        notification["data"] = data
    
    await manager.broadcast(json.dumps(notification))