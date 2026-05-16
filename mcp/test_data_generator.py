from mcp.llm_client import (
    client,
    MODEL_NAME
)


class AITestDataGenerator:

    @staticmethod
    def generate_note():

        prompt = """
        Generate a realistic note title and description
        for automation testing.

        Return concise text.
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