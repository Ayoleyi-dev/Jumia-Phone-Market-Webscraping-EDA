"""Build a snapshot HTML dashboard from the processed dataset."""
from __future__ import annotations
import json
from pathlib import Path
from analysis import brand_summary, channel_summary, load_processed, market_kpis, segment_summary

def pct(v): return f"{v*100:.1f}%"
def money(v): return f"₦{v:,.0f}"

def build_html() -> str:
    df=load_processed()
    k=market_kpis(df)
    brands=brand_summary(df)
    seg=segment_summary(df)
    channels=channel_summary(df)
    top=brands.head(10)
    major=brands[brands["listings"]>=20].head(12)
    data={
        "brands":top["brand"].tolist(),
        "shares":(top["listing_share"]*100).round(1).tolist(),
        "priceBrands":major["brand"].tolist(),
        "prices":major["median_price_ngn"].round(0).tolist(),
        "segments":seg["price_segment"].tolist(),
        "segmentCounts":seg["listings"].tolist(),
        "channels":channels["channel"].tolist(),
        "channelShares":(channels["listing_share"]*100).round(1).tolist(),
        "ratingCoverage":(channels["rating_coverage"]*100).round(1).tolist(),
    }
    return f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Jumia Smartphone Market Intelligence</title>
<script src='https://cdn.plot.ly/plotly-2.35.2.min.js'></script>
<style>body{{font-family:Segoe UI,Arial;background:#0b1020;color:#eef2ff;margin:0}}.wrap{{max-width:1200px;margin:auto;padding:28px}}.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}.card,.chart{{background:#11182b;border:1px solid #24304d;border-radius:14px;padding:16px}}.value{{font-size:28px;font-weight:700}}.label{{color:#9aa6c4}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:16px;margin-top:16px}}.chart{{min-height:380px}}</style></head><body><div class='wrap'>
<h1>Jumia Nigeria Smartphone Market Intelligence</h1><p class='label'>Point-in-time listing analysis — smartphone candidates only</p>
<div class='kpis'><div class='card'><div class='label'>Smartphone listings</div><div class='value'>{k["smartphone_rows"]:,}</div></div>
<div class='card'><div class='label'>Brands</div><div class='value'>{k["brands"]}</div></div>
<div class='card'><div class='label'>Median price</div><div class='value'>{money(k["median_price_ngn"])}</div></div>
<div class='card'><div class='label'>Top-5 concentration</div><div class='value'>{pct(k["top_5_brand_share"])}</div></div>
<div class='card'><div class='label'>Official-store listings</div><div class='value'>{pct(k["official_listing_share"])}</div></div>
<div class='card'><div class='label'>Listings with ratings</div><div class='value'>{pct(k["rating_coverage"])}</div></div></div>
<div class='grid'><div id='brand' class='chart'></div><div id='segments' class='chart'></div><div id='price' class='chart'></div><div id='channels' class='chart'></div><div id='coverage' class='chart'></div></div>
<p class='label'>Interpretation: descriptive listing-level patterns only; not sales, inventory, conversion, or national market share.</p></div>
<script>const D={json.dumps(data)};const L=t=>({{title:t,paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{{color:'#eef2ff'}},xaxis:{{gridcolor:'#24304d'}},yaxis:{{gridcolor:'#24304d'}},showlegend:false}});
Plotly.newPlot('brand',[{{type:'bar',x:D.shares,y:D.brands,orientation:'h'}}],{{...L('Top brands by listing share'),yaxis:{{autorange:'reversed'}}}});
Plotly.newPlot('segments',[{{type:'pie',labels:D.segments,values:D.segmentCounts,hole:.5}}],L('Price-segment mix'));
Plotly.newPlot('price',[{{type:'bar',x:D.priceBrands,y:D.prices}}],{{...L('Median advertised price by major brand'),xaxis:{{tickangle:-35}}}});
Plotly.newPlot('channels',[{{type:'bar',x:D.channels,y:D.channelShares}}],L('Official vs third-party listing share'));
Plotly.newPlot('coverage',[{{type:'bar',x:D.channels,y:D.ratingCoverage}}],L('Rating-data coverage by channel'));</script></body></html>"""

def main():
    out=Path("dashboard/jumia_market_dashboard.html")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(build_html(),encoding="utf-8")
    print(f"Wrote {out}")

if __name__=="__main__":
    main()
