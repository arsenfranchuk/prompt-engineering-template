import { createSlice, type PayloadAction } from '@reduxjs/toolkit';
import type { User } from '@/types/auth';

const TOKEN_KEY = 'budget_planner_token';
const USER_KEY = 'budget_planner_user';

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
}

const storedToken = localStorage.getItem(TOKEN_KEY);
let storedUser: User | null = null;
const storedUserJson = localStorage.getItem(USER_KEY);
if (storedUserJson) {
  try {
    storedUser = JSON.parse(storedUserJson);
  } catch {
    storedUser = null;
  }
}

const initialState: AuthState = {
  token: storedToken,
  user: storedUser,
  isAuthenticated: !!storedToken,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials(state, action: PayloadAction<{ token: string; user: User }>) {
      state.token = action.payload.token;
      state.user = action.payload.user;
      state.isAuthenticated = true;
      localStorage.setItem(TOKEN_KEY, action.payload.token);
      localStorage.setItem(USER_KEY, JSON.stringify(action.payload.user));
    },
    setUser(state, action: PayloadAction<User>) {
      state.user = action.payload;
      localStorage.setItem(USER_KEY, JSON.stringify(action.payload));
    },
    clearCredentials(state) {
      state.token = null;
      state.user = null;
      state.isAuthenticated = false;
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    },
  },
});

export const { setCredentials, setUser, clearCredentials } = authSlice.actions;
export default authSlice.reducer;
