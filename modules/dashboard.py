"""
Dashboard Module
Handles dashboard UI and layout
"""

import streamlit as st
from modules.analysis import CrimeAnalyzer
from modules.filters import DataFilter


class Dashboard:
    """Manages crime analysis dashboard"""
    
    def __init__(self):
        """Initialize dashboard"""
        self.analyzer = CrimeAnalyzer()
        self.filter = DataFilter()
    
    def load_data(self):
        """Load data for dashboard"""
        self.analyzer.load_data()
        self.filter.load_data()
    
    def render_header(self):
        """Render dashboard header"""
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.title("📊 Crime Analysis Dashboard")
        with col2:
            st.markdown("")
            st.markdown("")
            st.info("Real-time Crime Analytics")
    
    def render_summary_cards(self, filtered_data=None):
        """Render summary statistics cards"""
        st.markdown("### 📈 Summary Statistics")
        
        stats = self.filter.get_summary_stats(filtered_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Crimes", stats['total_crimes'])
        
        with col2:
            st.metric("Cities", stats['unique_cities'])
        
        with col3:
            st.metric("Crime Types", stats['unique_types'])
        
        with col4:
            st.metric("Common Weapon", stats['most_common_weapon'])
    
    def render_filters(self):
        """Render filter sidebar with session state tracking"""
        st.sidebar.markdown("---")
        st.sidebar.title("🔍 Filters")
        
        # Initialize session state for filters
        if 'filter_city' not in st.session_state:
            st.session_state.filter_city = "All"
        if 'filter_crime' not in st.session_state:
            st.session_state.filter_crime = "All"
        if 'filter_gender' not in st.session_state:
            st.session_state.filter_gender = "All"
        
        cities = ["All"] + self.filter.get_unique_cities()
        crime_types = ["All"] + self.filter.get_unique_crime_types()
        genders = ["All"] + self.filter.get_unique_genders()
        
        # Use session state for filter persistence
        selected_city = st.sidebar.selectbox(
            "🏙️ Select City", 
            cities, 
            index=cities.index(st.session_state.filter_city),
            key='filter_city'
        )
        
        selected_crime = st.sidebar.selectbox(
            "⚠️ Select Crime Type", 
            crime_types, 
            index=crime_types.index(st.session_state.filter_crime),
            key='filter_crime'
        )
        
        selected_gender = st.sidebar.selectbox(
            "👤 Select Victim Gender", 
            genders, 
            index=genders.index(st.session_state.filter_gender),
            key='filter_gender'
        )
        
        # Reset filters button
        if st.sidebar.button("🔄 Reset Filters"):
            st.session_state.filter_city = "All"
            st.session_state.filter_crime = "All"
            st.session_state.filter_gender = "All"
            st.rerun()
        
        return selected_city, selected_crime, selected_gender
    
    def apply_filters(self, city, crime_type, gender):
        """Apply filters to data and return filtered dataframe"""
        return self.filter.filter_multiple(city, crime_type, gender)
    
    def render_safety_status(self, filtered_data=None):
        """Render safety status"""
        df = filtered_data if filtered_data is not None else self.filter.df
        
        if df is None or len(df) == 0:
            return
        
        st.markdown("### 🚨 Safety Status")
        
        safety = self.analyzer.safety_level()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.warning(safety)
        
        with col2:
            st.info(f"Total Records: {len(df)}")
    
    def render_analysis_section(self, filtered_data=None):
        """Render main analysis section with dynamic interactive charts"""
        st.markdown("---")
        st.markdown("### 📊 Analysis & Visualizations")
        
        # Display filter status
        if filtered_data is not None and len(filtered_data) > 0:
            info_text = f"**Showing {len(filtered_data):,} records** from filtered dataset"
            st.info(info_text)
        
        # Chart type selector
        st.markdown("#### 🎨 Chart Patterns")
        chart_type = st.selectbox(
            "Choose visualization pattern:",
            [
                "📊 Standard Analysis (5 Charts)",
                "🔥 Heatmap Pattern",
                "🌳 Hierarchy Sunburst",
                "📍 Crime Pattern Scatter",
                "📦 Distribution Comparison",
                "🎯 Advanced Analytics Mix"
            ]
        )
        
        st.markdown("---")
        
        # Render charts based on selection
        if chart_type == "📊 Standard Analysis (5 Charts)":
            self._render_standard_charts(filtered_data)
        elif chart_type == "🔥 Heatmap Pattern":
            self._render_heatmap_pattern(filtered_data)
        elif chart_type == "🌳 Hierarchy Sunburst":
            self._render_sunburst_pattern(filtered_data)
        elif chart_type == "📍 Crime Pattern Scatter":
            self._render_scatter_pattern(filtered_data)
        elif chart_type == "📦 Distribution Comparison":
            self._render_distribution_pattern(filtered_data)
        elif chart_type == "🎯 Advanced Analytics Mix":
            self._render_advanced_mix(filtered_data)
    
    def _render_standard_charts(self, filtered_data=None):
        """Render 5 standard chart tabs"""
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📍 By City", "⚠️ By Type", "📈 Trend", "👥 Gender", "🔫 Weapons"]
        )
        
        with tab1:
            fig = self.analyzer.bar_chart_city_crimes(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available")
        
        with tab2:
            fig = self.analyzer.bar_chart_crime_type(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available")
        
        with tab3:
            fig = self.analyzer.line_chart_monthly_trend(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No trend data available")
        
        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                fig = self.analyzer.pie_chart_gender_distribution(filtered_data)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = self.analyzer.bar_chart_gender_by_city(filtered_data)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab5:
            fig = self.analyzer.pie_chart_weapon_usage(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available")
    
    def _render_heatmap_pattern(self, filtered_data=None):
        """Render heatmap pattern visualization"""
        st.subheader("🔥 Crime Intensity Heatmap")
        st.markdown("Interactive heatmap showing crime intensity across cities and types")
        
        fig = self.analyzer.heatmap_city_type(filtered_data)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data for heatmap")
    
    def _render_sunburst_pattern(self, filtered_data=None):
        """Render sunburst hierarchy pattern"""
        st.subheader("🌳 Crime Distribution Hierarchy")
        st.markdown("Interactive sunburst showing crime hierarchy (Crime Type → Cities)")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = self.analyzer.sunburst_crime_hierarchy(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient data for sunburst")
        
        with col2:
            st.markdown("**How to use:**")
            st.markdown("- Click segments to zoom in")
            st.markdown("- Double-click to zoom out")
            st.markdown("- Hover to see details")
    
    def _render_scatter_pattern(self, filtered_data=None):
        """Render scatter pattern visualization"""
        st.subheader("📍 Crime Pattern Scatter Analysis")
        st.markdown("Multi-dimensional scatter plot: City × Type × Gender (bubble size = frequency)")
        
        fig = self.analyzer.scatter_crime_pattern(filtered_data)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data for scatter plot")
    
    def _render_distribution_pattern(self, filtered_data=None):
        """Render distribution comparison charts"""
        st.subheader("📦 Distribution Pattern Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Box Plot - Crime Type Distribution**")
            fig = self.analyzer.box_plot_crime_by_type(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available")
        
        with col2:
            st.markdown("**Weapon Usage Histogram**")
            fig = self.analyzer.histogram_crime_distribution(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available")
    
    def _render_advanced_mix(self, filtered_data=None):
        """Render advanced analytics mix"""
        st.subheader("🎯 Advanced Multi-Pattern Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Heatmap", "Scatter", "Weapons"])
        
        with tab1:
            fig = self.analyzer.heatmap_city_type(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = self.analyzer.scatter_crime_pattern(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            fig = self.analyzer.bar_crime_by_weapon_city(filtered_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    def render_data_table(self, filtered_data=None):
        """Render data table"""
        st.markdown("---")
        st.markdown("### 📋 Crime Records")
        
        df = filtered_data if filtered_data is not None else self.filter.df
        
        if df is None or len(df) == 0:
            st.warning("No records found")
            return
        
        # Select columns to display
        display_cols = ['id', 'type', 'city', 'date', 'time', 'gender', 'weapon']
        available_cols = [col for col in display_cols if col in df.columns]
        
        st.dataframe(df[available_cols], use_container_width=True, height=400)
    
    def render_emergency_contacts(self):
        """Render emergency contacts"""
        st.markdown("---")
        st.markdown("### 📞 Emergency Contacts")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success("**Police Emergency**\n☎️ 100")
        
        with col2:
            st.info("**Women Safety**\n☎️ 1091")
        
        with col3:
            st.error("**Ambulance**\n☎️ 102")
    
    def render_footer(self):
        """Render dashboard footer"""
        st.markdown("---")
        st.markdown("**📊 Crime Record Management & Analysis System**")
        st.markdown("Data updated in real-time | For official use only")
