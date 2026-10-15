import { useState } from 'react';
import { useListBudgetsQuery, useDeleteBudgetMutation } from '@/store/api/budgetsApi';
import { dashboardApi } from '@/store/api/dashboardApi';
import { transactionsApi } from '@/store/api/transactionsApi';
import { useAppDispatch } from '@/store/hooks';
import type { Budget } from '@/types/budget';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BudgetDialog } from './BudgetDialog';
import { Plus, Target, AlertCircle, Loader2 } from 'lucide-react';
import { formatCurrency, cn } from '@/lib/utils';

export function BudgetsPage() {
  const dispatch = useAppDispatch();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingBudget, setEditingBudget] = useState<Budget | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [confirmDelete, setConfirmDelete] = useState<Budget | null>(null);

  const { data: budgets = [] } = useListBudgetsQuery();
  const [deleteBudget] = useDeleteBudgetMutation();

  const handleDelete = async (budget: Budget) => {
    setDeletingId(budget.id);
    try {
      await deleteBudget(budget.id).unwrap();
      dispatch(dashboardApi.util.invalidateTags(['Dashboard']));
      dispatch(transactionsApi.util.invalidateTags([{ type: 'Transaction', id: 'LIST' }]));
    } finally {
      setDeletingId(null);
      setConfirmDelete(null);
    }
  };

  const statusColor = (status: string) =>
    status === 'exceeded' ? 'bg-red-500' : status === 'warning' ? 'bg-amber-400' : 'bg-emerald-500';

  const statusLabel = (status: string) =>
    status === 'exceeded'
      ? 'Over Budget'
      : status === 'warning'
        ? 'Approaching Limit'
        : 'Within Budget';

  return (
    <div className="p-4 md:p-6 space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Budgets</h1>
          <p className="text-slate-500 text-sm">Track your spending limits</p>
        </div>
        <Button
          onClick={() => {
            setEditingBudget(null);
            setDialogOpen(true);
          }}
          className="bg-emerald-500 hover:bg-emerald-600"
        >
          <Plus className="w-4 h-4 mr-2" />
          Create Budget
        </Button>
      </div>

      {/* Budget Summary */}
      {budgets.length === 0 ? (
        <div className="text-center py-16 text-slate-400">
          <Target className="w-16 h-16 mx-auto mb-4 opacity-30" />
          <p className="font-medium">No budgets yet</p>
          <p className="text-sm mt-1">Create budgets to track your spending limits</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {budgets.map((budget) => (
            <Card key={budget.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <CardTitle className="text-base">{budget.category_name}</CardTitle>
                  <div
                    className={cn(
                      'px-2 py-1 rounded-full text-xs font-medium',
                      budget.status === 'exceeded'
                        ? 'bg-red-100 text-red-700'
                        : budget.status === 'warning'
                          ? 'bg-amber-100 text-amber-700'
                          : 'bg-emerald-100 text-emerald-700'
                    )}
                  >
                    {statusLabel(budget.status)}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {/* Progress Bar */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-500">Budgeted</span>
                      <span className="font-semibold text-slate-800">
                        {formatCurrency(budget.planned_amount)}
                      </span>
                    </div>
                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className={cn(
                          'h-full rounded-full transition-all',
                          statusColor(budget.status)
                        )}
                        style={{ width: `${Math.min(budget.percentage_used, 100)}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-xs text-slate-500">
                      <span>{budget.percentage_used.toFixed(1)}% used</span>
                      <span>{formatCurrency(budget.remaining_amount)} remaining</span>
                    </div>
                  </div>

                  {/* Period Info */}
                  <div className="flex items-center gap-4 text-xs text-slate-500 border-t pt-3">
                    <div>
                      <span className="block text-slate-400">Period</span>
                      <span className="font-medium">{budget.period}</span>
                    </div>
                    <div>
                      <span className="block text-slate-400">Start</span>
                      <span className="font-medium">
                        {new Date(budget.start_date).toLocaleDateString()}
                      </span>
                    </div>
                    {budget.end_date && (
                      <div>
                        <span className="block text-slate-400">End</span>
                        <span className="font-medium">
                          {new Date(budget.end_date).toLocaleDateString()}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 pt-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="flex-1 text-xs"
                      onClick={() => {
                        setEditingBudget(budget);
                        setDialogOpen(true);
                      }}
                    >
                      Edit
                    </Button>
                    <Button
                      variant="outline"
                      size="icon"
                      className="h-8 w-8 text-red-600 hover:bg-red-50"
                      onClick={() => setConfirmDelete(budget)}
                      disabled={deletingId === budget.id}
                    >
                      {deletingId === budget.id ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <AlertCircle className="w-4 h-4" />
                      )}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Delete Confirmation */}
      {confirmDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/30">
          <Card className="max-w-sm w-full p-6 space-y-4">
            <h3 className="font-semibold text-slate-800">Delete budget?</h3>
            <p className="text-sm text-slate-500">
              This will permanently delete the budget for{' '}
              <strong>{confirmDelete.category_name}</strong>.
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

      <BudgetDialog
        open={dialogOpen}
        onClose={() => {
          setDialogOpen(false);
          setEditingBudget(null);
        }}
        editingBudget={editingBudget}
      />
    </div>
  );
}
