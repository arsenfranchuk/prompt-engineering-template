export type TransactionType = 'income' | 'expense'

export interface Transaction {
  id: string
  user_id: string
  type: TransactionType
  amount: number
  category_id: string
  category_name: string
  date: string
  description: string
  created_at: string
  updated_at: string
}

export interface TransactionCreateInput {
  type: TransactionType
  amount: number
  category_id: string
  date: string
  description?: string
}

export interface TransactionUpdateInput {
  type?: TransactionType
  amount?: number
  category_id?: string
  date?: string
  description?: string
}

export interface TransactionFilters {
  type?: TransactionType | 'all'
  category_id?: string
  start_date?: string
  end_date?: string
  search?: string
  sort_by?: 'date' | 'amount'
  sort_order?: 'asc' | 'desc'
}
