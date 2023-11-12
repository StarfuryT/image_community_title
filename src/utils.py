import os
import configparser
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from config import TEXT_MODEL, OPEN_AI_MODEL, NUMBER_OF_TITLES

config = configparser.ConfigParser()
config.read('/home/starfury/api_config.txt');
os.environ['OPENAI_API_KEY'] = config['OPEN-AI']['api_key']


def get_caption(img_loc):
    """Creates a caption for the input image"""
    pl = pipeline("image-to-text", model=TEXT_MODEL)
    caption = pl(img_loc, max_new_tokens=20)[0]["generated_text"]
    return caption


def generate_titles(img_descr):
    """Creates five title ideas based on the following image descriptions:"""
    template = """
    You are a creative title generator;
    You can suggest creative title ideas based on a set of phrases. Each title should capture as many concepts from all phrases as possible and it should be playful. Each title should have four words of less and it should contain no more than two relavant emojis.
    PHRASES: {img_descr}
    FIVE TITLE IDEAS:
    """
    template = """
        You are a creative title generator;
        You can suggest catchy title of four words or less based on these phrases.
        PHRASES: {img_descr}
        TEN TITLE IDEAS:
        """
    prompt = PromptTemplate(template=template, input_variables=["img_descr"])

    llm_story = LLMChain(
        llm=ChatOpenAI(model_name=OPEN_AI_MODEL, temperature=.1),
        prompt=prompt,
    )
    story = llm_story.predict(img_descr=img_descr)

    return story
