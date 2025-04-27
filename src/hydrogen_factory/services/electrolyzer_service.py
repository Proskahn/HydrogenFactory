import json
from hydrogen_factory.models.electrolyzer import ElectrolyzerConfig

class ElectrolyzerService:
    def __init__(self):
        """Initialize the ElectrolyzerService with a configuration file path and load existing electrolyzer configs.

        Variables:
        - self.config_file (str): Path to the JSON configuration file ('config.json').
        - self.electrolyzers (dict): Dictionary mapping electrolyzer IDs to their configuration data.

        Raises:
        - ValueError: If loading the configuration file fails (e.g., file corruption).
        """
        self.config_file = "config.json"
        try:
            self.electrolyzers = self._load_configs().get("electrolyzers", {})
        except Exception as e:
            raise ValueError(f"Failed to initialize electrolyzers: {str(e)}")

    def configure(self, config: ElectrolyzerConfig):
        """Configure a new electrolyzer and save it to the configuration file.

        Args:
        - config (ElectrolyzerConfig): Pydantic model containing electrolyzer configuration
          (electrolyzer_id, type, capacity, efficiency).

        Variables:
        - config.electrolyzer_id (str): Unique identifier for the electrolyzer.
        - self.electrolyzers (dict): Updated with the new electrolyzer configuration.

        Raises:
        - ValueError: If the electrolyzer_id already exists or saving to config.json fails.
        """
        if config.electrolyzer_id in self.electrolyzers:
            raise ValueError("Electrolyzer ID already exists")
        self.electrolyzers[config.electrolyzer_id] = config.model_dump()
        try:
            self._save_configs()
        except Exception as e:
            raise ValueError(f"Failed to save configuration: {str(e)}")

    def get_config(self, electrolyzer_id: str) -> ElectrolyzerConfig:
        """Retrieve the configuration for a specific electrolyzer by its ID.

        Args:
        - electrolyzer_id (str): Unique identifier of the electrolyzer to retrieve.

        Returns:
        - ElectrolyzerConfig: Pydantic model containing the electrolyzer's configuration.

        Variables:
        - electrolyzer_id (str): The ID used to look up the electrolyzer.
        - self.electrolyzers (dict): Source of the electrolyzer configuration data.

        Raises:
        - ValueError: If the electrolyzer_id is not found in the stored configurations.
        """
        if electrolyzer_id not in self.electrolyzers:
            raise ValueError("Electrolyzer ID not found")
        return ElectrolyzerConfig(**self.electrolyzers[electrolyzer_id])

    def _load_configs(self) -> dict:
        """Load the configuration data from config.json.

        Returns:
        - dict: Configuration data containing 'electrolyzers' and 'storages' dictionaries.
                Returns empty defaults if the file is missing or invalid.

        Variables:
        - self.config_file (str): Path to the configuration file.

        Raises:
        - FileNotFoundError: Handled internally, returns default empty config.
        - json.JSONDecodeError: Handled internally, returns default empty config.
        """
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"electrolyzers": {}, "storages": {}}

    def _save_configs(self):
        """Save the current electrolyzer configurations to config.json.

        Variables:
        - configs (dict): Configuration data with 'electrolyzers' and 'storages' keys.
        - self.electrolyzers (dict): Current electrolyzer configurations to save.
        - self.config_file (str): Path to the configuration file.

        Raises:
        - ValueError: If writing to config.json fails (e.g., permission denied).
        """
        configs = self._load_configs()
        configs["electrolyzers"] = self.electrolyzers
        configs["storages"] = configs.get("storages", {})
        try:
            with open(self.config_file, "w") as f:
                json.dump(configs, f, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to write to config.json: {str(e)}")