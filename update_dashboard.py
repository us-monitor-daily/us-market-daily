import subprocess
import json
from datetime import datetime

def generate_summary():
    # ECO102-style macroeconomic summary based on today's large cap tech sell-off data
    summary_html = """
    <div class="summary-section">
        <h2>오늘의 시장 핵심 테마 (Macro Insights)</h2>
        <ul class="summary-list">
            <li><strong>빅테크 중심의 기술주 약세:</strong> 시가총액 상위 종목 중 주요 빅테크(NVDA, AAPL 등)가 일제히 하락하며, 시장의 폭(Breadth)이 축소되고 대형 성장주 전반에 대한 차익실현이 나타났습니다.</li>
            <li><strong>할인율(Discount Rate) 민감도에 따른 섹터 로테이션:</strong> 미래 가치 할인 영향을 크게 받는 기술주가 하락한 반면, 필수소비재(WMT)는 반등하는 등 금리 우려 속 방어주로의 자금 이동(Sector Rotation)이 관찰됩니다.</li>
            <li><strong>시가총액 가중(Market Cap Weighting)의 역효과:</strong> 소수 대형주의 쏠림 현상이 강했던 랠리 이후, Top 종목들의 동반 하락이 전체 지수의 뚜렷한 조정을 견인하는 전형적인 'Top-heavy' 장세의 취약성을 보여줍니다.</li>
        </ul>
    </div>
    """
    return summary_html

def create_dashboard():
    # 1. Run extract_tradingview_movers.py
    print("Extracting data...")
    result = subprocess.run(['python3', 'extract_tradingview_movers.py'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error extracting data")
        print(result.stderr)
        return
        
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Error parsing JSON output from extract_tradingview_movers.py")
        print("Raw output:", result.stdout)
        return
    
    # 2. Generate HTML
    print("Generating HTML...")
    
    cards_html = ""
    for item in data:
        # Use US Standard colors (Green = Up, Red = Down)
        change = item['change_percent']
        if change > 0:
            color_class = "pos"
            sign = "+"
        elif change < 0:
            color_class = "neg"
            sign = ""
        else:
            color_class = "neu"
            sign = ""
            
        formatted_price = f"${item['price_usd']:,.2f}"
            
        cards_html += f"""
        <div class="card">
            <div class="card-left">
                <div class="ticker">{item['ticker']}</div>
                <div class="name">{item['name']}</div>
            </div>
            <div class="card-right {color_class}">
                <div class="price">{formatted_price}</div>
                <div class="change">{sign}{change}%</div>
            </div>
        </div>
        """
        
    html_template = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Market Movers</title>
    <!-- Premium Fonts: Playfair Display for headings and Inter for UI text -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f1115;
            --card-bg: rgba(255, 255, 255, 0.02);
            --card-border: rgba(255, 255, 255, 0.06);
            --text-main: #f0f2f5;
            --text-muted: #8b949e;
            --accent-pos: #3fb950; /* US standard green */
            --accent-neg: #f85149; /* US standard red */
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            -webkit-font-smoothing: antialiased;
            padding: 30px 20px;
        }}
        
        .container {{
            max-width: 440px;
            margin: 0 auto;
        }}
        
        header {{
            margin-bottom: 30px;
        }}
        
        h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 2.4rem;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
            background: linear-gradient(90deg, #ffffff, #a3b1c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .date {{
            font-size: 0.9rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }}
        
        .summary-section {{
            background: linear-gradient(145deg, rgba(30, 35, 45, 0.8), rgba(20, 25, 30, 0.4));
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 32px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(12px);
        }}
        
        .summary-section h2 {{
            font-size: 1.15rem;
            margin-bottom: 16px;
            color: #fff;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 12px;
        }}
        
        .summary-list {{
            list-style: none;
        }}
        
        .summary-list li {{
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 14px;
            color: #d1d5da;
            padding-left: 20px;
            position: relative;
        }}
        
        .summary-list li:last-child {{
            margin-bottom: 0;
        }}
        
        .summary-list li::before {{
            content: '•';
            position: absolute;
            left: 0;
            color: #58a6ff;
            font-size: 1.2rem;
            line-height: 1.2;
        }}
        
        .summary-list li strong {{
            color: #fff;
            font-weight: 600;
        }}
        
        .cards-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        
        .card {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 16px 20px;
            transition: transform 0.2s, background 0.2s;
        }}
        
        .card:hover {{
            background: rgba(255, 255, 255, 0.05);
            transform: translateY(-2px);
        }}
        
        .card-left .ticker {{
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}
        
        .card-left .name {{
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 4px;
            max-width: 180px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .card-right {{
            text-align: right;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }}
        
        .card-right .price {{
            font-size: 1.05rem;
            font-weight: 600;
        }}
        
        .card-right .change {{
            font-size: 0.9rem;
            font-weight: 800;
            margin-top: 6px;
            padding: 4px 10px;
            border-radius: 6px;
            display: inline-block;
        }}
        
        .pos .price {{ color: #fff; }}
        .pos .change {{ background-color: rgba(63, 185, 80, 0.15); color: var(--accent-pos); }}
        
        .neg .price {{ color: #fff; }}
        .neg .change {{ background-color: rgba(248, 81, 73, 0.15); color: var(--accent-neg); }}
        
        .neu .change {{ background-color: rgba(139, 148, 158, 0.15); color: var(--text-muted); }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Market Movers</h1>
            <div class="date">{datetime.now().strftime('%B %d, %Y')}</div>
        </header>
        
        {generate_summary()}
        
        <div class="cards-list">
            {cards_html}
        </div>
    </div>
</body>
</html>
    """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print("Dashboard created successfully at index.html")
    
    # Automate pushing to GitHub
    update_git()

def update_git():
    print("Pushing updates to GitHub...")
    import subprocess
    
    # Stage the updated index.html
    subprocess.run(['git', 'add', 'index.html'], check=False)
    
    # Create the commit
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_msg = f"Update dashboard: {date_str}"
    
    commit_res = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
    if "nothing to commit" in commit_res.stdout:
        print("No changes to commit.")
        return
        
    print(commit_res.stdout)
    
    # Push to origin main
    push_res = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
    if push_res.returncode == 0:
        print("✓ Successfully pushed to GitHub Pages!")
    else:
        print("⚠️ Failed to push. Ensure git is authenticated and remote origin is set.")
        print(push_res.stderr)

if __name__ == '__main__':
    create_dashboard()
