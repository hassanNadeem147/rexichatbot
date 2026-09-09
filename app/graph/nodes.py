from app.graph.state import State
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import config_model
llm = ChatGoogleGenerativeAI(
    api_key=config_model.GOOGLE_API_KEY,
    model=config_model.GOOGLE_MODEL,
    temperature=config_model.TEMPERATURE
)


def _response_text(response) -> str:
    content = response.content
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "".join(parts).strip()
    return str(content).strip()


async def summarizing_node(state: State) -> dict:
    """This node summarizes the given text."""
    prompt = f"""
You are an expert summarizer.
Your task is to summarize the given text in simple, clear, and grammatically
correct English.
Rules:
- Summarize only the information provided in the given text.
- Do not add information, assumptions, or opinions that are not present in the text.
- Use simple and easy-to-understand English.
- Maintain the important meaning and key points of the original text.
- Do not use hashtags (#) or asterisks (*).
- Do not make grammar or spelling mistakes.
- Return only the summary. Do not add introductions, explanations, or comments.
Input validation:
- If the input is meaningless, random, or does not form a useful topic or text
  (for example: "h", "a", "jhjkads"), respond exactly with:
  "Please write a proper topic or text."
- If the input contains meaningful words or a meaningful topic, treat it as valid.
Given text:
{state["text"]}
"""
    response = await llm.ainvoke(prompt)
    return {
        "summarized_text": _response_text(response)
    }

async def explanation_node(state: State) -> dict:
    """This node explains the given text or topic."""
    prompt = f"""
You are an expert explainer who can explain any valid text or topic.
Your task is to explain the given text or topic in detailed, clear, and simple English.
Rules:
- Explain the complete text or topic thoroughly and in depth.
- Use simple, easy-to-understand English.
- Explain difficult concepts in a beginner-friendly, step-by-step style.
- Include examples when they help the user understand the concept.
- Do not skip important information from the given text.
- Do not add false or unrelated information.
- Do not make grammar or spelling mistakes.
- Do not use hashtags (#) or asterisks (*).
- Return only the explanation. Do not add unnecessary introductions or comments.
Input validation:
- If the input is meaningless, random, or does not represent a valid topic or text
  (for example: "h", "a", "jhjkads"), respond exactly with:
  "Please provide a valid text or topic."
- If the input contains meaningful words or a meaningful topic, treat it as valid.
Text or topic to explain:
{state["text"]}
"""
    response = await llm.ainvoke(prompt)
    return {
        "explain_text": _response_text(response)
    }

async def translation_node(state: State) -> dict:
    """This node translates the given text or topic."""
    prompt = f"""
You are an expert translator capable of translating text between any languages.
Your task is to accurately translate the given text into the requested target language.
Rules:
- Translate the complete given text accurately.
- Preserve the original meaning, context, and tone as much as possible.
- Use natural, grammatically correct, and fluent language.
- Do not summarize, explain, or add information to the text.
- Do not change names, numbers, or important details unnecessarily.
- Do not use hashtags (#) or asterisks (*) unless they are part of the original text.
- Return only the translated text.
- Do not add introductions, explanations, or comments.
Input validation:
- A single meaningful word is valid and must be translated.
- Multiple meaningful words or a complete sentence are also valid.
- If the input is meaningless or random
  (for example: "jhjkads", "xqzplm"), respond exactly with:
  "Please provide valid text to translate."
Target language:
{state.get("target_language", "English")}
Text to translate:
{state["text"]}
"""
    response = await llm.ainvoke(prompt)
    return {
        "translate_text": _response_text(response)
    }

async def podcast_node(state: State) -> dict:
    """This node generates a two-person podcast conversation."""
    prompt = f"""
You are an expert podcast script writer.
Your task is to create an interesting and engaging podcast conversation
between two people based on the given text or topic.
Rules:
- Create a natural conversation between exactly two speakers.
- Use the speaker names "Host" and "Guest".
- The Host should introduce the topic and ask interesting questions.
- The Guest should explain and discuss the topic clearly.
- Make the conversation engaging, natural, and easy to follow.
- Explain important concepts in simple English.
- Include examples or simple analogies when they help explain the topic.
- Cover the important information from the given text or topic.
- Do not make grammar or spelling mistakes.
- Do not invent facts that contradict the given text.
- Do not use hashtags (#) or asterisks (*).
- Do not make the conversation unnecessarily repetitive.
- Do not include stage directions, sound effects, or background music instructions.
- Return only the podcast dialogue.
Input validation:
- A meaningful topic, sentence, paragraph, or detailed text is valid.
- If the input is meaningless or random, such as "h", "a", or "jhjkads",
  respond exactly with:
  "Please provide a valid text or topic."
Format:
Host: ...
Guest: ...
Host: ...
Guest: ...
Text or topic for the podcast:
{state["text"]}
"""
    response = await llm.ainvoke(prompt)

    return {
        "podcast": _response_text(response)
    }

def router(state: State) -> str:
    """Routes the workflow based on the selected operation."""
    if state["operation"] == "summarize":
        return "summarize"
    elif state["operation"] == "explain":
        return "explain"
    elif state["operation"] == "translate":
        return "translate"
    elif state["operation"] == "podcast":
        return "podcast"
    return "summarize"