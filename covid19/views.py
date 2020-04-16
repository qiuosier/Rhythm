import pandas as pd
import numpy as np
import requests
import datetime
import logging
from django.shortcuts import render
from Aries.visual.plotly import PlotlyFigure
from .data import ECDCDataSet
logger = logging.getLogger(__name__)


def trim_df(df, starting_case):
    total = 0
    for i in range(len(df), 0, -1):
        idx = i - 1
        total += df['cases'][idx]
        if total > starting_case:
            logger.debug(df.index[idx])
            return df[df.index >= df.index[idx]]


def index(request):
    figure = PlotlyFigure()

    scale = request.GET.get("scale")
    if scale in ["log10", "log2"]:
        title_y = "Number of Cases %s" % scale
        scale = getattr(np, scale)
    else:
        title_y = "Number of Cases"
        scale = ""

    

    starting_case = request.GET.get("starting_case")
    if starting_case and str(starting_case).isdigit():
        starting_case = int(starting_case)
        figure.set_title(
            "Number of Daily New Cases", 
            title_x="Days since first %d cases" % starting_case,
            title_y=title_y
        )
    else:
        starting_case = None
        figure.set_title(
            "Number of Daily New Cases", 
            title_x="Date",
            title_y=title_y
        )

    country_codes = request.GET.getlist("country")

    for country_code in country_codes:
        df = ECDCDataSet().filter('countryterritoryCode', country_code)
        if starting_case is not None:
            df = trim_df(df, starting_case)
            idx = list(range(len(df), 0, -1))
        else:
            idx = df.index

        if scale:
            cases = scale(df['cases'])
        else:
            cases = df['cases']
        figure.line(idx, cases, name=country_code)
    return render(request, "covid19/index.html", {
        "title": "COVID 19 Data",
        "message": "",
        "chart": figure.to_html()
    })
