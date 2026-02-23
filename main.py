# main.py

import os
import json
from dotenv import load_dotenv
from app.agent import run_agent

load_dotenv()

def main():
    question = input("Enter research question:\n")

    try:
        report, trace = run_agent(question)

        os.makedirs("outputs", exist_ok=True)

        with open("outputs/report.md", "w") as f:
            f.write(report)

        with open("outputs/trace.json", "w") as f:
            json.dump(trace, f, indent=4)

        print("\nResearch complete.")
        print("Report saved to outputs/report.md")
        print("Trace saved to outputs/trace.json")

    except ValueError as e:
        print("\n Invalid Input\n")
        print(str(e))
        print("\nThis agent is designed for research-oriented, multi-source questions.")
        print("Example valid inputs:")
        print("- What are the risks of synthetic data in LLM training?")
        print("- How does use of powered toothbrush reduce gum related problems compared to a normal one?")
        print()

    except Exception as e:
        print("\n⚠️ Unexpected Error\n")
        print("Something went wrong during execution.")
        print("Error:", str(e))


if __name__ == "__main__":
    main()