import torch
from transformers import AutoModel, AutoTokenizer
from utils.image_processing import load_image


class LLM:
    def __init__(self, model_name="5CD-AI/Vintern-1B-v2", device=None):
        """
        Initialize the LLM class with a model and tokenizer from Hugging Face.

        :param model_name: Name of the LLM model on Hugging Face
        :param device: Device to run the model on (cuda or cpu)
        """
        self.model_name = model_name
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')

        # Load the model and tokenizer
        self.model = AutoModel.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        ).eval().to(self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            use_fast=False
        )

    def analyze_image(self, image_path, question, max_num=12, max_new_tokens=1024, do_sample=False, num_beams=3, repetition_penalty=2.5):
        """
        Analyze an image and return a response based on the input question.

        :param image_path: Path to the image file to be analyzed
        :param question: Question for the model to generate a response
        :param max_num: Maximum number of blocks when processing the image
        :param max_new_tokens: Maximum number of new tokens to generate
        :param do_sample: Whether to use sampling for generation
        :param num_beams: Number of beams for beam search
        :param repetition_penalty: Penalty for repeated phrases
        :return: Response from the model as a text string
        """
        # Load and preprocess the image
        pixel_values = load_image(image_path, max_num=max_num).to(torch.bfloat16).to(self.device)

        # Configuration for text generation
        generation_config = dict(
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            num_beams=num_beams,
            repetition_penalty=repetition_penalty
        )

        # Generate response from the model using the question and image
        response, history = self.model.chat(
            self.tokenizer, pixel_values, question, generation_config, history=None, return_history=True
        )
        return response
