from dataclasses import dataclass

GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4" 

PRICING = {GPT3: (0.02, 0.02), GPT4: (0.03, 0.06)} # prices per 1k tokens

@dataclass
class OpenAIAPIStats:
    model_name: str = GPT3
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    def cost(self):
        token_prices = PRICING[self.model_name]
        return (token_prices[0] * self.prompt_tokens + token_prices[1] * self.completion_tokens) / 1000

    def update(self, stats):
        self.prompt_tokens += stats['prompt_tokens']
        self.completion_tokens += stats['completion_tokens']
        self.total_tokens += stats['total_tokens']

    def __repr__(self):
        return (f"Model Name: {self.model_name} -> "
                f"Prompt tokens: {self.prompt_tokens}, Completion tokens: {self.completion_tokens}, "
                f"Total tokens: {self.total_tokens}, Estimated cost: ${self.cost():.2f}")
