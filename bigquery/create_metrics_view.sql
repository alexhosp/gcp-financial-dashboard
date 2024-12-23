 -- Create a CTE here for efficiency
WITH cte AS (
  SELECT
    company_symbol,
    fiscal_year,
    fiscal_period,
    total_revenue,
    net_income,
    research_and_development AS r_d_expenses, -- rename for convenience
    interest_expense,
    income_tax_expense,
    depreciation,
    amortization,
    operating_cash_flow,
    capital_expenditures,

    -- Get previous quarter's revenue using a window function
    LAG(total_revenue) OVER (
      PARTITION BY company_symbol
      ORDER BY fiscal_year, fiscal_period
    ) AS prev_revenue
  FROM `alpha_vantage_data.financial_statements_raw`
)
SELECT
  company_symbol,
  fiscal_year,
  fiscal_period,

  -- 1) Compute revenue growth
  CASE 
    -- First check ensures there is a value, second ensures it is not 0
    WHEN prev_revenue IS NOT NULL AND prev_revenue != 0 THEN
      (total_revenue - prev_revenue) / prev_revenue
    ELSE NULL
  END AS revenue_growth,

  -- 2) Compute net profit margin
  CASE 
    WHEN total_revenue != 0 THEN net_income / total_revenue
    ELSE NULL
  END AS net_profit_margin,

  -- 3) Select R&D to include in the view
  r_d_expenses,

  -- 4) Compute EBITDA
  (net_income
  -- The COALESCECE function replaces NULL values in columns with 0
   + COALESCE(interest_expense, 0)
   + COALESCE(income_tax_expense, 0)
   + COALESCE(depreciation, 0)
   + COALESCE(amortization, 0)
  ) AS ebitda,

  -- 5) Compute free cash flow
  (COALESCE(operating_cash_flow, 0) 
   - COALESCE(capital_expenditures, 0)
  ) AS free_cash_flow

FROM cte
ORDER BY company_symbol, fiscal_year, fiscal_period;
