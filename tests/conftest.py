"""
Global test setup.

object_detector.py instantiates ObjectDetector (and loads the YOLO weights)
at module-level on import.  We intercept `ultralytics` in sys.modules BEFORE
any app module is imported so the model is never actually loaded in CI.
"""

import sys
from unittest.mock import MagicMock

_mock_model = MagicMock()
_mock_model.names = {0: "person", 2: "car"}

_mock_ultralytics = MagicMock()
_mock_ultralytics.YOLO.return_value = _mock_model

sys.modules["ultralytics"] = _mock_ultralytics
