import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(layout="wide", page_title="National Park Analytics", page_icon="🌲")

# Enhanced data with consistent structure - using text instead of emojis in dictionary keys
PARKS_DATA = {
    "Yellowstone": {"positive": 78, "negative": 22, "neutral": 0, "reviews": [], "url": "https://www.nps.gov/yell/index.htm", "emoji": "🏞️"},
    "Yosemite": {"positive": 85, "negative": 15, "neutral": 0, "reviews": [], "url": "https://www.nps.gov/yose/index.htm", "emoji": "⛰️"},
    "Grand Canyon": {"positive": 92, "negative": 8, "neutral": 0, "reviews": [], "url": "https://www.nps.gov/grca/index.htm", "emoji": "🏜️"},
    "Zion": {"positive": 70, "negative": 30, "neutral": 0, "reviews": [], "url": "https://www.nps.gov/zion/index.htm", "emoji": "🪨"},
    "Big Bend": {"positive": 82, "negative": 12, "neutral": 6, "reviews": [], "url": "https://www.nps.gov/bibe/index.htm", "emoji": "🌋"},
    "Black Canyon": {"positive": 75, "negative": 20, "neutral": 5, "reviews": [], "url": "https://www.nps.gov/blca/index.htm", "emoji": "🏔️"},
    "Biscayne": {"positive": 68, "negative": 25, "neutral": 7, "reviews": [], "url": "https://www.nps.gov/bisc/index.htm", "emoji": "🌊"},
    "Hot Springs": {"positive": 72, "negative": 18, "neutral": 10, "reviews": [], "url": "https://www.nps.gov/hosp/index.htm", "emoji": "🌡️"},
    "Independence": {"positive": 88, "negative": 10, "neutral": 2, "reviews": [], "url": "https://www.nps.gov/inde/index.htm", "emoji": "🏛️"},
    "Valley Forge": {"positive": 80, "negative": 15, "neutral": 5, "reviews": [], "url": "https://www.nps.gov/vafo/index.htm", "emoji": "⚔️"},
    "Dry Tortugas": {"positive": 95, "negative": 4, "neutral": 1, "reviews": [], "url": "https://www.nps.gov/drto/index.htm", "emoji": "🏝️"},
    "Everglades": {"positive": 84, "negative": 12, "neutral": 4, "reviews": [], "url": "https://www.nps.gov/ever/index.htm", "emoji": "🐊"},
}

FEATURE_DATA = [
    {"feature": "Hiking", "positive": 65, "negative": 35, "neutral": 0, "emoji": "🥾"},
    {"feature": "Camping", "positive": 58, "negative": 42, "neutral": 0, "emoji": "🏕️"},
    {"feature": "Scenery", "positive": 95, "negative": 5, "neutral": 0, "emoji": "🌄"},
    {"feature": "Wildlife", "positive": 82, "negative": 18, "neutral": 0, "emoji": "🐻"},
    {"feature": "Facilities", "positive": 45, "negative": 48, "neutral": 7, "emoji": "🚻"},
    {"feature": "Crowds", "positive": 30, "negative": 65, "neutral": 5, "emoji": "👨‍👩‍👧‍👦"},
    {"feature": "Fees", "positive": 35, "negative": 60, "neutral": 5, "emoji": "💵"},
    {"feature": "Parking", "positive": 40, "negative": 55, "neutral": 5, "emoji": "🅿️"},
]

