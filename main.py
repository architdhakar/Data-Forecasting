from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os

from analysis import load_data, preprocess_data
from insights import analyze_metric, generate_insight, improvement_suggestion
from visualization import generate_plot
from forecasting import influence_analysis

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
os.makedirs("static/plots", exist_ok=True)

def infer_time_unit(time_series):
    sample = time_series.iloc[:3].astype(str).str.lower()

    if any("jan" in v or "feb" in v for v in sample):
        return "month"
    if time_series.diff().median().days == 1:
        return "day"
    if time_series.diff().median().days >= 28:
        return "month"
    if time_series.diff().median().days >= 90:
        return "quarter"

    return "period"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
def upload_file(request: Request, file: UploadFile = File(...)):
    df = load_data(file)
    df, time_col, numeric_cols = preprocess_data(df)

    reports = []

    
    for col in numeric_cols:
        series = df[col]
        trend, pct = analyze_metric(series)

        insight = generate_insight(col, trend, pct)
        suggestion = improvement_suggestion(col, trend)

        plot_path = f"static/plots/{col}.png"
        generate_plot(df[time_col], series, col, plot_path)

        reports.append({
            "metric": col,
            "trend": trend,
            "change": pct,
            "insight": insight,
            "suggestion": suggestion,
            "plot": "/" + plot_path
        })

   
    influence_reports = {}

    for target in numeric_cols:
        influences = influence_analysis(df[numeric_cols], target)
        if influences:
            influence_reports[target] = influences
    print(influence_reports)
    time_unit = infer_time_unit(df[time_col])
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "reports": reports,
            "influences": influence_reports,  # OPTIONAL
            "time_unit": time_unit
        }
    )
