from story_ai.app import StoryAI
from story_ai.config import Config
from story_ai.utils.logger import create_logger

create_logger(Config.LOG_ROOT, enable_console_log=True)

if __name__ == '__main__':
    story_ai = StoryAI()
    writer_style = [
        "内容神转折，对角色的描写有非常多的细节",
        "给角色创造很多苦难",
        "总是给角色创造一些希望，剧情有教育意义"
    ]
    story = story_ai.generate("从前有座山", writer_style, turn_count=1)
    print(story)
