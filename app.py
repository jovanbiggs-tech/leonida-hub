import streamlit as st
import feedparser
import pandas as pd
import requests
from datetime import datetime

# ==========================================
# 1. SYSTEM & MONETIZATION CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Leonida Hub | GTA VI Companion & PC Readiness",
    page_icon="🌴",
    layout="wide"
)

# Replace these with your live payout & affiliate links
MONETIZATION = {
    "amazon_tag": "YOUR_AMAZON_TAG-20",        # Amazon Associates ID
    "pro_checkout": "https://lemonsqueezy.com", # Global payouts (supports Jamaica via PayPal/Wise/Bank)
    "app_url": "https://your-app.streamlit.app" # Update once deployed
}

RSS_SOURCES = {
    "IGN Games": "https://feeds.feedburner.com/ign/games-all",
    "GameSpot": "https://www.gamespot.com/feeds/game-news/",
    "PC Gamer": "https://www.pcgamer.com/rss/"
}

# ==========================================
# 2. LIVE DATA PULLING ENGINES (NEWS + REDDIT)
# ==========================================
@st.cache_data(ttl=3600)
def fetch_live_gta_news():
    articles = []
    keywords = ["gta", "grand theft auto", "rockstar", "leonida", "vice city"]
    for source_name, url in RSS_SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:25]:
                if any(k in entry.title.lower() for k in keywords):
                    articles.append({
                        "source": source_name,
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.get("published", datetime.now().strftime("%Y-%m-%d")),
                        "summary": entry.get("summary", "")[:220] + "..."
                    })
        except Exception:
            continue
    return articles

@st.cache_data(ttl=1800)
def fetch_reddit_trends():
    posts = []
    headers = {"User-Agent": "LeonidaHubBot/1.0"}
    try:
        resp = requests.get("https://www.reddit.com/r/GTA6/hot.json?limit=12", headers=headers, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            for child in data["data"]["children"]:
                p = child["data"]
                if not p.get("stickied"):
                    posts.append({
                        "title": p["title"],
                        "upvotes": p["ups"],
                        "comments": p["num_comments"],
                        "url": f"https://reddit.com{p['permalink']}",
                        "flair": p.get("link_flair_text", "Discussion")
                    })
    except Exception:
        pass
    return posts

# ==========================================
# 3. HEADER & GLOBAL REVENUE BANNER
# ==========================================
st.title("🌴 Leonida Hub: GTA VI Companion & PC Readiness Engine")
st.caption(f"Live Data Sync Active • Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

b_col1, b_col2 = st.columns([3, 1])
with b_col1:
    st.info("🔥 **Console Launch Live!** Track your Leonida empire now or prep your PC rig for the upcoming PC port.")
with b_col2:
    st.link_button("💎 Unlock Pro Tracker ($9)", MONETIZATION["pro_checkout"], use_container_width=True)

# ==========================================
# 4. UNIFIED 3-TAB REVENUE ARCHITECTURE
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "🖥️ 1. PC Readiness & Affiliate Engine",
    "💰 2. Leonida Profit & Completion Tracker",
    "🎬 3. Live News, Reddit Trends & Script Generator"
])

# ------------------------------------------
# TAB 1: PC READINESS & HARDWARE AFFILIATES
# ------------------------------------------
with tab1:
    st.subheader("Check Your PC Hardware Before the GTA VI PC Release")
    
    GPU_DATA = {
        "GTX 1660 / RX 580": {"score": 30, "tier": "Below Minimum (Upgrade Required)", "rec_gpu": "RTX+4060+Ti"},
        "RTX 3060 / RX 6600 XT": {"score": 62, "tier": "1080p Medium (60 FPS Target)", "rec_gpu": "RTX+4070+Super"},
        "RTX 4070 / RX 7800 XT": {"score": 85, "tier": "1440p High (Ray Tracing Ready)", "rec_gpu": "RTX+4080+Super"},
        "RTX 4080 Super / RX 7900 XTX": {"score": 98, "tier": "4K Ultra Enthusiast", "rec_gpu": None},
    }
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        gpu = st.selectbox("Current Graphics Card (GPU)", list(GPU_DATA.keys()))
    with col_b:
        ram = st.select_slider("System RAM (GB)", options=[8, 16, 32, 64], value=16)
    with col_c:
        ssd = st.selectbox("Primary Storage", ["Hard Drive (HDD)", "SATA SSD", "NVMe Gen4 SSD"], index=1)

    if st.button("Calculate Readiness & Upgrade Path", type="primary"):
        g_info = GPU_DATA[gpu]
        ram_pts = 100 if ram >= 32 else (65 if ram == 16 else 25)
        ssd_pts = 100 if ssd == "NVMe Gen4 SSD" else (55 if ssd == "SATA SSD" else 20)
        final_score = int((g_info["score"] * 0.55) + (ram_pts * 0.25) + (ssd_pts * 0.20))

        st.metric("GTA VI PC Readiness Score", f"{final_score} / 100", g_info["tier"])
        st.progress(final_score / 100)

        st.markdown("### 🛒 Automated Hardware Upgrade Recommendations")
        tag = MONETIZATION["amazon_tag"]
        
        if g_info["rec_gpu"]:
            st.warning(f"**GPU Bottleneck:** Upgrade to handle Vice City's dense crowds and ray tracing. [**Check Live GPU Deals →**](https://www.amazon.com/s?k={g_info['rec_gpu']}&tag={tag})")
        if ram < 32:
            st.warning(f"**Memory Bottleneck:** 32GB is recommended for smooth open-world streaming. [**Compare 32GB DDR5 Kits →**](https://www.amazon.com/s?k=32GB+DDR5+Gaming+RAM&tag={tag})")
        if ssd != "NVMe Gen4 SSD":
            st.warning(f"**Storage Bottleneck:** NVMe Gen4 prevents texture pop-in. [**View 2TB Gen4 NVMe SSDs →**](https://www.amazon.com/s?k=2TB+NVMe+Gen4+SSD&tag={tag})")

