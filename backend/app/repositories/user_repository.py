from pathlib import Path

from app.models.user import SessionInDb, UserInDb
from app.utils.json_store import read_list_file, write_list_file
from app.utils.security import generate_session_token


class UserRepository:
    def __init__(self, users_file: Path, sessions_file: Path) -> None:
        self._users_file = users_file
        self._sessions_file = sessions_file

    def list_all(self) -> list[UserInDb]:
        return read_list_file(self._users_file, UserInDb)

    def get_by_id(self, user_id: str) -> UserInDb | None:
        return next((u for u in self.list_all() if u.id == user_id), None)

    def get_by_email(self, email: str) -> UserInDb | None:
        target = email.strip().lower()
        return next((u for u in self.list_all() if u.email.lower() == target), None)

    def get_by_username(self, username: str) -> UserInDb | None:
        target = username.strip().lower()
        return next((u for u in self.list_all() if u.username.lower() == target), None)

    def create(self, user: UserInDb) -> UserInDb:
        users = self.list_all()
        users.append(user)
        write_list_file(self._users_file, users)
        return user

    def update(self, user: UserInDb) -> UserInDb:
        users = self.list_all()
        for idx, u in enumerate(users):
            if u.id == user.id:
                users[idx] = user
                write_list_file(self._users_file, users)
                return user
        raise KeyError(f"User {user.id} not found")

    # Session methods
    def list_sessions(self) -> list[SessionInDb]:
        return read_list_file(self._sessions_file, SessionInDb)

    def create_session(self, user_id: str) -> SessionInDb:
        sessions = self.list_sessions()
        token = generate_session_token()
        session = SessionInDb(token=token, user_id=user_id)
        sessions.append(session)
        write_list_file(self._sessions_file, sessions)
        return session

    def get_session(self, token: str) -> SessionInDb | None:
        return next((s for s in self.list_sessions() if s.token == token), None)

    def delete_session(self, token: str) -> bool:
        sessions = self.list_sessions()
        filtered = [s for s in sessions if s.token != token]
        if len(filtered) == len(sessions):
            return False
        write_list_file(self._sessions_file, filtered)
        return True
