class OutputFactoryInterface:
    """
    A interface for output factory that formats list of datapoints
    into the following format:
    - csv
    - txt
    - json
    """

    def format_to_json(self, query_type, dp_list) -> str:
        pass

    def format_to_txt(self, query_type, dp_list) -> str:
        pass

    def format_to_csv(self, query_type, dp_list) -> str:
        pass
