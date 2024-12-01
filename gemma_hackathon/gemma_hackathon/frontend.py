import streamlit as st
import random
from main import perform_rag_query

# Set page configuration
st.set_page_config(page_title="IOMarkets", page_icon="💰", layout="wide")

# Investment Headlines (previous code remains the same)
INVESTMENT_HEADLINES = [
    "Global Markets Showing Steady Growth in Q2",
    "Venture Capital Investments Surge in Tech Sector",
    "Renewable Energy Infrastructure Attracts Major Investments",
    "Private Equity Firms Explore Emerging Market Opportunities",
    "Real Estate Market Demonstrates Resilience",
    "Natural Resources Sector Gains Investor Attention",
    "Investment Funds Performance Exceeds Expectations",
    "Private Debt Markets Expand with Innovative Strategies",
    "Sustainable Investment Trends Gaining Momentum",
    "Technology Startups Attract Significant Capital"
]

# Investment Categories Descriptions (previous code remains the same)
CATEGORY_DESCRIPTIONS = {
    "Funds": "Professionally managed investment portfolios that pool money from multiple investors to invest in diversified assets. Offers broad market exposure and potential for balanced returns.",
    "Infrastructure & Energy": "Investments in physical systems and facilities like transportation, utilities, and energy production. Focuses on critical infrastructure projects with stable, long-term revenue potential.",
    "Natural Resources": "Investments in raw materials and commodities such as minerals, metals, oil, gas, and agricultural products. Provides exposure to global resource markets and potential hedge against inflation.",
    "Private Debt": "Lending to private companies outside traditional bank financing. Offers potentially higher yields and more tailored investment opportunities compared to public debt markets.",
    "Private Equity": "Direct investments in private companies not listed on public exchanges. Aims to create value through strategic improvements, operational efficiencies, and growth strategies.",
    "Real Estate": "Investments in physical properties including commercial, residential, and industrial real estate. Offers potential for rental income, property value appreciation, and portfolio diversification.",
    "Venture Capital": "Funding for early-stage, high-potential startup companies. Focuses on innovative businesses with significant growth prospects across various technological and innovative sectors."
}

# Investment Deals List
INVESTMENT_DEALS = [
    {"description": "Award-Winning Hedge Fund - Digital Assets Fund of Funds",
        "returns": "Funds", "raise_amount": "USD 25M to USD 75M", "highlights": "World's first Digital Assets Fund of Funds"},
    {"description": "A Geothermal Energy project in Bavaria",
        "returns": "Infrastructure & Energy", "raise_amount": "Lending upwards of USD 500K", "highlights": "Lending against listed equities and cryptocurrencies"},
    {"description": "A company with producing graphite assets in Africa and Latin America looking to raise circa USD 20M",
        "returns": "Natural Resources", "raise_amount": "Not specified", "highlights": "Established investment strategy"},
    {"description": "GBP 25M Tier 1/2 Capital is required for a UK Bank.",
        "returns": "Private Debt", "raise_amount": "USD 500M (USD 200M already committed)", "highlights": "Established international Venture Capital fund"},
    {"description": "Military Grade Cybersecurity Company looking for USD 50M Growth Capital.",
        "returns": "Private Equity", "raise_amount": "Up to USD 200M per strategy", "highlights": "40 different investment strategies"},
    {"description": "Green Hotels Development Platform looking to raise GBP 300M equity.",
        "returns": "Real State", "raise_amount": "EUR 913M (debt and equity)", "highlights": "Additional pipeline of circa EUR 3B"},
    {"description": "North Africa focused Early Stage VC Fund raising up to USD 20M.",
        "returns": "Venture Capital ", "raise_amount": "Circa GBP 300M", "highlights": "Social housing infrastructure project"},

]

# Initialize session state for chat history if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom CSS for cards and headlines (previous CSS remains the same)
st.markdown("""
<style>
@keyframes scrollHeadlines {
    0% { transform: translateY(100%); }
    10% { transform: translateY(0); }
    90% { transform: translateY(0); }
    100% { transform: translateY(-100%); }
}

.headlines-container {
    width: 100%;
    height: 50px;
    overflow: hidden;
    background-color: #f0f0f0;
    border-radius: 8px;
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.headlines-wrapper {
    display: flex;
    flex-direction: column;
    animation: scrollHeadlines 20s linear infinite;
}

.headline {
    padding: 10px;
    text-align: center;
    white-space: nowrap;
    font-weight: bold;
    color: #333;
}

.category-card, .deal-card {
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 15px;
    margin:4px 0 ;
    background-color: #f9f9f9;
    transition: transform 0.3s ease;
}

.category-card:hover, .deal-card:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.deal-card {
    
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# Main page layout
st.title("🤖 Get The Best Recommendation For Your Future Investments From Our AI-Powered Business Intelligence Engine.")

# Scrolling Headlines (previous code remains the same)


# Create columns for Investment Categories and Deals
col1, col2 = st.columns(2)

with col1:
    st.header("Investment Categories")
    for category, description in CATEGORY_DESCRIPTIONS.items():
        st.markdown(f"""
        <div class="category-card">
            <h3>{category}</h3>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.header("Top Trending Opportunities 🔥")
    for deal in INVESTMENT_DEALS:
        st.markdown(f"""
        <div class="deal-card">
            <h3>{deal['description']}</h3>
            <p><strong>Category:</strong> {deal['returns']}</p>

        </div>
        """, unsafe_allow_html=True)

# Divider
st.divider()

# Chat input at the top
prompt = st.chat_input("Enter your investment-related question")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate and display AI response for the latest user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        response = perform_rag_query(
            "./gemma_hackathon/AllStatus.csv", st.session_state.messages[-1]["content"])
        st.write(response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