# Create reviews without emojis in dictionary keys
REVIEWS = [
    {"park": "Yellowstone", "feature": "Wildlife", "sentiment": "Positive",
     "text": "Amazing wildlife sightings including bears and wolves!", "park_emoji": "🏞️", "feature_emoji": "🐻"},
    {"park": "Grand Canyon", "feature": "Scenery", "sentiment": "Positive",
     "text": "Most breathtaking views I've ever experienced!", "park_emoji": "🏜️", "feature_emoji": "🌄"},
    {"park": "Yosemite", "feature": "Hiking", "sentiment": "Positive",
     "text": "The trails offer incredible variety and challenge for all skill levels.", "park_emoji": "⛰️", "feature_emoji": "🥾"},
    {"park": "Zion", "feature": "Camping", "sentiment": "Negative",
     "text": "Campgrounds were overcrowded and facilities needed maintenance.", "park_emoji": "🪨", "feature_emoji": "🏕️"},
    {"park": "Big Bend", "feature": "Scenery", "sentiment": "Positive",
     "text": "The desert and mountain landscapes are stunning, especially at sunset.", "park_emoji": "🌋", "feature_emoji": "🌄"},
    {"park": "Black Canyon", "feature": "Hiking", "sentiment": "Positive",
     "text": "The rim trails offer vertigo-inducing views that are worth every step!", "park_emoji": "🏔️", "feature_emoji": "🥾"},
    {"park": "Biscayne", "feature": "Wildlife", "sentiment": "Positive",
     "text": "Snorkeling here was incredible - so many colorful fish and coral formations.", "park_emoji": "🌊", "feature_emoji": "🐻"},
    {"park": "Hot Springs", "feature": "Facilities", "sentiment": "Neutral",
     "text": "The bathhouses are historic but could use some modern updates.", "park_emoji": "🌡️", "feature_emoji": "🚻"},
    {"park": "Independence", "feature": "Scenery", "sentiment": "Positive",
     "text": "Walking through history with beautifully preserved buildings and monuments.", "park_emoji": "🏛️", "feature_emoji": "🌄"},
    {"park": "Valley Forge", "feature": "Crowds", "sentiment": "Negative",
     "text": "Too many people on weekends made it difficult to enjoy the historical sites.", "park_emoji": "⚔️", "feature_emoji": "👨‍👩‍👧‍👦"},
    {"park": "Dry Tortugas", "feature": "Wildlife", "sentiment": "Positive",
     "text": "The sea turtles and reef fish were abundant and the water clarity was perfect!", "park_emoji": "🏝️", "feature_emoji": "🐻"},
    {"park": "Everglades", "feature": "Wildlife", "sentiment": "Positive",
     "text": "Saw countless alligators, beautiful birds, and even a rare Florida panther from a distance!", "park_emoji": "🐊", "feature_emoji": "🐻"},
    {"park": "Yellowstone", "feature": "Facilities", "sentiment": "Negative",
     "text": "Restrooms were poorly maintained and often out of supplies.", "park_emoji": "🏞️", "feature_emoji": "🚻"},
    {"park": "Grand Canyon", "feature": "Fees", "sentiment": "Negative",
     "text": "Entry price is too steep for families, especially with additional parking costs.", "park_emoji": "🏜️", "feature_emoji": "💵"},
    {"park": "Yosemite", "feature": "Parking", "sentiment": "Negative",
     "text": "Impossible to find parking near popular trailheads after 9am.", "park_emoji": "⛰️", "feature_emoji": "🅿️"},
    {"park": "Zion", "feature": "Crowds", "sentiment": "Negative",
     "text": "Angels Landing was so crowded it felt dangerous on narrow sections.", "park_emoji": "🪨", "feature_emoji": "👨‍👩‍👧‍👦"},
    {"park": "Big Bend", "feature": "Camping", "sentiment": "Positive",
     "text": "Chisos Basin campground has some of the best stargazing in the country!", "park_emoji": "🌋", "feature_emoji": "🏕️"},
    {"park": "Black Canyon", "feature": "Fees", "sentiment": "Neutral",
     "text": "The entrance fee is reasonable considering the amazing views.", "park_emoji": "🏔️", "feature_emoji": "💵"},
    {"park": "Biscayne", "feature": "Camping", "sentiment": "Positive",
     "text": "Camping on Boca Chita Key was a unique and peaceful experience.", "park_emoji": "🌊", "feature_emoji": "🏕️"},
    {"park": "Hot Springs", "feature": "Hiking", "sentiment": "Positive",
     "text": "The Hot Springs Mountain Trail offers beautiful forest views and historic sites.", "park_emoji": "🌡️", "feature_emoji": "🥾"},
]

def create_bar_chart(data, x_col, y_col, title, color_map):
    """Create a customized bar chart using plotly express"""
    fig = px.bar(data, x=x_col, y=y_col, title=title,
                 color=y_col, color_discrete_map=color_map)
    fig.update_layout(showlegend=False)
    return fig

def create_pie_chart(positive, negative, neutral=0):
    """Create a pie chart showing sentiment distribution"""
    fig = go.Figure(data=[go.Pie(
        labels=['Positive', 'Negative', 'Neutral'] if neutral > 0 else ['Positive', 'Negative'],
        values=[positive, negative, neutral] if neutral > 0 else [positive, negative],
        marker={'colors': ['#4CAF50', '#F44336', '#FF9800'] if neutral > 0 else ['#4CAF50', '#F44336']}
    )])
    fig.update_layout(title='Overall Sentiment Distribution')
    return fig

