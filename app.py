import streamlit as st
import pandas as pd
import altair as alt

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')
    df.columns = df.columns.str.strip()
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed')
    df['Year'] = df['Order Date'].dt.year
    df['YearMonth'] = df['Order Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# ── Sidebar navigation ─────────────────────────────────────────────────────────
st.sidebar.title('Navigation')
page = st.sidebar.selectbox('Choose a Page', [
    'Introduction',
    'Basic Analysis',
    'Bar Chart + Scatter Plot',
    'Line Chart + Histogram',
    'Pie Chart + Bar Chart',
    'Map View + Scatter Plot'
])

# ══════════════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ══════════════════════════════════════════════════════════════════════════════
if page == 'Introduction':
    st.title('🛒 Global Superstore Sales Dashboard')
    st.write('Use the sidebar to explore different interactive visualizations.')
    st.dataframe(df.head(10))
    st.write(f"**Total rows:** {len(df):,} | **Columns:** {len(df.columns)}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. BASIC ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == 'Basic Analysis':
    st.title('Basic Analysis')

    # Dropdown
    categories = ['All'] + sorted(df['Category'].unique().tolist())
    selected_cat = st.selectbox('Select Product Category', categories)

    # Slider
    min_sales = int(df['Sales'].min())
    max_sales = int(df['Sales'].max())
    sales_range = st.slider('Filter by Sales Amount', min_sales, max_sales, (min_sales, max_sales))

    # Filter
    filtered = df.copy()
    if selected_cat != 'All':
        filtered = filtered[filtered['Category'] == selected_cat]
    filtered = filtered[(filtered['Sales'] >= sales_range[0]) & (filtered['Sales'] <= sales_range[1])]

    st.write(f"Showing **{len(filtered):,}** records")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Sales by Category (Bar)')
        bar_data = filtered.groupby('Category')['Sales'].sum().reset_index()
        bar = alt.Chart(bar_data).mark_bar().encode(
            x=alt.X('Category:N', title='Category'),
            y=alt.Y('Sales:Q', title='Total Sales'),
            color=alt.Color('Category:N', legend=None),
            tooltip=['Category', 'Sales']
        ).properties(width=300, height=300)
        st.altair_chart(bar, use_container_width=True)

    with col2:
        st.subheader('Sales by Category (Pie)')
        pie_data = filtered.groupby('Category')['Sales'].sum().reset_index()
        pie = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta('Sales:Q'),
            color=alt.Color('Category:N'),
            tooltip=['Category', 'Sales']
        ).properties(width=300, height=300)
        st.altair_chart(pie, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 3. BAR CHART + SCATTER PLOT
# ══════════════════════════════════════════════════════════════════════════════
elif page == 'Bar Chart + Scatter Plot':
    st.title('Bar Chart + Scatter Plot')
    st.info('Select a category from the dropdown to filter the scatter plot.')

    selected_cat = st.selectbox('Select Category', sorted(df['Category'].unique().tolist()))
    filtered = df[df['Category'] == selected_cat]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Sales by Category')
        bar_data = df.groupby('Category')['Sales'].sum().reset_index()
        bar = alt.Chart(bar_data).mark_bar().encode(
            x=alt.X('Category:N'),
            y=alt.Y('Sales:Q'),
            color=alt.condition(
                alt.datum.Category == selected_cat,
                alt.value('#E8593C'),
                alt.value('#B4B2A9')
            ),
            tooltip=['Category', 'Sales']
        ).properties(width=300, height=300)
        st.altair_chart(bar, use_container_width=True)

    with col2:
        st.subheader(f'Price vs Quantity — {selected_cat}')
        scatter = alt.Chart(filtered).mark_circle(size=60, opacity=0.6).encode(
            x=alt.X('Sales:Q', title='Sales (Price)'),
            y=alt.Y('Quantity:Q', title='Quantity'),
            color=alt.Color('Sub-Category:N'),
            tooltip=['Product Name', 'Sales', 'Quantity', 'Sub-Category']
        ).properties(width=300, height=300)
        st.altair_chart(scatter, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 4. LINE CHART + HISTOGRAM
# ══════════════════════════════════════════════════════════════════════════════
elif page == 'Line Chart + Histogram':
    st.title('Line Chart + Histogram')
    st.info('Select a year to filter both charts.')

    years = sorted(df['Year'].unique().tolist())
    selected_year = st.selectbox('Select Year', years)
    filtered = df[df['Year'] == selected_year]

    monthly = filtered.groupby('YearMonth')['Sales'].sum().reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f'Monthly Sales — {selected_year}')
        line = alt.Chart(monthly).mark_line(point=True, color='#1D9E75').encode(
            x=alt.X('YearMonth:N', title='Month', sort=None),
            y=alt.Y('Sales:Q', title='Total Sales'),
            tooltip=['YearMonth', 'Sales']
        ).properties(width=300, height=300)
        st.altair_chart(line, use_container_width=True)

    with col2:
        st.subheader(f'Quantity Distribution — {selected_year}')
        hist = alt.Chart(filtered).mark_bar(color='#534AB7').encode(
            x=alt.X('Quantity:Q', bin=alt.Bin(maxbins=20), title='Quantity'),
            y=alt.Y('count()', title='Count'),
            tooltip=['count()']
        ).properties(width=300, height=300)
        st.altair_chart(hist, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 5. PIE CHART + BAR CHART
# ══════════════════════════════════════════════════════════════════════════════
elif page == 'Pie Chart + Bar Chart':
    st.title('Pie Chart + Bar Chart')
    st.info('Select a category from the dropdown to see sales by country.')

    selected_cat = st.selectbox('Select Category', sorted(df['Category'].unique().tolist()))
    filtered = df[df['Category'] == selected_cat]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Sales Distribution by Category')
        pie_data = df.groupby('Category')['Sales'].sum().reset_index()
        pie = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta('Sales:Q'),
            color=alt.Color('Category:N'),
            tooltip=['Category', 'Sales']
        ).properties(width=300, height=300)
        st.altair_chart(pie, use_container_width=True)

    with col2:
        st.subheader(f'Top 10 States by Sales - {selected_cat}')
        state_data = filtered.groupby('State')['Sales'].sum().reset_index().sort_values('Sales', ascending=False).head(10)
        bar = alt.Chart(state_data).mark_bar(color='#1D9E75').encode(
            x=alt.X('Sales:Q', title='Total Sales'),
            y=alt.Y('State:N', sort='-x'),
            tooltip=['State', 'Sales']
        ).properties(width=300, height=300)
        st.altair_chart(bar, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 6. MAP VIEW + SCATTER PLOT
# ══════════════════════════════════════════════════════════════════════════════
elif page == 'Map View + Scatter Plot':
    st.title('Map View + Scatter Plot')
    st.info('Select a state to filter the scatter plot.')

    states = sorted(df['State'].unique().tolist())
    selected_state = st.selectbox('Select State', states)
    filtered = df[df['State'] == selected_state]

    st.subheader('Top 20 States by Sales')
    state_sales = df.groupby('State')['Sales'].sum().reset_index()
    state_bar = alt.Chart(state_sales.sort_values('Sales', ascending=False).head(20)).mark_bar().encode(
        x=alt.X('Sales:Q'),
        y=alt.Y('State:N', sort='-x'),
        color=alt.condition(
            alt.datum.State == selected_state,
            alt.value('#E8593C'),
            alt.value('#378ADD')
        ),
        tooltip=['State', 'Sales']
    ).properties(height=400)
    st.altair_chart(state_bar, use_container_width=True)

    st.subheader(f'Sales vs Quantity — {selected_state}')
    scatter = alt.Chart(filtered).mark_circle(size=60, opacity=0.6).encode(
        x=alt.X('Sales:Q', title='Sales'),
        y=alt.Y('Quantity:Q', title='Quantity'),
        color=alt.Color('Category:N'),
        tooltip=['Product Name', 'Sales', 'Quantity', 'Category']
    ).properties(height=350)
    st.altair_chart(scatter, use_container_width=True)
