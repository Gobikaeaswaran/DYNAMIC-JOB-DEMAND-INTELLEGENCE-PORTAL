import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="Job Market Insights", page_icon="📈")

# ----- Data schema sample and load path -----
@st.cache_data(ttl=120)
def sample_data(n=3000):
    rng = np.random.default_rng(2026)
    skills = [
        "Python","SQL","AWS","Docker","Kubernetes","React","TensorFlow","Spark","Go","Java","Node.js","Django","NoSQL","MLOps","Generative AI"
    ]
    locs = ["NY","SF","SEA","AUS","CHI","LDN","BER","TOR","BOM","SGP"]
    titles = [
        "Data Engineer","ML Engineer","Software Engineer","Product Manager",
        "Data Scientist","DevOps Engineer","Frontend Engineer","Backend Engineer"
    ]

    base = datetime.now() - timedelta(days=365)
    rows = []
    for i in range(n):
        title = rng.choice(titles)
        loc = rng.choice(locs)
        x = int(rng.integers(0, 16))
        salary_med = 65000 + x * 9000 + int(rng.integers(-8000, 12000))
        salary_min = int(salary_med * (0.75 + rng.random() * 0.1))
        salary_max = int(salary_med * (1.2 + rng.random() * 0.2))
        posted = base + timedelta(days=int(rng.integers(0, 365)))
        skill_count = int(rng.integers(2, 6))
        row_skills = rng.choice(skills, skill_count, replace=False).tolist()
        rows.append({
            "id": f"job_{i:06d}",
            "job_title": title,
            "location": loc,
            "years_experience": x,
            "salary_min": salary_min,
            "salary_median": salary_med,
            "salary_max": salary_max,
            "required_skills": row_skills,
            "posting_date": posted
        })
    return pd.DataFrame(rows)


df = sample_data(3000)

# ----- Sidebar filters -----
st.sidebar.header("Market filters")
with st.sidebar.form("filter_form"):
    start_date = st.date_input("From", value=datetime.now().date() - timedelta(days=180))
    end_date = st.date_input("To", value=datetime.now().date())
    experience_range = st.slider("Years experience", 0, 20, (0, 12))
    loc = st.multiselect("Locations", sorted(df["location"].unique()), default=sorted(df["location"].unique())[:5])
    title = st.multiselect("Job Titles", sorted(df["job_title"].unique()), default=sorted(df["job_title"].unique())[:5])
    all_skills = sorted({s for x in df["required_skills"] for s in x})
    user_skills = st.multiselect("Your skills", all_skills, default=["Python","SQL"])
    submitted = st.form_submit_button("Apply filters")

filtered = df[
    (df["posting_date"].dt.date >= start_date) &
    (df["posting_date"].dt.date <= end_date) &
    (df["years_experience"] >= experience_range[0]) &
    (df["years_experience"] <= experience_range[1]) &
    (df["location"].isin(loc)) &
    (df["job_title"].isin(title))
].copy()

st.title("Interactive Job Market Insights Dashboard")
st.markdown("Real-time oriented - dynamic slicing and what-if skill coverage.")

# ----- KPI cards -----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Open jobs", f"{len(filtered):,}")
c2.metric("Median salary", f"${int(filtered['salary_median'].median()):,}")
c3.metric("Average experience", f"{filtered['years_experience'].mean():.1f}")
c4.metric("Unique skills", f"{filtered['required_skills'].explode().nunique()}")

# ----- Trend line (experience, salary) -----
st.subheader("Salary trend by posting week")
weekly = (
    filtered.assign(post_week=filtered["posting_date"].dt.to_period("W").dt.start_time)
    .groupby("post_week")
    .agg(salary_median=("salary_median","median"), count=("id","size"))
    .reset_index()
)
fig_trend = px.line(
    weekly, x="post_week", y="salary_median",
    markers=True, title="Weekly median salary trend",
    labels={"post_week":"Week","salary_median":"Median Salary"}
)
fig_trend.add_bar(
    x=weekly["post_week"], y=weekly["count"], name="Job count", opacity=0.35, yaxis="y2"
)
fig_trend.update_layout(
    yaxis2=dict(overlaying="y", side="right", title="Jobs"),
    legend=dict(orientation="h")
)
st.plotly_chart(fig_trend, use_container_width=True)

# ----- Heatmap via pivot for location x role (job density) -----
st.subheader("Job density by location and title")
pivot = filtered.pivot_table(index="location", columns="job_title", values="id", aggfunc="count", fill_value=0)
fig_heat = px.imshow(
    pivot,
    labels=dict(x="Job Title", y="Location", color="Postings"),
    x=pivot.columns, y=pivot.index,
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_heat, use_container_width=True)

# ----- Skill gap radar (user skills vs demand) -----
st.subheader("Skill gap comparison")
skill_counts = filtered.explode("required_skills").groupby("required_skills").size().sort_values(ascending=False)
top_skills = skill_counts.head(9).index.tolist()
demand = skill_counts.reindex(top_skills, fill_value=0)
owned = [1 if skill in user_skills else 0 for skill in top_skills]
skill_gap = pd.DataFrame({
    "skill": top_skills,
    "market_demand": demand.values,
    "user_coverage": owned
})
fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=skill_gap["market_demand"], theta=skill_gap["skill"],
    fill="toself", name="Market demand"
))
fig_radar.add_trace(go.Scatterpolar(
    r=skill_gap["user_coverage"] * skill_gap["market_demand"].max(),
    theta=skill_gap["skill"], fill="toself", name="Your coverage"
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True
)
st.plotly_chart(fig_radar, use_container_width=True)

# ----- What-if analysis -----
st.subheader("What-if results")
if len(user_skills) == 0:
    st.warning("Select at least one skill to compute what-if results.")
else:
    matching = filtered[filtered["required_skills"].apply(lambda x: set(user_skills).issubset(set(x)))]
    st.markdown(f"*Jobs matching your skill set:* **{len(matching):,}**")
    if not matching.empty:
        st.write("Estimated salary range (matching subset):")
        st.metric("Min", f"${int(matching['salary_min'].quantile(0.1)):,}")
        st.metric("Median", f"${int(matching['salary_median'].median()):,}")
        st.metric("Max", f"${int(matching['salary_max'].quantile(0.9)):,}")
    else:
        st.info("No exact skill-match jobs in this filter. Try broader role/location or fewer required skills.")

# ----- Real-time design note -----
st.info(
    "For live data: implement streaming workers + DB upsert + FastAPI SSE.\n"
    "This demo uses cached synthetic data and 2-minute cache TTL for instant tinkering."
)
