from utils.llm_integration import LLM

# Instantiate the LLM object
llm = LLM()


def process_invoice(image_path):
    """
    Process the invoice by analyzing the image and returning results from the LLM.

    :param image_path: Path to the invoice image file
    :return: Analysis results as a JSON object
    """
    # The prompt to ask for a detailed description of the image
    question = "<image>\nDescribe the image in detail."

    # Analyze the image using the LLM
    response = llm.analyze_image(image_path, question)

    # Return the analysis results in JSON format
    return {
        "invoice_data": response
    }
