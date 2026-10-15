import { configureStore } from '@reduxjs/toolkit';

import { authApi } from '@/store/api/authApi';
import { budgetsApi } from '@/store/api/budgetsApi';
import { categoriesApi } from '@/store/api/categoriesApi';
import { dashboardApi } from '@/store/api/dashboardApi';
import { transactionsApi } from '@/store/api/transactionsApi';
import authReducer from '@/store/slices/authSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    [authApi.reducerPath]: authApi.reducer,
    [categoriesApi.reducerPath]: categoriesApi.reducer,
    [transactionsApi.reducerPath]: transactionsApi.reducer,
    [budgetsApi.reducerPath]: budgetsApi.reducer,
    [dashboardApi.reducerPath]: dashboardApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      authApi.middleware,
      categoriesApi.middleware,
      transactionsApi.middleware,
      budgetsApi.middleware,
      dashboardApi.middleware
    ),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
