class AISuggestions:

    @staticmethod
    def analyze_failure(error_message):

        error = error_message.lower()

        if "timeout" in error:

            return (
                "Possible synchronization issue. "
                "Consider stronger waits or "
                "fallback locators."
            )

        if "no such element" in error:

            return (
                "Locator may be unstable. "
                "Consider XPath or CSS fallback."
            )

        if "stale element" in error:

            return (
                "DOM updated before interaction. "
                "Retry after refresh."
            )

        if "connection refused" in error:

            return (
                "Selenium Grid may not be running."
            )

        return (
            "No intelligent suggestion available."
        )

    @staticmethod
    def suggest_locator_strategy(locator_type):

        strategies = {

            "id":
            "Prefer stable unique IDs.",

            "xpath":
            "Avoid deeply nested XPath expressions.",

            "css":
            "Prefer data-testid selectors when available."
        }

        return strategies.get(
            locator_type.lower(),
            "Use stable unique locators."
        )

    @staticmethod
    def generate_test_data(prefix):

        import uuid

        return (
            f"{prefix}_"
            f"{str(uuid.uuid4())[:8]}"
        )