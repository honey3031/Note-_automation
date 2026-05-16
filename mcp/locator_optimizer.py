from mcp.llm_client import ask_llm


def optimize_locator(locator):

    prompt = f"""
    Improve this Selenium locator.

    Requirements:
    - stable
    - maintainable
    - production ready

    Locator:
    {locator}
    """

    return ask_llm(prompt)