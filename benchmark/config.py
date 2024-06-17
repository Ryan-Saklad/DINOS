import os
import random

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from utils.problem_type import ProblemType


class Config:
    def __init__(self, seed: int | None = None, template_dir: str = "benchmark/prompts", languages: list[str] = ["en"], fallback_language: str | None = "en"):
        self.supported_languages: list[str] = ["en"]

        self.seed: int = seed if seed is not None else random.randint(0, int(1e8))
        self.rng: random.Random = random.Random(self.seed)
        self.template_dir: str = template_dir
        self.languages: list[str] = languages if languages else self.supported_languages
        self.fallback_language: str | None = fallback_language  # Allows for strict evaluation, without a fallback language
        
        self.env: Environment = self._create_env()

    def _create_env(self) -> Environment:
        language_dirs = [os.path.join(self.template_dir, lang) for lang in self.languages]
        fallback_dir = os.path.join(self.template_dir, self.fallback_language)
        
        loader = FileSystemLoader(language_dirs + [fallback_dir])
        env = Environment(loader=loader)
        
        return env
    
    def get_template(self, template_name: str) -> str:
        try:
            return self.env.get_template(template_name)
        except TemplateNotFound:
            for language in self.languages:
                fallback_template_name = f"{language}/{template_name}"
                try:
                    return self.env.get_template(fallback_template_name)
                except TemplateNotFound:
                    continue
            raise ValueError(f"Template '{template_name}' not found in any of the specified languages or fallback language '{self.fallback_language}'")

    def render_template(self, problem: "BaseProblem", examples: list["BaseProblem"] | None = None, **kwargs) -> str:
        template = self.get_template(problem.problem_name + ".jinja")
        rendered_template = template.render(Problem=problem, ProblemType=ProblemType, examples=examples, **kwargs)
        
        return rendered_template.strip()

    def increment_seed(self) -> None:
        self.seed += 1
        self.rng.seed(self.seed)
