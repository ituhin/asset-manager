import os
from dotenv import load_dotenv
from commands import execute_command
from logger import get_logger

logger = get_logger()

# Load environment variables from .env file
load_dotenv()

print(" " * 60)
print(f"SANDBOX = {os.getenv('EXCHANGE_SANDBOX', False)}")
print(" " * 60)


def main():
    # Command loop
    while True:
        try:
            command = input("💰$$$ ")
            execute_command(command)  # Pass the logger to execute_command
        except KeyboardInterrupt:
            print("\nExiting...")
            print(" " * 60)
            break
        except Exception as e:
            print(f"Error: {e}")
            logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
