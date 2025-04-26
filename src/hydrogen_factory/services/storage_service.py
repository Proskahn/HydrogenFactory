import json
from hydrogen_factory.models.storage import StorageConfig

class StorageService:
    def __init__(self):
        self.config_file = "config.json"
        try:
            self.storages = self._load_configs().get("storages", {})
        except Exception as e:
            raise ValueError(f"Failed to initialize storages: {str(e)}")

    def configure(self, config: StorageConfig):
        if config.storage_id in self.storages:
            raise ValueError("Storage ID already exists")
        self.storages[config.storage_id] = config.model_dump()
        try:
            self._save_configs()
        except Exception as e:
            raise ValueError(f"Failed to save configuration: {str(e)}")

    def get_config(self, storage_id: str) -> StorageConfig:
        if storage_id not in self.storages:
            raise ValueError("Storage ID not found")
        return StorageConfig(**self.storages[storage_id])

    def _load_configs(self) -> dict:
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"electrolyzers": {}, "storages": {}}

    def _save_configs(self):
        configs = self._load_configs()
        configs["storages"] = self.storages
        configs["electrolyzers"] = configs.get("electrolyzers", {})
        try:
            with open(self.config_file, "w") as f:
                json.dump(configs, f, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to write to config.json: {str(e)}")