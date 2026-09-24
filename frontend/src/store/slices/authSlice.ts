import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import type { User } from '@/types/auth'

const TOKEN_KEY = 'budget_planner_token'

interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
}

const storedToken = localStorage.getItem(TOKEN_KEY)

const initialState: AuthState = {
  token: storedToken,
  user: null,
  isAuthenticated: !!storedToken,
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials(state, action: PayloadAction<{ token: string; user: User }>) {
      state.token = action.payload.token
      state.user = action.payload.user
      state.isAuthenticated = true
      localStorage.setItem(TOKEN_KEY, action.payload.token)
    },
    setUser(state, action: PayloadAction<User>) {
      state.user = action.payload
    },
    clearCredentials(state) {
      state.token = null
      state.user = null
      state.isAuthenticated = false
      localStorage.removeItem(TOKEN_KEY)
    },
  },
})

export const { setCredentials, setUser, clearCredentials } = authSlice.actions
export default authSlice.reducer
