import json
from hydrogen_factory.models.electrolyzer import ElectrolyzerConfig

class ElectrolyzerService:
    def __init__(self):
        self.config_file = "config.json"
        try:
            self.electrolyzers = self._load_configs().get("electrolyzers", {})
        except Exception as e:
            raise ValueError(f"Failed to initialize electrolyzers: {str(e)}")

    def configure(self, config: ElectrolyzerConfig):
        if config.electrolyzer_id in self.electrolyzers:
            raise ValueError("Electrolyzer ID already exists")
        self.electrolyzers[config.electrolyzer_id] = config.model_dump()
        try:
            self._save_configs()
        except Exception as e:
            raise ValueError(f"Failed to save configuration: {str(e)}")

    def get_config(self, electrolyzer_id: str) -> ElectrolyzerConfig:
        if electrolyzer_id not in self.electrolyzers:
            raise ValueError("Electrolyzer ID not found")
        return ElectrolyzerConfig(**self.electrolyzers[electrolyzer_id])

    def _load_configs(self) -> dict:
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"electrolyzers": {}, "storages": {}}

    def _save_configs(self):
        configs = self._load_configs()
        configs["electrolyzers"] = self.electrolyzers
        configs["storages"] = configs.get("storages", {})
        try:
            with open(self.config_file, "w") as f:
                json.dump(configs, f, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to write to config.json: {str(e)}")