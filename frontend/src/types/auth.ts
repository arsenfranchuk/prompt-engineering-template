export interface User {
  id: string
  username: string
  email: string
  created_at: string
}

export interface AuthResponse {
  token: string
  user: User
}

export interface RegisterInput {
  username: string
  email: string
  password: string
  password_confirm: string
}

export interface LoginInput {
  identifier: string
  password: string
}

export interface ProfileUpdateInput {
  username?: string
  email?: string
}

export interface ChangePasswordInput {
  current_password: string
  new_password: string
  new_password_confirm: string
}
