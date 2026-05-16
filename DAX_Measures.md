# Power BI DAX Measures

These measures should be created in a dedicated disconnected table named "Measures".

## 5.1 Revenue & Growth Measures

```dax
Total Revenue = SUM(fact_profit_loss[sales])
```

```dax
Total Net Profit = SUM(fact_profit_loss[net_profit])
```

```dax
Avg OPM % = AVERAGE(fact_profit_loss[opm_pct])
```

```dax
Revenue YoY Growth % = 
VAR CurrentYear = CALCULATE(SUM(fact_profit_loss[sales]))
VAR PreviousYear = CALCULATE(
    SUM(fact_profit_loss[sales]),
    DATEADD(dim_year[year_date], -1, YEAR)
)
RETURN
IF(
    NOT ISBLANK(PreviousYear) && PreviousYear <> 0,
    DIVIDE(CurrentYear - PreviousYear, PreviousYear) * 100,
    BLANK()
)
```

```dax
Profit YoY Growth % = 
VAR CurrentYear = CALCULATE(SUM(fact_profit_loss[net_profit]))
VAR PreviousYear = CALCULATE(
    SUM(fact_profit_loss[net_profit]),
    DATEADD(dim_year[year_date], -1, YEAR)
)
RETURN
IF(
    NOT ISBLANK(PreviousYear) && PreviousYear <> 0,
    DIVIDE(CurrentYear - PreviousYear, PreviousYear) * 100,
    BLANK()
)
```

```dax
3Y Sales CAGR % = 
CALCULATE(
    AVERAGE(fact_analysis[value_pct]),
    fact_analysis[period_label] = "3Y",
    fact_analysis[metric] = "compounded_sales_growth"
)
```

```dax
5Y Sales CAGR % = 
CALCULATE(
    AVERAGE(fact_analysis[value_pct]),
    fact_analysis[period_label] = "5Y",
    fact_analysis[metric] = "compounded_sales_growth"
)
```

```dax
10Y Sales CAGR % = 
CALCULATE(
    AVERAGE(fact_analysis[value_pct]),
    fact_analysis[period_label] = "10Y",
    fact_analysis[metric] = "compounded_sales_growth"
)
```

## 5.2 Profitability Measures

```dax
Net Profit Margin % = DIVIDE(SUM(fact_profit_loss[net_profit]), SUM(fact_profit_loss[sales])) * 100
```

```dax
Avg ROE % = AVERAGE(dim_company[roe_percentage])
```

```dax
ROE Last Year = 
CALCULATE(
    AVERAGE(fact_analysis[value_pct]),
    fact_analysis[period_label] = "Last Year",
    fact_analysis[metric] = "roe"
)
```

```dax
Interest Coverage Ratio = 
DIVIDE(
    SUM(fact_profit_loss[operating_profit]),
    SUM(fact_profit_loss[interest])
)
```

```dax
Expense Ratio % = DIVIDE(SUM(fact_profit_loss[expenses]), SUM(fact_profit_loss[sales])) * 100
```

## 5.3 Balance Sheet & Leverage Measures

```dax
Avg Debt to Equity = AVERAGE(fact_balance_sheet[debt_to_equity])
```

```dax
Latest Debt to Equity = 
CALCULATE(
    AVERAGE(fact_balance_sheet[debt_to_equity]),
    LASTDATE(dim_year[year_date])
)
```

```dax
Total Borrowings = SUM(fact_balance_sheet[borrowings])
```

```dax
Equity Ratio = 
DIVIDE(
    SUM(fact_balance_sheet[equity_capital]) + SUM(fact_balance_sheet[reserves]),
    SUM(fact_balance_sheet[total_assets])
)
```

```dax
Debt Free Flag = IF([Latest Debt to Equity] < 0.1, "Debt Free", "Has Debt")
```

## 5.4 Cash Flow Measures

```dax
Free Cash Flow = SUM(fact_cash_flow[operating_activity]) + SUM(fact_cash_flow[investing_activity])
```

```dax
Cash Conversion Ratio = 
DIVIDE(
    SUM(fact_cash_flow[operating_activity]),
    SUM(fact_profit_loss[net_profit])
)
```

```dax
Positive FCF Years Count = 
COUNTROWS(
    FILTER(
        fact_cash_flow,
        fact_cash_flow[free_cash_flow] > 0
    )
)
```

## 5.5 Dividend Measures

```dax
Avg Dividend Payout % = AVERAGE(fact_profit_loss[dividend_payout_pct])
```

```dax
Consistent Dividend Payer = 
VAR YearsWithDividend = COUNTROWS(
    FILTER(fact_profit_loss, fact_profit_loss[dividend_payout_pct] > 0)
)
VAR TotalYears = COUNTROWS(fact_profit_loss)
RETURN
IF(DIVIDE(YearsWithDividend, TotalYears) >= 0.8, "Yes", "No")
```

## 5.6 ML Score Measures

```dax
Latest Health Score = 
CALCULATE(
    MAX(fact_ml_scores[overall_score]),
    LASTDATE(fact_ml_scores[computed_at])
)
```

```dax
Health Label = 
SWITCH(
    TRUE(),
    [Latest Health Score] >= 85, "EXCELLENT",
    [Latest Health Score] >= 70, "GOOD",
    [Latest Health Score] >= 50, "AVERAGE",
    [Latest Health Score] >= 35, "WEAK",
    "POOR"
)
```

```dax
Health Score Color = 
SWITCH(
    [Health Label],
    "EXCELLENT", "#2ECC71",
    "GOOD", "#82E0AA",
    "AVERAGE", "#F7DC6F",
    "WEAK", "#F0A500",
    "POOR", "#E74C3C",
    "#CCCCCC"
)
```

```dax
Companies with Excellent Health = 
CALCULATE(
    COUNTROWS(fact_ml_scores),
    fact_ml_scores[health_label] = "EXCELLENT",
    LASTDATE(fact_ml_scores[computed_at])
)
```

```dax
Companies Needing Attention = 
CALCULATE(
    COUNTROWS(fact_ml_scores),
    fact_ml_scores[health_label] IN {"WEAK", "POOR"},
    LASTDATE(fact_ml_scores[computed_at])
)
```
