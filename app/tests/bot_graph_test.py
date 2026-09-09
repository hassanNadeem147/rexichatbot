from app.graph.workflow import app
from app.logging.logger import logger
import asyncio
async def main():
    logger.info("Starting the application...")
    user_input = input("-> ")
    logger.info(f"User Input: {user_input}")
    try:
        logger.info("Invoking the workflow...")
        initial_state = {
            "text": user_input,
            "summarized_text": "",
            "explain_text": "",
            "translate_text": "",
            "podcast": "",
            "target_language": "english",
            "operation": "podcast"
        }
        result = await app.ainvoke(initial_state)
        logger.info(f"Final State: {result}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
if __name__ == "__main__":
    asyncio.run(main())
