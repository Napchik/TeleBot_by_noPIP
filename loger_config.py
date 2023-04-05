"""
    Description: Configure logging.

    Author: Ivan Maruzhenko
    Version: 0.5
"""
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
