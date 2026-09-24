import { useState } from 'react'
import {
  useListCategoriesQuery,
  useDeleteCategoryMutation,
} from '@/store/api/categoriesApi'
import type { Category, CategoryType } from '@/types/category'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { CategoryDialog } from './CategoryDialog'
import {
  Plus,
  Search,
  Pencil,
  Trash2,
  Tag,
  AlertCircle,
  Loader2,
  TrendingDown,
  TrendingUp,
} from 'lucide-react'
import { cn } from '@/lib/utils'

export function CategoriesPage() {
  const [typeFilter, setTypeFilter] = useState<'all' | CategoryType>('all')
  const [search, setSearch] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingCategory, setEditingCategory] = useState<Category | null>(null)
  const [confirmDelete, setConfirmDelete] = useState<Category | null>(null)
  const [deleteError, setDeleteError] = useState<string | null>(null)

  const { data: categories = [], isLoading, isError } = useListCategoriesQuery()
  const [deleteCategory, { isLoading: isDeleting }] = useDeleteCategoryMutation()

  const handleOpenCreate = () => {
    setEditingCategory(null)
    setDialogOpen(true)
  }

  const handleOpenEdit = (cat: Category) => {
    setEditingCategory(cat)
    setDialogOpen(true)
  }

  const handleDelete = async (cat: Category) => {
    setDeleteError(null)
    try {
      await deleteCategory(cat.id).unwrap()
      setConfirmDelete(null)
    } catch (err: any) {
      setDeleteError(err?.data?.detail ?? 'Failed to delete category. It may be in use.')
    }
  }

  const filtered = categories.filter((cat) => {
    if (typeFilter !== 'all' && cat.type !== typeFilter) return false
    if (search.trim() && !cat.name.toLowerCase().includes(search.toLowerCase())) return false
    return true
  })

  const expenseCategories = filtered.filter((c) => c.type === 'expense')
  const incomeCategories = filtered.filter((c) => c.type === 'income')

  return (
    <div className="p-4 md:p-6 space-y-6 max-w-6xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center gap-4 justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Categories</h1>
          <p className="text-slate-500 text-sm">
            Organize your income and expenses with default and custom categories
          </p>
        </div>
        <Button
          onClick={handleOpenCreate}
          className="bg-emerald-600 hover:bg-emerald-700 text-white self-start sm:self-auto"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Category
        </Button>
      </div>

      {deleteError && (
        <div className="flex items-center gap-2 p-3 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{deleteError}</span>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
        <div className="flex gap-2">
          {(['all', 'expense', 'income'] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTypeFilter(t)}
              className={cn(
                'px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors capitalize',
                typeFilter === t
                  ? 'bg-emerald-500 text-white shadow-sm'
                  : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50',
              )}
            >
              {t === 'all' ? 'All Categories' : `${t}s`}
            </button>
          ))}
        </div>

        <div className="relative max-w-xs w-full">
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-400" />
          <Input
            placeholder="Search categories..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9 bg-white"
          />
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
        </div>
      ) : isError ? (
        <div className="p-8 text-center text-red-600 bg-white rounded-xl border border-red-100">
          Failed to load categories. Please try refreshing the page.
        </div>
      ) : filtered.length === 0 ? (
        <Card className="p-12 text-center">
          <Tag className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <p className="text-slate-600 font-medium">No categories found</p>
          <p className="text-slate-400 text-sm mt-1">
            {search ? 'Try adjusting your search criteria.' : 'Create a category to get started.'}
          </p>
          {!search && (
            <Button
              onClick={handleOpenCreate}
              variant="outline"
              size="sm"
              className="mt-4"
            >
              <Plus className="w-4 h-4 mr-1" /> Add Category
            </Button>
          )}
        </Card>
      ) : (
        <div className="space-y-6">
          {/* Expenses Group */}
          {(typeFilter === 'all' || typeFilter === 'expense') && expenseCategories.length > 0 && (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <TrendingDown className="w-5 h-5 text-rose-500" />
                <h2 className="text-lg font-semibold text-slate-800">
                  Expense Categories ({expenseCategories.length})
                </h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                {expenseCategories.map((cat) => (
                  <CategoryCard
                    key={cat.id}
                    category={cat}
                    onEdit={() => handleOpenEdit(cat)}
                    onDelete={() => setConfirmDelete(cat)}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Income Group */}
          {(typeFilter === 'all' || typeFilter === 'income') && incomeCategories.length > 0 && (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-emerald-500" />
                <h2 className="text-lg font-semibold text-slate-800">
                  Income Categories ({incomeCategories.length})
                </h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                {incomeCategories.map((cat) => (
                  <CategoryCard
                    key={cat.id}
                    category={cat}
                    onEdit={() => handleOpenEdit(cat)}
                    onDelete={() => setConfirmDelete(cat)}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {confirmDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 space-y-4">
            <h3 className="text-lg font-bold text-slate-800">Delete Category</h3>
            <p className="text-sm text-slate-600">
              Are you sure you want to delete <span className="font-semibold text-slate-900">"{confirmDelete.name}"</span>?
            </p>
            <p className="text-xs text-amber-600 bg-amber-50 p-2.5 rounded-lg border border-amber-200">
              Note: Categories associated with existing transactions or budgets cannot be deleted.
            </p>
            <div className="flex justify-end gap-3 pt-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setConfirmDelete(null)}
                disabled={isDeleting}
              >
                Cancel
              </Button>
              <Button
                size="sm"
                className="bg-red-600 hover:bg-red-700 text-white"
                onClick={() => handleDelete(confirmDelete)}
                disabled={isDeleting}
              >
                {isDeleting ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Delete'}
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Dialog for create / edit */}
      <CategoryDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        category={editingCategory}
      />
    </div>
  )
}

function CategoryCard({
  category,
  onEdit,
  onDelete,
}: {
  category: Category
  onEdit: () => void
  onDelete: () => void
}) {
  return (
    <Card className="hover:shadow-sm transition-shadow">
      <CardContent className="p-4 flex items-center justify-between">
        <div className="min-w-0 space-y-1">
          <div className="flex items-center gap-2">
            <span className="font-medium text-slate-800 truncate">{category.name}</span>
            {category.is_default ? (
              <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">
                Default
              </span>
            ) : (
              <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700">
                Custom
              </span>
            )}
          </div>
          <p className="text-xs text-slate-400 capitalize">{category.type}</p>
        </div>

        <div className="flex items-center gap-1 shrink-0">
          <Button
            variant="ghost"
            size="icon"
            className="w-8 h-8 text-slate-500 hover:text-slate-800"
            onClick={onEdit}
            title="Edit category"
          >
            <Pencil className="w-3.5 h-3.5" />
          </Button>
          {!category.is_default && (
            <Button
              variant="ghost"
              size="icon"
              className="w-8 h-8 text-slate-500 hover:text-red-600 hover:bg-red-50"
              onClick={onDelete}
              title="Delete category"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
