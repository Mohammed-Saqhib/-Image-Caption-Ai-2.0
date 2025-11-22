# Contributing to AI Image Analysis Platform

First off, thank you for considering contributing to the AI Image Analysis Platform! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## 📜 Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

---

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** describing the issue
- **Detailed description** of the problem
- **Steps to reproduce** the bug
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

**Template**:
```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., macOS 13.0]
- Python: [e.g., 3.10.5]
- Browser: [e.g., Chrome 120]
```

### 💡 Suggesting Features

Feature suggestions are welcome! Please provide:

- **Clear title** for the feature
- **Detailed description** of the feature
- **Use case** explaining why it's needed
- **Potential implementation** ideas (optional)

### 📝 Documentation Improvements

Documentation is crucial! You can help by:

- Fixing typos or grammatical errors
- Adding missing documentation
- Improving existing explanations
- Creating tutorials or guides
- Translating documentation

### 🔧 Code Contributions

We welcome code contributions! Areas where you can help:

- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test coverage
- Accessibility improvements

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv or conda)

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Image-AI-Platform.git
   cd Image-AI-Platform
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

5. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

6. **Make your changes**
   ```bash
   # Edit files, add features, fix bugs
   ```

7. **Test your changes**
   ```bash
   # Run the application
   ./run_pro.sh pro
   
   # Run tests (if available)
   pytest tests/
   ```

8. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

9. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

10. **Create Pull Request**
    - Go to your fork on GitHub
    - Click "New Pull Request"
    - Fill in the PR template

---

## 📏 Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: 100 characters max
- **Docstrings**: Google style
- **Naming**:
  - Classes: `PascalCase`
  - Functions/Variables: `snake_case`
  - Constants: `UPPER_CASE`

### Example

```python
"""
Module docstring describing the module's purpose.
"""

from typing import Optional, List
import streamlit as st


class ImageProcessor:
    """
    Process images for OCR and AI analysis.
    
    Attributes:
        config (dict): Configuration parameters
        cache_enabled (bool): Whether caching is enabled
    """
    
    def __init__(self, config: dict):
        """
        Initialize the ImageProcessor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.cache_enabled = True
    
    def process_image(
        self, 
        image: Image, 
        mode: str = "auto"
    ) -> Optional[dict]:
        """
        Process an image with specified mode.
        
        Args:
            image: PIL Image object to process
            mode: Processing mode ('auto', 'custom', 'aggressive')
        
        Returns:
            Dictionary containing processed results or None if failed
        
        Raises:
            ValueError: If mode is invalid
        """
        if mode not in ["auto", "custom", "aggressive"]:
            raise ValueError(f"Invalid mode: {mode}")
        
        # Process image
        result = self._internal_process(image)
        return result
```

### Documentation

- **Every function** should have a docstring
- **Complex logic** should have inline comments
- **Public APIs** need comprehensive documentation
- **Examples** are encouraged in docstrings

### Testing

- Write tests for new features
- Maintain existing test coverage
- Test edge cases
- Include integration tests

---

## 📤 Submitting Changes

### Pull Request Process

1. **Update documentation** if needed
2. **Add/update tests** for your changes
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Fill PR template** completely
6. **Link related issues** using keywords (Fixes #123)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests
- [ ] All tests pass
```

### Commit Message Guidelines

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

**Examples**:
```bash
feat(ocr): add support for Arabic language
fix(tts): resolve audio generation bug on Windows
docs(readme): update installation instructions
```

---

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_ocr.py

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_ocr.py::test_english_extraction
```

### Writing Tests

```python
import pytest
from src.ocr_engine import OCREngine

class TestOCREngine:
    """Test OCR functionality"""
    
    @pytest.fixture
    def ocr_engine(self):
        """Create OCR engine instance"""
        return OCREngine()
    
    def test_initialize(self, ocr_engine):
        """Test engine initialization"""
        assert ocr_engine is not None
        assert ocr_engine.languages == ['en']
    
    def test_extract_text(self, ocr_engine):
        """Test text extraction"""
        # Load test image
        image = load_test_image("sample_english.jpg")
        
        # Extract text
        result = ocr_engine.extract_text(image)
        
        # Assertions
        assert result is not None
        assert 'text' in result
        assert len(result['text']) > 0
```

---

## 🎨 UI/UX Contributions

When contributing to UI:

- **Maintain consistency** with existing design
- **Test responsiveness** on different screen sizes
- **Consider accessibility** (ARIA labels, keyboard navigation)
- **Follow theme colors** defined in config
- **Add loading states** for async operations

---

## 📚 Documentation Contributions

### Areas to Contribute

- **README improvements**
- **Code comments**
- **API documentation**
- **Tutorials and guides**
- **Example use cases**
- **Video tutorials**

### Documentation Style

- Use **clear, concise** language
- Include **code examples**
- Add **screenshots** where helpful
- Organize with **headings**
- Use **tables** for comparisons
- Add **emoji** for visual appeal (but don't overdo it)

---

## 🏆 Recognition

Contributors will be recognized in:

- **README.md** Contributors section
- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions

---

## 📞 Getting Help

- **Documentation**: Check existing docs first
- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Search existing issues before creating new ones
- **Discord/Slack**: Join our community chat (if available)

---

## 🎯 Priority Areas

Current priorities for contributions:

1. **Bug fixes** - Always welcome
2. **Performance improvements** - Optimization is key
3. **Additional language support** - Expand OCR/TTS languages
4. **Mobile optimization** - Better mobile experience
5. **API development** - REST API for platform
6. **Advanced preprocessing** - More image enhancement techniques
7. **GPU acceleration** - Faster processing
8. **Cloud integration** - Storage and deployment options

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Thank you for taking the time to contribute! Every contribution, no matter how small, is valued and appreciated.

**Happy coding! 🚀**

---

<div align="center">

Questions? Feel free to reach out!

[GitHub Issues](https://github.com/YOUR_USERNAME/Image-AI-Platform/issues) • [Discussions](https://github.com/YOUR_USERNAME/Image-AI-Platform/discussions)

</div>
