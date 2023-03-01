import aiohttp
from loguru import logger

from story_ai.config import Config


class ChatGPTAPI:
    @classmethod
    async def text_completion(cls, conversation_id, parent_message_id, prompt: str):
        request_body = {"questions": prompt}
        context = {"conversation_id": conversation_id, "parent_message_id": parent_message_id}
        if conversation_id:
            request_body["conversationId"] = conversation_id
        if parent_message_id:
            request_body["parentMessageId"] = parent_message_id

        reply_message = "抱歉，服务正在维护中，请稍等。"
        try:
            async with aiohttp.ClientSession() as session:
                service_mt_openai = f"{Config.SERVICE_MT_OPENAI}/chat-gpt/send"
                async with session.post(service_mt_openai, json=request_body) as response:
                    if response and response.status == 200:
                        data = await response.json()
                        reply_message = data.get("response", "抱歉无法回答您的问题")
                        context = {"conversation_id": data["conversationId"], "parent_message_id": data["messageId"]}
                    else:
                        logger.error(f"Error: SERVICE_MT_OPENAI-{service_mt_openai} 失败： status_code: {response.status}")
        except Exception as e:
            logger.error(f"Error: 调用chatGPT服务失败, {e}")

        return reply_message, context

    @classmethod
    async def text_to_image(cls, prompt: str, size="512x512"):
        style = "octane render highly detailed, pastel pink, white, iridescent, glowing light, unreal engine, 8k , center image"
        request_body = {
            "prompt": prompt + "," + style,
            "size": size}
        try:
            async with aiohttp.ClientSession() as session:
                service_mt_openai = f"{Config.SERVICE_MT_OPENAI}/image-generator/generator"
                async with session.post(service_mt_openai, json=request_body) as response:
                    if response and response.status == 200:
                        data = await response.json()
                        reply_message = data.get("url", "抱歉无法生成图片")
                    else:
                        logger.error(f"Error: SERVICE_MT_OPENAI-{service_mt_openai} 失败： status_code: {response.status}")
        except Exception as e:
            logger.error(f"Error: 调用chatGPT服务失败, {e}")

        return reply_message
