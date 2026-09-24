import type { Transaction } from './transaction'

export type DashboardPeriod = 'current_month' | 'previous_month' | 'current_year' | 'all'

export interface CategorySpendingItem {
  category_id: string
  category_name: string
  amount: number
  percentage: number
}

export interface CategoryIncomeItem {
  category_id: string
  category_name: string
  amount: number
  percentage: number
}

export interface BudgetSummary {
  total_planned: number
  total_spent: number
  total_remaining: number
  percentage_used: number
  active_count: number
}

export interface MonthlyTrendItem {
  month: string
  label: string
  income: number
  expense: number
  net: number
}

export interface DashboardSummary {
  current_balance: number
  period: string
  period_income: number
  period_expenses: number
  period_net: number
  savings_rate: number
  spending_by_category: CategorySpendingItem[]
  income_by_category: CategoryIncomeItem[]
  budget_summary: BudgetSummary
  recent_transactions: Transaction[]
  monthly_trend: MonthlyTrendItem[]
}
