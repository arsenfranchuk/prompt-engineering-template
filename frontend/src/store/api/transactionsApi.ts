import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { RootState } from '@/store/store'
import type { Transaction, TransactionCreateInput, TransactionUpdateInput } from '@/types/transaction'
import { API_BASE_URL } from '@/lib/config'

export const transactionsApi = createApi({
  reducerPath: 'transactionsApi',
  baseQuery: fetchBaseQuery({
    baseUrl: API_BASE_URL,
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token
      if (token) {
        headers.set('Authorization', `Bearer ${token}`)
      }
      return headers
    },
  }),
  tagTypes: ['Transaction'],
  endpoints: (builder) => ({
    listTransactions: builder.query<
      Transaction[],
      {
        type?: string
        category_id?: string
        start_date?: string
        end_date?: string
        search?: string
        sort_by?: string
        sort_order?: string
      }
    >({
      query: (params = {}) => {
        const search = new URLSearchParams()
        Object.entries(params).forEach(([k, v]) => {
          if (v !== undefined && v !== '') search.set(k, String(v))
        })
        return `/transactions?${search.toString()}`
      },
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: 'Transaction' as const, id })),
              { type: 'Transaction', id: 'LIST' },
            ]
          : [{ type: 'Transaction', id: 'LIST' }],
    }),
    createTransaction: builder.mutation<Transaction, TransactionCreateInput>({
      query: (body) => ({
        url: '/transactions',
        method: 'POST',
        body,
      }),
      invalidatesTags: [{ type: 'Transaction', id: 'LIST' }],
    }),
    updateTransaction: builder.mutation<
      Transaction,
      { id: string; body: TransactionUpdateInput }
    >({
      query: ({ id, body }) => ({
        url: `/transactions/${id}`,
        method: 'PATCH',
        body,
      }),
      invalidatesTags: (_result, _error, { id }) => [
        { type: 'Transaction', id },
        { type: 'Transaction', id: 'LIST' },
      ],
    }),
    deleteTransaction: builder.mutation<void, string>({
      query: (id) => ({
        url: `/transactions/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, id) => [
        { type: 'Transaction', id },
        { type: 'Transaction', id: 'LIST' },
      ],
    }),
  }),
})

export const {
  useListTransactionsQuery,
  useCreateTransactionMutation,
  useUpdateTransactionMutation,
  useDeleteTransactionMutation,
} = transactionsApi
