import { useState, useEffect } from 'react';
import { useCreateCategoryMutation, useUpdateCategoryMutation } from '@/store/api/categoriesApi';
import { dashboardApi } from '@/store/api/dashboardApi';
import { budgetsApi } from '@/store/api/budgetsApi';
import { transactionsApi } from '@/store/api/transactionsApi';
import { useAppDispatch } from '@/store/hooks';
import type { Category, CategoryType } from '@/types/category';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AlertCircle, Loader2 } from 'lucide-react';

interface CategoryDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  category?: Category | null;
}

export function CategoryDialog({ open, onOpenChange, category }: CategoryDialogProps) {
  const dispatch = useAppDispatch();
  const isEditing = !!category;

  const [name, setName] = useState('');
  const [type, setType] = useState<CategoryType>('expense');
  const [error, setError] = useState<string | null>(null);

  const [createCategory, { isLoading: isCreating }] = useCreateCategoryMutation();
  const [updateCategory, { isLoading: isUpdating }] = useUpdateCategoryMutation();

  const isSubmitting = isCreating || isUpdating;

  useEffect(() => {
    if (open) {
      if (category) {
        setName(category.name);
        setType(category.type);
      } else {
        setName('');
        setType('expense');
      }
      setError(null);
    }
  }, [open, category]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const trimmed = name.trim();
    if (!trimmed) {
      setError('Category name is required');
      return;
    }

    try {
      if (isEditing && category) {
        await updateCategory({
          id: category.id,
          body: { name: trimmed },
        }).unwrap();
      } else {
        await createCategory({
          name: trimmed,
          type,
        }).unwrap();
      }
      dispatch(dashboardApi.util.invalidateTags(['Dashboard']));
      dispatch(budgetsApi.util.invalidateTags([{ type: 'Budget', id: 'LIST' }]));
      dispatch(transactionsApi.util.invalidateTags([{ type: 'Transaction', id: 'LIST' }]));
      onOpenChange(false);
    } catch (err: any) {
      setError(err?.data?.detail ?? 'Failed to save category. Please try again.');
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{isEditing ? 'Edit Category' : 'Create New Category'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4 py-2">
          {error && (
            <div className="flex items-center gap-2 p-3 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="category-name">Category Name</Label>
            <Input
              id="category-name"
              placeholder="e.g. Subscriptions, Freelance, Groceries"
              value={name}
              onChange={(e) => setName(e.target.value)}
              autoFocus
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="category-type">Category Type</Label>
            {isEditing ? (
              <div className="px-3 py-2 bg-slate-100 border border-slate-200 rounded-md text-sm text-slate-700 capitalize">
                {type} Category (cannot change type of existing category)
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setType('expense')}
                  className={`py-2 px-3 text-sm font-medium rounded-lg border text-center transition-colors ${
                    type === 'expense'
                      ? 'bg-rose-50 border-rose-500 text-rose-700'
                      : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  Expense
                </button>
                <button
                  type="button"
                  onClick={() => setType('income')}
                  className={`py-2 px-3 text-sm font-medium rounded-lg border text-center transition-colors ${
                    type === 'income'
                      ? 'bg-emerald-50 border-emerald-500 text-emerald-700'
                      : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  Income
                </button>
              </div>
            )}
          </div>

          <DialogFooter className="pt-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="bg-emerald-600 hover:bg-emerald-700 text-white"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Saving...
                </>
              ) : isEditing ? (
                'Save Changes'
              ) : (
                'Create Category'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
