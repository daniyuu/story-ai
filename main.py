from story_ai.app import StoryAI
from story_ai.config import Config
from story_ai.utils.logger import create_logger

create_logger(Config.LOG_ROOT, enable_console_log=True)

if __name__ == '__main__':
    story_ai = StoryAI()
    story = story_ai.generate("从前有座山")
    print(story)
