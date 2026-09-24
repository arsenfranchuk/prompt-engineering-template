import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { RootState } from '@/store/store'
import type { DashboardSummary, DashboardPeriod } from '@/types/dashboard'
import { API_BASE_URL } from '@/lib/config'

export const dashboardApi = createApi({
  reducerPath: 'dashboardApi',
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
  tagTypes: ['Dashboard'],
  endpoints: (builder) => ({
    getDashboardSummary: builder.query<DashboardSummary, DashboardPeriod | void>({
      query: (period = 'current_month') => `/dashboard/summary?period=${period}`,
      providesTags: ['Dashboard'],
    }),
  }),
})

export const { useGetDashboardSummaryQuery } = dashboardApi
