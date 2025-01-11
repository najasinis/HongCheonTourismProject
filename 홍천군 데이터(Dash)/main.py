import sqlite3
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Constants
COLORS = {
    'background': '#1a1a1a',
    'text': 'white',
    'primary': '#7FDBFF',
    'secondary': '#FFD700',
    'accent': '#FF4136',
    'grid': '#333333'
}

# Updated celebrity visit data excluding 2024-Q2
CELEBRITY_VISITS = [
    {'date': '2024-Q4', 'celebrity': '한혜진', 'description': '홍천 별장', 'count': 1},
    {'date': '2024-Q4', 'celebrity': '유재석', 'description': '수타사 방문', 'count': 1},
    {'date': '2024-Q4', 'celebrity': '위문공연', 'description': '홍천 군인의 날', 'count': 2},
    {'date': '2024-Q1', 'celebrity': '차은우/정국', 'description': '홍천 방문', 'count': 2},
    {'date': '2023-Q2', 'celebrity': '백종원', 'description': '홍천 맛집 방문', 'count': 1},
    {'date': '2022-Q4', 'celebrity': '무한도전', 'description': '홍천 방문 편', 'count': 1},
    {'date': '2022-Q4', 'celebrity': '1박2일', 'description': '홍천 방문', 'count': 1},
    {'date': '2019-Q3', 'celebrity': '차은우/정국', 'description': '명가춘천닭갈비막국수', 'count': 1},
    {'date': '2010-Q3', 'celebrity': '전국노래자랑', 'description': '홍천 방송', 'count': 1},
]

# Simulated MZ tourist data per quarter (단위: 천명)
MZ_TOURISTS = {
    '2024-Q1': 180,  # Adjusted to be below 100 less than X value
    '2024-Q4': 250,
    '2023-Q2': 200,
    '2022-Q4': 160,
    '2019-Q3': 120,
    '2010-Q3': 80,
}

class Dashboard:
    def __init__(self):
        self.app = Dash(__name__)
        self.init_db()
        self.setup_layout()
        self.setup_callbacks()

    def init_db(self):
        """Initialize database with tables and real data"""
        conn = sqlite3.connect('hongcheon_visits.db')
        cursor = conn.cursor()
        
        # Create tables with correct schema
        cursor.execute('''DROP TABLE IF EXISTS celebrity_visits''')  # 기존 테이블 삭제
        cursor.execute('''
            CREATE TABLE celebrity_visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quarter TEXT,
                celebrity TEXT,
                description TEXT,
                visit_count INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert celebrity visit data
        for visit in CELEBRITY_VISITS:
            cursor.execute("""
                INSERT INTO celebrity_visits 
                (quarter, celebrity, description, visit_count) 
                VALUES (?, ?, ?, ?)
            """, (visit['date'], visit['celebrity'], visit['description'], visit['count']))
        
        conn.commit()
        conn.close()

    def setup_layout(self):
        """Setup dashboard layout"""
        self.app.layout = html.Div([
            # Header
            self.create_header(),
            
            # Main content
            html.Div([
                # Left panel
                self.create_left_panel(),
                
                # Right panel
                self.create_right_panel()
            ], style={'padding': '20px'})
        ], style={'backgroundColor': COLORS['background']})

    def create_header(self):
        return html.Div([
            html.H1("홍천군 관광 데이터 대시보드", style={'color': COLORS['text']}),
            html.P("연예인 방문 및 MZ세대 관광객 동향 분석", style={'color': COLORS['text']}),
        ], style={'backgroundColor': COLORS['background'], 
                 'padding': '20px',
                 'borderBottom': f'1px solid {COLORS["grid"]}'})

    def create_left_panel(self):
        return html.Div([
            html.H3("주요 방문 내역", style={'color': COLORS['text']}),
            html.Div(id='visit-list',
                    children=[html.Ul([
                        html.Li(f"{visit['celebrity']} - {visit['description']} ({visit['date']})", 
                               style={'color': COLORS['text']})
                        for visit in CELEBRITY_VISITS
                    ])],
                    style={'margin': '20px 0'})
        ], style={'width': '30%',
                  'display': 'inline-block',
                  'vertical-align': 'top'})

    def create_right_panel(self):
        return html.Div([
            html.H3("데이터 분석", style={'color': COLORS['text']}),
            
            html.Div([
                # Celebrity vs MZ Chart
                html.H4("분기별 연예인 방문과 MZ관광객 상관관계", 
                       style={'color': COLORS['text']}),
                dcc.Graph(id='correlation-chart'),
                
                # Update interval
                dcc.Interval(id='update-interval',
                           interval=5000,
                           n_intervals=0)
            ])
        ], style={'width': '70%',
                  'display': 'inline-block'})

    def setup_callbacks(self):
        @self.app.callback(
            Output('correlation-chart', 'figure'),
            Input('update-interval', 'n_intervals')
        )
        def update_correlation_chart(n):
            conn = sqlite3.connect('hongcheon_visits.db')
            df = pd.read_sql_query("""
                SELECT quarter, SUM(visit_count) AS total_visits 
                FROM celebrity_visits 
                GROUP BY quarter
            """, conn)
            conn.close()
            
            # Add MZ tourist data
            df['mz_tourists'] = df['quarter'].map(MZ_TOURISTS)
            
            fig = go.Figure()
            
            # Add scatter plot
            fig.add_trace(go.Scatter(
                x=df['total_visits'],
                y=df['mz_tourists'],
                mode='markers+text',
                marker=dict(
                    size=12,
                    color=COLORS['secondary'],
                ),
                text=df['quarter'],
                textposition="top center",
                name='분기별 데이터'
            ))
            
            # Update layout
            fig.update_layout(
                title='연예인 방문횟수와 MZ관광객 수 상관관계',
                xaxis_title='연예인 방문횟수 (회)',
                yaxis_title='MZ관광객 수 (천명)',
                plot_bgcolor=COLORS['background'],
                paper_bgcolor=COLORS['background'],
                font={'color': COLORS['text']},
                showlegend=True,
                xaxis=dict(
                    gridcolor=COLORS['grid'],
                    range=[0, 5],  # 방문횟수 범위 조정
                ),
                yaxis=dict(
                    gridcolor=COLORS['grid'],
                    range=[0, 450]  # MZ관광객 수 범위 조정
                )
            )
            
            return fig

    def run_server(self, debug=True):
        self.app.run_server(debug=debug)

if __name__ == '__main__':
    dashboard = Dashboard()
    dashboard.run_server()