# National Park Review Analyzer
link:https://huggingface.co/spaces/Navya-Sree/National_parks

Overview

The National Park Review Analyzer is a web application that uses natural language processing to analyze visitor reviews of national parks. It provides insights into visitor sentiment across different categories like hiking trails, facilities, fees, and more.
Live Demo: Visit on Hugging Face Spaces

Features

🧠 Sentiment Analysis: Analyzes reviews to determine positive, negative, and neutral sentiments
📊 Interactive Visualizations: Charts showing sentiment distribution across different categories
💰 Fee Information Extraction: Automatically detects and extracts entrance fee information
🏕️ Facility & Activity Detection: Identifies facilities and activities mentioned in reviews
🔤 Word Cloud Generation: Visual representation of most common terms used in reviews
📝 Top Review Highlights: Shows the most positive and negative reviews with confidence scores

Screenshots
<div align="center">
  <img src="https://i.imgur.com/placeholder1.jpg" width="45%" alt="Dashboard with sentiment analysis" />
  <img src="https://i.imgur.com/placeholder2.jpg" width="45%" alt="Category breakdown" />
</div>
Getting Started
Prerequisites

Python 3.8+
pip package manager

Installation

Clone the repository
bashgit clone https://github.com/yourusername/national-park-review-analyzer.git
cd national-park-review-analyzer

Create and activate a virtual environment (recommended)
bashpython -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install the dependencies
bashpip install -r requirements.txt

Download the SpaCy model
bashpython -m spacy download en_core_web_sm


Running the Application
bashstreamlit run app.py
The application will open in your default web browser at http://localhost:8501.
Usage

Enter a URL from one of the supported websites:

Recreation.gov
NPS.gov
NationalParks.org


Click "Analyze" and wait for the results to be processed
Explore the different visualizations and insights:

Overall sentiment distribution
Category-specific sentiment analysis
Word cloud of common terms
Top positive and negative reviews
Extracted park information



How It Works

Web Scraping: The application scrapes review content from the provided URL
Text Processing: Reviews are split into sentences and categorized by topic
Sentiment Analysis: Each sentence is analyzed using a pre-trained transformer model
Data Visualization: Results are compiled into interactive charts and displays
Information Extraction: Park details, fees, and facilities are extracted using pattern matching

Technologies Used

Streamlit: For the web application interface
Transformers: For sentiment analysis (DistilBERT model)
SpaCy: For natural language processing tasks
Beautiful Soup: For web scraping
Pandas: For data manipulation
Matplotlib & WordCloud: For data visualization

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

Future Enhancements

 Cross-park comparison functionality
 Historical sentiment tracking over time
 User accounts to save favorite parks
 More detailed category analysis
 Integration with more review sources

License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

National Park Service for their commitment to preserving natural wonders
The open-source NLP community for their amazing tools
All contributors and park enthusiasts who provided feedback


<div align="center">
  <p>
    <strong>National park sentiment analysis for visitor reviews.</strong>
  </p>
  <p>
    Created with ❤️ for nature lovers and data enthusiasts alike.
  </p>
</div>
