"""
Analysis Module
Handles all data analysis and calculations
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modules.db_operations import DatabaseManager


class CrimeAnalyzer:
    """Analyzes crime data"""
    
    def __init__(self):
        """Initialize analyzer"""
        self.db = DatabaseManager()
        self.df = None
    
    def load_data(self):
        """Load data from database into DataFrame"""
        try:
            columns, results = self.db.fetch_all_crimes()
            if results is None:
                return None
            
            self.df = pd.DataFrame(results, columns=columns)
            self.df['date'] = pd.to_datetime(self.df['date'])
            return self.df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def crime_count_by_city(self):
        """Get crime count by city"""
        if self.df is None or len(self.df) == 0:
            return None
        
        return self.df['city'].value_counts().reset_index()
    
    def crime_count_by_type(self):
        """Get crime count by type"""
        if self.df is None or len(self.df) == 0:
            return None
        
        return self.df['type'].value_counts().reset_index()
    
    def gender_distribution(self):
        """Get victim gender distribution"""
        if self.df is None or len(self.df) == 0:
            return None
        
        return self.df['gender'].value_counts().reset_index()
    
    def weapon_usage(self):
        """Get weapon usage statistics"""
        if self.df is None or len(self.df) == 0:
            return None
        
        return self.df['weapon'].value_counts().reset_index()
    
    def monthly_trend(self):
        """Get monthly crime trend"""
        if self.df is None or len(self.df) == 0:
            return None
        
        monthly = self.df.groupby(self.df['date'].dt.to_period('M')).size()
        monthly.index = monthly.index.to_timestamp()
        return monthly
    
    def safety_level(self, city=None):
        """
        Calculate safety level for a city
        Safe: < 5 crimes
        Moderate: 5-15 crimes
        High Risk: > 15 crimes
        """
        if self.df is None or len(self.df) == 0:
            return None
        
        if city:
            count = len(self.df[self.df['city'] == city])
        else:
            count = len(self.df)
        
        if count < 5:
            return "🟢 Safe"
        elif count < 15:
            return "🟡 Moderate"
        else:
            return "🔴 High Risk"
    
    def crime_by_city_and_type(self, city):
        """Get crime distribution by type for specific city"""
        if self.df is None or len(self.df) == 0:
            return None
        
        return self.df[self.df['city'] == city]['type'].value_counts().reset_index()
    
    # ==================== CHART GENERATION ====================
    
    def bar_chart_city_crimes(self, filtered_data=None):
        """Generate bar chart for crime count by city"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        data = df['city'].value_counts().reset_index()
        
        fig = px.bar(
            data,
            x='city',
            y='count',
            title='Crime Count by City',
            labels={'city': 'City', 'count': 'Number of Crimes'},
            color='count',
            color_continuous_scale='Reds',
            hover_data={'count': True, 'city': True}
        )
        fig.update_layout(height=500)
        return fig
    
    def bar_chart_crime_type(self, filtered_data=None):
        """Generate bar chart for crime by type"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        data = df['type'].value_counts().reset_index()
        
        fig = px.bar(
            data,
            x='type',
            y='count',
            title='Crime Count by Type',
            labels={'type': 'Crime Type', 'count': 'Number of Crimes'},
            color='count',
            color_continuous_scale='Blues',
            hover_data={'count': True, 'type': True}
        )
        fig.update_xaxes(tickangle=-45)
        fig.update_layout(height=500)
        return fig
    
    def line_chart_monthly_trend(self, filtered_data=None):
        """Generate line chart for monthly trend"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        monthly = df.groupby(df['date'].dt.to_period('M')).size()
        monthly.index = monthly.index.to_timestamp()
        
        df_trend = pd.DataFrame({'date': monthly.index, 'count': monthly.values})
        
        fig = px.line(
            df_trend,
            x='date',
            y='count',
            title='Monthly Crime Trend',
            labels={'date': 'Month', 'count': 'Number of Crimes'},
            markers=True,
            line_shape='spline'
        )
        fig.update_layout(height=500, hovermode='x unified')
        return fig
    
    def pie_chart_gender_distribution(self, filtered_data=None):
        """Generate pie chart for gender distribution"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        data = df['gender'].value_counts().reset_index()
        
        fig = px.pie(
            data,
            names='gender',
            values='count',
            title='Victim Gender Distribution',
            hover_data={'count': True}
        )
        fig.update_layout(height=500)
        return fig
    
    def pie_chart_weapon_usage(self, filtered_data=None):
        """Generate pie chart for weapon usage"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        data = df['weapon'].value_counts().reset_index()
        
        fig = px.pie(
            data,
            names='weapon',
            values='count',
            title='Weapon Usage Distribution',
            hover_data={'count': True}
        )
        fig.update_layout(height=500)
        return fig
    
    def bar_chart_gender_by_city(self, filtered_data=None):
        """Generate bar chart for gender distribution by city"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        data = df.groupby(['city', 'gender']).size().reset_index(name='count')
        
        fig = px.bar(
            data,
            x='city',
            y='count',
            color='gender',
            title='Gender Distribution by City',
            labels={'city': 'City', 'count': 'Number of Crimes'},
            barmode='group'
        )
        fig.update_layout(height=500)
        return fig
    
    # ==================== NEW INTERACTIVE CHART PATTERNS ====================
    
    def heatmap_city_type(self, filtered_data=None):
        """Generate heatmap for Crime Type distribution across Cities"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        # Create pivot table
        data = df.groupby(['city', 'type']).size().unstack(fill_value=0)
        
        fig = go.Figure(data=go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index,
            colorscale='YlOrRd',
            hoverongaps=False,
            colorbar=dict(title='Crime Count')
        ))
        
        fig.update_layout(
            title='Crime Type Intensity Map (City vs Type)',
            xaxis_title='Crime Type',
            yaxis_title='City',
            height=500
        )
        return fig
    
    def sunburst_crime_hierarchy(self, filtered_data=None):
        """Generate sunburst chart showing Crime Type hierarchy"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        data = df.groupby(['type', 'city']).size().reset_index(name='count')
        
        if len(data) == 0:
            return None
        
        # Create sunburst with proper hierarchy
        fig = px.sunburst(
            data,
            ids=data['type'] + ' - ' + data['city'],
            labels=data['type'] + ' - ' + data['city'],
            parents=[t for t in data['type']],
            values=data['count'],
            title='Crime Distribution Hierarchy',
            color='count',
            color_continuous_scale='RdYlBu_r'
        )
        fig.update_layout(height=500)
        return fig
    
    def scatter_crime_pattern(self, filtered_data=None):
        """Generate scatter plot showing crime patterns"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        # Count crimes by city and type
        data = df.groupby(['city', 'type', 'gender']).size().reset_index(name='count')
        
        fig = px.scatter(
            data,
            x='city',
            y='type',
            size='count',
            color='gender',
            hover_data={'count': True},
            title='Crime Pattern Scatter Plot (City × Type × Gender)',
            labels={'city': 'City', 'type': 'Crime Type', 'count': 'Frequency'}
        )
        fig.update_layout(height=500)
        return fig
    
    def box_plot_crime_by_type(self, filtered_data=None):
        """Generate box plot for crime distribution by type"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        # Create a numeric value for visualization
        data = df.groupby('type').size().reset_index(name='count')
        
        fig = px.box(
            data,
            y='count',
            x='type',
            title='Crime Type Distribution Pattern',
            labels={'type': 'Crime Type', 'count': 'Number of Crimes'},
            points='all'
        )
        fig.update_layout(height=500)
        return fig
    
    def bar_crime_by_weapon_city(self, filtered_data=None):
        """Generate bar chart for weapons by city"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        data = df.groupby(['city', 'weapon']).size().reset_index(name='count').head(20)
        
        fig = px.bar(
            data,
            x='city',
            y='count',
            color='weapon',
            title='Weapon Usage by City (Top 20)',
            labels={'city': 'City', 'count': 'Frequency'},
            barmode='stack'
        )
        fig.update_layout(height=500)
        return fig
    
    def histogram_crime_distribution(self, filtered_data=None):
        """Generate histogram for crime frequency distribution"""
        df = filtered_data if filtered_data is not None else self.df
        
        if df is None or len(df) == 0:
            return None
        
        data = df['type'].value_counts().reset_index()
        
        fig = px.histogram(
            data,
            x='type',
            y='count',
            nbins=20,
            title='Crime Type Distribution Histogram',
            labels={'type': 'Crime Type', 'count': 'Frequency'},
            color='count',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=500)
        return fig