def filter_data(park_filter, feature_filter):
    """Filter reviews based on selected park and feature"""
    filtered_reviews = REVIEWS
    
    if park_filter != "All Parks":
        # Remove emoji from park filter
        park_name = park_filter.split(" ", 1)[1] if " " in park_filter else park_filter
        filtered_reviews = [r for r in filtered_reviews if r["park"] == park_name]
    
    if feature_filter != "All Features":
        # Remove emoji from feature filter
        feature_name = feature_filter.split(" ", 1)[1] if " " in feature_filter else feature_filter
        filtered_reviews = [r for r in filtered_reviews if r["feature"] == feature_name]
        
    return filtered_reviews

def get_recommendations(park):
    """Get park-specific recommendations based on sentiment analysis research"""
    # First extract park name without emoji if needed
    park_name = park.split(" ", 1)[1] if " " in park else park 
    
    recommendations = {
        "Yellowstone": {
            "improvements": [
                "Increase wildlife protection zones and viewing platforms 🦬",
                "Improve facility maintenance schedules for restrooms 🚽",
                "Implement traffic management system during peak seasons 🚦"
            ],
            "enhancements": [
                "Expand guided wolf watching programs 🐺",
                "Create virtual reality geyser experiences 🌋",
                "Develop wildlife tracking apps for visitors 📱"
            ],
            "research": "Research shows visitors highly value wildlife viewing experiences in Yellowstone, with social media posts demonstrating positive emotional responses to wildlife sightings."
        },
        "Yosemite": {
            "improvements": [
                "Implement reservations for popular trails 🥾",
                "Increase shuttle service frequency 🚌",
                "Expand parking capacity at main trailheads 🅿️"
            ],
            "enhancements": [
                "Create more climbing programs for beginners 🧗",
                "Develop stargazing observation points ✨",
                "Add more interpretive hiking trails 🪧"
            ],
            "research": "Studies indicate visitors to Yosemite express high satisfaction with scenic beauty but frustration with parking and crowding issues during peak seasons."
        },
        "Grand Canyon": {
            "improvements": [
                "Expand shade structures at viewpoints ⛱️",
                "Increase water refill stations on trails 💧",
                "Implement tiered pricing structure for different access levels 💰"
            ],
            "enhancements": [
                "Create accessible viewpoints for visitors with disabilities ♿",
                "Develop geology-focused educational programs 🪨",
                "Install time-lapse cameras for erosion education 📷"
            ],
            "research": "Analysis of visitor reviews shows extremely high positive sentiment regarding Grand Canyon's scenery, but concerns about fees and facilities."
        },
        "Zion": {
            "improvements": [
                "Redesign shuttle loading areas to reduce wait times ⏱️",
                "Renovate restroom facilities parkwide 🚻",
                "Implement digital permits for popular hikes to reduce crowding 📲"
            ],
            "enhancements": [
                "Create flash flood awareness programs 🌊",
                "Develop night sky observation areas 🌌",
                "Add more family-friendly short trail options 👨‍👩‍👧‍👦"
            ],
            "research": "Sentiment analysis reveals visitor frustration with crowding on popular trails like Angels Landing and concerns about safety in narrow sections."
        },
        "Big Bend": {
            "improvements": [
                "Improve cellular coverage in emergency areas 📶",
                "Increase water availability at remote trailheads 🚰",
                "Enhance road maintenance in remote areas 🛣️"
            ],
            "enhancements": [
                "Develop dark sky viewing platforms with telescopes 🔭",
                "Create desert ecology educational programs 🌵",
                "Expand guided border culture experiences 🏜️"
            ],
            "research": "Reviews highlight exceptional stargazing opportunities and desert landscapes, with neutral to positive sentiment about remote camping experiences."
        },
        "Black Canyon": {
            "improvements": [
                "Add safety railings at selected viewpoints 🚧",
                "Improve trail marking for difficulty levels 🥾",
                "Expand visitor center educational displays 🏫"
            ],
            "enhancements": [
                "Create guided geology tours 🪨",
                "Develop photography workshops focused on canyon lighting 📸",
                "Add more intermediate hiking options 🏞️"
            ],
            "research": "Visitor sentiment shows strong positive reactions to dramatic views but concerns about trail safety and clarity of difficulty ratings."
        },
        "Biscayne": {
            "improvements": [
                "Enhance boat launch facilities ⛵",
                "Improve reef protection markers 🪸",
                "Increase water quality monitoring 🔍"
            ],
            "enhancements": [
                "Expand guided snorkeling tours with marine biologists 🐠",
                "Create underwater photography programs 📷",
                "Develop coral reef conservation education 🐡"
            ],
            "research": "Analysis of reviews indicates high satisfaction with marine wildlife viewing but some concerns about facility maintenance and accessibility."
        },
        "Hot Springs": {
            "improvements": [
                "Modernize historic bathhouse facilities while preserving character 🏛️",
                "Create more seating areas along promenade 🪑",
                "Improve accessibility options for mobility-limited visitors ♿"
            ],
            "enhancements": [
                "Develop interactive exhibits on thermal water science ♨️",
                "Create historical reenactments of 1920s spa culture 🕰️",
                "Expand wellness programs using natural springs 💆"
            ],
            "research": "Sentiment analysis shows mixed opinions about facilities, with positive reactions to historical aspects but desire for modernization of amenities."
        },
        "Independence": {
            "improvements": [
                "Reduce queue times at Liberty Bell with timed entries ⏳",
                "Enhance signage for self-guided history tours 🪧",
                "Improve accessibility for historic buildings ♿"
            ],
            "enhancements": [
                "Create augmented reality historical experiences 📱",
                "Develop interactive constitutional history programs 📜",
                "Expand living history demonstrations 🎭"
            ],
            "research": "Visitors express highly positive sentiment about historical significance and preservation, with suggestions for enhanced interpretive experiences."
        },
        "Valley Forge": {
            "improvements": [
                "Implement weekend crowd management strategies 👥",
                "Expand parking at popular monuments 🅿️",
                "Create more rest areas along hiking trails 🪑"
            ],
            "enhancements": [
                "Develop Revolutionary War reenactments ⚔️",
                "Create military strategy educational programs 🗺️",
                "Expand winter encampment living history exhibits ❄️"
            ],
            "research": "Review analysis indicates concerns about weekend crowding affecting visitor experience at historical monuments."
        },
        "Dry Tortugas": {
            "improvements": [
                "Increase frequency of ferry service ⛴️",
                "Enhance camping reservations system ⛺",
                "Improve weather shelter facilities ⛈️"
            ],
            "enhancements": [
                "Expand guided snorkeling programs 🤿",
                "Create night sky viewing events 🌠",
                "Develop marine conservation education 🐬"
            ],
            "research": "Extremely high positive sentiment in visitor reviews, especially regarding marine wildlife and remote island experience quality."
        },
        "Everglades": {
            "improvements": [
                "Enhance mosquito management during peak seasons 🦟",
                "Improve accessibility of wilderness waterways 🛶",
                "Create more elevated boardwalks for wildlife viewing 👀"
            ],
            "enhancements": [
                "Develop guided night expeditions 🌙",
                "Create ecosystem restoration education programs 🌿",
                "Expand photography blinds for wildlife viewing 📸"
            ],
            "research": "Social media sentiment analysis shows strong positive emotions related to wildlife sightings, especially birds and alligators."
        },
        "All Parks": {
            "improvements": [
                "Implement timed entry systems to reduce crowding ⏱️",
                "Increase maintenance frequency for restroom facilities 🧹",
                "Consider tiered pricing options 💰"
            ],
            "enhancements": [
                "Develop more wildlife viewing programs 🦉",
                "Add panoramic viewpoint installations 🌅",
                "Create interactive educational displays 📚"
            ],
            "research": "Research across multiple parks shows visitors generally express positive sentiment, with joy and anticipation being common emotions in social media posts about park visits."
        }
    }
    
    return recommendations.get(park_name, recommendations["All Parks"])

