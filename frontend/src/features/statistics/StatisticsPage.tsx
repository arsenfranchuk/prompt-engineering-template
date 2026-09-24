import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useGetDashboardSummaryQuery } from '@/store/api/dashboardApi'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { TrendingUp, TrendingDown, PieChart, Wallet, ArrowRight, Loader2 } from 'lucide-react'
import { formatCurrency, cn } from '@/lib/utils'

const PERIOD_OPTIONS = [
  { value: 'current_month', label: 'This Month' },
  { value: 'previous_month', label: 'Last Month' },
  { value: 'current_year', label: 'This Year' },
  { value: 'all', label: 'All Time' },
]

export function StatisticsPage() {
  const navigate = useNavigate()
  const [period, setPeriod] = useState<'current_month' | 'previous_month' | 'current_year' | 'all'>('current_month')

  const { data, isLoading, isError } = useGetDashboardSummaryQuery(period)

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
      </div>
    )
  }

  if (isError || !data) {
    return (
      <div className="p-6 text-center text-red-600">
        Failed to load statistics. Please refresh.
      </div>
    )
  }

  return (
    <div className="p-4 md:p-6 space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Statistics</h1>
          <p className="text-slate-500 text-sm">Your financial insights</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {PERIOD_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => setPeriod(opt.value as 'current_month' | 'previous_month' | 'current_year' | 'all')}
              className={cn(
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                period === opt.value
                  ? 'bg-emerald-500 text-white'
                  : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50',
              )}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-slate-500 font-medium">Current Balance</p>
                <p className={cn('text-2xl font-bold mt-1', data.current_balance >= 0 ? 'text-slate-800' : 'text-red-600')}>
                  {formatCurrency(data.current_balance)}
                </p>
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
                <p className="text-sm text-slate-500 font-medium">Total Income</p>
                <p className="text-2xl font-bold mt-1 text-emerald-600">{formatCurrency(data.period_income)}</p>
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
                <p className="text-sm text-slate-500 font-medium">Total Expenses</p>
                <p className="text-2xl font-bold mt-1 text-red-600">{formatCurrency(data.period_expenses)}</p>
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
                <p className="text-2xl font-bold mt-1 text-slate-800">{data.savings_rate.toFixed(1)}%</p>
                <p className={cn('text-xs mt-1', data.period_net >= 0 ? 'text-emerald-600' : 'text-red-600')}>
                  Net {formatCurrency(data.period_net)}
                </p>
              </div>
              <div className="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center">
                <PieChart className="w-5 h-5 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Spending by Category */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-3">
            <CardTitle className="text-base">Spending by Category</CardTitle>
            <Button variant="ghost" size="sm" onClick={() => navigate('/budgets')} className="text-emerald-600 h-8">
              Manage Budgets <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </CardHeader>
          <CardContent>
            {data.spending_by_category.length === 0 ? (
              <div className="py-8 text-center text-slate-400">
                <PieChart className="w-8 h-8 mx-auto mb-2 opacity-30" />
                <p className="text-sm">No expense data available</p>
              </div>
            ) : (
              <div className="space-y-4">
                {data.spending_by_category.map((item) => (
                  <div key={item.category_id}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-700 font-medium">{item.category_name}</span>
                      <span className="text-slate-600 font-medium">{item.percentage}%</span>
                    </div>
                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-emerald-500 rounded-full"
                        style={{ width: `${Math.min(item.percentage, 100)}%` }}
                      />
                    </div>
                    <p className="text-xs text-slate-500 mt-1">{formatCurrency(item.amount)}</p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Income by Category */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-3">
            <CardTitle className="text-base">Income by Category</CardTitle>
          </CardHeader>
          <CardContent>
            {data.income_by_category.length === 0 ? (
              <div className="py-8 text-center text-slate-400">
                <PieChart className="w-8 h-8 mx-auto mb-2 opacity-30" />
                <p className="text-sm">No income data available</p>
              </div>
            ) : (
              <div className="space-y-4">
                {data.income_by_category.map((item) => (
                  <div key={item.category_id}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-700 font-medium">{item.category_name}</span>
                      <span className="text-slate-600 font-medium">{item.percentage}%</span>
                    </div>
                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-500 rounded-full"
                        style={{ width: `${Math.min(item.percentage, 100)}%` }}
                      />
                    </div>
                    <p className="text-xs text-slate-500 mt-1">{formatCurrency(item.amount)}</p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Monthly Trend */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Monthly Trend</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {data.monthly_trend.map((item) => (
              <div key={item.month} className="flex items-center gap-4">
                <div className="w-24 text-sm font-medium text-slate-600">{item.label}</div>
                <div className="flex-1 space-y-2">
                  {/* Income Bar */}
                  <div className="relative h-2 bg-emerald-100 rounded-full overflow-hidden">
                    <div
                      className="absolute left-0 top-0 bottom-0 bg-emerald-500 rounded-full"
                      style={{ width: `${Math.min((item.income / (Math.max(data.period_income, 1))) * 100, 100)}%` }}
                    />
                  </div>
                  {/* Expense Bar */}
                  <div className="relative h-2 bg-red-100 rounded-full overflow-hidden">
                    <div
                      className="absolute left-0 top-0 bottom-0 bg-red-500 rounded-full"
                      style={{ width: `${Math.min((item.expense / (Math.max(data.period_expenses, 1))) * 100, 100)}%` }}
                    />
                  </div>
                </div>
                <div className="w-32 text-xs text-right space-y-1">
                  <div className="text-emerald-600 font-medium">+{formatCurrency(item.income)}</div>
                  <div className="text-red-600 font-medium">-{formatCurrency(item.expense)}</div>
                  <div className={cn('font-semibold', item.net >= 0 ? 'text-slate-700' : 'text-red-600')}>
                    Net: {formatCurrency(item.net)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
