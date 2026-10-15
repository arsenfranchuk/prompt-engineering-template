import { useState, useEffect } from 'react';
import { useListCategoriesQuery } from '@/store/api/categoriesApi';
import { useCreateBudgetMutation, useUpdateBudgetMutation } from '@/store/api/budgetsApi';
import { budgetsApi } from '@/store/api/budgetsApi';
import { transactionsApi } from '@/store/api/transactionsApi';
import { dashboardApi } from '@/store/api/dashboardApi';
import { useAppDispatch } from '@/store/hooks';
import type { Budget, BudgetPeriod } from '@/types/budget';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Props {
  open: boolean;
  onClose: () => void;
  editingBudget?: Budget | null;
}

export function BudgetDialog({ open, onClose, editingBudget }: Props) {
  const dispatch = useAppDispatch();
  const { data: categories = [] } = useListCategoriesQuery();
  const [createBudget, { isLoading: creating }] = useCreateBudgetMutation();
  const [updateBudget, { isLoading: updating }] = useUpdateBudgetMutation();
  const isLoading = creating || updating;

  const [categoryId, setCategoryId] = useState('');
  const [plannedAmount, setPlannedAmount] = useState('');
  const [period, setPeriod] = useState<BudgetPeriod>('monthly');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [error, setError] = useState<string | null>(null);

  // Get expense categories only
  const expenseCategories = categories.filter((c) => c.type === 'expense');

  useEffect(() => {
    if (open) {
      if (editingBudget) {
        setCategoryId(editingBudget.category_id);
        setPlannedAmount(String(editingBudget.planned_amount));
        setPeriod(editingBudget.period);
        setStartDate(editingBudget.start_date);
        setEndDate(editingBudget.end_date || '');
      } else {
        // Set default to current month (YYYY-MM-01 to end of month) for new budget
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const defaultStart = `${year}-${month}-01`;
        const lastDay = new Date(year, today.getMonth() + 1, 0).getDate();
        const defaultEnd = `${year}-${month}-${String(lastDay).padStart(2, '0')}`;
        setCategoryId('');
        setPlannedAmount('');
        setPeriod('monthly');
        setStartDate(defaultStart);
        setEndDate(defaultEnd);
      }
      setError(null);
    }
  }, [open, editingBudget]);

  // For monthly period, ensure end_date is set to last day of month
  useEffect(() => {
    if (period === 'monthly' && startDate) {
      const parts = startDate.split('-');
      if (parts.length >= 2) {
        const y = parseInt(parts[0], 10);
        const m = parseInt(parts[1], 10);
        if (!isNaN(y) && !isNaN(m)) {
          const lastDay = new Date(y, m, 0);
          const endDay = `${lastDay.getFullYear()}-${String(lastDay.getMonth() + 1).padStart(2, '0')}-${String(lastDay.getDate()).padStart(2, '0')}`;
          setEndDate(endDay);
        }
      }
    }
  }, [period, startDate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const parsedAmount = parseFloat(plannedAmount);
    if (isNaN(parsedAmount) || parsedAmount <= 0) {
      setError('Please enter a valid amount');
      return;
    }
    if (!categoryId) {
      setError('Please select a category');
      return;
    }
    if (!startDate) {
      setError('Please select a start date');
      return;
    }

    let normalizedStartDate = startDate;
    if (/^\d{4}-\d{2}$/.test(normalizedStartDate)) {
      normalizedStartDate = `${normalizedStartDate}-01`;
    }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(normalizedStartDate)) {
      setError('Please select a valid start date (YYYY-MM-DD)');
      return;
    }

    let normalizedEndDate: string | undefined = undefined;
    if (period === 'custom') {
      if (endDate) {
        if (!/^\d{4}-\d{2}-\d{2}$/.test(endDate)) {
          setError('Please select a valid end date (YYYY-MM-DD)');
          return;
        }
        normalizedEndDate = endDate;
      }
    } else {
      if (endDate && /^\d{4}-\d{2}-\d{2}$/.test(endDate)) {
        normalizedEndDate = endDate;
      }
    }

    try {
      const payload = {
        category_id: categoryId,
        planned_amount: parsedAmount,
        period,
        start_date: normalizedStartDate,
        end_date: normalizedEndDate,
      };

      if (editingBudget) {
        await updateBudget({
          id: editingBudget.id,
          body: payload,
        }).unwrap();
      } else {
        await createBudget(payload).unwrap();
      }

      // Invalidate caches
      dispatch(dashboardApi.util.invalidateTags(['Dashboard']));
      dispatch(budgetsApi.util.invalidateTags([{ type: 'Budget', id: 'LIST' }]));
      dispatch(transactionsApi.util.invalidateTags([{ type: 'Transaction', id: 'LIST' }]));
      onClose();
    } catch (err: any) {
      setError(err?.data?.detail ?? 'Failed to save budget');
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>{editingBudget ? 'Edit Budget' : 'Create Budget'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <div>
            <Label htmlFor="category">Category (Expense)</Label>
            <select
              id="category"
              value={categoryId}
              onChange={(e) => setCategoryId(e.target.value)}
              className="mt-1.5 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">Select an expense category...</option>
              {expenseCategories.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <Label htmlFor="amount">Planned Amount</Label>
            <Input
              id="amount"
              type="number"
              step="0.01"
              min="0.01"
              placeholder="0.00"
              value={plannedAmount}
              onChange={(e) => setPlannedAmount(e.target.value)}
              className="mt-1.5"
            />
          </div>

          <div>
            <Label htmlFor="period">Period</Label>
            <div className="flex mt-1.5 rounded-lg overflow-hidden border border-slate-200">
              {(['monthly', 'custom'] as BudgetPeriod[]).map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => setPeriod(p)}
                  className={cn(
                    'flex-1 py-2 text-sm font-medium transition-colors capitalize',
                    period === p
                      ? 'bg-emerald-500 text-white'
                      : 'bg-white text-slate-600 hover:bg-slate-50'
                  )}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          <div>
            <Label htmlFor="startDate">Start Date</Label>
            <Input
              id="startDate"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="mt-1.5"
            />
          </div>

          {period === 'custom' && (
            <div>
              <Label htmlFor="endDate">End Date</Label>
              <Input
                id="endDate"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="mt-1.5"
              />
            </div>
          )}

          <div className="flex gap-3 pt-2">
            <Button
              type="button"
              variant="outline"
              className="flex-1"
              onClick={onClose}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1 bg-emerald-500 hover:bg-emerald-600 text-white"
              disabled={isLoading}
            >
              {isLoading ? 'Saving...' : editingBudget ? 'Update Budget' : 'Create Budget'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
