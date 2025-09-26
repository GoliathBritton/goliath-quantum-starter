class ModelContentProtocol:
    def __init__(self):
        pass

    def format_content(self, input_data, domain):
        # Dummy implementation to allow the server to start
        return {
            "premise": input_data,
            "desired_outcome": f"Processed for {domain}",
            "text": input_data
        }