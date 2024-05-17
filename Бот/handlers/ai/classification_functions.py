from transformers import BartForConditionalGeneration, BartTokenizer


# Класс для работы с классификатором
class AIClassifier:

    def __init__(self, model_dir='handlers/ai/bart-pc-qclassifier'):
        self.model = BartForConditionalGeneration.from_pretrained(model_dir, use_safetensors=True)
        self.tokenizer = BartTokenizer.from_pretrained(model_dir)
        self.max_new_tokens = 100

    # Функция классификации сообщений
    def classify_message(self, input_text: str) -> int:
        inputs = self.tokenizer(input_text, return_tensors='pt')
        outputs = self.model.generate(inputs['input_ids'], max_new_tokens=self.max_new_tokens)
        output_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return int(output_text)

