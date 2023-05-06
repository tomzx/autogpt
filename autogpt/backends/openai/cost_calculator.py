class CostCalculator:
    def calculate(self, number_of_tokens: int, model: str) -> float:
        if model == "gpt-3.5-turbo" or model == "gpt-3.5-turbo-0301":
            return number_of_tokens / 1000 * 0.002

        raise ValueError(f"Cost for model {model} not implemented")
