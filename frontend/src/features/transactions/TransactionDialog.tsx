import { useState, useEffect } from 'react';
import { useListCategoriesQuery } from '@/store/api/categoriesApi';
import {
  useCreateTransactionMutation,
  useUpdateTransactionMutation,
} from '@/store/api/transactionsApi';
import { budgetsApi } from '@/store/api/budgetsApi';
import { dashboardApi } from '@/store/api/dashboardApi';
import { useAppDispatch } from '@/store/hooks';
import type { Transaction, TransactionType } from '@/types/transaction';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AlertCircle } from 'lucide-react';
import { cn, todayString } from '@/lib/utils';

interface Props {
  open: boolean;
  onClose: () => void;
  defaultType?: TransactionType;
  editingTransaction?: Transaction | null;
}

export function TransactionDialog({
  open,
  onClose,
  defaultType = 'expense',
  editingTransaction,
}: Props) {
  const dispatch = useAppDispatch();
  const { data: categories = [] } = useListCategoriesQuery();
  const [createTransaction, { isLoading: creating }] = useCreateTransactionMutation();
  const [updateTransaction, { isLoading: updating }] = useUpdateTransactionMutation();
  const isLoading = creating || updating;

  const [type, setType] = useState<TransactionType>(defaultType);
  const [amount, setAmount] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [date, setDate] = useState(todayString());
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);

  const filteredCategories = categories.filter((c) => c.type === type);

  useEffect(() => {
    if (open) {
      if (editingTransaction) {
        setType(editingTransaction.type);
        setAmount(String(editingTransaction.amount));
        setCategoryId(editingTransaction.category_id);
        setDate(editingTransaction.date);
        setDescription(editingTransaction.description);
      } else {
        setType(defaultType);
        setAmount('');
        setCategoryId('');
        setDate(todayString());
        setDescription('');
      }
      setError(null);
    }
  }, [open, editingTransaction, defaultType]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const parsedAmount = parseFloat(amount);
    if (isNaN(parsedAmount) || parsedAmount <= 0) {
      setError('Amount must be a positive number');
      return;
    }
    if (!categoryId) {
      setError('Please select a category');
      return;
    }
    if (!date) {
      setError('Please select a date');
      return;
    }

    try {
      if (editingTransaction) {
        await updateTransaction({
          id: editingTransaction.id,
          body: { type, amount: parsedAmount, category_id: categoryId, date, description },
        }).unwrap();
      } else {
        await createTransaction({
          type,
          amount: parsedAmount,
          category_id: categoryId,
          date,
          description,
        }).unwrap();
      }
      // Invalidate dashboard cache so stats refresh
      dispatch(dashboardApi.util.invalidateTags(['Dashboard']));
      dispatch(budgetsApi.util.invalidateTags([{ type: 'Budget', id: 'LIST' }]));
      onClose();
    } catch (err: any) {
      setError(err?.data?.detail ?? 'Failed to save transaction');
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>{editingTransaction ? 'Edit Transaction' : 'Add Transaction'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Type Toggle */}
          <div>
            <Label>Type</Label>
            <div className="flex mt-1.5 rounded-lg overflow-hidden border border-slate-200">
              {(['income', 'expense'] as TransactionType[]).map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => {
                    if (t !== type) {
                      setType(t);
                      setCategoryId('');
                    }
                  }}
                  className={cn(
                    'flex-1 py-2 text-sm font-medium transition-colors capitalize',
                    type === t
                      ? t === 'income'
                        ? 'bg-emerald-500 text-white'
                        : 'bg-red-500 text-white'
                      : 'bg-white text-slate-600 hover:bg-slate-50'
                  )}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          <div>
            <Label htmlFor="amount">Amount</Label>
            <Input
              id="amount"
              type="number"
              step="0.01"
              min="0.01"
              placeholder="0.00"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="mt-1.5"
            />
          </div>

          <div>
            <Label htmlFor="category">Category</Label>
            <select
              id="category"
              value={categoryId}
              onChange={(e) => setCategoryId(e.target.value)}
              className="mt-1.5 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">Select a category…</option>
              {filteredCategories.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <Label htmlFor="date">Date</Label>
            <Input
              id="date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="mt-1.5"
            />
          </div>

          <div>
            <Label htmlFor="description">
              Description <span className="text-slate-400 font-normal">(optional)</span>
            </Label>
            <Input
              id="description"
              placeholder="What was this for?"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="mt-1.5"
            />
          </div>

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
              className={cn(
                'flex-1',
                type === 'income'
                  ? 'bg-emerald-500 hover:bg-emerald-600'
                  : 'bg-red-500 hover:bg-red-600'
              )}
              disabled={isLoading}
            >
              {isLoading ? 'Saving…' : editingTransaction ? 'Update' : 'Add Transaction'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
