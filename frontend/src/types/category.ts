export type CategoryType = 'income' | 'expense'

export interface Category {
  id: string
  user_id: string
  name: string
  type: CategoryType
  is_default: boolean
  created_at: string
}

export interface CategoryCreateInput {
  name: string
  type: CategoryType
}

export interface CategoryUpdateInput {
  name: string
}
