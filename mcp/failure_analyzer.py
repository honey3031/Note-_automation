from mcp.llm_client import (
    client,
    MODEL_NAME
)


class AIFailureAnalyzer:

    @staticmethod
    def analyze(error_message):

        prompt = f"""
        Analyze this Selenium automation failure:

        {error_message}

        Suggest:
        1. Root cause
        2. Synchronization fix
        3. Locator improvement
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return (
            response
            .choices[0]
            .message.content
        )