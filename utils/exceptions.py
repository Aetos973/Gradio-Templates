class TrackerError(Exception):
    """Base class for tracker-related errors."""
    pass

class ValidationError(TrackerError):
    """Raised when validation fails."""
    pass

class ConfigError(TrackerError):
    """Raised when configuration is invalid."""
    pass

class ModelRegistryError(TrackerError):
    """Raised when model registration fails."""
    pass

class ThemeError(TrackerError):
    """Raised when theme loading fails."""
    pass

