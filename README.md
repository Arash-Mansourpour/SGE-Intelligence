# SGE-Intelligence

**A cutting-edge Python tool for supercharging search with Generative AI.**

SGE-Intelligence is an advanced platform designed to empower content creators, SEO professionals, and developers with the capabilities of Search Generative Experience (SGE). Built with Python and leveraging the Groq API for access to large language models like Llama and others, this tool provides an all-in-one solution for generating SGE-optimized content, analyzing search intent, creating structured data (schema), and optimizing for modern Search Engine Results Page (SERP) features.

---

## Features

- **SGE-Optimized Content Generation**: Create engaging, search-friendly content with natural keyword integration, meta descriptions, headings, and rich media suggestions.
- **Search Intent Analysis**: Gain deep insights into user intent (informational, navigational, transactional) and tailor content strategies accordingly.
- **Schema Markup Generator**: Produce SEO-ready JSON-LD schema markup with detailed explanations and implementation guidance.
- **SERP Feature Optimization**: Strategize for featured snippets, knowledge panels, People Also Ask, and other SERP enhancements.
- **Customizable Templates**: Use pre-built or custom templates to streamline content creation workflows.
- **Analytics Dashboard**: Visualize search type distribution with an integrated Matplotlib-powered analytics view.
- **Modern UI**: A sleek, dark-themed interface built with CustomTkinter for an intuitive user experience.
- **History Tracking**: Access and reload recent searches with ease.

---

## Prerequisites

Before running SGE-Intelligence, ensure you have the following installed:

- Python 3.8+
- A valid Groq API key (replace the `API_KEY` in `SGE.py` with your own)

### Required Libraries
Install the dependencies using pip:
```bash
pip install customtkinter groq pillow matplotlib requests
```

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Arash-Mansourpour/SGE-Intelligence.git
   cd SGE-Intelligence
   ```

2. **Install Dependencies**:
   Run the command above to install required Python libraries.

3. **Set Up API Key**:
   Replace the placeholder API key in `SGE.py` with your Groq API key:
   ```python
   API_KEY = "your-groq-api-key-here"
   ```

4. **Run the Application**:
   Launch the tool by executing:
   ```bash
   python SGE.py
   ```

---

## Usage

1. **Launch the Application**:
   Start the tool with `python SGE.py`, and a modern GUI will appear with a sidebar, input fields, and output tabs.

2. **Input Details**:
   - Enter a **Search Query** (e.g., "best running shoes").
   - Specify **Target Keywords** (e.g., "running shoes, athletic footwear").
   - Select an **AI Model** (e.g., "llama-3.3-70b-versatile") and **Content Type** from the dropdowns.

3. **Choose an Action**:
   - Click **Generate SGE Content** for optimized content creation.
   - Use **Analyze Search Intent** for intent insights.
   - Select **Schema Generator** for structured data.
   - Opt for **SERP Feature Optimizer** for SERP enhancement strategies.

4. **View Results**:
   - Results stream into the respective tabs: **Content**, **Analysis**, or **Schema**.
   - Save, copy, or clear the output using the status bar buttons.

5. **Explore Additional Features**:
   - Use templates from the sidebar or add your own.
   - Review recent searches in the history panel.
   - Open the **Analytics Dashboard** to visualize usage patterns.

---

## Project Structure

```
SGE-Intelligence/
├── SGE.py                # Main application script
├── settings.json         # Configuration file (auto-generated)
├── README.md             # This documentation
└── .gitignore            # Ignores Python cache files and local configs
```

---

## Configuration

- **Settings**: Adjust AI model, temperature, and max tokens via the settings dialog (⚙️ button). Changes persist in `settings.json`.
- **Templates**: Customize or add content templates through the sidebar for reusable prompts.

---

## Example

### Input
- Search Query: "best running shoes 2026"
- Target Keywords: "running shoes, best sneakers, athletic footwear"
- Action: Generate SGE Content

### Output (Content Tab)
```markdown
# Best Running Shoes of 2026: Top Picks for Performance

**Meta Description**: Discover the best running shoes of 2023, featuring top picks for comfort, durability, and style. Explore expert recommendations now! (134 chars)

## Introduction
Looking for the best running shoes in 2023? This guide highlights top-performing athletic footwear...

## Key Features
- **Comfort**: Enhanced cushioning for long runs
- **Durability**: Built to last with premium materials

## Linking Suggestions
- Internal: /blog/running-tips
- External: runningmagazine.com

## Call to Action
Find your perfect pair of running shoes today!
```

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository at [https://github.com/Arash-Mansourpour/SGE-Intelligence](https://github.com/Arash-Mansourpour/SGE-Intelligence).
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the license terms.

---

## Acknowledgments

- Powered by the [Groq API](https://groq.com) for accessing advanced language models like Llama and others.
- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the UI.
- Analytics visualization via [Matplotlib](https://matplotlib.org).

---

For questions, issues, or suggestions, please open an issue on [GitHub](https://github.com/Arash-Mansourpour/SGE-Intelligence) or contact the repository owner, Arash Mansourpour.

---

