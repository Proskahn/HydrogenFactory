import json
from hydrogen_factory.models.storage import StorageConfig

class StorageService:
    def __init__(self):
        """Initialize the StorageService with a configuration file path and load existing storage configs.

        Variables:
        - self.config_file (str): Path to the JSON configuration file ('config.json').
        - self.storages (dict): Dictionary mapping storage IDs to their configuration data.

        Raises:
        - ValueError: If loading the configuration file fails (e.g., file corruption).
        """
        self.config_file = "config.json"
        try:
            self.storages = self._load_configs().get("storages", {})
        except Exception as e:
            raise ValueError(f"Failed to initialize storages: {str(e)}")

    def configure(self, config: StorageConfig):
        """Configure a new storage unit and save it to the configuration file.

        Args:
        - config (StorageConfig): Pydantic model containing storage configuration
          (storage_id, max_capacity).

        Variables:
        - config.storage_id (str): Unique identifier for the storage unit.
        - self.storages (dict): Updated with the new storage configuration.

        Raises:
        - ValueError: If the storage_id already exists or saving to config.json fails.
        """
        if config.storage_id in self.storages:
            raise ValueError("Storage ID already exists")
        self.storages[config.storage_id] = config.model_dump()
        try:
            self._save_configs()
        except Exception as e:
            raise ValueError(f"Failed to save configuration: {str(e)}")

    def get_config(self, storage_id: str) -> StorageConfig:
        """Retrieve the configuration for a specific storage unit by its ID.

        Args:
        - storage_id (str): Unique identifier of the storage unit to retrieve.

        Returns:
        - StorageConfig: Pydantic model containing the storage unit's configuration.

        Variables:
        - storage_id (str): The ID used to look up the storage unit.
        - self.storages (dict): Source of the storage configuration data.

        Raises:
        - ValueError: If the storage_id is not found in the stored configurations.
        """
        if storage_id not in self.storages:
            raise ValueError("Storage ID not found")
        return StorageConfig(**self.storages[storage_id])

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
        """Save the current storage configurations to config.json.

        Variables:
        - configs (dict): Configuration data with 'electrolyzers' and 'storages' keys.
        - self.storages (dict): Current storage configurations to save.
        - self.config_file (str): Path to the configuration file.

        Raises:
        - ValueError: If writing to config.json fails (e.g., permission denied).
        """
        configs = self._load_configs()
        configs["storages"] = self.storages
        configs["electrolyzers"] = configs.get("electrolyzers", {})
        try:
            with open(self.config_file, "w") as f:
                json.dump(configs, f, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to write to config.json: {str(e)}")