def national_park_dashboard():    
    # Header
    st.title("🏞️ National Park Sentiment Dashboard")
    st.markdown("Analyzing visitor experiences across U.S. National Parks")
    
    # Create display names with emojis for UI
    park_display_names = ["All Parks"] + [f"{data['emoji']} {park}" for park, data in PARKS_DATA.items()]
    feature_display_names = ["All Features"] + [f"{f['emoji']} {f['feature']}" for f in FEATURE_DATA]
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_park_display = st.selectbox("Filter by Park", park_display_names)
    with col2:
        selected_feature_display = st.selectbox("Filter by Feature", feature_display_names)
    
    # Convert display names back to internal names
    selected_park = selected_park_display
    selected_feature = selected_feature_display
    
    # Display selected park header if a specific park is selected
    if selected_park != "All Parks":
        st.markdown(f"## {selected_park} Analysis")
        
        # Extract park name without emoji
        park_name = selected_park.split(" ", 1)[1] if " " in selected_park else selected_park
        
        # Display park website link
        if park_name in PARKS_DATA and "url" in PARKS_DATA[park_name]:
            st.markdown(f"[Visit Official NPS Website]({PARKS_DATA[park_name]['url']})")
        
        st.markdown(f"Detailed analysis and recommendations for {selected_park}")
    
    # Main metrics
    st.subheader("📊 Key Metrics")
    m1, m2, m3, m4 = st.columns(4)
    
    # Dynamic metrics based on selection
    if selected_park != "All Parks":
        # Extract park name without emoji
        park_name = selected_park.split(" ", 1)[1] if " " in selected_park else selected_park
        
        # Park-specific metrics
        park_data = PARKS_DATA[park_name]
        m1.metric("Park Name", selected_park)
        m2.metric("Positive Sentiment", f"{park_data['positive']}%")
        m3.metric("Negative Sentiment", f"{park_data['negative']}%")
        
        if 'neutral' in park_data and park_data['neutral'] > 0:
            m4.metric("Neutral Sentiment", f"{park_data['neutral']}%")
        else:
            # Find park's position in ranking
            parks_sorted = sorted(PARKS_DATA.items(), key=lambda x: x[1]['positive'], reverse=True)
            park_rank = next(i+1 for i, p in enumerate(parks_sorted) if p[0] == park_name)
            m4.metric("Rank (by Positive)", f"{park_rank} of {len(PARKS_DATA)}")
    else:
        # Overall metrics
        avg_positive = sum(p['positive'] for p in PARKS_DATA.values())/len(PARKS_DATA)
        avg_negative = sum(p['negative'] for p in PARKS_DATA.values())/len(PARKS_DATA)
        avg_neutral = sum(p.get('neutral', 0) for p in PARKS_DATA.values())/len(PARKS_DATA)
        most_positive_park = max(PARKS_DATA.items(), key=lambda x: x[1]['positive'])
        most_positive_display = f"{most_positive_park[1]['emoji']} {most_positive_park[0]}"
        
        m1.metric("Total Parks", len(PARKS_DATA))
        m2.metric("Average Positive", f"{avg_positive:.1f}%")
        m3.metric("Average Negative", f"{avg_negative:.1f}%")
        m4.metric("Most Positive Park", f"{most_positive_display} ({most_positive_park[1]['positive']}%)")
    
    # Charts
    st.subheader("📈 Sentiment Analysis")
    chart1, chart2 = st.columns(2)
    
    with chart1:
        # Park comparison chart (highlight selected park if applicable)
        park_df = pd.DataFrame([
            {"Park": f"{v['emoji']} {k}", "Positive": v["positive"], "Negative": v["negative"], 
             "Neutral": v.get("neutral", 0), "ParkName": k}
            for k, v in PARKS_DATA.items()
        ])
        
        # Filter to selected park if applicable
        if selected_park != "All Parks":
            chart_title = f"{selected_park} vs Other Parks"
            # Highlight the selected park with a different color pattern
            fig = px.bar(park_df, x="Park", y=["Positive", "Negative", "Neutral"] if "Neutral" in park_df.columns and park_df["Neutral"].sum() > 0 else ["Positive", "Negative"], 
                        title=chart_title, barmode='stack',
                        color_discrete_map={"Positive": "#4CAF50", "Negative": "#F44336", "Neutral": "#FF9800"})
            
            # Add a pattern to highlight the selected park
            for i, bar in enumerate(fig.data):
                for j, park in enumerate(park_df["Park"]):
                    if park == selected_park:
                        if i < 3:  # Apply to all sentiment bars for selected park
                            bar.marker.line = dict(width=2, color="#1E88E5")
                            bar.marker.pattern = dict(shape="x", solidity=0.2)
        else:
            chart_title = "Park Sentiment Distribution"
            fig = px.bar(park_df, x="Park", y=["Positive", "Negative", "Neutral"] if "Neutral" in park_df.columns and park_df["Neutral"].sum() > 0 else ["Positive", "Negative"], 
                        title=chart_title, barmode='stack',
                        color_discrete_map={"Positive": "#4CAF50", "Negative": "#F44336", "Neutral": "#FF9800"})
        
        st.plotly_chart(fig, use_container_width=True)
    
    with chart2:
        # For feature analysis, filter to selected park's features if applicable
        if selected_park != "All Parks":
            # Extract park name without emoji
            park_name = selected_park.split(" ", 1)[1] if " " in selected_park else selected_park
            
            # Get features mentioned in reviews for this park
            park_features = [r["feature"] for r in REVIEWS if r["park"] == park_name]
            
            # Create a filtered feature dataset focused on this park
            feature_df = pd.DataFrame(FEATURE_DATA)
            # Add display name with emoji
            feature_df["display_name"] = feature_df.apply(lambda row: f"{row['emoji']} {row['feature']}", axis=1)
            chart_title = f"{selected_park} Feature Analysis"
        else:
            feature_df = pd.DataFrame(FEATURE_DATA)
            # Add display name with emoji
            feature_df["display_name"] = feature_df.apply(lambda row: f"{row['emoji']} {row['feature']}", axis=1)
            chart_title = "Feature Sentiment Analysis"
        
        # Apply feature filter if selected
        if selected_feature != "All Features":
            # Extract feature name without emoji
            feature_name = selected_feature.split(" ", 1)[1] if " " in selected_feature else selected_feature
            feature_df = feature_df[feature_df["feature"] == feature_name]
        
        fig = px.bar(feature_df, x="display_name", y=["positive", "negative", "neutral"] if "neutral" in feature_df.columns and feature_df["neutral"].sum() > 0 else ["positive", "negative"], 
                    title=chart_title, barmode='stack',
                    color_discrete_map={"positive": "#4CAF50", "negative": "#F44336", "neutral": "#FF9800"})
        fig.update_xaxes(title="Feature")
        fig.update_yaxes(title="Sentiment %")
        st.plotly_chart(fig, use_container_width=True)
    
    # Insights and Pie Chart
    st.subheader("🔍 Detailed Insights")
    insight_col, pie_col = st.columns([2, 1])
    
    with insight_col:
        with st.expander("🌟 Top Positive Aspects", expanded=True):
            if selected_park != "All Parks":
                # Extract park name without emoji
                park_name = selected_park.split(" ", 1)[1] if " " in selected_park else selected_park
                
                # Park-specific positive aspects
                if park_name == "Yellowstone":
                    st.markdown("""
                    - **Wildlife** 🐻: 92% positive reviews
                    - **Geysers** 🌋: 88% positive reviews
                    - **Hiking Trails** 🥾: 75% positive reviews
                    """)
                elif park_name == "Yosemite":
                    st.markdown("""
                    - **Waterfalls** 🌊: 96% positive reviews
                    - **Hiking** 🥾: 90% positive reviews
                    - **Forests** 🌲: 85% positive reviews
                    """)
                elif park_name == "Grand Canyon":
                    st.markdown("""
                    - **Scenery** 🌄: 98% positive reviews
                    - **Rim Trails** 🥾: 90% positive reviews
                    - **Viewpoints** 👀: 85% positive reviews
                    """)
                elif park_name == "Zion":
                    st.markdown("""
                    - **Narrows** 🏞️: 92% positive reviews
                    - **Angels Landing** 😇: 85% positive reviews
                    - **Scenery** 🌅: 80% positive reviews
                    """)
                elif park_name == "Big Bend":
                    st.markdown("""
                    - **Night Skies** 🌌: 95% positive reviews
                    - **Desert Views** 🏜️: 90% positive reviews
                    - **Mountain Trails** ⛰️: 85% positive reviews
                    """)
                elif park_name == "Black Canyon":
                    st.markdown("""
                    - **Canyon Views** 🏞️: 96% positive reviews
                    - **Photography** 📸: 88% positive reviews
                    - **Rim Trails** 🥾: 82% positive reviews
                    """)
                elif park_name == "Biscayne":
                    st.markdown("""
                    - **Snorkeling** 🤿: 94% positive reviews
                    - **Boating** ⛵: 88% positive reviews
                    - **Marine Life** 🐠: 86% positive reviews
                    """)
                elif park_name == "Hot Springs":
                    st.markdown("""
                    - **Thermal Waters** ♨️: 95% positive reviews
                    - **Historic Buildings** 🏛️: 85% positive reviews
                    - **Health Benefits** 💆: 80% positive reviews
                    """)
                elif park_name == "Independence":
                    st.markdown("""
                    - **Historical Significance** 🏛️: 95% positive reviews
                    - **Liberty Bell** 🔔: 92% positive reviews
                    - **Architecture** 🏛️: 88% positive reviews
                    """)
                elif park_name == "Valley Forge":
                    st.markdown("""
                    - **Historical Significance** ⚔️: 92% positive reviews
                    - **Memorial Monuments** 🗿: 85% positive reviews
                    - **Walking Trails** 🚶: 80% positive reviews
                    """)
                elif park_name == "Dry Tortugas":
                    st.markdown("""
                    - **Marine Life** 🐠: 98% positive reviews
                    - **Fort Jefferson** 🏰: 94% positive reviews
                    - **Snorkeling** 🤿: 92% positive reviews
                    """)
                elif park_name == "Everglades":
                    st.markdown("""
                    - **Wildlife Diversity** 🐊: 95% positive reviews
                    - **Airboat Tours** 🚤: 88% positive reviews
                    - **Bird Watching** 🦅: 86% positive reviews
                    """)
                else:
                    st.markdown("""
                    - **Scenery** 🌄: 90% positive reviews
                    - **Wildlife** 🦌: 85% positive reviews
                    - **Natural Features** 🏞️: 82% positive reviews
                    """)
            else:
                # Overall positive aspects
                st.markdown("""
                - **Scenery** 🌄: 95% positive reviews
                - **Wildlife** 🦌: 82% positive reviews
                - **Hiking Trails** 🥾: 65% positive reviews
                """)
        
        with st.expander("⚠️ Common Complaints", expanded=True):
            if selected_park != "All Parks":
                # Extract park name without emoji
                park_name = selected_park.split(" ", 1)[1] if " " in selected_park else selected_park
                
                # Park-specific complaints
                if park_name == "Yellowstone":
                    st.markdown("""
                    - **Crowds** 👥: 75% negative mentions
                    - **Traffic** 🚗: 65% negative mentions
                    - **Lodging Availability** 🏨: 60% negative mentions
                    """)
                elif park_name == "Yosemite":
                    st.markdown("""
                    - **Parking** 🅿️: 80% negative mentions
                    - **Valley Crowds** 👥: 70% negative mentions
                    - **Campsite Reservations** ⛺: 65% negative mentions
                    """)
                elif park_name == "Grand Canyon":
                    st.markdown("""
                    - **Summer Heat** ☀️: 70% negative mentions
                    - **Tour Prices** 💰: 60% negative mentions
                    - **Shuttle Waits** ⏱️: 55% negative mentions
                    """)
                elif park_name == "Zion":
                    st.markdown("""
                    - **Shuttle System** 🚌: 80% negative mentions
                    - **Crowds** 👥: 75% negative mentions  
                    - **Trail Safety** ⚠️: 60% negative mentions
                    - **Parking Availability** 🅿️: 55% negative mentions
                    """)
                elif park_name == "Big Bend":
                    st.markdown("""
                    - **Remote Location** 🏜️: 70% negative mentions
                    - **Lack of Services** 🏪: 65% negative mentions
                    - **Extreme Temperatures** 🌡️: 60% negative mentions
                    """)
                elif park_name == "Black Canyon":
                    st.markdown("""
                    - **Limited Accessibility** ♿: 75% negative mentions
                    - **Steep Trails** ⚠️: 65% negative mentions
                    - **Weather Variability** ⛈️: 55% negative mentions
                    """)
                elif park_name == "Biscayne":
                    st.markdown("""
                    - **Boat Access Only** ⛵: 80% negative mentions
                    - **Mosquitoes** 🦟: 70% negative mentions
                    - **Limited Facilities** 🚻: 60% negative mentions
                    """)
                elif park_name == "Hot Springs":
                    st.markdown("""
                    - **Aging Facilities** 🏚️: 75% negative mentions
                    - **Limited Parking** 🅿️: 65% negative mentions
                    - **Commercialization** 💰: 55% negative mentions
                    """)
                elif park_name == "Independence":
                    st.markdown("""
                    - **Urban Setting** 🏙️: 70% negative mentions
                    - **Wait Times** ⏳: 65% negative mentions
                    - **Noise Levels** 🔊: 55% negative mentions
                    """)
                elif park_name == "Valley Forge":
                    st.markdown("""
                    - **Weekend Crowds** 👥: 80% negative mentions
                    - **Limited Shade** ☀️: 70% negative mentions
                    - **Trail Maintenance** 🚧: 55% negative mentions
                    """)
                elif park_name == "Dry Tortugas":
                    st.markdown("""
                    - **Ferry Costs** ⛴️: 75% negative mentions
                    - **Weather Dependence** ⛈️: 70% negative mentions
                    - **Limited Amenities** 🏝️: 65% negative mentions
                    """)
                elif park_name == "Everglades":
                    st.markdown("""
                    - **Mosquitoes** 🦟: 85% negative mentions
                    - **Humidity** 💦: 75% negative mentions
                    - **Limited Wildlife Sightings** 👀: 55% negative mentions
                    """)
                else:
                    st.markdown("""
                    - **Crowds** 👥: 75% negative mentions
                    - **Fees** 💰: 65% negative mentions
                    - **Facility Maintenance** 🚽: 60% negative mentions
                    """)
            else:
                # Overall complaints
                st.markdown("""
                - **Crowds** 👥: 75% negative mentions
                - **Parking** 🅿️: 70% negative mentions
                - **Facilities** 🚻: 65% negative mentions
                - **Fees** 💰: 60% negative mentions
                """)
    
    with pie_col:
        if selected_park != "All Parks":
            # Extract park name without emoji
            park_name = selected_park.split(" ", 1)[1] if " " in selected_park else selected_park
            park_data = PARKS_DATA[park_name]
            st.plotly_chart(create_pie_chart(park_data['positive'], park_data['negative'], park_data.get('neutral', 0)), 
                           use_container_width=True)
        else:
            avg_positive = sum(p['positive'] for p in PARKS_DATA.values())/len(PARKS_DATA)
            avg_negative = sum(p['negative'] for p in PARKS_DATA.values())/len(PARKS_DATA)
            avg_neutral = sum(p.get('neutral', 0) for p in PARKS_DATA.values())/len(PARKS_DATA)
            st.plotly_chart(create_pie_chart(avg_positive, avg_negative, avg_neutral), 
                           use_container_width=True)
        
        # Display recommendations if a specific park is selected
        if selected_park != "All Parks":
            with st.expander("💡 Recommendations", expanded=True):
                park_name = selected_park.split(" ", 1)[1] if " " in selected_park else selected_park
                recs = get_recommendations(park_name)
                
                st.subheader("🛠️ Suggested Improvements")
                for improvement in recs["improvements"]:
                    st.markdown(f"- {improvement}")
                
                st.subheader("✨ Potential Enhancements")
                for enhancement in recs["enhancements"]:
                    st.markdown(f"- {enhancement}")
                
                st.subheader("🔬 Research Insights")
                st.markdown(recs["research"])
    
    # Reviews section
    st.subheader("📝 Visitor Reviews")
    filtered_reviews = filter_data(selected_park, selected_feature)
    
    if not filtered_reviews:
        st.warning("No reviews match the current filters")
    else:
        for review in filtered_reviews:
            sentiment_color = "#4CAF50" if review["sentiment"] == "Positive" else "#F44336" if review["sentiment"] == "Negative" else "#FF9800"
            
            with st.container():
                cols = st.columns([1, 10])
                with cols[0]:
                    st.markdown(f"<h3 style='text-align: center;'>{review['park_emoji']}{review['feature_emoji']}</h3>", unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"""
                    <div style="border-left: 4px solid {sentiment_color}; padding-left: 1rem;">
                        <p style="font-weight: bold; margin-bottom: 0.2rem;">{review['park']} - {review['feature']}</p>
                        <p style="color: {sentiment_color}; margin-top: 0; margin-bottom: 0.5rem;">{review['sentiment']}</p>
                        <p style="margin-top: 0;">{review['text']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("---")

# Run the dashboard
if __name__ == "__main__":
    national_park_dashboard()
