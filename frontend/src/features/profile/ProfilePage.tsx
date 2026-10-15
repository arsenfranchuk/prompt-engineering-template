import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  useGetMeQuery,
  useLogoutMutation,
  useUpdateProfileMutation,
  useChangePasswordMutation,
} from '@/store/api/authApi';
import { clearCredentials } from '@/store/slices/authSlice';
import { useAppDispatch } from '@/store/hooks';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AlertCircle } from 'lucide-react';

export function ProfilePage() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { data: user, isLoading: isLoadingUser } = useGetMeQuery();
  const [logout] = useLogoutMutation();
  const [updateProfile, { isLoading: isLoadingProfile }] = useUpdateProfileMutation();
  const [changePassword, { isLoading: isLoadingPassword }] = useChangePasswordMutation();

  const [editMode, setEditMode] = useState(false);
  const [profileForm, setProfileForm] = useState({ username: '', email: '' });
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    newPasswordConfirm: '',
  });
  const [profileError, setProfileError] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const [showPasswordSection, setShowPasswordSection] = useState(false);

  // Initialize profile form when user loads
  useEffect(() => {
    if (user) {
      setProfileForm({ username: user.username, email: user.email });
    }
  }, [user]);

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileError(null);
    setSuccessMessage(null);

    try {
      await updateProfile({
        username: profileForm.username.trim() || undefined,
        email: profileForm.email.trim().toLowerCase() || undefined,
      }).unwrap();
      setEditMode(false);
      setSuccessMessage('Profile updated successfully');
    } catch (err: any) {
      setProfileError(err?.data?.detail ?? 'Failed to update profile');
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError(null);
    setSuccessMessage(null);

    // Validate
    if (!passwordForm.currentPassword) {
      setPasswordError('Current password is required');
      return;
    }
    if (!passwordForm.newPassword) {
      setPasswordError('New password is required');
      return;
    }
    if (passwordForm.newPassword.length < 6) {
      setPasswordError('New password must be at least 6 characters');
      return;
    }
    if (passwordForm.newPassword !== passwordForm.newPasswordConfirm) {
      setPasswordError('New passwords do not match');
      return;
    }

    try {
      await changePassword({
        current_password: passwordForm.currentPassword,
        new_password: passwordForm.newPassword,
        new_password_confirm: passwordForm.newPasswordConfirm,
      }).unwrap();
      setPasswordForm({ currentPassword: '', newPassword: '', newPasswordConfirm: '' });
      setShowPasswordSection(false);
      setSuccessMessage('Password changed successfully');
    } catch (err: any) {
      setPasswordError(err?.data?.detail ?? 'Failed to change password');
    }
  };

  const handleLogout = async () => {
    try {
      await logout().unwrap();
      dispatch(clearCredentials());
      navigate('/login');
    } catch {
      dispatch(clearCredentials());
      navigate('/login');
    }
  };

  if (isLoadingUser) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="p-6 text-center">
        <p className="text-red-600">Not authenticated</p>
        <Button onClick={() => navigate('/login')} className="mt-4">
          Go to Login
        </Button>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6 space-y-6 max-w-2xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Profile</h1>
        <p className="text-slate-500 text-sm">Manage your account settings</p>
      </div>

      {/* User Info */}
      <Card>
        <CardHeader>
          <CardTitle>Personal Information</CardTitle>
          <CardDescription>Your account details</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Username</Label>
                {editMode ? (
                  <Input
                    value={profileForm.username}
                    onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })}
                    className="mt-1"
                  />
                ) : (
                  <div className="mt-1.5 px-3 py-2 bg-slate-50 rounded-md font-medium text-slate-800">
                    {user.username}
                  </div>
                )}
              </div>
              <div>
                <Label>Email</Label>
                {editMode ? (
                  <Input
                    type="email"
                    value={profileForm.email}
                    onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
                    className="mt-1"
                  />
                ) : (
                  <div className="mt-1.5 px-3 py-2 bg-slate-50 rounded-md font-medium text-slate-800">
                    {user.email}
                  </div>
                )}
              </div>
            </div>

            <div className="pt-4 border-t flex gap-3">
              {editMode ? (
                <>
                  <Button
                    onClick={handleProfileUpdate}
                    disabled={isLoadingProfile}
                    className="flex-1"
                  >
                    Save Changes
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setEditMode(false);
                      setProfileForm({ username: user.username, email: user.email });
                    }}
                  >
                    Cancel
                  </Button>
                </>
              ) : (
                <Button
                  onClick={() => {
                    setEditMode(true);
                    setProfileError(null);
                  }}
                  className="flex-1"
                >
                  Edit Profile
                </Button>
              )}
            </div>

            {profileError && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{profileError}</span>
              </div>
            )}
            {successMessage && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm">
                <span>{successMessage}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Change Password Section */}
      {showPasswordSection && (
        <Card>
          <CardHeader>
            <CardTitle>Change Password</CardTitle>
            <CardDescription>Update your password securely</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleChangePassword} className="space-y-4">
              <div>
                <Label htmlFor="currentPassword">Current Password</Label>
                <Input
                  id="currentPassword"
                  type="password"
                  value={passwordForm.currentPassword}
                  onChange={(e) =>
                    setPasswordForm({ ...passwordForm, currentPassword: e.target.value })
                  }
                  className="mt-1"
                />
              </div>
              <div>
                <Label htmlFor="newPassword">New Password</Label>
                <Input
                  id="newPassword"
                  type="password"
                  value={passwordForm.newPassword}
                  onChange={(e) =>
                    setPasswordForm({ ...passwordForm, newPassword: e.target.value })
                  }
                  className="mt-1"
                />
              </div>
              <div>
                <Label htmlFor="newPasswordConfirm">Confirm New Password</Label>
                <Input
                  id="newPasswordConfirm"
                  type="password"
                  value={passwordForm.newPasswordConfirm}
                  onChange={(e) =>
                    setPasswordForm({ ...passwordForm, newPasswordConfirm: e.target.value })
                  }
                  className="mt-1"
                />
              </div>

              <div className="flex gap-3 pt-2">
                <Button type="submit" disabled={isLoadingPassword} className="flex-1">
                  Change Password
                </Button>
                <Button variant="outline" onClick={() => setShowPasswordSection(false)}>
                  Cancel
                </Button>
              </div>

              {passwordError && (
                <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>{passwordError}</span>
                </div>
              )}
            </form>
          </CardContent>
        </Card>
      )}

      {!showPasswordSection && (
        <Button variant="outline" onClick={() => setShowPasswordSection(true)} className="w-full">
          Change Password
        </Button>
      )}

      {/* Logout */}
      <div className="pt-6 border-t">
        <Button
          variant="outline"
          className="w-full text-red-600 hover:bg-red-50"
          onClick={handleLogout}
        >
          Log Out
        </Button>
      </div>

      {/* Account Stats */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Account Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
          <div className="flex justify-between">
            <span className="text-slate-500">Account Created</span>
            <span className="font-medium text-slate-800">
              {new Date(user.created_at).toLocaleDateString()}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Last Updated</span>
            <span className="font-medium text-slate-800">
              {new Date(user.created_at).toLocaleDateString()}
            </span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
