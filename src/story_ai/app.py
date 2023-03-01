import asyncio

from loguru import logger
from shortuuid import uuid

from story_ai.external.ai_service.mt_openai import ChatGPTAPI
from story_ai.model.story import Story


class Writer:
    def __init__(self, style="内容曲折，角色描写要有很多细节"):
        self.id = uuid()
        self.count = 0
        self.conversion_id = uuid()
        self.parent_message_id = None
        self.style = style

    def write(self, pre_story: str) -> str:
        if self.count == 0:
            prompt = f"来进行故事接龙，要求每次的接龙{self.style}，故事的开头是:{pre_story}"
        else:
            prompt = pre_story

        reply_message, context = asyncio.run(
            ChatGPTAPI.text_completion(self.conversion_id, parent_message_id=self.parent_message_id,
                                       prompt=prompt))
        self.conversion_id = context["conversation_id"]
        self.parent_message_id = context['parent_message_id']
        self.count += 1

        return reply_message


class StoryAI:
    def __init__(self):
        pass

    def generate(self, beginning: str) -> Story:
        logger.debug(f"Start generate a story with beginning: {beginning}")
        story = Story(beginning=beginning)
        writer_style = [
            "内容神转折，对角色的描写有非常多的细节",
            "给角色创造很多苦难",
            "总是给角色创造一些希望，剧情有教育意义"
        ]
        writers = [Writer(style) for style in writer_style]
        paragraph = beginning
        turn_count = 2
        content = paragraph
        for turn_index in range(turn_count):
            for writer in writers:
                paragraph = writer.write(paragraph)
                logger.debug(paragraph)
                content += f"\n{paragraph}"
        story.content = content
        return story
