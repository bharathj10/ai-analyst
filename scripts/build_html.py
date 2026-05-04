"""
Interactive HTML report builder — the primary shareable output format.

Produces a self-contained HTML file with:
  - Executive summary (large-stat cards)
  - Interactive Plotly charts (hover, zoom, filter)
  - Data summary section (Appendix B equivalent — membership profile check)
  - Full data table at the bottom (DataTables — sortable, searchable, paginated)

The HTML file works in any browser and can be emailed or shared on SharePoint.
Charts are interactive: executives can hover, zoom, and explore the data themselves.

Usage:
    # From findings JSON + data file (standard workflow)
    python scripts/build_html.py outputs/2026-04-29_findings.json data/super_members_clean.parquet

    # Rebuild the salary sacrifice demo
    python scripts/build_html.py
"""

from __future__ import annotations
import json
import sys
import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd
import numpy as np

# ── Brand / design constants ──────────────────────────────────────────────────

NAVY   = "#1B3557"
TEAL   = "#0A8A8F"
AMBER  = "#E8A020"
CHARCOAL = "#2C3E50"
LGREY  = "#F7F8FA"
MGREY  = "#E5E8EC"
SLATE  = "#8A99AA"
WHITE  = "#FFFFFF"
POSITIVE = "#187A4E"
NEGATIVE = "#C0392B"

PALETTE = [TEAL, AMBER, NAVY, "#6A5ACD", POSITIVE, NEGATIVE, "#E67E22", "#2980B9"]

# ── HTML template ─────────────────────────────────────────────────────────────

HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  :root {{
    --navy: {navy};
    --teal: {teal};
    --amber: {amber};
    --charcoal: {charcoal};
    --lgrey: {lgrey};
    --slate: {slate};
  }}
  body {{ font-family: 'Segoe UI', Calibri, sans-serif; color: var(--charcoal); background: #f9fafb; }}
  .report-header {{ background: var(--navy); color: white; padding: 2.5rem 2rem 1.8rem; border-bottom: 4px solid var(--teal); }}
  .report-header h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 0.3rem; }}
  .report-header .meta {{ color: #8aaac8; font-size: 0.9rem; margin-top: 0.5rem; }}
  .classification {{ background: var(--teal); color: white; font-size: 0.8rem; padding: 0.25rem 0.75rem; display: inline-block; border-radius: 3px; margin-bottom: 0.75rem; letter-spacing: 0.05em; }}
  .section {{ background: white; border-radius: 8px; padding: 1.75rem 2rem; margin-bottom: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.07); }}
  .section-title {{ font-size: 1.15rem; font-weight: 700; color: var(--navy); border-bottom: 2px solid var(--teal); padding-bottom: 0.5rem; margin-bottom: 1.25rem; }}
  .kpi-card {{ background: var(--lgrey); border-radius: 8px; padding: 1.25rem 1rem; text-align: center; border-top: 3px solid var(--teal); }}
  .kpi-value {{ font-size: 2.4rem; font-weight: 700; color: var(--navy); line-height: 1; }}
  .kpi-label {{ font-size: 0.82rem; color: var(--slate); margin-top: 0.3rem; }}
  .kpi-note  {{ font-size: 0.75rem; color: var(--slate); margin-top: 0.15rem; font-style: italic; }}
  .kpi-positive {{ border-top-color: {positive}; }}
  .kpi-positive .kpi-value {{ color: {positive}; }}
  .kpi-negative {{ border-top-color: {negative}; }}
  .kpi-negative .kpi-value {{ color: {negative}; }}
  .kpi-amber {{ border-top-color: var(--amber); }}
  .kpi-amber .kpi-value {{ color: var(--amber); }}
  .finding-lead {{ font-size: 1.05rem; color: var(--charcoal); line-height: 1.6; margin-bottom: 1rem; }}
  .insight-box {{ border-left: 4px solid var(--teal); background: #e5f5f6; padding: 0.85rem 1rem; border-radius: 0 6px 6px 0; margin: 1rem 0; font-size: 0.95rem; }}
  .insight-box.amber {{ border-left-color: var(--amber); background: #fdf3e0; }}
  .insight-box strong {{ color: var(--navy); }}
  .data-summary-table {{ font-size: 0.88rem; }}
  .caveat-item {{ padding: 0.5rem 0; border-bottom: 1px solid var(--lgrey); font-size: 0.92rem; }}
  .caveat-item:last-child {{ border-bottom: none; }}
  .source-note {{ font-size: 0.78rem; color: var(--slate); font-style: italic; margin-top: 0.5rem; }}
  .appendix-b {{ background: #f0f4f8; border: 1px solid var(--mgrey); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }}
  .appendix-b h5 {{ color: var(--navy); font-weight: 600; }}
  .stat-pill {{ display: inline-block; background: white; border: 1px solid var(--mgrey); border-radius: 20px; padding: 0.2rem 0.75rem; font-size: 0.82rem; margin: 0.15rem; color: var(--charcoal); }}
  footer {{ background: var(--navy); color: #8aaac8; text-align: center; padding: 1rem; font-size: 0.8rem; margin-top: 2rem; }}
  .nav-sticky {{ position: sticky; top: 0; z-index: 100; background: white; border-bottom: 1px solid var(--mgrey); padding: 0.5rem 1rem; }}
  .nav-link {{ color: var(--navy) !important; font-size: 0.85rem; }}
  .nav-link:hover {{ color: var(--teal) !important; }}
  @media print {{ .nav-sticky {{ display: none; }} }}
</style>
</head>
<body>
"""

HTML_TAIL = """
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>
<script>
$(document).ready(function() {{
  if ($('#full-data-table').length) {{
    $('#full-data-table').DataTable({{
      pageLength: 25,
      scrollX: true,
      order: [],
      dom: '<"row mb-2"<"col-sm-6"l><"col-sm-6"f>>rtip',
      language: {{ search: "Filter records:" }}
    }});
  }}
}});
</script>
<footer>
  {classification} &nbsp;|&nbsp; {source_note} &nbsp;|&nbsp; Generated {today}
</footer>
</body></html>
"""

# ── Plotly chart generators ───────────────────────────────────────────────────

def _plotly_bar(
    categories: list, values: list, *,
    title: str = "", yaxis_title: str = "", xaxis_title: str = "",
    colour: str = TEAL, reference_line: float = None, reference_label: str = "",
    text_format: str = ".1f", orientation: str = "v",
    height: int = 420,
) -> str:
    """Return an HTML div containing a Plotly bar chart."""
    import plotly.graph_objects as go

    if orientation == "h":
        fig = go.Figure(go.Bar(
            x=values, y=categories, orientation="h",
            marker_color=colour, text=[f"{v:{text_format}}" for v in values],
            textposition="outside",
        ))
        fig.update_layout(
            xaxis_title=xaxis_title or yaxis_title,
            yaxis=dict(autorange="reversed"),
        )
    else:
        fig = go.Figure(go.Bar(
            x=categories, y=values, marker_color=colour,
            text=[f"{v:{text_format}}" for v in values],
            textposition="outside",
        ))
        if reference_line is not None:
            fig.add_hline(y=reference_line, line_dash="dash", line_color=SLATE,
                          annotation_text=reference_label,
                          annotation_position="top right")
        fig.update_layout(yaxis_title=yaxis_title)

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=NAVY), x=0),
        plot_bgcolor=WHITE, paper_bgcolor=WHITE,
        font=dict(family="Segoe UI, Calibri, sans-serif", color=CHARCOAL),
        height=height,
        margin=dict(l=40, r=40, t=50, b=40),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor=MGREY)

    return fig.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True})


def _plotly_grouped_bar(
    categories: list, series: dict[str, list], *,
    title: str = "", yaxis_title: str = "",
    colours: list = None, height: int = 420,
) -> str:
    import plotly.graph_objects as go

    colours = colours or PALETTE
    fig = go.Figure()
    for i, (name, values) in enumerate(series.items()):
        fig.add_trace(go.Bar(
            name=name, x=categories, y=values,
            marker_color=colours[i % len(colours)],
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=NAVY), x=0),
        barmode="group", plot_bgcolor=WHITE, paper_bgcolor=WHITE,
        font=dict(family="Segoe UI, Calibri, sans-serif", color=CHARCOAL),
        yaxis_title=yaxis_title, height=height,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor=MGREY)
    return fig.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True})


def _plotly_histogram(
    values: pd.Series, *,
    title: str = "", xaxis_title: str = "", log_x: bool = False,
    colour: str = TEAL, height: int = 380,
) -> str:
    import plotly.graph_objects as go

    fig = go.Figure(go.Histogram(
        x=np.log10(values.clip(lower=1)) if log_x else values,
        marker_color=colour, opacity=0.85,
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=NAVY), x=0),
        xaxis_title=xaxis_title + (" (log₁₀ scale)" if log_x else ""),
        yaxis_title="Number of members",
        plot_bgcolor=WHITE, paper_bgcolor=WHITE,
        font=dict(family="Segoe UI, Calibri, sans-serif"),
        height=height,
        margin=dict(l=40, r=20, t=50, b=40),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor=MGREY)
    return fig.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True})


def _plotly_scatter(
    x: pd.Series, y: pd.Series, colour_col: pd.Series = None, *,
    title: str = "", xaxis_title: str = "", yaxis_title: str = "",
    height: int = 420,
) -> str:
    import plotly.express as px
    import plotly.graph_objects as go

    df_plot = pd.DataFrame({"x": x, "y": y})
    if colour_col is not None:
        df_plot["group"] = colour_col.astype(str)
        fig = px.scatter(df_plot, x="x", y="y", color="group",
                         color_discrete_sequence=PALETTE)
    else:
        fig = go.Figure(go.Scatter(x=x, y=y, mode="markers", marker=dict(color=TEAL, opacity=0.5)))

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=NAVY), x=0),
        xaxis_title=xaxis_title, yaxis_title=yaxis_title,
        plot_bgcolor=WHITE, paper_bgcolor=WHITE,
        font=dict(family="Segoe UI, Calibri, sans-serif"),
        height=height, margin=dict(l=40, r=40, t=50, b=40),
    )
    return fig.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True})


# ── Data summary section (Appendix B equivalent) ─────────────────────────────

def build_data_summary_html(df: pd.DataFrame, dataset_name: str) -> str:
    """
    Generate the membership data summary section.
    This is the Appendix B equivalent — a quality check that shows what the
    analysis is based on before executives read the findings.
    """
    import plotly.graph_objects as go

    n_rows, n_cols = df.shape
    n_dupes = df.duplicated().sum()
    null_pcts = {c: df[c].isna().mean() * 100 for c in df.columns if df[c].isna().any()}

    # Pills for key stats
    pills_html = "".join([
        f'<span class="stat-pill"><strong>{n_rows:,}</strong> total records</span>',
        f'<span class="stat-pill"><strong>{n_cols}</strong> columns</span>',
        f'<span class="stat-pill"><strong>{n_dupes:,}</strong> duplicate rows</span>',
        f'<span class="stat-pill"><strong>{df.memory_usage(deep=True).sum() / 1e6:.1f} MB</strong> in memory</span>',
    ])

    # Schema table
    schema_rows = ""
    for col in df.columns:
        nn = df[col].notna().sum()
        null_pct = (1 - nn / n_rows) * 100
        dtype = str(df[col].dtype)
        flag = " ⚠" if null_pct > 20 else (" !" if null_pct > 5 else "")
        schema_rows += f"<tr><td><code>{col}</code></td><td>{dtype}</td><td>{nn:,}</td><td>{null_pct:.1f}%{flag}</td></tr>"

    # Numeric summary table
    num_cols = df.select_dtypes(include=np.number).columns
    num_summary_html = ""
    if len(num_cols):
        desc = df[num_cols].describe(percentiles=[0.25, 0.5, 0.75, 0.9]).round(2)
        num_summary_html = f"""
        <h6 class="mt-3 mb-2" style="color:{NAVY}">Numeric columns — distribution summary</h6>
        <div class="table-responsive">
        {desc.to_html(classes="table table-sm data-summary-table", border=0)}
        </div>"""

    # Categorical summary
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    cat_summary_html = ""
    if len(cat_cols):
        cat_parts = []
        for col in cat_cols[:8]:  # cap at 8 categorical columns
            top = df[col].value_counts().head(5)
            rows = "".join(f"<tr><td>{v}</td><td>{c:,}</td><td>{c/n_rows*100:.1f}%</td></tr>"
                           for v, c in top.items())
            cat_parts.append(f"""
            <div class="col-md-6 mb-3">
              <div style="background:white;border:1px solid {MGREY};border-radius:6px;padding:0.75rem;">
                <strong style="color:{NAVY}">{col}</strong>
                <span class="text-muted" style="font-size:0.78rem"> — {df[col].nunique()} unique values</span>
                <table class="table table-sm mb-0 mt-1" style="font-size:0.82rem">
                  <thead><tr><th>Value</th><th>Count</th><th>%</th></tr></thead>
                  <tbody>{rows}</tbody>
                </table>
              </div>
            </div>""")
        cat_summary_html = f"""
        <h6 class="mt-3 mb-2" style="color:{NAVY}">Categorical columns — top values</h6>
        <div class="row">{''.join(cat_parts)}</div>"""

    # Quality flags
    flags = []
    if n_dupes > 0:
        flags.append(f"<li class='text-warning'>⚠ {n_dupes:,} duplicate rows detected</li>")
    for col, pct in null_pcts.items():
        if pct > 20:
            flags.append(f"<li class='text-danger'>⚠ <code>{col}</code>: {pct:.1f}% null — may affect results</li>")
        elif pct > 5:
            flags.append(f"<li class='text-warning'>! <code>{col}</code>: {pct:.1f}% null</li>")
    flags_html = f"<ul class='mb-0'>{''.join(flags)}</ul>" if flags else "<p class='text-success mb-0'>✓ No major data quality flags</p>"

    return f"""
<div class="appendix-b" id="data-summary">
  <h5>Data Summary — Quality Check</h5>
  <p class="text-muted" style="font-size:0.88rem">
    This section confirms what data the analysis is based on. Check that the totals and
    distributions look reasonable before relying on the findings above.
    <strong>Source: {dataset_name}</strong>
  </p>
  <div class="mb-2">{pills_html}</div>

  <div class="row mt-3">
    <div class="col-md-7">
      <h6 style="color:{NAVY}">Column schema</h6>
      <div class="table-responsive">
        <table class="table table-sm data-summary-table">
          <thead><tr><th>Column</th><th>Type</th><th>Non-null</th><th>Null %</th></tr></thead>
          <tbody>{schema_rows}</tbody>
        </table>
      </div>
    </div>
    <div class="col-md-5">
      <h6 style="color:{NAVY}">Data quality flags</h6>
      {flags_html}
    </div>
  </div>
  {num_summary_html}
  {cat_summary_html}
</div>"""


def build_full_data_table_html(df: pd.DataFrame, max_rows: int = 5000) -> str:
    """
    Generate the full data table at the bottom of the report.
    Truncates to max_rows and excludes columns that look like IDs/PII.
    """
    # Exclude PII-looking columns
    pii_patterns = ["member_id", "email", "phone", "name", "address", "tfn", "tax_file"]
    safe_cols = [c for c in df.columns
                 if not any(p in c.lower() for p in pii_patterns)]

    display_df = df[safe_cols].head(max_rows).copy()

    # Round numerics to 2dp for readability
    for col in display_df.select_dtypes(include=np.number).columns:
        display_df[col] = display_df[col].round(2)

    truncation_note = f"<p class='text-muted' style='font-size:0.8rem'>Showing first {max_rows:,} of {len(df):,} records. PII columns hidden.</p>" if len(df) > max_rows else f"<p class='text-muted' style='font-size:0.8rem'>All {len(df):,} records. PII columns hidden.</p>"

    table_html = display_df.to_html(
        table_id="full-data-table",
        classes="table table-sm table-striped table-hover",
        border=0,
        index=False,
        na_rep="—",
    )

    return f"""
<div class="section" id="full-data">
  <div class="section-title">Full Dataset — Explore & Verify</div>
  <p class="finding-lead">
    Use this table to spot-check that the findings make sense, verify totals,
    or drill down into specific rows. Use the search box to filter.
  </p>
  {truncation_note}
  <div class="table-responsive">
    {table_html}
  </div>
</div>"""


# ── Main report builder ───────────────────────────────────────────────────────

@dataclass
class HTMLReportConfig:
    title: str
    subtitle: str = ""
    organisation: str = ""
    prepared_by: str = "Analytics & Insights"
    prepared_date: str = ""
    classification: str = "CONFIDENTIAL — INTERNAL USE ONLY"
    source_note: str = ""

    kpis: list[dict] = field(default_factory=list)
    exec_summary: list[str] = field(default_factory=list)
    findings: list[dict] = field(default_factory=list)
    caveats: list[str] = field(default_factory=list)

    # Dataset for data quality summary (always shown if dataset_path is set)
    # include_full_table is OFF by default — embedding raw rows is a data risk
    # for member-level datasets and impractical for large extracts (millions of rows).
    # Only enable for small, non-sensitive reference datasets.
    dataset_path: str = ""
    dataset_name: str = ""
    include_full_table: bool = False
    max_table_rows: int = 500


def build_html_report(cfg: HTMLReportConfig, out_path: Path) -> None:
    """Assemble the complete HTML report and write to out_path."""
    if not cfg.prepared_date:
        cfg.prepared_date = datetime.date.today().strftime("%d %B %Y")

    today_str = datetime.date.today().strftime("%d/%m/%Y")
    nav_links = ""
    body_parts = []

    # ── Header ─────────────────────────────────────────────────────────────────
    header_html = f"""
<div class="report-header">
  <span class="classification">{cfg.classification}</span>
  <h1>{cfg.title}</h1>
  <div class="meta">
    {cfg.subtitle + " &nbsp;|&nbsp; " if cfg.subtitle else ""}
    {cfg.organisation + " &nbsp;|&nbsp; " if cfg.organisation else ""}
    Prepared by {cfg.prepared_by} &nbsp;|&nbsp; {cfg.prepared_date}
  </div>
</div>"""

    # ── Navigation ─────────────────────────────────────────────────────────────
    nav_items = ["exec-summary", "findings", "data-summary", "full-data", "caveats"]
    nav_labels = ["Executive Summary", "Findings", "Data Summary", "Full Data", "Caveats"]
    nav_html = f"""
<div class="nav-sticky">
  <div class="container-fluid">
    <nav class="d-flex gap-3 flex-wrap">
      {''.join(f'<a class="nav-link" href="#{i}">{l}</a>' for i, l in zip(nav_items, nav_labels))}
    </nav>
  </div>
</div>"""

    # ── KPI strip ──────────────────────────────────────────────────────────────
    kpi_html = ""
    if cfg.kpis:
        cards = []
        for kpi in cfg.kpis:
            flag_class = f" kpi-{kpi.get('flag', '')}" if kpi.get("flag") else ""
            note = f'<div class="kpi-note">{kpi["note"]}</div>' if kpi.get("note") else ""
            cards.append(f"""
            <div class="col">
              <div class="kpi-card{flag_class}">
                <div class="kpi-value">{kpi["value"]}</div>
                <div class="kpi-label">{kpi["label"]}</div>
                {note}
              </div>
            </div>""")
        kpi_html = f'<div class="section"><div class="row g-3">{"".join(cards)}</div></div>'

    # ── Executive summary ──────────────────────────────────────────────────────
    exec_html = ""
    if cfg.exec_summary:
        items = "".join(f'<li class="caveat-item">{b}</li>' for b in cfg.exec_summary)
        exec_html = f"""
<div class="section" id="exec-summary">
  <div class="section-title">Executive Summary</div>
  <ul class="list-unstyled mb-0">{items}</ul>
</div>"""

    # ── Findings ───────────────────────────────────────────────────────────────
    findings_html = '<div id="findings">'
    for i, finding in enumerate(cfg.findings):
        chart_div = finding.get("chart_html", "")
        insight_html = ""
        if finding.get("insight"):
            insight_style = "amber" if finding.get("insight_style") == "amber" else ""
            insight_html = f'<div class="insight-box {insight_style}"><strong>Key insight: </strong>{finding["insight"]}</div>'

        findings_html += f"""
<div class="section">
  <div class="section-title">{i+1}. {finding["title"]}</div>
  <p class="finding-lead">{finding.get("narrative", "")}</p>
  {insight_html}
  {chart_div}
  {f'<p class="source-note">{finding["source_note"]}</p>' if finding.get("source_note") else ""}
</div>"""
    findings_html += "</div>"

    # ── Caveats ────────────────────────────────────────────────────────────────
    caveats_html = ""
    if cfg.caveats:
        items = "".join(f'<div class="caveat-item">– {c}</div>' for c in cfg.caveats)
        caveats_html = f"""
<div class="section" id="caveats">
  <div class="section-title">Caveats & Limitations</div>
  {items}
</div>"""

    # ── Data summary (Appendix B) ──────────────────────────────────────────────
    data_summary_html = ""
    full_data_html = ""
    if cfg.dataset_path:
        try:
            p = Path(cfg.dataset_path)
            if p.exists():
                df = pd.read_parquet(p) if p.suffix == ".parquet" else pd.read_csv(p)
                dataset_name = cfg.dataset_name or p.name
                data_summary_html = f'<div id="data-summary">{build_data_summary_html(df, dataset_name)}</div>'
                if cfg.include_full_table:
                    full_data_html = build_full_data_table_html(df, cfg.max_table_rows)
        except Exception as e:
            data_summary_html = f'<div class="section"><div class="section-title">Data Summary</div><p class="text-muted">Could not load dataset: {e}</p></div>'

    # ── Assemble ───────────────────────────────────────────────────────────────
    body = f"""
{header_html}
{nav_html}
<div class="container-fluid py-4 px-4">
  {kpi_html}
  {exec_html}
  {findings_html}
  {data_summary_html}
  {full_data_html}
  {caveats_html}
</div>"""

    html = HTML_HEAD.format(
        title=cfg.title, navy=NAVY, teal=TEAL, amber=AMBER,
        charcoal=CHARCOAL, lgrey=LGREY, slate=SLATE, mgrey=MGREY,
        positive=POSITIVE, negative=NEGATIVE,
    ) + body + HTML_TAIL.format(
        classification=cfg.classification,
        source_note=cfg.source_note,
        today=today_str,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"HTML report saved: {out_path}")


# ── Salary sacrifice demo ─────────────────────────────────────────────────────

def build_salary_sacrifice_html() -> None:
    """Build the interactive HTML version of the salary sacrifice analysis."""

    age_bands = ["18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
    participation_rates = [9.2, 27.1, 48.0, 60.5, 63.5, 58.9]
    median_amounts = [7396, 6301, 6024, 6086, 6263, 6298]
    mean_amounts = [7414, 6470, 6422, 6436, 6488, 6586]
    n_members = [338, 787, 1382, 1448, 748, 297]
    n_participants = [31, 213, 664, 876, 475, 175]
    sacrifice_pct_salary = [7.0, 6.6, 6.3, 6.1, 5.7, 5.1]

    # Build Plotly chart divs
    chart_participation = _plotly_bar(
        age_bands, participation_rates,
        title="Participation Rate Climbs Steadily With Age",
        yaxis_title="Participation rate (%)",
        xaxis_title="Age band",
        colour=TEAL,
        reference_line=48.7,
        reference_label="Fund average: 48.7%",
        text_format=".1f",
    )

    chart_amounts = _plotly_grouped_bar(
        age_bands,
        {"Median (AUD)": median_amounts, "Mean (AUD)": mean_amounts},
        title="Conditional Sacrifice Amounts — Flat Across Age Bands (Participants Only)",
        yaxis_title="Annual salary sacrifice (AUD)",
        colours=[TEAL, AMBER],
    )

    # Salary quartile data
    salary_q_labels = ["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"]
    participation_by_q = {
        "18–24": [0.7, 4.2, 11.8, 33.3],
        "35–44": [16.1, 42.2, 53.8, 55.7],
        "55–64": [37.5, 68.1, 72.4, 66.8],
    }
    chart_salary_q = _plotly_grouped_bar(
        salary_q_labels,
        {band: rates for band, rates in participation_by_q.items()},
        title="Salary Drives Participation for Young Members, Less So for Older Ones",
        yaxis_title="Participation rate (%)",
        colours=[TEAL, AMBER, NAVY],
    )

    chart_pct_salary = _plotly_bar(
        age_bands, sacrifice_pct_salary,
        title="Younger Participants Sacrifice a Higher Share of Their Salary",
        yaxis_title="Sacrifice as % of salary",
        xaxis_title="Age band",
        colour=AMBER,
        text_format=".1f",
    )

    cfg = HTMLReportConfig(
        title="The Age Gap Is a Participation Problem",
        subtitle="Salary Sacrifice Behaviour Across Age Bands — Q1 2026",
        organisation="Analytics & Insights",
        prepared_by="Bharath",
        prepared_date="29 April 2026",
        source_note="Source: super_members_2026Q1.csv | n=5,000 members | Snapshot: 31 March 2026",
        dataset_path="data/super_members_clean.parquet",
        dataset_name="super_members_2026Q1.csv",
        include_full_table=False,

        kpis=[
            {"value": "48.7%", "label": "Fund participation rate", "note": "2,434 of 5,000 members"},
            {"value": "9.2%", "label": "18–24 participation", "note": "vs 63.5% at 55–64", "flag": "negative"},
            {"value": "63.5%", "label": "55–64 participation", "note": "Peak cohort", "flag": "positive"},
            {"value": "$6,300", "label": "Median annual sacrifice", "note": "Participants only — flat across ages"},
            {"value": "718", "label": "35–44 non-participants", "note": "Biggest activation opportunity", "flag": "amber"},
        ],

        exec_summary=[
            "Participation climbs from 9.2% (age 18–24) to 63.5% (age 55–64) — a 54-percentage-point gap driven by life stage, not salary.",
            "Once a member opts in, annual sacrifice amounts are nearly flat across all age bands ($6,024–$7,396 median).",
            "Age is 2.3× more predictive of participation than salary: standardised OLS coefficients 0.110 vs 0.048.",
            "High-earners aged 55–64 participate less than mid-earners — likely the $30K concessional cap becoming binding.",
            "718 non-participating 35–44 year-olds at the inflection point represent the single largest activation opportunity.",
        ],

        findings=[
            {
                "title": "Participation Triples Between Ages 25 and 55 — The Activation Gap Is the Story",
                "narrative": (
                    "The fund's overall participation rate of 48.7% masks a 54-percentage-point spread across age cohorts. "
                    "Only 9.2% of 18–24 year-olds salary sacrifice; by age 55–64, 63.5% do. "
                    "This is not primarily a salary story — age rank is 2.3× more predictive than log salary in an OLS model. "
                    "Life-stage factors (proximity to retirement, family obligations discharged, financial advice relationships) "
                    "drive the effect more than earnings capacity."
                ),
                "chart_html": chart_participation,
                "insight": "The gap is in who opts in, not how much they contribute once they do. Strategy: focus on activation, not on lifting amounts among existing participants.",
                "source_note": "n=5,000 members | Dashed line = fund average (48.7%) | Source: super_members_2026Q1.csv",
            },
            {
                "title": "Conditional Amounts Are Nearly Flat — $6,024 to $7,396 Across All Age Bands",
                "narrative": (
                    "Among members who do salary sacrifice, the annual amount is remarkably consistent regardless of age. "
                    "The median ranges from $6,024 (35–44 band) to $7,396 (18–24 band). "
                    "The 18–24 figure is based on only 31 participants and should be treated as indicative. "
                    "The interquartile range across all bands is approximately $3,700–$9,100, "
                    "indicating wide individual variation that age alone does not explain. "
                    "This confirms that the intervention required is activation, not persuasion to contribute more."
                ),
                "chart_html": chart_amounts,
                "source_note": "Participants only (n=2,434) | Source: super_members_2026Q1.csv",
            },
            {
                "title": "Salary Is the Gating Factor for Young Members — But Life Stage Dominates for 45+",
                "narrative": (
                    "Breaking participation down by salary quartile reveals a clear pattern: "
                    "for members aged 18–34, salary is the primary barrier. Q1 earners in those bands barely participate; "
                    "Q4 earners reach 33–61% participation. For members aged 45+, even Q1 earners participate at meaningful rates, "
                    "suggesting that proximity to retirement and life-stage factors become the dominant drivers as members age. "
                    "An important anomaly appears: in the 55–64 band, Q4 earners participate less than Q2 and Q3. "
                    "Non-participants in that band have higher median salaries ($129,200) than participants ($111,400)."
                ),
                "chart_html": chart_salary_q,
                "insight": "55–64 Q4 earners likely face concessional cap constraints: at $150K salary, employer SG of $17,250 leaves only $12,750 before hitting the $30K cap. These members may be using personal deductible contributions instead.",
                "insight_style": "amber",
                "source_note": "Three representative age bands shown | Source: super_members_2026Q1.csv",
            },
            {
                "title": "Younger Participants Stretch Further Proportionally — 7.0% vs 5.1% of Salary",
                "narrative": (
                    "When sacrifice is expressed as a percentage of annual salary, younger participants are "
                    "contributing more relative to their income than older cohorts: 7.0% at age 18–24 versus 5.1% at 65+. "
                    "This inverse relationship reflects the concessional cap ($30,000 p.a. including employer SG) "
                    "becoming binding for higher-earning older members. A 55-year-old on $130,000 salary has "
                    "employer SG of $14,950 (11.5% FY2025) — leaving only $15,050 of concessional headroom. "
                    "Younger participants on lower salaries face no such constraint and can sacrifice a higher proportion."
                ),
                "chart_html": chart_pct_salary,
                "source_note": "Participants only (n=2,434) | Concessional cap interactions are inferred, not modelled | Source: super_members_2026Q1.csv",
            },
        ],

        caveats=[
            "Cross-sectional snapshot (31 March 2026) — causality cannot be established from observational data.",
            "Salary nulls: 100 members (2.0%) have missing salary data and are excluded from salary-stratified analyses.",
            "18–24 participant group is small (n=31) — conditional amounts for this band are indicative only.",
            "No adviser relationship data — a likely important omitted variable explaining residual participation variance.",
            "Concessional cap interactions not explicitly modelled — estimates are inferred, not measured.",
            "OLS model R²=9.5% — significant unobserved variation; findings are descriptive, not causal.",
        ],
    )

    out = Path("outputs/2026-04-29_salary_sacrifice_interactive.html")
    build_html_report(cfg, out)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        # build_html.py <findings_json> <data_path>
        findings_path = sys.argv[1]
        data_path = sys.argv[2]
        print(f"Building HTML from {findings_path} + {data_path}")
        # Generic build from findings JSON
        with open(findings_path) as f:
            findings = json.load(f)
        cfg = HTMLReportConfig(
            title=findings.get("analysis_name", "Analysis Report"),
            source_note=f"Source: {data_path} | n={findings.get('sample_size', '?')} | {findings.get('date_range', '')}",
            dataset_path=data_path,
            kpis=[],
            exec_summary=[f["claim"] for f in findings.get("findings", [])[:5]],
            caveats=findings.get("data_quality_flags", []),
        )
        out = Path(f"outputs/{Path(findings_path).stem}_interactive.html")
        build_html_report(cfg, out)
    else:
        build_salary_sacrifice_html()
