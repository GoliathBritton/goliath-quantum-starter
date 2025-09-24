from celery import Celery
from typing import Dict, Any, List, Optional, Union
import json
import uuid
import time
from datetime import datetime, timedelta
import redis.asyncio as redis
import structlog
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import ssl

logger = structlog.get_logger()

# Get Celery app instance
from src.app_consolidated import celery_app

class NotificationService:
    """Unified notification service for email, SMS, and push notifications"""
    
    def __init__(self):
        self.redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Email configuration (would come from environment in production)
        self.smtp_config = {
            "host": "smtp.gmail.com",
            "port": 587,
            "username": "notifications@company.com",
            "password": "app_password",  # Use app password in production
            "use_tls": True
        }
        
        # SMS configuration (would use Twilio, AWS SNS, etc.)
        self.sms_config = {
            "provider": "twilio",
            "account_sid": "your_account_sid",
            "auth_token": "your_auth_token",
            "from_number": "+1234567890"
        }
    
    async def send_email(self, to_email: str, subject: str, body: str, 
                        html_body: Optional[str] = None, 
                        attachments: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Send email notification"""
        branding_text = "\n\n-- \nFLYFOX AI\nGoliath of All Trade\nSigma Select"
        body += branding_text
        if html_body:
            branding_html = '<br><br><hr><p style="font-size: small; color: gray;">FLYFOX AI | Goliath of All Trade | Sigma Select</p>'
            html_body += branding_html
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_config['username']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment['content'])
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {attachment["filename"]}'
                    )
                    msg.attach(part)
            
            # Simulate email sending (in production, use actual SMTP)
            await asyncio.sleep(0.5)  # Simulate network delay
            
            # In production, you would do:
            # context = ssl.create_default_context()
            # with smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port']) as server:
            #     server.starttls(context=context)
            #     server.login(self.smtp_config['username'], self.smtp_config['password'])
            #     server.send_message(msg)
            
            return {
                "status": "sent",
                "message_id": f"email_{uuid.uuid4().hex[:12]}",
                "to": to_email,
                "subject": subject,
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Email sending failed", error=str(e), to_email=to_email)
            return {
                "status": "failed",
                "error": str(e),
                "to": to_email,
                "failed_at": datetime.utcnow().isoformat()
            }
    
    async def send_sms(self, to_number: str, message: str) -> Dict[str, Any]:
        """Send SMS notification"""
        try:
            # Simulate SMS sending (in production, use Twilio, AWS SNS, etc.)
            await asyncio.sleep(0.3)
            
            # In production, you would use Twilio client:
            # from twilio.rest import Client
            # client = Client(self.sms_config['account_sid'], self.sms_config['auth_token'])
            # message = client.messages.create(
            #     body=message,
            #     from_=self.sms_config['from_number'],
            #     to=to_number
            # )
            
            return {
                "status": "sent",
                "message_id": f"sms_{uuid.uuid4().hex[:12]}",
                "to": to_number,
                "message": message,
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("SMS sending failed", error=str(e), to_number=to_number)
            return {
                "status": "failed",
                "error": str(e),
                "to": to_number,
                "failed_at": datetime.utcnow().isoformat()
            }
    
    async def send_push_notification(self, user_id: str, title: str, body: str, 
                                   data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send push notification"""
        try:
            # Simulate push notification (in production, use FCM, APNS, etc.)
            await asyncio.sleep(0.2)
            
            # In production, you would use Firebase Admin SDK:
            # from firebase_admin import messaging
            # message = messaging.Message(
            #     notification=messaging.Notification(title=title, body=body),
            #     data=data or {},
            #     token=user_device_token
            # )
            # response = messaging.send(message)
            
            return {
                "status": "sent",
                "message_id": f"push_{uuid.uuid4().hex[:12]}",
                "user_id": user_id,
                "title": title,
                "body": body,
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Push notification failed", error=str(e), user_id=user_id)
            return {
                "status": "failed",
                "error": str(e),
                "user_id": user_id,
                "failed_at": datetime.utcnow().isoformat()
            }

@celery_app.task(bind=True, name="notifications.send_email")
def send_email_notification(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send email notification asynchronously
    
    Args:
        email_data: Email configuration and content
        
    Returns:
        Email sending result
    """
    task_id = self.request.id
    logger.info("Sending email notification", task_id=task_id, to=email_data.get("to"))
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        notification_service = NotificationService()
        
        # Set processing status
        asyncio.run(redis_client.hset(
            f"notification:email:{task_id}",
            mapping={
                "status": "sending",
                "started_at": datetime.utcnow().isoformat(),
                "to": email_data.get("to", "unknown"),
                "subject": email_data.get("subject", "No Subject")
            }
        ))
        
        # Send email
        result = asyncio.run(notification_service.send_email(
            to_email=email_data["to"],
            subject=email_data["subject"],
            body=email_data["body"],
            html_body=email_data.get("html_body"),
            attachments=email_data.get("attachments")
        ))
        
        # Update completion status
        completion_data = {
            "status": result["status"],
            "completed_at": datetime.utcnow().isoformat(),
            "message_id": result.get("message_id"),
            "result": json.dumps(result)
        }
        
        if result["status"] == "failed":
            completion_data["error"] = result.get("error")
        
        asyncio.run(redis_client.hset(
            f"notification:email:{task_id}",
            mapping=completion_data
        ))
        
        # Publish notification event
        asyncio.run(redis_client.publish(
            "notification:updates",
            json.dumps({
                "task_id": task_id,
                "type": "email",
                "status": result["status"],
                "to": email_data["to"],
                "timestamp": datetime.utcnow().isoformat()
            })
        ))
        
        logger.info("Email notification completed", task_id=task_id, status=result["status"])
        
        return {
            "task_id": task_id,
            "status": result["status"],
            "notification_result": result
        }
        
    except Exception as e:
        logger.error("Email notification failed", task_id=task_id, error=str(e))
        
        # Update error status
        error_data = {
            "status": "failed",
            "failed_at": datetime.utcnow().isoformat(),
            "error": str(e)
        }
        
        asyncio.run(redis_client.hset(
            f"notification:email:{task_id}",
            mapping=error_data
        ))
        
        raise

@celery_app.task(bind=True, name="notifications.send_sms")
def send_sms_notification(self, sms_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send SMS notification asynchronously
    
    Args:
        sms_data: SMS configuration and content
        
    Returns:
        SMS sending result
    """
    task_id = self.request.id
    logger.info("Sending SMS notification", task_id=task_id, to=sms_data.get("to"))
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        notification_service = NotificationService()
        
        # Set processing status
        asyncio.run(redis_client.hset(
            f"notification:sms:{task_id}",
            mapping={
                "status": "sending",
                "started_at": datetime.utcnow().isoformat(),
                "to": sms_data.get("to", "unknown"),
                "message_preview": sms_data.get("message", "")[:50]
            }
        ))
        
        # Send SMS
        result = asyncio.run(notification_service.send_sms(
            to_number=sms_data["to"],
            message=sms_data["message"]
        ))
        
        # Update completion status
        completion_data = {
            "status": result["status"],
            "completed_at": datetime.utcnow().isoformat(),
            "message_id": result.get("message_id"),
            "result": json.dumps(result)
        }
        
        if result["status"] == "failed":
            completion_data["error"] = result.get("error")
        
        asyncio.run(redis_client.hset(
            f"notification:sms:{task_id}",
            mapping=completion_data
        ))
        
        # Publish notification event
        asyncio.run(redis_client.publish(
            "notification:updates",
            json.dumps({
                "task_id": task_id,
                "type": "sms",
                "status": result["status"],
                "to": sms_data["to"],
                "timestamp": datetime.utcnow().isoformat()
            })
        ))
        
        logger.info("SMS notification completed", task_id=task_id, status=result["status"])
        
        return {
            "task_id": task_id,
            "status": result["status"],
            "notification_result": result
        }
        
    except Exception as e:
        logger.error("SMS notification failed", task_id=task_id, error=str(e))
        
        # Update error status
        error_data = {
            "status": "failed",
            "failed_at": datetime.utcnow().isoformat(),
            "error": str(e)
        }
        
        asyncio.run(redis_client.hset(
            f"notification:sms:{task_id}",
            mapping=error_data
        ))
        
        raise

@celery_app.task(bind=True, name="notifications.send_push")
def send_push_notification_task(self, push_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send push notification asynchronously
    
    Args:
        push_data: Push notification configuration and content
        
    Returns:
        Push notification sending result
    """
    task_id = self.request.id
    logger.info("Sending push notification", task_id=task_id, user_id=push_data.get("user_id"))
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        notification_service = NotificationService()
        
        # Set processing status
        asyncio.run(redis_client.hset(
            f"notification:push:{task_id}",
            mapping={
                "status": "sending",
                "started_at": datetime.utcnow().isoformat(),
                "user_id": push_data.get("user_id", "unknown"),
                "title": push_data.get("title", "No Title")
            }
        ))
        
        # Send push notification
        result = asyncio.run(notification_service.send_push_notification(
            user_id=push_data["user_id"],
            title=push_data["title"],
            body=push_data["body"],
            data=push_data.get("data")
        ))
        
        # Update completion status
        completion_data = {
            "status": result["status"],
            "completed_at": datetime.utcnow().isoformat(),
            "message_id": result.get("message_id"),
            "result": json.dumps(result)
        }
        
        if result["status"] == "failed":
            completion_data["error"] = result.get("error")
        
        asyncio.run(redis_client.hset(
            f"notification:push:{task_id}",
            mapping=completion_data
        ))
        
        # Publish notification event
        asyncio.run(redis_client.publish(
            "notification:updates",
            json.dumps({
                "task_id": task_id,
                "type": "push",
                "status": result["status"],
                "user_id": push_data["user_id"],
                "timestamp": datetime.utcnow().isoformat()
            })
        ))
        
        logger.info("Push notification completed", task_id=task_id, status=result["status"])
        
        return {
            "task_id": task_id,
            "status": result["status"],
            "notification_result": result
        }
        
    except Exception as e:
        logger.error("Push notification failed", task_id=task_id, error=str(e))
        
        # Update error status
        error_data = {
            "status": "failed",
            "failed_at": datetime.utcnow().isoformat(),
            "error": str(e)
        }
        
        asyncio.run(redis_client.hset(
            f"notification:push:{task_id}",
            mapping=error_data
        ))
        
        raise

@celery_app.task(bind=True, name="notifications.batch_send")
def batch_send_notifications(self, notifications: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Send multiple notifications in batch
    
    Args:
        notifications: List of notification configurations
        
    Returns:
        Batch sending results
    """
    task_id = self.request.id
    logger.info("Starting batch notification sending", task_id=task_id, batch_size=len(notifications))
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Set initial batch status
        asyncio.run(redis_client.hset(
            f"notification:batch:{task_id}",
            mapping={
                "status": "processing",
                "started_at": datetime.utcnow().isoformat(),
                "total_notifications": len(notifications),
                "completed_notifications": 0
            }
        ))
        
        results = []
        
        for i, notification in enumerate(notifications):
            try:
                notification_type = notification.get("type", "email")
                
                if notification_type == "email":
                    task = send_email_notification.apply_async(args=[notification])
                elif notification_type == "sms":
                    task = send_sms_notification.apply_async(args=[notification])
                elif notification_type == "push":
                    task = send_push_notification_task.apply_async(args=[notification])
                else:
                    raise ValueError(f"Unknown notification type: {notification_type}")
                
                result = task.get(timeout=30)  # 30 second timeout
                
                results.append({
                    "notification_index": i,
                    "type": notification_type,
                    "status": "success",
                    "result": result
                })
                
                # Update progress
                asyncio.run(redis_client.hset(
                    f"notification:batch:{task_id}",
                    "completed_notifications", i + 1
                ))
                
            except Exception as e:
                logger.error("Batch notification failed", task_id=task_id, 
                           notification_index=i, error=str(e))
                results.append({
                    "notification_index": i,
                    "type": notification.get("type", "unknown"),
                    "status": "failed",
                    "error": str(e)
                })
        
        # Calculate batch statistics
        successful_notifications = [r for r in results if r["status"] == "success"]
        failed_notifications = [r for r in results if r["status"] == "failed"]
        
        # Group by notification type
        type_distribution = {}
        for result in results:
            notification_type = result["type"]
            type_distribution[notification_type] = type_distribution.get(notification_type, 0) + 1
        
        batch_result = {
            "task_id": task_id,
            "status": "completed",
            "total_notifications": len(notifications),
            "successful_notifications": len(successful_notifications),
            "failed_notifications": len(failed_notifications),
            "type_distribution": type_distribution,
            "results": results,
            "completed_at": datetime.utcnow().isoformat()
        }
        
        # Update completion status
        completion_data = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "successful_notifications": len(successful_notifications),
            "failed_notifications": len(failed_notifications),
            "result": json.dumps(batch_result)
        }
        
        asyncio.run(redis_client.hset(
            f"notification:batch:{task_id}",
            mapping=completion_data
        ))
        
        logger.info("Batch notification sending completed", task_id=task_id,
                   successful=len(successful_notifications), 
                   failed=len(failed_notifications))
        
        return batch_result
        
    except Exception as e:
        logger.error("Batch notification sending failed", task_id=task_id, error=str(e))
        raise

@celery_app.task(bind=True, name="notifications.schedule_notification")
def schedule_notification(self, notification_data: Dict[str, Any], 
                         schedule_time: str) -> Dict[str, Any]:
    """
    Schedule a notification for future delivery
    
    Args:
        notification_data: Notification configuration
        schedule_time: ISO format datetime string for when to send
        
    Returns:
        Scheduling result
    """
    task_id = self.request.id
    logger.info("Scheduling notification", task_id=task_id, schedule_time=schedule_time)
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Parse schedule time
        eta = datetime.fromisoformat(schedule_time.replace('Z', '+00:00'))
        
        notification_type = notification_data.get("type", "email")
        
        # Schedule the appropriate notification task
        if notification_type == "email":
            scheduled_task = send_email_notification.apply_async(
                args=[notification_data],
                eta=eta
            )
        elif notification_type == "sms":
            scheduled_task = send_sms_notification.apply_async(
                args=[notification_data],
                eta=eta
            )
        elif notification_type == "push":
            scheduled_task = send_push_notification_task.apply_async(
                args=[notification_data],
                eta=eta
            )
        else:
            raise ValueError(f"Unknown notification type: {notification_type}")
        
        schedule_result = {
            "scheduled_task_id": scheduled_task.id,
            "notification_type": notification_type,
            "schedule_time": schedule_time,
            "eta": eta.isoformat(),
            "scheduled_at": datetime.utcnow().isoformat()
        }
        
        # Store schedule information
        schedule_key = f"notification:schedule:{task_id}"
        asyncio.run(redis_client.hset(
            schedule_key,
            mapping={
                "status": "scheduled",
                "notification_type": notification_type,
                "schedule_time": schedule_time,
                "scheduled_task_id": scheduled_task.id,
                "result": json.dumps(schedule_result)
            }
        ))
        
        logger.info("Notification scheduled successfully", task_id=task_id, 
                   notification_type=notification_type)
        
        return {
            "task_id": task_id,
            "status": "scheduled",
            "schedule_result": schedule_result
        }
        
    except Exception as e:
        logger.error("Notification scheduling failed", task_id=task_id, error=str(e))
        raise

@celery_app.task(bind=True, name="notifications.cleanup_old_notifications")
def cleanup_old_notifications(self, retention_days: int = 30) -> Dict[str, Any]:
    """
    Clean up old notification data
    
    Args:
        retention_days: Number of days to retain notification data
        
    Returns:
        Cleanup results
    """
    task_id = self.request.id
    logger.info("Starting notification cleanup", task_id=task_id, retention_days=retention_days)
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        # Find old notification keys
        email_keys = asyncio.run(redis_client.keys("notification:email:*"))
        sms_keys = asyncio.run(redis_client.keys("notification:sms:*"))
        push_keys = asyncio.run(redis_client.keys("notification:push:*"))
        batch_keys = asyncio.run(redis_client.keys("notification:batch:*"))
        schedule_keys = asyncio.run(redis_client.keys("notification:schedule:*"))
        
        cleaned_count = 0
        
        # Clean up old notifications
        for key_list in [email_keys, sms_keys, push_keys, batch_keys, schedule_keys]:
            for key in key_list:
                try:
                    started_at_str = asyncio.run(redis_client.hget(key, "started_at"))
                    if started_at_str:
                        started_at = datetime.fromisoformat(started_at_str)
                        if started_at < cutoff_date:
                            asyncio.run(redis_client.delete(key))
                            cleaned_count += 1
                except Exception:
                    # If we can't parse the date, delete it anyway
                    asyncio.run(redis_client.delete(key))
                    cleaned_count += 1
        
        cleanup_result = {
            "cleaned_notifications": cleaned_count,
            "retention_days": retention_days,
            "cutoff_date": cutoff_date.isoformat(),
            "cleaned_at": datetime.utcnow().isoformat()
        }
        
        logger.info("Notification cleanup completed", task_id=task_id, 
                   cleaned_count=cleaned_count)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "cleanup_result": cleanup_result
        }
        
    except Exception as e:
        logger.error("Notification cleanup failed", task_id=task_id, error=str(e))
        raise