export type BudgetPeriod = 'monthly' | 'custom'
export type BudgetStatus = 'within' | 'warning' | 'exceeded'

export interface Budget {
  id: string
  user_id: string
  category_id: string
  category_name: string
  planned_amount: number
  period: BudgetPeriod
  start_date: string
  end_date: string | null
  spent_amount: number
  remaining_amount: number
  percentage_used: number
  status: BudgetStatus
  created_at: string
  updated_at: string
}

export interface BudgetCreateInput {
  category_id: string
  planned_amount: number
  period: BudgetPeriod
  start_date: string
  end_date?: string
}

export interface BudgetUpdateInput {
  category_id?: string
  planned_amount?: number
  period?: BudgetPeriod
  start_date?: string
  end_date?: string
}
