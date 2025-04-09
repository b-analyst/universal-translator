from transformers import pipeline
from langdetect import detect, DetectorFactory
from typing import Dict

# Set a seed for reproducibility
DetectorFactory.seed = 0

class TranslationService:
    def __init__(self):
        self.models: Dict[str, pipeline] = {}

    def load_model(self, model_name: str):
        if model_name not in self.models:
            self.models[model_name] = pipeline("translation", model=model_name)

    def detect_language(self, text: str) -> str:
        return detect(text)

    def translate(self, text: str, model_name: str, target_language: str) -> str:
        if model_name not in self.models:
            self.load_model(model_name)
        translation = self.models[model_name](text, target_lang=target_language)
        return translation[0]['translation_text']
