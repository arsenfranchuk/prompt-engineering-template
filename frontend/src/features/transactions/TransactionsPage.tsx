import { useState } from 'react';
import {
  useListTransactionsQuery,
  useDeleteTransactionMutation,
} from '@/store/api/transactionsApi';
import { dashboardApi } from '@/store/api/dashboardApi';
import { budgetsApi } from '@/store/api/budgetsApi';
import { useListCategoriesQuery } from '@/store/api/categoriesApi';
import { useAppDispatch } from '@/store/hooks';
import type { Transaction, TransactionType } from '@/types/transaction';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Plus, Search, Pencil, Trash2, Loader2, ArrowUpDown } from 'lucide-react';
import { cn, formatCurrency, formatDate } from '@/lib/utils';
import { TransactionDialog } from './TransactionDialog';

export function TransactionsPage() {
  const dispatch = useAppDispatch();

  const [typeFilter, setTypeFilter] = useState<'all' | TransactionType>('all');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState<'date' | 'amount'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingTx, setEditingTx] = useState<Transaction | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [confirmDelete, setConfirmDelete] = useState<Transaction | null>(null);

  const { data: categories = [] } = useListCategoriesQuery();
  const {
    data: transactions = [],
    isLoading,
    isError,
  } = useListTransactionsQuery({
    type: typeFilter === 'all' ? undefined : typeFilter,
    category_id: categoryFilter || undefined,
    search: search || undefined,
    sort_by: sortBy,
    sort_order: sortOrder,
  });
  const [deleteTransaction] = useDeleteTransactionMutation();

  const handleDelete = async (tx: Transaction) => {
    setDeletingId(tx.id);
    try {
      await deleteTransaction(tx.id).unwrap();
      dispatch(dashboardApi.util.invalidateTags(['Dashboard']));
      dispatch(budgetsApi.util.invalidateTags([{ type: 'Budget', id: 'LIST' }]));
    } finally {
      setDeletingId(null);
      setConfirmDelete(null);
    }
  };

  const toggleSort = (field: 'date' | 'amount') => {
    if (sortBy === field) {
      setSortOrder((o) => (o === 'desc' ? 'asc' : 'desc'));
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  return (
    <div className="p-4 md:p-6 space-y-5 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Transactions</h1>
          <p className="text-slate-500 text-sm">
            {transactions.length} transaction{transactions.length !== 1 ? 's' : ''}
          </p>
        </div>
        <Button
          onClick={() => {
            setEditingTx(null);
            setDialogOpen(true);
          }}
          className="bg-emerald-500 hover:bg-emerald-600"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add
        </Button>
      </div>

      {/* Filters */}
      <Card className="p-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input
              placeholder="Search transactions…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9"
            />
          </div>

          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value as any)}
            className="rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="all">All Types</option>
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>

          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name} ({cat.type})
              </option>
            ))}
          </select>
        </div>
      </Card>

      {/* Sort Controls */}
      <div className="flex gap-2">
        <button
          onClick={() => toggleSort('date')}
          className={cn(
            'flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors',
            sortBy === 'date'
              ? 'bg-slate-800 text-white border-slate-800'
              : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
          )}
        >
          <ArrowUpDown className="w-3 h-3" />
          Date {sortBy === 'date' ? (sortOrder === 'desc' ? '↓' : '↑') : ''}
        </button>
        <button
          onClick={() => toggleSort('amount')}
          className={cn(
            'flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors',
            sortBy === 'amount'
              ? 'bg-slate-800 text-white border-slate-800'
              : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
          )}
        >
          <ArrowUpDown className="w-3 h-3" />
          Amount {sortBy === 'amount' ? (sortOrder === 'desc' ? '↓' : '↑') : ''}
        </button>
      </div>

      {/* Transaction List */}
      {isLoading ? (
        <div className="flex items-center justify-center h-40">
          <Loader2 className="w-6 h-6 animate-spin text-emerald-500" />
        </div>
      ) : isError ? (
        <div className="text-center text-red-600 py-10">Failed to load transactions</div>
      ) : transactions.length === 0 ? (
        <div className="text-center py-16 text-slate-400">
          <Plus className="w-10 h-10 mx-auto mb-3 opacity-30" />
          <p className="font-medium">No transactions found</p>
          <p className="text-sm mt-1">Try adjusting your filters or add a new transaction</p>
        </div>
      ) : (
        <div className="space-y-2">
          {transactions.map((tx) => (
            <Card key={tx.id} className="p-4">
              <div className="flex items-center gap-4">
                <div
                  className={cn(
                    'w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shrink-0',
                    tx.type === 'income'
                      ? 'bg-emerald-100 text-emerald-700'
                      : 'bg-red-100 text-red-700'
                  )}
                >
                  {tx.type === 'income' ? '+' : '−'}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-slate-800 truncate">
                    {tx.description || tx.category_name}
                  </p>
                  <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
                    <span
                      className={cn(
                        'px-1.5 py-0.5 rounded text-xs font-medium',
                        tx.type === 'income'
                          ? 'bg-emerald-50 text-emerald-700'
                          : 'bg-red-50 text-red-700'
                      )}
                    >
                      {tx.category_name}
                    </span>
                    <span>·</span>
                    <span>{formatDate(tx.date)}</span>
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <p
                    className={cn(
                      'font-semibold',
                      tx.type === 'income' ? 'text-emerald-600' : 'text-red-600'
                    )}
                  >
                    {tx.type === 'income' ? '+' : '−'}
                    {formatCurrency(tx.amount)}
                  </p>
                </div>
                <div className="flex gap-1 shrink-0">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 text-slate-400 hover:text-slate-600"
                    onClick={() => {
                      setEditingTx(tx);
                      setDialogOpen(true);
                    }}
                  >
                    <Pencil className="w-3.5 h-3.5" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 text-slate-400 hover:text-red-600"
                    onClick={() => setConfirmDelete(tx)}
                    disabled={deletingId === tx.id}
                  >
                    {deletingId === tx.id ? (
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <Trash2 className="w-3.5 h-3.5" />
                    )}
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Delete Confirmation */}
      {confirmDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/30">
          <Card className="max-w-sm w-full p-6 space-y-4">
            <h3 className="font-semibold text-slate-800">Delete transaction?</h3>
            <p className="text-sm text-slate-500">
              This will permanently remove{' '}
              <strong>{confirmDelete.description || confirmDelete.category_name}</strong> (
              {formatCurrency(confirmDelete.amount)}).
            </p>
            <div className="flex gap-3">
              <Button variant="outline" className="flex-1" onClick={() => setConfirmDelete(null)}>
                Cancel
              </Button>
              <Button
                className="flex-1 bg-red-500 hover:bg-red-600 text-white"
                onClick={() => handleDelete(confirmDelete)}
              >
                Delete
              </Button>
            </div>
          </Card>
        </div>
      )}

      <TransactionDialog
        open={dialogOpen}
        onClose={() => {
          setDialogOpen(false);
          setEditingTx(null);
        }}
        editingTransaction={editingTx}
      />
    </div>
  );
}
