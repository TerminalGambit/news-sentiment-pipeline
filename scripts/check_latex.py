#!/usr/bin/env python3
"""
Script to check and install required LaTeX packages.
"""

import subprocess
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Required LaTeX packages
REQUIRED_PACKAGES = [
    'latexmk',
    'latex-bin',
    'latex-fonts-extra',
    'texlive-latex-extra',
    'texlive-fonts-extra',
    'texlive-latex-recommended'
]

def check_latex_installation():
    """Check if LaTeX is installed and install required packages."""
    try:
        # Check if pdflatex is available
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
        logger.info("LaTeX is installed")
        
        # Check and install required packages
        for package in REQUIRED_PACKAGES:
            try:
                subprocess.run(['tlmgr', 'info', package], capture_output=True, check=True)
                logger.info(f"Package {package} is installed")
            except subprocess.CalledProcessError:
                logger.info(f"Installing package {package}...")
                subprocess.run(['tlmgr', 'install', package], check=True)
                logger.info(f"Package {package} installed successfully")
                
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking LaTeX installation: {str(e)}")
        return False
    except FileNotFoundError:
        logger.error("LaTeX is not installed. Please install TeX Live or MiKTeX")
        return False

def main():
    """Main entry point."""
    if not check_latex_installation():
        sys.exit(1)
        
    logger.info("LaTeX setup completed successfully")

if __name__ == "__main__":
    main() 