# ------------------------------------------
# TAB 2: IN-GAME PROFIT & COMPLETION TRACKER
# ------------------------------------------
with tab2:
    st.subheader("Leonida Empire & Cash-Per-Hour Optimizer")
    st.write("Interactive calculator for console players—drives repeat daily visits and Pro template conversions.")

    businesses = pd.DataFrame([
        {"Asset": "Vice City Nightclub", "Hourly Passive ($)": 50000, "Setup Cost ($)": 1500000, "Owned": True},
        {"Asset": "Port Gellhorn Cargo Depot", "Hourly Passive ($)": 75000, "Setup Cost ($)": 2200000, "Owned": False},
        {"Asset": "Keys Smuggling Run", "Hourly Passive ($)": 90000, "Setup Cost ($)": 2800000, "Owned": False},
        {"Asset": "Downtown Auto Chop Shop", "Hourly Passive ($)": 40000, "Setup Cost ($)": 1100000, "Owned": True},
    ])

    edited_df = st.data_editor(businesses, use_container_width=True, hide_index=True)
    owned_assets = edited_df[edited_df["Owned"] == True]
    
    m1, m2 = st.columns(2)
    m1.metric("Current In-Game Hourly Income", f"${owned_assets['Hourly Passive ($)'].sum():,.0f} / hr")
    m2.metric("Assets Unlocked", f"{len(owned_assets)} / {len(edited_df)}")

    st.success("💡 **Pro Upsell Hook:** Unlock cloud-synced progress across mobile & PC + the full 100% Collectible Checklist.")
    st.link_button("Download Full Pro Notion & CSV Tracker ($9)", MONETIZATION["pro_checkout"])

# ------------------------------------------
# TAB 3: LIVE NEWS, REDDIT & SCRIPT GENERATOR
# ------------------------------------------
with tab3:
    st.subheader("Live Intelligence & Automated Short-Form Video Scripts")
    
    feed_col1, feed_col2 = st.columns(2)
    
    with feed_col1:
        st.markdown("#### 📰 Official Gaming Press (RSS)")
        news_items = fetch_live_gta_news()
        if not news_items:
            st.info("No breaking press headlines in the last hour.")
        for idx, item in enumerate(news_items[:4]):
            with st.expander(f"[{item['source']}] {item['title']}", expanded=(idx == 0)):
                st.write(item["summary"])
                st.markdown(f"[Read Article]({item['link']})")
                script = f"""HOOK (0-3s): Huge GTA 6 news just broke via {item['source']}!
BODY (3-20s): {item['title']}. Here is what this means for console players right now—and for the upcoming PC port.
CTA (20-25s): Test if your PC can run GTA 6 or track your 100% completion at {MONETIZATION['app_url']}!"""
                st.text_area("Copy Video Script:", script, height=130, key=f"news_{idx}")

    with feed_col2:
        st.markdown("#### 🔥 Trending on r/GTA6 (Viral Hooks)")
        reddit_posts = fetch_reddit_trends()
        if not reddit_posts:
            st.info("Could not reach Reddit feed right now.")
        for idx, post in enumerate(reddit_posts[:4]):
            with st.expander(f"⬆️ {post['upvotes']} | {post['title'][:60]}...", expanded=(idx == 0)):
                st.write(f"**Full Topic:** {post['title']} ({post['comments']} comments)")
                st.markdown(f"[View Thread]({post['url']})")
                r_script = f"""HOOK (0-3s): The GTA 6 community is going crazy over this discovery!
BODY (3-20s): Over {post['upvotes']} players are talking about: "{post['title']}". Here's the breakdown you need to know.
CTA (20-25s): Use my free Leonida Hub tracker & PC readiness tool—link in bio!"""
                st.text_area("Copy Viral Community Script:", r_script, height=130, key=f"red_{idx}")
