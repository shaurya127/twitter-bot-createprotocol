import asyncio
import csv
import dotenv
from src.lambda_function import lambda_handler

dotenv.load_dotenv()

async def main():
    await lambda_handler(event=None,context=None)

if __name__ == "__main__":
    asyncio.run(main())
