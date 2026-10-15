import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGetDashboardSummaryQuery } from '@/store/api/dashboardApi';
import type { DashboardPeriod } from '@/types/dashboard';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  TrendingUp,
  TrendingDown,
  Wallet,
  PiggyBank,
  Plus,
  ArrowRight,
  Target,
  Loader2,
} from 'lucide-react';
import { cn, formatCurrency } from '@/lib/utils';
import { TransactionDialog } from '@/features/transactions/TransactionDialog';
import { BudgetDialog } from '@/features/budgets/BudgetDialog';

const PERIOD_OPTIONS: { value: DashboardPeriod; label: string }[] = [
  { value: 'current_month', label: 'This Month' },
  { value: 'previous_month', label: 'Last Month' },
  { value: 'current_year', label: 'This Year' },
  { value: 'all', label: 'All Time' },
];

export function DashboardPage() {
  const navigate = useNavigate();
  const [period, setPeriod] = useState<DashboardPeriod>('current_month');
  const [txDialogOpen, setTxDialogOpen] = useState(false);
  const [txDialogType, setTxDialogType] = useState<'income' | 'expense'>('expense');
  const [budgetDialogOpen, setBudgetDialogOpen] = useState(false);

  const { data, isLoading, isError } = useGetDashboardSummaryQuery(period);

  const openIncome = () => {
    setTxDialogType('income');
    setTxDialogOpen(true);
  };
  const openExpense = () => {
    setTxDialogType('expense');
    setTxDialogOpen(true);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="p-6 text-center text-red-600">
        Failed to load dashboard data. Please refresh.
      </div>
    );
  }

  const statusColor = (s: string) =>
    s === 'exceeded' ? 'bg-red-500' : s === 'warning' ? 'bg-amber-400' : 'bg-emerald-500';

  return (
    <div className="p-4 md:p-6 space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Dashboard</h1>
          <p className="text-slate-500 text-sm">Your financial overview</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {PERIOD_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => setPeriod(opt.value)}
              className={cn(
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                period === opt.value
                  ? 'bg-emerald-500 text-white'
                  : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'
              )}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-slate-500 font-medium">Balance</p>
                <p
                  className={cn(
                    'text-2xl font-bold mt-1',
                    data.current_balance >= 0 ? 'text-slate-800' : 'text-red-600'
                  )}
                >
                  {formatCurrency(data.current_balance)}
                </p>
                <p className="text-xs text-slate-400 mt-1">All time</p>
              </div>
              <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center">
                <Wallet className="w-5 h-5 text-slate-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-slate-500 font-medium">Income</p>
                <p className="text-2xl font-bold mt-1 text-emerald-600">
                  {formatCurrency(data.period_income)}
                </p>
                <p className="text-xs text-slate-400 mt-1">
                  {PERIOD_OPTIONS.find((o) => o.value === period)?.label}
                </p>
              </div>
              <div className="w-10 h-10 bg-emerald-50 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-emerald-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-slate-500 font-medium">Expenses</p>
                <p className="text-2xl font-bold mt-1 text-red-600">
                  {formatCurrency(data.period_expenses)}
                </p>
                <p className="text-xs text-slate-400 mt-1">
                  {PERIOD_OPTIONS.find((o) => o.value === period)?.label}
                </p>
              </div>
              <div className="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center">
                <TrendingDown className="w-5 h-5 text-red-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-slate-500 font-medium">Savings Rate</p>
                <p className="text-2xl font-bold mt-1 text-slate-800">
                  {data.savings_rate.toFixed(1)}%
                </p>
                <p
                  className={cn(
                    'text-xs mt-1',
                    data.period_net >= 0 ? 'text-emerald-600' : 'text-red-600'
                  )}
                >
                  Net {formatCurrency(data.period_net)}
                </p>
              </div>
              <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center">
                <PiggyBank className="w-5 h-5 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-wrap gap-3">
        <Button onClick={openIncome} className="bg-emerald-500 hover:bg-emerald-600 text-white">
          <Plus className="w-4 h-4 mr-2" />
          Add Income
        </Button>
        <Button
          onClick={openExpense}
          variant="outline"
          className="border-red-200 text-red-600 hover:bg-red-50"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Expense
        </Button>
        <Button onClick={() => setBudgetDialogOpen(true)} variant="outline">
          <Target className="w-4 h-4 mr-2" />
          Set Budget
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Transactions */}
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between pb-3">
            <CardTitle className="text-base">Recent Transactions</CardTitle>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/transactions')}
              className="text-emerald-600 h-8"
            >
              View all <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </CardHeader>
          <CardContent>
            {data.recent_transactions.length === 0 ? (
              <div className="py-8 text-center text-slate-400">
                <ArrowRight className="w-8 h-8 mx-auto mb-2 opacity-30" />
                <p className="text-sm">No transactions yet</p>
                <p className="text-xs mt-1">Add your first income or expense to get started</p>
              </div>
            ) : (
              <div className="space-y-3">
                {data.recent_transactions.map((tx) => (
                  <div key={tx.id} className="flex items-center gap-3">
                    <div
                      className={cn(
                        'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shrink-0',
                        tx.type === 'income'
                          ? 'bg-emerald-100 text-emerald-700'
                          : 'bg-red-100 text-red-700'
                      )}
                    >
                      {tx.type === 'income' ? '+' : '−'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-800 truncate">
                        {tx.description || tx.category_name}
                      </p>
                      <p className="text-xs text-slate-400">
                        {tx.category_name} · {tx.date}
                      </p>
                    </div>
                    <span
                      className={cn(
                        'text-sm font-semibold shrink-0',
                        tx.type === 'income' ? 'text-emerald-600' : 'text-red-600'
                      )}
                    >
                      {tx.type === 'income' ? '+' : '−'}
                      {formatCurrency(tx.amount)}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Spending by Category */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Spending by Category</CardTitle>
          </CardHeader>
          <CardContent>
            {data.spending_by_category.length === 0 ? (
              <div className="py-6 text-center text-slate-400 text-sm">No expenses recorded</div>
            ) : (
              <div className="space-y-3">
                {data.spending_by_category.slice(0, 6).map((cat) => (
                  <div key={cat.category_id}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-600 font-medium truncate">
                        {cat.category_name}
                      </span>
                      <span className="text-slate-500 ml-2 shrink-0">{cat.percentage}%</span>
                    </div>
                    <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-emerald-400 rounded-full"
                        style={{ width: `${Math.min(cat.percentage, 100)}%` }}
                      />
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">{formatCurrency(cat.amount)}</p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Budget Health */}
      {data.budget_summary.active_count > 0 && (
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-3">
            <CardTitle className="text-base">Budget Health</CardTitle>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/budgets')}
              className="text-emerald-600 h-8"
            >
              Manage <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
              <div className="text-center">
                <p className="text-xs text-slate-500">Active Budgets</p>
                <p className="text-xl font-bold text-slate-800 mt-1">
                  {data.budget_summary.active_count}
                </p>
              </div>
              <div className="text-center">
                <p className="text-xs text-slate-500">Planned</p>
                <p className="text-xl font-bold text-slate-800 mt-1">
                  {formatCurrency(data.budget_summary.total_planned)}
                </p>
              </div>
              <div className="text-center">
                <p className="text-xs text-slate-500">Spent</p>
                <p className="text-xl font-bold text-red-600 mt-1">
                  {formatCurrency(data.budget_summary.total_spent)}
                </p>
              </div>
              <div className="text-center">
                <p className="text-xs text-slate-500">Remaining</p>
                <p
                  className={cn(
                    'text-xl font-bold mt-1',
                    data.budget_summary.total_remaining >= 0 ? 'text-emerald-600' : 'text-red-600'
                  )}
                >
                  {formatCurrency(data.budget_summary.total_remaining)}
                </p>
              </div>
            </div>
            <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
              <div
                className={cn(
                  'h-full rounded-full transition-all',
                  statusColor(
                    data.budget_summary.percentage_used >= 100
                      ? 'exceeded'
                      : data.budget_summary.percentage_used >= 80
                        ? 'warning'
                        : 'within'
                  )
                )}
                style={{ width: `${Math.min(data.budget_summary.percentage_used, 100)}%` }}
              />
            </div>
            <p className="text-xs text-slate-500 mt-1">
              {data.budget_summary.percentage_used.toFixed(1)}% of total budget used
            </p>
          </CardContent>
        </Card>
      )}

      {/* Dialogs */}
      <TransactionDialog
        open={txDialogOpen}
        onClose={() => setTxDialogOpen(false)}
        defaultType={txDialogType}
      />
      <BudgetDialog open={budgetDialogOpen} onClose={() => setBudgetDialogOpen(false)} />
    </div>
  );
}
