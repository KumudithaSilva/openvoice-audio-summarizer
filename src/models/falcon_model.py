from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from logs.logger_singleton import Logger
import torch


class Falcon:
    """
    Falcon local model loader and inference handler.

    Attributes:
        model_details (str): Dictionary containing the model details.
        device (str): Device to load the model on, e.g., 'cuda' or 'cpu'.
        model (AutoModelForCausalLM): Loaded causal language model.
        tokenizer (AutoTokenizer): Corresponding tokenizer.
    """

    def __init__(self, model_details: dict, device="cuda", logger=None):
        """
        Initialize the Falcon model loader.

        Args:
            model_details (dict): Model details.
            device (str, optional): Device to load the model on. Defaults to 'cuda'.
            logger (Logger, optional): Logger instance. If None, a default is used.
        """
        self.logger = logger or Logger(self.__class__.__name__)
        self.device = device
        self.cache_dir = model_details.get("location")
        self.model = None
        self.tokenizer = None

    def configure_model(self):
        """
        Configure and load the Falcon model with 4-bit quantization
        and the corresponding tokenizer.
        """
        try:
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
            )
            self.logger.info(f"Loading Falcon model from cache: {self.cache_dir}")

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.cache_dir, local_files_only=True
            )
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.logger.info("Tokenizer loaded successfully.")

            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.cache_dir,
                device_map="auto",
                dtype=torch.float16,
                quantization_config=quant_config,
                local_files_only=True,
            )
            self.logger.info("Falcon model successfully loaded.")

        except Exception as e:
            self.logger.error(f"Error loading Falcon model: {e}")
            raise RuntimeError(f"Failed to load Falcon model: {e}")

    def create(self, messages: list) -> str:
        """
        Generate a response from the model for a given list of messages.

        Args:
            messages (list): List of input messages (strings).

        Returns:
            str: The model-generated text.
        """
        # Tokenize input
        if not self.model or not self.tokenizer:
            self.logger.info("Model or tokenizer not loaded. Loading now...")
            self.configure_model()
        try:
            # Get the BatchEncoding
            inputs = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt",
                padding=True,
                truncation=True,
            ).to(self.device)

            attention_mask = (
                (inputs != self.tokenizer.pad_token_id).long().to(self.device)
            )

            # Generate output
            output = self.model.generate(
                input_ids=inputs,
                attention_mask=attention_mask,
                pad_token_id=self.tokenizer.pad_token_id,
                max_new_tokens=100,
            )

            generated_tokens = output[0][inputs.shape[-1] :]
            result = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            self.logger.info("Response generated successfully.")
            return result

        except Exception as e:
            self.logger.error(f"Error during text generation: {e}")
            raise RuntimeError(f"Falcon model generation failed: {e}")
